# Q0239 · Pack context under a token budget

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Context assembly | Medium |

## Question

Given scored chunks, pack the best ones into a token budget: skip exact duplicates, cap the chunks per document (for diversity), and skip chunks that don't fit while still trying smaller ones.

## Answer

```python
from collections import Counter
from typing import Callable


def pack_context(chunks: list[dict], budget: int, count: Callable[[str], int], max_per_doc: int = 2) -> list[dict]:
    chosen, used, per_doc, seen = [], 0, Counter(), set()
    for c in sorted(chunks, key=lambda c: -c["score"]):
        if per_doc[c["doc_id"]] >= max_per_doc or c["text"] in seen:
            continue
        cost = count(c["text"])
        if used + cost > budget:
            continue
        chosen.append(c)
        used += cost
        per_doc[c["doc_id"]] += 1
        seen.add(c["text"])
    return chosen


words = lambda s: len(s.split())
chunks = [
    {"id": 1, "doc_id": "A", "score": 0.9, "text": "a " * 50},
    {"id": 2, "doc_id": "A", "score": 0.85, "text": "b " * 50},
    {"id": 3, "doc_id": "A", "score": 0.8, "text": "c " * 10},
    {"id": 4, "doc_id": "B", "score": 0.7, "text": "d " * 80},
    {"id": 5, "doc_id": "C", "score": 0.6, "text": "e " * 20},
    {"id": 6, "doc_id": "C", "score": 0.59, "text": "e " * 20},
]
assert [c["id"] for c in pack_context(chunks, budget=130, count=words)] == [1, 2, 5]
```

Chunk 3 is skipped by the per-document cap, chunk 4 doesn't fit, and chunk 6 is a duplicate. Greedy-by-score is a good default. Knapsack-style optimisation rarely pays off, because scores are noisy.

## Likely follow-ups

- When would you allow more than two chunks from the same document?

---

[← Q0238](../../batch_03_rag_retrieval/0238_build_numbered_context_with_a_citation_map/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0240 →](../../batch_03_rag_retrieval/0240_reorder_context_against_lost_in_the_middle/README.md)
