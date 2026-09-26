# Q0337 · Select a model on the quality-cost frontier

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | Model selection | Medium |

## Question

Given evaluation results for several models (quality score and cost per 1,000 requests), compute the Pareto frontier and pick the cheapest model that meets a minimum quality bar.

## Answer

```python
def pareto_frontier(models: dict[str, tuple[float, float]]) -> list[str]:
    frontier = []
    for name, (q, c) in models.items():
        dominated = any((q2 >= q and c2 <= c) and (q2 > q or c2 < c) for n2, (q2, c2) in models.items() if n2 != name)
        if not dominated:
            frontier.append(name)
    return sorted(frontier, key=lambda n: models[n][1])


def cheapest_meeting(models: dict[str, tuple[float, float]], min_quality: float) -> str | None:
    ok = [n for n in pareto_frontier(models) if models[n][0] >= min_quality]
    return ok[0] if ok else None


models = {"small": (0.78, 0.40), "medium": (0.86, 1.50), "large": (0.91, 6.00),
          "old-large": (0.85, 7.00), "reasoning": (0.93, 18.00)}
assert pareto_frontier(models) == ["small", "medium", "large", "reasoning"]
assert cheapest_meeting(models, 0.85) == "medium"
assert cheapest_meeting(models, 0.95) is None
```

"old-large" is dominated: "medium" is better and cheaper. Add latency as a third dimension when it matters. Re-run the analysis whenever providers release new models or change prices. Also consider routing: small for easy traffic and large for hard cases often beats any single model on the frontier.

## Likely follow-ups

- How do you factor in confidence intervals when two models' quality scores overlap?

---

[← Q0336](../../batch_04_llm_evaluation_observability/0336_report_cost_and_latency_percentiles/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0338 →](../../batch_04_llm_evaluation_observability/0338_detect_per_case_regressions_between_versions/README.md)
