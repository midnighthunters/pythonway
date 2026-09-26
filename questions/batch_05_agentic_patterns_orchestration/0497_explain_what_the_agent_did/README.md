# Q0497 · Explain what the agent did

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | UX | Easy |

## Question

Turn an agent's action log into a short, user-friendly explanation of what it did, with approvals noted and sensitive values masked.

## Answer

```python
import re

TEMPLATES = {
    "search_flights": ("Searched for alternative flights to {destination}.", "Couldn't search flights to {destination}."),
    "hold_seat": ("Held a seat on {flight}.", "Couldn't hold a seat on {flight}."),
    "issue_refund": ("Issued a refund of {amount}.", "Couldn't issue a refund of {amount}."),
    "update_hotel": ("Moved your hotel booking to {date}.", "Couldn't move your hotel booking to {date}."),
}


def mask(value: str) -> str:
    return re.sub(r"\b\d{8,}\b", lambda m: "****" + m.group(0)[-4:], value)


def explain(action_log: list[dict]) -> list[str]:
    lines = []
    for a in action_log:
        done_tpl, fail_tpl = TEMPLATES.get(a["tool"], ("Performed {tool}.", "Couldn't perform {tool}."))
        tpl = fail_tpl if a.get("status") == "failed" else done_tpl
        text = tpl.format(tool=a["tool"], **{k: mask(str(v)) for k, v in a.get("args", {}).items()})
        if a.get("approved_by"):
            text += f" (approved by {a['approved_by']})"
        lines.append(text)
    return lines


log = [{"tool": "search_flights", "args": {"destination": "Frankfurt"}},
       {"tool": "hold_seat", "args": {"flight": "LH903"}},
       {"tool": "issue_refund", "args": {"amount": "£412.50 to account 12345678"}, "approved_by": "you"},
       {"tool": "update_hotel", "args": {"date": "2 Oct"}, "status": "failed"}]
assert explain(log) == [
    "Searched for alternative flights to Frankfurt.",
    "Held a seat on LH903.",
    "Issued a refund of £412.50 to account ****5678. (approved by you)",
    "Couldn't move your hotel booking to 2 Oct.",
]
```

Failures get their own wording, so the user can see what didn't happen. Generating the explanation from the action log (not from the model's memory) guarantees it reflects what actually happened. An LLM can then polish the tone while being grounded in the log.

## Likely follow-ups

- Why should explanations come from the action log rather than the model's narrative?

---

[← Q0496](../../batch_05_agentic_patterns_orchestration/0496_cross_user_isolation_in_shared_agents/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0498 →](../../batch_05_agentic_patterns_orchestration/0498_tamper_evident_audit_trail_for_agent_actions/README.md)
