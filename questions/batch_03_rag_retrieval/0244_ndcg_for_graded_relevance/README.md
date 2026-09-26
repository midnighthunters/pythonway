# Q0244 · nDCG for graded relevance

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Retrieval evaluation | Medium |

## Question

Implement nDCG@k with graded relevance (for example 0 = irrelevant, 1 = partial, 2 = fully answers), and show it rewards putting the best documents first.

## Answer

```python
import math


def dcg(grades: list[int]) -> float:
    return sum((2 ** g - 1) / math.log2(i + 2) for i, g in enumerate(grades))


def ndcg_at_k(ranked: list[str], grades: dict[str, int], k: int) -> float:
    actual = [grades.get(d, 0) for d in ranked[:k]]
    ideal = sorted(grades.values(), reverse=True)[:k]
    best = dcg(ideal)
    return dcg(actual) / best if best else 0.0


grades = {"a": 2, "b": 1, "c": 0}
assert ndcg_at_k(["a", "b", "c"], grades, 3) == 1.0
assert ndcg_at_k(["b", "a", "c"], grades, 3) < 1.0
assert ndcg_at_k(["c", "x", "b"], grades, 3) < ndcg_at_k(["b", "a", "c"], grades, 3)
assert ndcg_at_k(["x"], {}, 1) == 0.0
```

Use nDCG when relevance isn't binary (for example to compare rerankers). It needs graded labels, which cost more to collect. LLM-assisted grading with human spot checks is a practical way to label at scale.

## Likely follow-ups

- How would you collect graded relevance labels cost-effectively?

---

[← Q0243](../../batch_03_rag_retrieval/0243_hit_rate_and_mrr_for_a_retriever/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0245 →](../../batch_03_rag_retrieval/0245_build_a_retrieval_golden_set/README.md)
