# Q0371 · Canary analysis for prompt or model rollouts

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | Release engineering | Medium |

## Question

A new model version is serving 5% of traffic as a canary. Implement an automated decision (promote, hold or roll back) that compares canary and control on error rate, p95 latency and judge pass rate.

## Answer

```python
def canary_decision(control: dict, canary: dict, min_requests: int = 500) -> tuple[str, list[str]]:
    if canary["requests"] < min_requests:
        return "hold", ["insufficient canary traffic"]
    problems = []
    if canary["error_rate"] > control["error_rate"] * 1.5 + 0.002:
        problems.append("error rate regression")
    if canary["p95_ms"] > control["p95_ms"] * 1.2:
        problems.append("p95 latency regression")
    if canary["judge_pass"] < control["judge_pass"] - 0.03:
        problems.append("quality regression")
    if canary.get("safety_incidents", 0) > 0:
        return "rollback", problems + ["safety incident"]
    return ("rollback", problems) if problems else ("promote", [])


control = {"requests": 20_000, "error_rate": 0.004, "p95_ms": 3_000, "judge_pass": 0.93}
assert canary_decision(control, {"requests": 900, "error_rate": 0.005, "p95_ms": 3_100, "judge_pass": 0.94}) == (
    "promote", [])
assert canary_decision(control, {"requests": 900, "error_rate": 0.004, "p95_ms": 4_000, "judge_pass": 0.88})[1] == [
    "p95 latency regression", "quality regression"]
assert canary_decision(control, {"requests": 100, "error_rate": 0, "p95_ms": 1, "judge_pass": 1})[0] == "hold"
```

The thresholds should come from measured variance between identical groups (an A/A test), not intuition. Keep the rollback automatic and fast (a feature flag or routing weight), and a single safety incident overrides everything else.

## Likely follow-ups

- Why run an A/A comparison before trusting canary thresholds?

---

[← Q0370](../../batch_04_llm_evaluation_observability/0370_alert_on_an_online_quality_regression/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0372 →](../../batch_04_llm_evaluation_observability/0372_shadow_testing_a_new_model/README.md)
