# Q0445 · Return tool errors the model can act on

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Tooling | Medium |

## Question

Map tool exceptions to model-facing error messages that say whether to retry, what to change, and which tool might help, without leaking internals.

## Answer

```python
class NotFound(Exception):
    pass


class RateLimited(Exception):
    pass


HINTS = {
    NotFound: (False, "The item doesn't exist. Check the id, or call list_accounts to see valid ids."),
    PermissionError: (False, "The user isn't allowed to do this. Explain that to the user; don't retry."),
    RateLimited: (True, "The service is busy. Wait and retry once, or continue without this data."),
    ValueError: (False, "The arguments were invalid. Fix them using the tool schema and try again."),
}


def model_facing_error(tool: str, exc: Exception) -> dict:
    for exc_type, (retryable, hint) in HINTS.items():
        if isinstance(exc, exc_type):
            return {"tool": tool, "ok": False, "error_type": exc_type.__name__, "retryable": retryable,
                    "message": str(exc)[:150], "hint": hint}
    return {"tool": tool, "ok": False, "error_type": "InternalError", "retryable": False,
            "message": "The tool failed unexpectedly.", "hint": "Tell the user the system had a problem."}


e = model_facing_error("get_balance", NotFound("account ACC-9 not found"))
assert e["error_type"] == "NotFound" and "list_accounts" in e["hint"] and not e["retryable"]
assert model_facing_error("x", RateLimited("429"))["retryable"]
internal = model_facing_error("x", KeyError("db_password"))
assert "db_password" not in str(internal) and internal["error_type"] == "InternalError"
```

Unknown exceptions return a generic message, so internal details (such as a leaked `KeyError('db_password')`) never reach the model or the user. The full exception goes to logs and traces. Good hints noticeably improve agent recovery rates.

## Likely follow-ups

- How would you measure whether better hints improved recovery?

---

[← Q0444](../../batch_05_agentic_patterns_orchestration/0444_agent_failure_modes_and_recovery/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0446 →](../../batch_05_agentic_patterns_orchestration/0446_business_rule_validation_for_tool_arguments/README.md)
