# Q0232 · Extract metadata filters from queries

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Query understanding | Medium |

## Question

Implement "self-query" filter extraction: pull a year, jurisdiction and document type from the question into structured filters restricted to allowed values, while keeping the semantic query. Watch out for ambiguous tokens such as the pronoun "us".

## Answer

```python
import re

JURISDICTIONS = [("united kingdom", "UK"), ("uk", "UK"), ("usa", "US"), ("eu", "EU")]
DOC_TYPES = {"policy": "policy", "procedure": "procedure", "faq": "faq"}


def extract_filters(q: str) -> tuple[str, dict]:
    filters: dict = {}
    low = q.lower()
    if m := re.search(r"\b(20[0-4]\d)\b", low):
        filters["year"] = int(m.group(1))
    for key, value in JURISDICTIONS:
        if re.search(rf"\b{re.escape(key)}\b", low):
            filters["jurisdiction"] = value
            break
    else:
        if re.search(r"\bUS\b", q):  # upper-case only, so the pronoun "us" doesn't match
            filters["jurisdiction"] = "US"
    for key, value in DOC_TYPES.items():
        if re.search(rf"\b{key}\b", low):
            filters["doc_type"] = value
            break
    return q, filters


assert extract_filters("What was the UK travel policy in 2025?")[1] == {"year": 2025, "jurisdiction": "UK",
                                                                        "doc_type": "policy"}
assert extract_filters("What is the US procedure?")[1] == {"jurisdiction": "US", "doc_type": "procedure"}
assert extract_filters("tell us about hotel caps")[1] == {}
assert extract_filters("hotel caps")[1] == {}
```

The pronoun case shows why rule-based extraction needs care. In practice, an LLM with a strict schema (enums of allowed values) usually extracts filters more robustly than regexes. Either way:
- Validate against the allowed values and the index's real field values.
- Treat inferred filters as soft: if a filtered search returns nothing, retry without them, or ask the user.
- Never let query-derived filters widen or override entitlement filters. They can only narrow the search.

## Likely follow-ups

- Why should extracted filters be soft rather than hard?

---

[← Q0231](../../batch_03_rag_retrieval/0231_query_decomposition_for_multi_hop_questions/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0233 →](../../batch_03_rag_retrieval/0233_entitlement_aware_retrieval/README.md)
