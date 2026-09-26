# Q0246 · Synthetic questions for retrieval evaluation

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Retrieval evaluation | Medium |

## Question

Implement synthetic evaluation-set generation: an LLM writes a question per chunk, and you keep only questions that aren't near-copies of the chunk and whose source chunk is retrievable in the top k (a round-trip filter).

## Answer

```python
from difflib import SequenceMatcher
from typing import Callable


def synth_questions(chunks: dict[str, str], llm: Callable[[str], str], retrieve: Callable[[str], list[str]],
                    k: int = 5, max_copy: float = 0.7) -> list[dict]:
    out, seen = [], set()
    for cid, text in chunks.items():
        q = llm(f"Write one question a colleague might ask that this passage answers:\n{text}").strip()
        if len(q) < 10 or q.lower() in seen:
            continue
        if SequenceMatcher(None, q.lower(), text.lower()).ratio() > max_copy:
            continue
        if cid not in retrieve(q)[:k]:
            continue
        seen.add(q.lower())
        out.append({"question": q, "relevant": {cid}})
    return out


chunks = {"c1": "London hotels are capped at 180 GBP per night.",
          "c2": "Claims must be filed within 30 days.",
          "c3": "Taxis are allowed after 9pm."}
QUESTIONS = {"c1": "What's the nightly hotel limit in London?", "c2": "Claims must be filed within 30 days.",
             "c3": "Can I take a cab late at night?"}
fake_llm = lambda p: next(q for cid, q in QUESTIONS.items() if chunks[cid] in p)
fake_retrieve = lambda q: ["c1"] if "hotel" in q.lower() else ["c9"]
out = synth_questions(chunks, fake_llm, fake_retrieve)
assert out == [{"question": "What's the nightly hotel limit in London?", "relevant": {"c1"}}]
```

The c2 question is a copy of its chunk, and the c3 question fails the round trip. The round-trip filter biases the set towards questions your current retriever already handles, so don't use it for the whole set. Keep a portion unfiltered and human-reviewed. Synthetic sets supplement real questions; they don't replace them.

## Likely follow-ups

- What bias does the round-trip filter introduce?

---

[← Q0245](../../batch_03_rag_retrieval/0245_build_a_retrieval_golden_set/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0247 →](../../batch_03_rag_retrieval/0247_diagnose_a_bad_rag_answer/README.md)
