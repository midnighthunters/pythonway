# Q0382 · Error taxonomy counts

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | Error analysis | Easy |

## Question

After labelling 200 failures with error categories, produce a ranked taxonomy with counts, percentages and example ids, so the team fixes the biggest buckets first.

## Answer

```python
from collections import Counter, defaultdict


def taxonomy(failures: list[dict], examples: int = 2) -> list[dict]:
    counts = Counter(f["category"] for f in failures)
    ex: dict[str, list[str]] = defaultdict(list)
    for f in failures:
        if len(ex[f["category"]]) < examples:
            ex[f["category"]].append(f["id"])
    total = len(failures)
    return [{"category": c, "count": n, "pct": round(100 * n / total, 1), "examples": ex[c]}
            for c, n in counts.most_common()]


fails = ([{"id": f"r{i}", "category": "retrieval_miss"} for i in range(90)]
         + [{"id": f"s{i}", "category": "stale_document"} for i in range(50)]
         + [{"id": f"h{i}", "category": "hallucinated_number"} for i in range(40)]
         + [{"id": f"f{i}", "category": "format_error"} for i in range(20)])
t = taxonomy(fails)
assert [row["category"] for row in t] == ["retrieval_miss", "stale_document", "hallucinated_number", "format_error"]
assert t[0] == {"category": "retrieval_miss", "count": 90, "pct": 45.0, "examples": ["r0", "r1"]}
```

Here retrieval misses and stale documents account for 70% of failures, which are data and retrieval problems, not model problems. Swapping in a bigger model would have been the wrong investment.

## Likely follow-ups

- How do you build the category list without biasing the labellers?

---

[← Q0381](../../batch_04_llm_evaluation_observability/0381_end_to_end_versus_component_rag_evaluation/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0383 →](../../batch_04_llm_evaluation_observability/0383_error_analysis_workflow/README.md)
