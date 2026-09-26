# Q0277 · Compare chunking strategies with an evaluation

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Chunking | Medium |

## Question

Write a small harness that compares chunking strategies by whether the top-1 retrieved chunk contains the full answer span, and show that sentence-aware chunking beats naive 5-word windows on a boundary-crossing answer.

## Answer

```python
import re
from typing import Callable


def fixed_words(text: str, n: int = 5) -> list[str]:
    w = text.split()
    return [" ".join(w[i:i + n]) for i in range(0, len(w), n)]


def sentences(text: str) -> list[str]:
    return re.split(r"(?<=\.)\s+", text.strip())


STOP = {"the", "is", "are", "what", "when", "how", "to", "at", "a"}


def overlap(q: str, t: str) -> int:
    words = lambda s: {w for w in re.findall(r"\w+", s.lower()) if w not in STOP}
    return len(words(q) & words(t))


def top1_contains_answer(chunker: Callable[[str], list[str]], doc: str, qa: list[tuple[str, str]]) -> float:
    chunks = chunker(doc)
    hits = 0
    for q, answer in qa:
        best = max(chunks, key=lambda c: overlap(q, c))
        hits += answer in best
    return hits / len(qa)


doc = ("Welcome to the policy. London hotels are capped at 180 GBP per night. "
       "Flights under six hours are economy. Claims are filed within 30 days.")
qa = [("How are London hotels capped?", "London hotels are capped at 180 GBP per night"),
      ("When are claims filed?", "Claims are filed within 30 days")]
assert top1_contains_answer(sentences, doc, qa) == 1.0
assert top1_contains_answer(fixed_words, doc, qa) < 1.0
```

On a real corpus, use the golden set and the production retriever, and look at retrieval metrics plus the downstream answer quality. The winning strategy is often corpus-specific.

## Likely follow-ups

- Why might answer quality improve even when retrieval hit rate stays flat?

---

[← Q0276](../../batch_03_rag_retrieval/0276_chunk_boundary_problems/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0278 →](../../batch_03_rag_retrieval/0278_abstain_when_retrieval_is_weak/README.md)
