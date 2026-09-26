# Q0189 · Validate parallel tool calls independently

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Tool use | Medium |

## Question

A model returns several tool calls in one turn. Validate each call independently (unique id, known tool, JSON arguments, schema), so that one bad call doesn't block the others, and return per-call results keyed by id.

## Answer

```python
import json
from typing import Any, Callable

from pydantic import BaseModel, Field, TypeAdapter


class BalanceArgs(BaseModel):
    account_id: str = Field(pattern=r"^ACC-\d{4}$")


class FxArgs(BaseModel):
    pair: str = Field(pattern=r"^[A-Z]{6}$")


VALIDATORS: dict[str, Callable[[Any], BaseModel]] = {
    "get_balance": TypeAdapter(BalanceArgs).validate_python,
    "get_fx_rate": TypeAdapter(FxArgs).validate_python,
}


def validate_tool_calls(calls: list[dict]) -> list[dict]:
    seen, results = set(), []
    for c in calls:
        cid = c.get("id")
        if not cid or cid in seen:
            results.append({"id": cid, "ok": False, "error": "missing or duplicate call id"})
            continue
        seen.add(cid)
        validator = VALIDATORS.get(c.get("name"))
        if validator is None:
            results.append({"id": cid, "ok": False, "error": f"unknown tool {c.get('name')!r}"})
            continue
        try:
            results.append({"id": cid, "ok": True, "args": validator(json.loads(c.get("arguments") or "{}"))})
        except ValueError as e:
            results.append({"id": cid, "ok": False, "error": str(e).splitlines()[0]})
    return results


calls = [
    {"id": "c1", "name": "get_balance", "arguments": '{"account_id": "ACC-1234"}'},
    {"id": "c2", "name": "get_fx_rate", "arguments": '{"pair": "gbp"}'},
    {"id": "c3", "name": "get_balance", "arguments": "{not json"},
    {"id": "c1", "name": "get_balance", "arguments": "{}"},
]
res = validate_tool_calls(calls)
assert [r["ok"] for r in res] == [True, False, False, False]
assert res[0]["args"].account_id == "ACC-1234" and "duplicate" in res[3]["error"]
```

Both `json.JSONDecodeError` and Pydantic's `ValidationError` are `ValueError` subclasses, so one `except` covers both. Run the valid calls (in parallel if independent), and return every result, including errors, to the model with its matching `tool_call_id`.

## Likely follow-ups

- How do you handle two parallel calls that conflict (for example two transfers from the same account)?

---

[← Q0188](../../batch_02_prompting_context_structured_output/0188_structured_outputs_versus_regex_post_processing/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0190 →](../../batch_02_prompting_context_structured_output/0190_handoff_payload_between_agents/README.md)
