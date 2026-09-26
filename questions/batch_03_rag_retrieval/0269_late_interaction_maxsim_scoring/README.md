# Q0269 · Late interaction MaxSim scoring

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Advanced retrieval | Medium |

## Question

Implement ColBERT-style late-interaction scoring: every query token vector finds its best-matching document token vector, and the document score is the sum of those maxima. Why does it beat single-vector similarity on some queries?

## Answer

```python
import numpy as np


def unit(x: np.ndarray) -> np.ndarray:
    return x / np.maximum(np.linalg.norm(x, axis=-1, keepdims=True), 1e-12)


def maxsim(query_tokens: np.ndarray, doc_tokens: np.ndarray) -> float:
    return float((unit(query_tokens) @ unit(doc_tokens).T).max(axis=1).sum())


E = {"london": [1, 0, 0, 0], "hotel": [0, 1, 0, 0], "cap": [0, 0, 1, 0], "flight": [0, 0, 0, 1]}
vec = lambda words: np.array([E[w] for w in words], dtype=float)
q = vec(["london", "hotel", "cap"])
doc_full = vec(["hotel", "cap", "london", "flight"])
doc_partial = vec(["london", "flight", "flight"])
assert maxsim(q, doc_full) == 3.0
assert maxsim(q, doc_full) > maxsim(q, doc_partial) == 1.0
```

Every query term must be matched by something in the document, which captures fine-grained term-level relevance that one pooled vector blurs. The cost is storing a vector per token (a much larger index) and heavier scoring, so late interaction is often used as a reranking stage or with compression (ColBERTv2, PLAID).

## Likely follow-ups

- How does the index size compare with single-vector embeddings?

---

[← Q0268](../../batch_03_rag_retrieval/0268_is_a_reranker_worth_it/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0270 →](../../batch_03_rag_retrieval/0270_learned_sparse_retrieval/README.md)
