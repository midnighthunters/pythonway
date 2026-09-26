# Q0447 · Authorisation checks inside tools

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Security | Hard |

## Question

A tool receives `account_id` from the model. Implement authorisation that derives the user from the authenticated session (never from model arguments) and checks ownership or entitlement before returning data.

## Answer

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Session:
    user_id: str
    roles: frozenset[str]


ENTITLEMENTS = {"u-priya": {"ACC-1", "ACC-2"}, "u-tom": {"ACC-3"}}
BALANCES = {"ACC-1": "1,200.00 GBP", "ACC-2": "90.00 GBP", "ACC-3": "5,000.00 GBP"}


def get_balance(session: Session, account_id: str, on_behalf_of: str | None = None) -> str:
    if on_behalf_of is not None and on_behalf_of != session.user_id and "support_agent" not in session.roles:
        raise PermissionError("cannot act on behalf of another user")
    subject = on_behalf_of or session.user_id
    if account_id not in ENTITLEMENTS.get(subject, set()):
        raise PermissionError(f"no access to {account_id}")
    return BALANCES[account_id]


priya = Session("u-priya", frozenset({"employee"}))
assert get_balance(priya, "ACC-1") == "1,200.00 GBP"
for attack in ({"account_id": "ACC-3"}, {"account_id": "ACC-3", "on_behalf_of": "u-tom"}):
    try:
        get_balance(priya, **attack)
        raise AssertionError(attack)
    except PermissionError:
        pass
support = Session("u-sam", frozenset({"support_agent"}))
assert get_balance(support, "ACC-3", on_behalf_of="u-tom") == "5,000.00 GBP"
```

The session is injected by the platform (from the validated token), never supplied or influenced by the model. That defeats prompt-injected requests like "get the balance of ACC-3 for user u-tom". In production, call the system of record with an on-behalf-of token (OAuth token exchange), so it enforces entitlements itself, and log the access.

## Likely follow-ups

- Why is an on-behalf-of token better than a service account with broad access?

---

[← Q0446](../../batch_05_agentic_patterns_orchestration/0446_business_rule_validation_for_tool_arguments/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0448 →](../../batch_05_agentic_patterns_orchestration/0448_scope_tools_to_the_task_with_capability_tokens/README.md)
