# Q0457 · Escalate to a human with context

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Human-in-the-loop | Medium |

## Question

Implement escalation from an agent to a human queue: decide when to escalate, and build a ticket with a concise summary, what was tried, the evidence, and a suggested next step, so the human doesn't start from zero.

## Answer

```python
def should_escalate(run: dict) -> str | None:
    if run["user_requested_human"]:
        return "user_request"
    if run["confidence"] == "low":
        return "low_confidence"
    if run["policy_blocked"]:
        return "policy"
    if run["failed_attempts"] >= 2:
        return "repeated_failure"
    return None


def build_ticket(run: dict, reason: str) -> dict:
    return {
        "reason": reason,
        "customer_ref": run["customer_ref"],
        "summary": run["goal"],
        "tried": [f"{s['tool']}: {s['outcome']}" for s in run["steps"]],
        "evidence": run["evidence"][:3],
        "suggested_next_step": run.get("suggestion", "Review and contact the customer"),
        "priority": "high" if reason in ("policy", "repeated_failure") else "normal",
    }


run = {"user_requested_human": False, "confidence": "medium", "policy_blocked": False, "failed_attempts": 2,
       "customer_ref": "CUS-88", "goal": "Rebook cancelled FRA flight for tomorrow morning",
       "steps": [{"tool": "search_flights", "outcome": "3 options"}, {"tool": "rebook", "outcome": "fare class blocks change"},
                 {"tool": "rebook", "outcome": "fare class blocks change"}],
       "evidence": ["Fare class: BASIC (non-changeable)"], "suggestion": "Request an airline waiver"}
reason = should_escalate(run)
ticket = build_ticket(run, reason)
assert reason == "repeated_failure" and ticket["priority"] == "high"
assert ticket["tried"][1] == "rebook: fare class blocks change" and ticket["suggested_next_step"] == "Request an airline waiver"
```

Include references rather than raw personal data, and link to the trace. Tell the user what's happening and the expected response time. Measure the escalation rate and how often humans overturn the agent's suggestion, which is a strong quality signal.

## Likely follow-ups

- How would you use human resolutions to improve the agent over time?

---

[← Q0456](../../batch_05_agentic_patterns_orchestration/0456_transactional_outbox_for_agent_side_effects/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0458 →](../../batch_05_agentic_patterns_orchestration/0458_proposer_and_critic_agents/README.md)
