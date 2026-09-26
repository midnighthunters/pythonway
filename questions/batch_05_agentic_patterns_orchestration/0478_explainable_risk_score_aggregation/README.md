# Q0478 · Explainable risk score aggregation

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Agent tools | Medium |

## Question

Implement a deterministic, explainable risk score: weighted signals produce a 0–100 score, and the tool returns the top contributing reasons so the agent (and the analyst) can explain the result.

## Answer

```python
def risk_score(signals: dict[str, float], weights: dict[str, float], cap: float = 100.0) -> dict:
    contributions = {name: weights[name] * value for name, value in signals.items() if name in weights}
    raw = sum(contributions.values())
    score = max(0.0, min(cap, raw))
    reasons = sorted(((c, n) for n, c in contributions.items() if c > 0), reverse=True)[:3]
    return {"score": round(score, 1), "reasons": [f"{n} (+{c:.1f})" for c, n in reasons],
            "band": "high" if score >= 70 else "medium" if score >= 40 else "low"}


weights = {"new_payee": 25, "amount_zscore": 8, "geo_mismatch": 20, "device_change": 15, "long_tenure": -10}
signals = {"new_payee": 1, "amount_zscore": 4.5, "geo_mismatch": 1, "device_change": 0, "long_tenure": 1}
r = risk_score(signals, weights)
assert r == {"score": 71.0, "reasons": ["amount_zscore (+36.0)", "new_payee (+25.0)", "geo_mismatch (+20.0)"],
             "band": "high"}
assert risk_score({"long_tenure": 1}, weights)["score"] == 0.0
```

Deterministic scoring is reproducible, testable and auditable, and it gives the LLM facts to narrate rather than numbers to invent. In a real bank, the scoring model itself falls under model risk management (validation, monitoring, fairness review), whether it is rules or ML.

## Likely follow-ups

- How would you explain a score to a customer who disputes a blocked payment?

---

[← Q0477](../../batch_05_agentic_patterns_orchestration/0477_fraud_investigation_agent_design/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0479 →](../../batch_05_agentic_patterns_orchestration/0479_guardrails_on_agent_actions/README.md)
