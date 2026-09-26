# Q0339 · CI evaluation gate

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | Regression testing | Medium |

## Question

Implement a release gate for an LLM change: absolute metric floors, a maximum allowed drop against the baseline, and zero regressions on cases tagged critical. Return pass/fail with human-readable reasons.

## Answer

```python
def evaluation_gate(current: dict[str, float], baseline: dict[str, float], floors: dict[str, float],
                    max_drop: dict[str, float], critical_regressions: list[str]) -> tuple[bool, list[str]]:
    reasons = []
    for metric, floor in floors.items():
        if current[metric] < floor:
            reasons.append(f"{metric}={current[metric]:.3f} below floor {floor:.3f}")
    for metric, allowed in max_drop.items():
        drop = baseline[metric] - current[metric]
        if drop > allowed:
            reasons.append(f"{metric} dropped {drop:.3f} (allowed {allowed:.3f})")
    if critical_regressions:
        reasons.append(f"critical cases regressed: {', '.join(critical_regressions)}")
    return not reasons, reasons


base = {"groundedness": 0.93, "answer_accuracy": 0.88, "abstain_recall": 0.90}
floors = {"groundedness": 0.90, "abstain_recall": 0.85}
drops = {"answer_accuracy": 0.02}
ok, why = evaluation_gate({"groundedness": 0.94, "answer_accuracy": 0.87, "abstain_recall": 0.91}, base, floors, drops, [])
assert ok and why == []
ok, why = evaluation_gate({"groundedness": 0.89, "answer_accuracy": 0.84, "abstain_recall": 0.91}, base, floors, drops,
                          ["entitlement_leak_07"])
assert not ok and len(why) == 3 and why[0].startswith("groundedness=0.890")
```

Allowed drops should exceed run-to-run noise (measured from repeated runs), or the gate becomes flaky. Tie the gate to CI for prompt, model, retrieval and guardrail changes, and store every gate result with the configuration that produced it.

## Likely follow-ups

- How do you set `max_drop` so the gate is neither flaky nor toothless?

---

[← Q0338](../../batch_04_llm_evaluation_observability/0338_detect_per_case_regressions_between_versions/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0340 →](../../batch_04_llm_evaluation_observability/0340_concurrent_evaluation_runner_with_retries/README.md)
