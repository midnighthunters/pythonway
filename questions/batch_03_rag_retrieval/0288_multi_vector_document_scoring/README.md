# Q0288 · Multi-vector document scoring

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Advanced retrieval | Medium |

## Question

A document has several chunk vectors. Implement document-level scoring as the maximum chunk similarity, or the mean of the top 2, and show when the aggregation choice matters.

## Answer

```python
import numpy as np


def doc_scores(query: np.ndarray, doc_chunks: dict[str, np.ndarray], mode: str = "max") -> dict[str, float]:
    q = query / np.linalg.norm(query)
    out = {}
    for doc, vecs in doc_chunks.items():
        sims = (vecs / np.linalg.norm(vecs, axis=1, keepdims=True)) @ q
        top = np.sort(sims)[::-1]
        out[doc] = float(top[0] if mode == "max" else top[:2].mean())
    return out


docs = {"focused": np.array([[1.0, 0.0], [0.0, 1.0]]),
        "broad": np.array([[0.95, 0.31], [0.9, 0.44]])}
q = np.array([1.0, 0.0])
mx, top2 = doc_scores(q, docs, "max"), doc_scores(q, docs, "top2")
assert max(mx, key=mx.get) == "focused"
assert max(top2, key=top2.get) == "broad"
```

Max rewards a single perfect passage, which is good for precise lookups. Top-n averaging rewards documents that are consistently about the topic, which is good for "find me the right document" navigation. Pick based on whether you return passages or documents, and validate on labelled data.

## Likely follow-ups

- Which aggregation suits a "find the policy document" search box?

---

[← Q0287](../../batch_03_rag_retrieval/0287_index_generated_question_answer_pairs/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0289 →](../../batch_03_rag_retrieval/0289_rag_over_code_repositories/README.md)
