# Q0224 · Measure ANN recall against exact search

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Vector search | Medium |

## Question

Implement a simple approximate index (random-hyperplane LSH with several hash tables), and measure its recall@10 against exact search. Show that more tables raise recall.

## Answer

```python
from collections import defaultdict

import numpy as np


class LSHIndex:
    def __init__(self, vectors: np.ndarray, n_tables: int, n_bits: int, seed: int = 0) -> None:
        rng = np.random.default_rng(seed)
        self.vectors = vectors
        self.planes = [rng.normal(size=(n_bits, vectors.shape[1])) for _ in range(n_tables)]
        self.tables = []
        for planes in self.planes:
            table = defaultdict(list)
            for i, key in enumerate(self._keys(planes, vectors)):
                table[key].append(i)
            self.tables.append(table)

    @staticmethod
    def _keys(planes: np.ndarray, x: np.ndarray) -> list[bytes]:
        return [row.tobytes() for row in (np.atleast_2d(x) @ planes.T > 0)]

    def search(self, q: np.ndarray, k: int) -> list[int]:
        cands = set()
        for planes, table in zip(self.planes, self.tables):
            cands.update(table.get(self._keys(planes, q)[0], []))
        cands = list(cands)
        if not cands:
            return []
        scores = self.vectors[cands] @ q
        return [cands[i] for i in np.argsort(-scores)[:k]]


def recall_at_k(index: LSHIndex, queries: np.ndarray, k: int) -> float:
    hits = 0
    for q in queries:
        exact = set(np.argsort(-(index.vectors @ q))[:k])
        hits += len(exact & set(index.search(q, k)))
    return hits / (k * len(queries))


rng = np.random.default_rng(1)
data = rng.normal(size=(2000, 32))
data /= np.linalg.norm(data, axis=1, keepdims=True)
queries = data[:50] + 0.05 * rng.normal(size=(50, 32))
r1 = recall_at_k(LSHIndex(data, n_tables=1, n_bits=8), queries, 10)
r8 = recall_at_k(LSHIndex(data, n_tables=8, n_bits=8), queries, 10)
assert 0 <= r1 < r8 <= 1
```

The same measurement methodology applies to any ANN index (HNSW, IVF): sample real queries, compute exact neighbours offline, and track recall@k alongside latency whenever you change index parameters.

## Likely follow-ups

- Why is recall@k of the ANN index not the same as end-to-end retrieval quality?

---

[← Q0223](../../batch_03_rag_retrieval/0223_ivf_and_product_quantisation/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0225 →](../../batch_03_rag_retrieval/0225_reciprocal_rank_fusion/README.md)
