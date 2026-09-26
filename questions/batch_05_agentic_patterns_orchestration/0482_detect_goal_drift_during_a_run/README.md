# Q0482 · Detect goal drift during a run

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Agent safety | Medium |

## Question

Implement a drift detector: compare each step's stated purpose with the original goal, and flag the run when several consecutive steps have low relevance to the goal.

## Answer

```python
import re

STOP = {"the", "a", "to", "for", "of", "and", "on", "in", "my", "check", "get"}


def terms(s: str) -> set[str]:
    return {w for w in re.findall(r"[a-z]+", s.lower()) if w not in STOP}


def drift_check(goal: str, step_purposes: list[str], min_overlap: int = 1, patience: int = 2) -> int | None:
    g = terms(goal)
    streak = 0
    for i, purpose in enumerate(step_purposes):
        streak = streak + 1 if len(g & terms(purpose)) < min_overlap else 0
        if streak >= patience:
            return i
    return None


goal = "Rebook the cancelled Frankfurt flight and update the hotel"
ok_steps = ["search Frankfurt flights", "hold seat on flight LH903", "update hotel dates"]
drifting = ["search Frankfurt flights", "read CEO inbox", "export contacts list", "update hotel dates"]
assert drift_check(goal, ok_steps) is None
assert drift_check(goal, drifting) == 2
```

Drift is a signal of confusion or of prompt injection ("read CEO inbox" is not part of rebooking). When it fires, pause and re-ground the agent on the goal, require approval for the next action, or stop and escalate. Use embeddings instead of word overlap in production, and combine this with the tool allowlist, which blocks the dangerous actions regardless.

## Likely follow-ups

- Why is drift detection a complement to, not a replacement for, tool allowlists?

---

[← Q0481](../../batch_05_agentic_patterns_orchestration/0481_per_user_rate_limits_on_agent_tools/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0483 →](../../batch_05_agentic_patterns_orchestration/0483_judging_the_quality_of_a_task_decomposition/README.md)
