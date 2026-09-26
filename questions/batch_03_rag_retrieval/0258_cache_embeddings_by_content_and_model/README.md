# Q0258 · Cache embeddings by content and model

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Ingestion | Medium |

## Question

Implement an embedding cache keyed by model and content hash that calls the embedding API only for misses (batched), returns vectors in input order, and reports cache statistics.

## Answer

```python
import hashlib
from typing import Callable


class EmbeddingCache:
    def __init__(self, model: str, embed_batch: Callable[[list[str]], list[list[float]]]) -> None:
        self.model, self._embed, self._store = model, embed_batch, {}
        self.hits = self.misses = self.api_calls = 0

    def _key(self, text: str) -> str:
        return hashlib.sha256(f"{self.model}\x00{text}".encode()).hexdigest()

    def embed(self, texts: list[str]) -> list[list[float]]:
        keys = [self._key(t) for t in texts]
        missing = list(dict.fromkeys(k for k in keys if k not in self._store))
        self.hits += sum(k in self._store for k in keys)
        self.misses += len(keys) - sum(k in self._store for k in keys)
        if missing:
            texts_by_key = {k: t for k, t in zip(keys, texts)}
            vectors = self._embed([texts_by_key[k] for k in missing])
            self.api_calls += 1
            self._store.update(zip(missing, vectors))
        return [self._store[k] for k in keys]


calls: list[list[str]] = []
fake = lambda batch: (calls.append(batch), [[float(len(t))] for t in batch])[1]
cache = EmbeddingCache("embed-v2", fake)
assert cache.embed(["a", "bb", "a"]) == [[1.0], [2.0], [1.0]]
assert cache.embed(["bb", "ccc"]) == [[2.0], [3.0]]
assert calls == [["a", "bb"], ["ccc"]] and cache.api_calls == 2
```

In production, back the cache with a persistent key-value store (Redis, DynamoDB or the vector store itself), batch within the API's item and token limits, and treat embeddings as sensitive data (they can leak information about the text).

## Likely follow-ups

- Why include a separator byte between the model and the text in the key?

---

[← Q0257](../../batch_03_rag_retrieval/0257_choose_long_context_or_retrieval_per_request/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0259 →](../../batch_03_rag_retrieval/0259_migrate_to_a_new_embedding_model/README.md)
