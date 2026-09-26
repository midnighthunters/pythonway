# Q0459 · Verify agent outputs before returning

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Verification | Medium |

## Question

Before an agent answers, verify it: every number in the answer must appear in some tool output, and every action it claims must appear in the action log. Return the issues found.

## Answer

```python
import re


def verify_answer(answer: str, tool_outputs: list[str], action_log: list[str], claimed_actions: list[str]) -> list[str]:
    issues = []
    haystack = " ".join(tool_outputs)
    for num in re.findall(r"\d+(?:[.,]\d+)*", answer):
        if num not in haystack:
            issues.append(f"number {num} not found in tool outputs")
    for action in claimed_actions:
        if action not in action_log:
            issues.append(f"claimed action '{action}' not in action log")
    return issues


outputs = ["Booking BK-9 cancelled; refund 412.50 GBP issued", "New flight LH903 departs 14:05"]
log = ["cancel_booking", "issue_refund", "rebook"]
assert verify_answer("Refunded 412.50 GBP; you're on LH903 at 14:05.", outputs, log, ["issue_refund", "rebook"]) == []
bad = verify_answer("Refunded 450.00 GBP and emailed your manager.", outputs, log, ["issue_refund", "send_email"])
assert bad == ["number 450.00 not found in tool outputs", "claimed action 'send_email' not in action log"]
```

Claiming actions that never happened is a real and dangerous agent failure. Deterministic checks like these are cheap to run on every answer. On failure, regenerate with the issues listed, or return a conservative answer built from the action log itself.

## Likely follow-ups

- How would you handle derived numbers (sums, conversions) that legitimately aren't in any tool output?

---

[← Q0458](../../batch_05_agentic_patterns_orchestration/0458_proposer_and_critic_agents/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0460 →](../../batch_05_agentic_patterns_orchestration/0460_weighted_voting_across_agents/README.md)
