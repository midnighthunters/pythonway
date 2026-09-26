# Q0446 · Business-rule validation for tool arguments

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Tooling | Medium |

## Question

Schema validation says the transfer arguments are well-formed. Implement the business-rule checks (daily limit remaining, currency matching the account, same-day cut-off time) that must also pass before execution.

## Answer

```python
from datetime import time
from decimal import Decimal


def transfer_violations(args: dict, account: dict, used_today: Decimal, now: time,
                        cutoff: time = time(16, 30)) -> list[str]:
    problems = []
    amount = Decimal(args["amount"])
    if amount <= 0:
        problems.append("amount must be positive")
    if used_today + amount > account["daily_limit"]:
        problems.append(f"exceeds daily limit: {account['daily_limit'] - used_today} remaining")
    if args["currency"] != account["currency"]:
        problems.append(f"account currency is {account['currency']}, not {args['currency']}")
    if args.get("same_day") and now > cutoff:
        problems.append(f"same-day cut-off {cutoff:%H:%M} has passed")
    return problems


acct = {"id": "ACC-1", "currency": "GBP", "daily_limit": Decimal("10000")}
ok = {"amount": "2500.00", "currency": "GBP", "same_day": True}
assert transfer_violations(ok, acct, Decimal("5000"), time(11, 0)) == []
bad = {"amount": "6000.00", "currency": "EUR", "same_day": True}
assert transfer_violations(bad, acct, Decimal("5000"), time(17, 0)) == [
    "exceeds daily limit: 5000 remaining", "account currency is GBP, not EUR", "same-day cut-off 16:30 has passed"]
```

These rules belong in the system of record's API as the source of truth. Checking them in the tool too gives the agent early, explainable feedback. Return all violations at once, so the agent can fix everything in one retry or explain to the user.

## Likely follow-ups

- Why should these checks also exist in the downstream payments API?

---

[← Q0445](../../batch_05_agentic_patterns_orchestration/0445_return_tool_errors_the_model_can_act_on/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0447 →](../../batch_05_agentic_patterns_orchestration/0447_authorisation_checks_inside_tools/README.md)
