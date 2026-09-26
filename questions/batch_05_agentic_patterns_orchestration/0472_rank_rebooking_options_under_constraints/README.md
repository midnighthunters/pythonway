# Q0472 · Rank rebooking options under constraints

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Agent tools | Medium |

## Question

Implement the deterministic ranking tool the rebooking agent calls: filter flights by hard constraints (arrive before the deadline, cabin at least the original, price increase within budget), score the rest, and return the reasons for rejected options.

## Answer

```python
from datetime import datetime

CABIN_RANK = {"economy": 0, "premium": 1, "business": 2}


def rank_options(options: list[dict], deadline: datetime, min_cabin: str, max_extra: float,
                 w_arrival: float = 1.0, w_stops: float = 2.0, w_cost: float = 0.01) -> tuple[list[dict], dict]:
    feasible, rejected = [], {}
    for o in options:
        reasons = []
        if o["arrive"] > deadline:
            reasons.append("arrives after deadline")
        if CABIN_RANK[o["cabin"]] < CABIN_RANK[min_cabin]:
            reasons.append("cabin downgrade")
        if o["extra_cost"] > max_extra:
            reasons.append("over budget")
        if reasons:
            rejected[o["id"]] = reasons
            continue
        slack_h = (deadline - o["arrive"]).total_seconds() / 3600
        score = w_arrival * min(slack_h, 6) - w_stops * o["stops"] - w_cost * o["extra_cost"]
        feasible.append({**o, "score": round(score, 3)})
    return sorted(feasible, key=lambda o: (-o["score"], o["id"])), rejected


d = datetime(2026, 10, 1, 18, 0)
opts = [
    {"id": "LH903", "arrive": datetime(2026, 10, 1, 14, 5), "cabin": "economy", "stops": 0, "extra_cost": 0},
    {"id": "BA912", "arrive": datetime(2026, 10, 1, 12, 30), "cabin": "economy", "stops": 1, "extra_cost": 120},
    {"id": "LX345", "arrive": datetime(2026, 10, 1, 19, 10), "cabin": "business", "stops": 0, "extra_cost": 0},
    {"id": "EW777", "arrive": datetime(2026, 10, 1, 9, 0), "cabin": "economy", "stops": 0, "extra_cost": 900},
]
ranked, rejected = rank_options(opts, d, "economy", max_extra=300)
assert [o["id"] for o in ranked] == ["LH903", "BA912"]
assert rejected == {"LX345": ["arrives after deadline"], "EW777": ["over budget"]}
```

Put hard constraints and scoring in code (deterministic, testable, explainable to the traveller). The LLM's role is to interpret soft preferences ("I'd rather not change at Heathrow") into parameters, and to explain the choice. The rejection reasons also make good user-facing explanations.

## Likely follow-ups

- How would you incorporate soft preferences without letting the model override hard rules?

---

[← Q0471](../../batch_05_agentic_patterns_orchestration/0471_design_a_flight_disruption_rebooking_agent/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0473 →](../../batch_05_agentic_patterns_orchestration/0473_trade_break_remediation_agent/README.md)
