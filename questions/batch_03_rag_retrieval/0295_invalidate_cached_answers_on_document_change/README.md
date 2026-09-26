# Q0295 · Invalidate cached answers on document change

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Caching | Medium |

## Question

Answers are cached. Implement tag-based invalidation, so that when a document is updated or deleted, every cached answer that cited it is dropped.

## Answer

```python
from collections import defaultdict


class TaggedAnswerCache:
    def __init__(self) -> None:
        self._answers: dict[str, dict] = {}
        self._by_doc: dict[str, set[str]] = defaultdict(set)

    def put(self, key: str, answer: str, doc_ids: set[str]) -> None:
        self._answers[key] = {"answer": answer, "docs": set(doc_ids)}
        for d in doc_ids:
            self._by_doc[d].add(key)

    def get(self, key: str) -> str | None:
        entry = self._answers.get(key)
        return entry["answer"] if entry else None

    def invalidate_doc(self, doc_id: str) -> int:
        keys = self._by_doc.pop(doc_id, set())
        for k in keys:
            entry = self._answers.pop(k, None)
            if entry:
                for d in entry["docs"] - {doc_id}:
                    self._by_doc[d].discard(k)
        return len(keys)


c = TaggedAnswerCache()
c.put("scope1:london hotel cap", "180 GBP [1]", {"pol-7"})
c.put("scope1:hotel and claims", "180 GBP [1], 30 days [2]", {"pol-7", "faq-2"})
c.put("scope1:claims deadline", "30 days [1]", {"faq-2"})
assert c.invalidate_doc("pol-7") == 2
assert c.get("scope1:london hotel cap") is None and c.get("scope1:claims deadline") == "30 days [1]"
assert "scope1:hotel and claims" not in c._by_doc["faq-2"]
```

Hook `invalidate_doc` to the ingestion pipeline's update and delete events. Keep a TTL as a backstop for missed events. In Redis, the same pattern uses a set per document holding the cache keys.

## Likely follow-ups

- What should happen to cached answers when a user's entitlements change?

---

[← Q0294](../../batch_03_rag_retrieval/0294_rag_over_scanned_and_image_heavy_documents/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0296 →](../../batch_03_rag_retrieval/0296_streaming_rag_answers_with_citations/README.md)
