# Q0460 · Weighted voting across agents

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Multi-agent | Medium |

## Question

Several independent agents classify a transaction (for example fraud or legitimate). Implement weighted voting, with each agent's weight set by its measured reliability, abstentions allowed, and escalation when the margin is too small.

## Answer

```python
from collections import defaultdict


def weighted_vote(votes: dict[str, str | None], weights: dict[str, float], min_margin: float = 0.25) -> dict:
    tally: dict[str, float] = defaultdict(float)
    for agent, label in votes.items():
        if label is not None:
            tally[label] += weights[agent]
    if not tally:
        return {"decision": "escalate", "reason": "all abstained"}
    ranked = sorted(tally.items(), key=lambda kv: -kv[1])
    total = sum(tally.values())
    top, second = ranked[0][1], ranked[1][1] if len(ranked) > 1 else 0.0
    if (top - second) / total < min_margin:
        return {"decision": "escalate", "reason": "no clear majority", "tally": dict(tally)}
    return {"decision": ranked[0][0], "confidence": round(top / total, 3)}


weights = {"rules_agent": 0.6, "pattern_agent": 0.9, "llm_agent": 0.7}
assert weighted_vote({"rules_agent": "fraud", "pattern_agent": "fraud", "llm_agent": "legit"}, weights) == {
    "decision": "fraud", "confidence": 0.682}
assert weighted_vote({"rules_agent": "fraud", "pattern_agent": "legit", "llm_agent": None}, weights)["decision"] == "escalate"
assert weighted_vote({"rules_agent": None, "pattern_agent": None, "llm_agent": None}, weights)["reason"] == "all abstained"
```

Voting helps only when the voters make somewhat independent errors: different models, data or methods. Three copies of the same prompt mostly agree on the same mistakes. Calibrate the weights on labelled outcomes, and never let a vote replace required human review for regulated decisions.

## Likely follow-ups

- How would you measure whether your voters' errors are correlated?

---

[← Q0459](../../batch_05_agentic_patterns_orchestration/0459_verify_agent_outputs_before_returning/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0461 →](../../batch_05_agentic_patterns_orchestration/0461_blackboard_architecture/README.md)
