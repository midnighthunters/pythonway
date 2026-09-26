# Q0287 · Index generated question-answer pairs

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Advanced retrieval | Medium |

## Question

Implement "question indexing": generate likely questions for each chunk at ingestion, index the questions, and at query time match user questions against them, returning the source chunks.

## Answer

```python
import re
from typing import Callable


def build_question_index(chunks: dict[str, str], gen: Callable[[str], list[str]]) -> list[tuple[str, str]]:
    return [(q, cid) for cid, text in chunks.items() for q in gen(text)]


STOP = {"i", "a", "the", "to", "do", "my", "can", "is", "what", "how", "have"}


def terms(s: str) -> set[str]:
    return {w for w in re.findall(r"\w+", s.lower()) if w not in STOP}


def search_questions(query: str, qindex: list[tuple[str, str]], k: int = 3) -> list[str]:
    qt = terms(query)
    scored = sorted(qindex, key=lambda qc: -len(qt & terms(qc[0])))
    out: list[str] = []
    for q, cid in scored:
        if not qt & terms(q):
            break
        if cid not in out:
            out.append(cid)
        if len(out) == k:
            break
    return out


chunks = {"c1": "Claims must be filed within 30 days of purchase.", "c2": "Taxis are permitted after 9pm."}
GEN = {"c1": ["How long do I have to submit expenses?", "What is the deadline for claims?"],
       "c2": ["Can I take a cab home late?"]}
gen = lambda text: next(qs for cid, qs in GEN.items() if chunks[cid] == text)
qi = build_question_index(chunks, gen)
assert search_questions("how long do I have to submit my expenses", qi) == ["c1"]
assert search_questions("late cab home", qi) == ["c2"]
```

Questions phrased the way users ask them close the vocabulary gap (question-to-question similarity beats question-to-passage). The costs are an LLM pass at ingestion and a larger index. Keep generated questions tied to chunk versions, so they're regenerated on change.

## Likely follow-ups

- How is this related to HyDE, and why is it cheaper at query time?

---

[← Q0286](../../batch_03_rag_retrieval/0286_hierarchical_summaries_as_retrieval_units/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0288 →](../../batch_03_rag_retrieval/0288_multi_vector_document_scoring/README.md)
