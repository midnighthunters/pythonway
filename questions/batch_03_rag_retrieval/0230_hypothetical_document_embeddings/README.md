# Q0230 · Hypothetical document embeddings

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Query understanding | Medium |

## Question

Explain HyDE and implement it with a toy bag-of-words embedding: when the query's vocabulary doesn't match the documents, embedding a hypothetical answer can retrieve the right document.

## Answer

HyDE asks an LLM to write a plausible answer passage (without sources), embeds that passage, and searches with it. Answers look more like documents than questions do, so the vocabulary aligns better.

```python
import math
import re
from collections import Counter


def embed(text: str) -> Counter:
    return Counter(re.findall(r"[a-z]+", text.lower()))


def cosine(a: Counter, b: Counter) -> float:
    dot = sum(a[t] * b[t] for t in a)
    na, nb = math.sqrt(sum(v * v for v in a.values())), math.sqrt(sum(v * v for v in b.values()))
    return dot / (na * nb) if na and nb else 0.0


docs = {"A": "Expense claims must be filed within 30 days of purchase.",
        "B": "Receipts for gifts above 50 GBP must be declared."}


def search(vec: Counter) -> str:
    return max(docs, key=lambda d: cosine(vec, embed(docs[d])))


query = "How long do I have to submit my receipts?"
fake_llm = lambda q: "Expense claims must be filed within a set number of days after purchase."
assert search(embed(query)) == "B"
assert search(embed(fake_llm(query))) == "A"
```

Risks: the hypothetical answer can be wrong and pull in wrong documents, it adds an LLM call to the latency, and it helps less with strong modern embedding models and hybrid search. Evaluate it before adopting. Never show the hypothetical text to users as an answer.

## Likely follow-ups

- Why is HyDE less useful for identifier-heavy queries?

---

[← Q0229](../../batch_03_rag_retrieval/0229_multi_query_retrieval/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0231 →](../../batch_03_rag_retrieval/0231_query_decomposition_for_multi_hop_questions/README.md)
