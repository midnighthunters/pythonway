# Q0208 · Sentence-window retrieval

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Retrieval patterns | Medium |

## Question

Implement sentence-window retrieval: match at the sentence level, then return the best sentence with w sentences of context on each side.

## Answer

```python
import re


def split_sentences(text: str) -> list[str]:
    return [s for s in re.split(r"(?<=[.!?])\s+", text.strip()) if s]


def sentence_window(text: str, query: str, w: int = 1) -> str:
    sents = split_sentences(text)
    q = set(query.lower().split())
    scores = [len(q & set(re.findall(r"\w+", s.lower()))) for s in sents]
    best = max(range(len(sents)), key=lambda i: (scores[i], -i))
    return " ".join(sents[max(0, best - w): best + w + 1])


doc = ("Our travel policy applies to all staff. Hotels in London are capped at 180 GBP. "
       "This includes breakfast. Exceptions need director approval. Flights are booked centrally.")
assert sentence_window(doc, "london hotels capped", w=1) == (
    "Our travel policy applies to all staff. Hotels in London are capped at 180 GBP. This includes breakfast.")
assert sentence_window(doc, "flights booked", w=0) == "Flights are booked centrally."
```

The neighbouring sentences carry the qualifiers ("this includes breakfast", "exceptions need approval") that a single-sentence hit would miss. In production, sentences are embedded individually and the window is expanded from stored neighbours.

## Likely follow-ups

- Compare sentence-window retrieval with parent-child retrieval.

---

[← Q0207](../../batch_03_rag_retrieval/0207_parent_child_retrieval/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0209 →](../../batch_03_rag_retrieval/0209_contextual_chunk_headers/README.md)
