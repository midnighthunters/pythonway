# Q0243 · Hit rate and MRR for a retriever

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Retrieval evaluation | Easy |

## Question

Implement hit rate@k and mean reciprocal rank (MRR) for a retriever, given ranked results and relevant document sets per query.

## Answer

```python
def hit_rate_at_k(results: dict[str, list[str]], relevant: dict[str, set[str]], k: int) -> float:
    return sum(any(d in relevant[q] for d in results[q][:k]) for q in relevant) / len(relevant)


def mrr(results: dict[str, list[str]], relevant: dict[str, set[str]]) -> float:
    total = 0.0
    for q, rel in relevant.items():
        for rank, d in enumerate(results.get(q, []), start=1):
            if d in rel:
                total += 1 / rank
                break
    return total / len(relevant)


results = {"q1": ["a", "b", "c"], "q2": ["x", "y", "z"], "q3": ["m", "n", "o"]}
relevant = {"q1": {"a"}, "q2": {"z"}, "q3": {"k"}}
assert hit_rate_at_k(results, relevant, 1) == 1 / 3
assert hit_rate_at_k(results, relevant, 3) == 2 / 3
assert abs(mrr(results, relevant) - (1 + 1 / 3 + 0) / 3) < 1e-12
```

Hit rate@k answers "is at least one right chunk in what we send to the model?", which is the most important retrieval number for RAG. MRR rewards putting it near the top. Also track recall@k when questions need several chunks, and break the metrics down by query type.

## Likely follow-ups

- Why is hit rate@k more relevant for RAG than precision@k?

---

[← Q0242](../../batch_03_rag_retrieval/0242_lexical_groundedness_check/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0244 →](../../batch_03_rag_retrieval/0244_ndcg_for_graded_relevance/README.md)
