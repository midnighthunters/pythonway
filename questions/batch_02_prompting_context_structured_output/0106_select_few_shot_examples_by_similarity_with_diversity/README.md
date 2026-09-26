# Q0106 · Select few-shot examples by similarity with diversity

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Few-shot | Medium |

## Question

Implement dynamic few-shot selection with maximal marginal relevance (MMR): pick k examples that are similar to the query but not redundant with each other.

## Answer

MMR repeatedly picks the candidate maximising `λ·sim(query, c) - (1-λ)·max sim(c, already selected)`.

```python
import numpy as np


def mmr(query: np.ndarray, candidates: np.ndarray, k: int, lam: float = 0.7) -> list[int]:
    def unit(x):
        return x / np.maximum(np.linalg.norm(x, axis=-1, keepdims=True), 1e-12)

    q, c = unit(query), unit(candidates)
    rel = c @ q
    selected: list[int] = []
    remaining = list(range(len(c)))
    while remaining and len(selected) < k:
        if selected:
            redundancy = (c[remaining] @ c[selected].T).max(axis=1)
        else:
            redundancy = np.zeros(len(remaining))
        scores = lam * rel[remaining] - (1 - lam) * redundancy
        best = remaining[int(np.argmax(scores))]
        selected.append(best)
        remaining.remove(best)
    return selected


cands = np.array([[1.0, 0.0], [0.99, -0.05], [0.7, 0.7], [0.0, 1.0]])
query = np.array([1.0, 0.2])
assert mmr(query, cands, 2, lam=1.0) == [0, 1]
assert mmr(query, cands, 2, lam=0.6) == [0, 2]
```

With pure relevance (λ = 1) you get two near-duplicates (0 and 1). With λ = 0.6, the second pick is a different kind of example (2), even though its raw relevance is lower. Embed the example inputs once and cache them. The same MMR routine is used to diversify RAG results.

## Likely follow-ups

- How would you stop a single noisy example from being selected for every query?

---

[← Q0105](../../batch_02_prompting_context_structured_output/0105_delimit_untrusted_content_in_prompts/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0107 →](../../batch_02_prompting_context_structured_output/0107_balance_few_shot_examples_across_labels/README.md)
