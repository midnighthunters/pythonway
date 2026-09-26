# Q0448 · Scope tools to the task with capability tokens

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Security | Medium |

## Question

Implement per-run capability tokens: when a run starts, issue a token listing exactly the tools (and argument constraints) this task needs. The dispatcher rejects anything outside it, even if the model asks.

## Answer

```python
import hashlib
import hmac
import json

SECRET = b"rotate-me-in-a-vault"


def issue_capability(run_id: str, tools: dict[str, dict]) -> str:
    body = json.dumps({"run": run_id, "tools": tools}, sort_keys=True)
    sig = hmac.new(SECRET, body.encode(), hashlib.sha256).hexdigest()
    return body + "." + sig


def authorize(token: str, tool: str, args: dict) -> None:
    body, sig = token.rsplit(".", 1)
    if not hmac.compare_digest(sig, hmac.new(SECRET, body.encode(), hashlib.sha256).hexdigest()):
        raise PermissionError("invalid capability token")
    caps = json.loads(body)["tools"]
    if tool not in caps:
        raise PermissionError(f"{tool} not in this run's capabilities")
    for key, allowed in caps[tool].items():
        if args.get(key) not in allowed:
            raise PermissionError(f"{tool}.{key}={args.get(key)!r} not permitted")


token = issue_capability("run-77", {"search_flights": {}, "hold_seat": {"booking_ref": ["BK-9"]}})
authorize(token, "search_flights", {"origin": "LHR"})
authorize(token, "hold_seat", {"booking_ref": "BK-9"})
for tool, args in (("issue_refund", {}), ("hold_seat", {"booking_ref": "BK-1"})):
    try:
        authorize(token, tool, args)
        raise AssertionError((tool, args))
    except PermissionError:
        pass
tampered = token.replace('"BK-9"', '"BK-1"')
try:
    authorize(tampered, "hold_seat", {"booking_ref": "BK-1"})
    raise AssertionError
except PermissionError as e:
    assert "invalid" in str(e)
```

A rebooking run for BK-9 can only touch BK-9, even if a malicious email convinces the model to try another booking. The HMAC signature stops tampering. Use `hmac.compare_digest` to avoid timing leaks, keep the keys in a vault, and add expiry to real tokens.

## Likely follow-ups

- How is this similar to OAuth scopes, and how is it different?

---

[← Q0447](../../batch_05_agentic_patterns_orchestration/0447_authorisation_checks_inside_tools/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0449 →](../../batch_05_agentic_patterns_orchestration/0449_sandboxed_code_execution_tool/README.md)
