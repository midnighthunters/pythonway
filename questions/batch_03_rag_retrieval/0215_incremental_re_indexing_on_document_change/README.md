# Q0215 · Incremental re-indexing on document change

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Ingestion | Medium |

## Question

When a document is edited, compute the minimal index operations (chunks to add and chunks to delete) by comparing content hashes, so unchanged chunks keep their embeddings.

## Answer

```python
import hashlib


def h(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def diff_chunks(old_hashes: set[str], new_chunks: list[str]) -> tuple[list[str], set[str], int]:
    new_by_hash = {h(t): t for t in new_chunks}
    to_add = [t for hh, t in new_by_hash.items() if hh not in old_hashes]
    to_delete = old_hashes - new_by_hash.keys()
    unchanged = len(new_by_hash.keys() & old_hashes)
    return to_add, to_delete, unchanged


old = ["Intro.", "Hotels capped at 180.", "Flights economy."]
new = ["Intro.", "Hotels capped at 180.", "Rail is first class over 2 hours.", "Flights economy."]
add, delete, same = diff_chunks({h(t) for t in old}, new)
assert add == ["Rail is first class over 2 hours."] and delete == set() and same == 3
add, delete, same = diff_chunks({h(t) for t in old}, ["Intro.", "Hotels capped at 200.", "Flights economy."])
assert add == ["Hotels capped at 200."] and delete == {h("Hotels capped at 180.")} and same == 2
```

Keying by content (not by position) means inserting a paragraph doesn't invalidate every later chunk. This only works if the chunker is stable: structure-aware chunking changes locally, while fixed-size windows shift everything after an edit. Apply adds and deletes atomically per document, or queries can briefly see both versions.

## Likely follow-ups

- How do you prevent readers from seeing a half-updated document?

---

[← Q0214](../../batch_03_rag_retrieval/0214_deterministic_chunk_ids_for_idempotent_ingestion/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0216 →](../../batch_03_rag_retrieval/0216_metadata_schema_for_chunks/README.md)
