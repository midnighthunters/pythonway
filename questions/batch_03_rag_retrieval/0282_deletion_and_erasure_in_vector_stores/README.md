# Q0282 · Deletion and erasure in vector stores

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Data governance | Hard |

## Question

A document must be removed immediately (sent in error, or a data-subject erasure request). Implement tombstone-based deletion that hides the document from search instantly, with later physical compaction, and list everything else that must be purged.

## Answer

```python
class Index:
    def __init__(self) -> None:
        self.chunks: dict[str, dict] = {}
        self.tombstoned_docs: set[str] = set()

    def upsert(self, chunk_id: str, doc_id: str, text: str) -> None:
        if doc_id in self.tombstoned_docs:
            raise PermissionError(f"{doc_id} is deleted; re-ingestion blocked")
        self.chunks[chunk_id] = {"doc_id": doc_id, "text": text}

    def delete_document(self, doc_id: str) -> None:
        self.tombstoned_docs.add(doc_id)

    def search(self, term: str) -> list[str]:
        return sorted(cid for cid, c in self.chunks.items()
                      if c["doc_id"] not in self.tombstoned_docs and term in c["text"].lower())

    def compact(self) -> int:
        doomed = [cid for cid, c in self.chunks.items() if c["doc_id"] in self.tombstoned_docs]
        for cid in doomed:
            del self.chunks[cid]
        return len(doomed)


idx = Index()
idx.upsert("c1", "memo-9", "restructuring plan salaries")
idx.upsert("c2", "pol-7", "travel salaries policy")
idx.delete_document("memo-9")
assert idx.search("salaries") == ["c2"]
assert idx.compact() == 1 and "c1" not in idx.chunks
try:
    idx.upsert("c1", "memo-9", "re-crawled copy")
    raise AssertionError
except PermissionError:
    pass
```

Blocking re-ingestion stops a crawler from bringing the document straight back. Also purge: embedding caches, semantic and answer caches that used the document, conversation memories and stored prompts or traces containing its text (per retention policy), evaluation sets, backups and snapshots (per policy), and replicas in other regions. Keep an auditable deletion record (what was deleted and when, but not the content).

## Likely follow-ups

- How do vector-index deletes work internally in HNSW, and why is compaction needed?

---

[← Q0281](../../batch_03_rag_retrieval/0281_document_versioning_in_the_index/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0283 →](../../batch_03_rag_retrieval/0283_pii_in_indexed_content/README.md)
