# Q0275 · Exact-match routing for identifiers

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Query understanding | Medium |

## Question

Queries often contain identifiers: policy ids, incident numbers, ISINs. Implement a router that detects them and performs an exact lookup first, falling back to hybrid search.

## Answer

```python
import re
from typing import Callable

ID_PATTERNS = {
    "policy": re.compile(r"\bPOL-\d{2,6}\b"),
    "incident": re.compile(r"\bINC\d{6,10}\b"),
    "isin": re.compile(r"\b[A-Z]{2}[A-Z0-9]{9}\d\b"),
}


def route_identifiers(q: str, exact_index: dict[str, list[str]], hybrid: Callable[[str], list[str]]) -> dict:
    ids = [m for pat in ID_PATTERNS.values() for m in pat.findall(q)]
    exact = [doc for i in ids for doc in exact_index.get(i, [])]
    if exact:
        return {"mode": "exact", "ids": ids, "results": list(dict.fromkeys(exact))}
    return {"mode": "hybrid", "ids": ids, "results": hybrid(q)}


index = {"POL-4471": ["doc-pol-4471-v3"], "US0378331005": ["doc-isin-apple"]}
hybrid = lambda q: ["semantic-hit"]
assert route_identifiers("What does POL-4471 say about gifts?", index, hybrid)["results"] == ["doc-pol-4471-v3"]
assert route_identifiers("Holdings in US0378331005", index, hybrid)["mode"] == "exact"
assert route_identifiers("POL-9999 details", index, hybrid) == {"mode": "hybrid", "ids": ["POL-9999"],
                                                              "results": ["semantic-hit"]}
```

Embeddings are unreliable for exact identifiers, and users expect the exact document. A keyword or term filter on a dedicated `ids` field does the job in production search engines. Combine exact hits with a few hybrid results when the question also has a semantic part.

## Likely follow-ups

- How would you validate an ISIN's check digit before routing?

---

[← Q0274](../../batch_03_rag_retrieval/0274_multilingual_rag/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0276 →](../../batch_03_rag_retrieval/0276_chunk_boundary_problems/README.md)
