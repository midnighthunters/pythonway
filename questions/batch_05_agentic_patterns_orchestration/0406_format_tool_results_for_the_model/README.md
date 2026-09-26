# Q0406 · Format tool results for the model

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Tooling | Medium |

## Question

Write a tool-result formatter: a consistent envelope for success and errors, JSON-safe serialisation of dates and Decimals, truncation with a note, and a `retryable` flag on errors to guide the model.

## Answer

```python
import json
from datetime import date
from decimal import Decimal


def format_result(data=None, error: Exception | None = None, max_chars: int = 500) -> str:
    if error is not None:
        retryable = isinstance(error, (TimeoutError, ConnectionError))
        env = {"ok": False, "error": {"type": type(error).__name__, "message": str(error)[:200], "retryable": retryable}}
        return json.dumps(env)
    body = json.dumps({"ok": True, "data": data}, default=lambda o: str(o) if isinstance(o, (Decimal, date)) else repr(o))
    if len(body) > max_chars:
        note = f'... [truncated {len(body) - max_chars} chars; request fewer results or a narrower filter]'
        return body[:max_chars] + note
    return body


ok = json.loads(format_result({"balance": Decimal("12.50"), "as_of": date(2026, 9, 26)}))
assert ok == {"ok": True, "data": {"balance": "12.50", "as_of": "2026-09-26"}}
err = json.loads(format_result(error=TimeoutError("upstream took 10s")))
assert err["error"] == {"type": "TimeoutError", "message": "upstream took 10s", "retryable": True}
big = format_result({"rows": list(range(1000))}, max_chars=100)
assert big.startswith('{"ok": true') and "truncated" in big
```

Consistent envelopes help models distinguish "no results" from "tool failed". The truncation note tells the model how to get a smaller result. Truncated JSON isn't valid JSON, which is acceptable for display to a model. For downstream code, keep the full result in state and give the model only the summary.

## Likely follow-ups

- Should the model see raw stack traces? Why or why not?

---

[← Q0405](../../batch_05_agentic_patterns_orchestration/0405_tool_registry_with_schemas_and_permissions/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0407 →](../../batch_05_agentic_patterns_orchestration/0407_loop_guards_steps_tokens_and_repetition/README.md)
