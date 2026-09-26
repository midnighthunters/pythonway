# Q0214 · Deterministic chunk ids for idempotent ingestion

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Ingestion | Medium |

## Question

Design chunk ids so re-running ingestion is idempotent, and so you can detect when chunk content changed. Implement it.

## Answer

```python
import hashlib


def chunk_records(doc_id: str, version: str, chunks: list[str], embed_model: str) -> list[dict]:
    records = []
    for i, text in enumerate(chunks):
        content_hash = hashlib.sha256(text.encode()).hexdigest()
        records.append({
            "chunk_id": hashlib.sha256(f"{doc_id}|{version}|{i}".encode()).hexdigest()[:24],
            "content_hash": content_hash,
            "embedding_key": hashlib.sha256(f"{embed_model}|{content_hash}".encode()).hexdigest()[:24],
            "doc_id": doc_id, "version": version, "ordinal": i, "text": text,
        })
    return records


a = chunk_records("pol-7", "v4", ["Hotels capped.", "Flights economy."], "embed-v2")
b = chunk_records("pol-7", "v4", ["Hotels capped.", "Flights economy."], "embed-v2")
assert a == b
c = chunk_records("pol-7", "v4", ["Hotels capped.", "Flights economy."], "embed-v3")
assert a[0]["content_hash"] == c[0]["content_hash"] and a[0]["embedding_key"] != c[0]["embedding_key"]
```

- `chunk_id` makes upserts idempotent, so retries after a crash don't create duplicates.
- `content_hash` detects changes, and powers incremental updates.
- `embedding_key` (model plus content) lets you cache embeddings and skip re-embedding unchanged text, while forcing a re-embed when the model changes.

## Likely follow-ups

- Why include the embedding model in the cache key?

---

[← Q0213](../../batch_03_rag_retrieval/0213_deduplicate_near_duplicate_chunks_with_minhash/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0215 →](../../batch_03_rag_retrieval/0215_incremental_re_indexing_on_document_change/README.md)
