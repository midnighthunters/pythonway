# Q0338 · Detect per-case regressions between versions

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | Regression testing | Medium |

## Question

Aggregate accuracy can stay flat while cases flip. Given per-case pass/fail over several runs for the old and new versions, list regressions (stably passing before, now failing), fixes, and flaky cases.

## Answer

```python
def compare_versions(old_runs: dict[str, list[bool]], new_runs: dict[str, list[bool]]) -> dict:
    def status(runs: list[bool]) -> str:
        return "pass" if all(runs) else "fail" if not any(runs) else "flaky"

    out = {"regressions": [], "fixes": [], "flaky": []}
    for case in sorted(old_runs.keys() & new_runs.keys()):
        o, n = status(old_runs[case]), status(new_runs[case])
        if "flaky" in (o, n):
            out["flaky"].append(case)
        elif o == "pass" and n == "fail":
            out["regressions"].append(case)
        elif o == "fail" and n == "pass":
            out["fixes"].append(case)
    return out


old = {"a": [True] * 3, "b": [True] * 3, "c": [False] * 3, "d": [True, False, True]}
new = {"a": [True] * 3, "b": [False] * 3, "c": [True] * 3, "d": [True] * 3}
assert compare_versions(old, new) == {"regressions": ["b"], "fixes": ["c"], "flaky": ["d"]}
```

Accuracy is identical here (2 of 4 stable passes before and after), but case b regressed. Review every regression before release, especially on high-severity tags. Flaky cases need more runs or a more tolerant scorer. Don't count them as wins or losses.

## Likely follow-ups

- How many runs per case do you need to call a case flaky with confidence?

---

[← Q0337](../../batch_04_llm_evaluation_observability/0337_select_a_model_on_the_quality_cost_frontier/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0339 →](../../batch_04_llm_evaluation_observability/0339_ci_evaluation_gate/README.md)
