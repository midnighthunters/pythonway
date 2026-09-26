# Q0377 · Stratified sampling for evaluation sets

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | Datasets | Medium |

## Question

Build an evaluation sample of size N from production queries, stratified by intent, proportional to traffic but with a minimum per stratum so rare intents are represented. Make it reproducible.

## Answer

```python
import random
from collections import defaultdict


def stratified_sample(items: list[dict], key: str, n: int, min_per: int, seed: int = 0) -> list[dict]:
    groups: dict[str, list[dict]] = defaultdict(list)
    for it in items:
        groups[it[key]].append(it)
    rng = random.Random(seed)
    alloc = {g: min(len(v), max(min_per, round(n * len(v) / len(items)))) for g, v in groups.items()}
    while sum(alloc.values()) > n:
        biggest = max(alloc, key=lambda g: (alloc[g] - min_per, alloc[g]))
        if alloc[biggest] <= min_per:
            break
        alloc[biggest] -= 1
    sample = []
    for g in sorted(groups):
        sample += rng.sample(groups[g], alloc[g])
    return sample


items = [{"id": i, "intent": "policy"} for i in range(900)] + [{"id": i, "intent": "it"} for i in range(900, 990)] + [
    {"id": i, "intent": "sanctions"} for i in range(990, 1000)]
s = stratified_sample(items, "intent", n=100, min_per=10)
counts = {g: sum(x["intent"] == g for x in s) for g in ("policy", "it", "sanctions")}
assert counts == {"policy": 80, "it": 10, "sanctions": 10} and len(s) == 100
assert stratified_sample(items, "intent", 100, 10) == s
```

Report both per-stratum metrics and a traffic-weighted overall metric (weight each stratum by its production share), because oversampling rare intents changes the unweighted average.

## Likely follow-ups

- How do you compute a traffic-weighted accuracy from a stratified sample?

---

[← Q0376](../../batch_04_llm_evaluation_observability/0376_deduplicate_evaluation_cases/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0378 →](../../batch_04_llm_evaluation_observability/0378_evaluating_multi_turn_conversations/README.md)
