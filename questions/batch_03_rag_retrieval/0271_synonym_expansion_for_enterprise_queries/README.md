# Q0271 · Synonym expansion for enterprise queries

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Query understanding | Easy |

## Question

Implement synonym expansion for keyword search from a curated synonym map, keeping quoted phrases untouched, and producing OR groups for the BM25 engine.

## Answer

```python
import re

SYNONYMS = {"leave": ["holiday", "vacation", "pto"], "expenses": ["reimbursement", "claims"], "laptop": ["notebook"]}


def expand_query(q: str) -> str:
    parts = re.findall(r'"[^"]+"|\S+', q)
    out = []
    for p in parts:
        if p.startswith('"'):
            out.append(p)
            continue
        word = p.lower().strip("?,.!")
        syns = SYNONYMS.get(word)
        out.append(f"({' OR '.join([word, *syns])})" if syns else p)
    return " ".join(out)


assert expand_query("How many leave days?") == "How many (leave OR holiday OR vacation OR pto) days?"
assert expand_query('"annual leave" policy') == '"annual leave" policy'
assert expand_query("submit expenses") == "submit (expenses OR reimbursement OR claims)"
```

Keep synonym lists curated by domain owners (a glossary), versioned and evaluated: bad synonyms hurt precision. Search engines support synonym filters at index or query time, which is usually better than string rewriting in the application.

## Likely follow-ups

- Index-time or query-time synonyms: what are the trade-offs?

---

[← Q0270](../../batch_03_rag_retrieval/0270_learned_sparse_retrieval/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0272 →](../../batch_03_rag_retrieval/0272_acronym_expansion/README.md)
