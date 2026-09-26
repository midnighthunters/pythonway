# Q0151 · Coerce and validate tool arguments

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Tool use | Medium |

## Question

Use Pydantic's `validate_call` to validate and coerce LLM-provided tool arguments (types, patterns, unknown arguments), and return structured errors the model can act on instead of raising.

## Answer

```python
from datetime import date
from typing import Annotated

from pydantic import Field, ValidationError, validate_call


@validate_call
def get_fx_rate(pair: Annotated[str, Field(pattern=r"^[A-Z]{6}$")], on: date) -> str:
    return f"{pair} on {on.isoformat()}: 1.2710"


TOOLS = {"get_fx_rate": get_fx_rate}


def dispatch(name: str, args: dict) -> dict:
    fn = TOOLS.get(name)
    if fn is None:
        return {"ok": False, "error": f"unknown tool {name!r}; available: {sorted(TOOLS)}"}
    try:
        return {"ok": True, "result": fn(**args)}
    except ValidationError as e:
        return {"ok": False, "error": "; ".join(f"{'.'.join(map(str, x['loc']))}: {x['msg']}" for x in e.errors())}


assert dispatch("get_fx_rate", {"pair": "GBPUSD", "on": "2026-09-25"}) == {
    "ok": True, "result": "GBPUSD on 2026-09-25: 1.2710"}
bad = dispatch("get_fx_rate", {"pair": "gbp/usd", "on": "tomorrow", "force": True})
assert not bad["ok"] and "pair" in bad["error"] and "on" in bad["error"] and "force" in bad["error"]
assert dispatch("delete_ledger", {})["ok"] is False
```

The ISO date string is coerced to a `date`. Unknown and invalid arguments come back as a readable error, which you send to the model as the tool result so it can self-correct. Validation is necessary but not sufficient: authorisation (may this user call this tool with these values?) is a separate check.

## Likely follow-ups

- Which validation belongs in the tool, and which in the dispatcher?

---

[← Q0150](../../batch_02_prompting_context_structured_output/0150_sanitise_model_markdown_before_rendering/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0152 →](../../batch_02_prompting_context_structured_output/0152_minimal_json_schema_validator/README.md)
