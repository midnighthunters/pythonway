# Q0831 · Redis vector similarity search for semantic prompt response caching

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | Semantic caching | Medium |

## Question

Write Python code implementing an in-memory cosine-similarity semantic response cache, checking whether an incoming prompt matches a previously answered prompt above a similarity threshold.

## Answer

Semantic caching bypasses costly LLM inference calls by indexing past prompt embeddings in a vector database (e.g. Redis RediSearch Vector Similarity or pgvector). If cosine similarity exceeds a threshold (e.g. 0.92), the cached response is returned immediately.

```python
import math
from typing import Dict, List, Optional, Tuple


def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    dot = sum(a * b for a, b in zip(v1, v2))
    norm_a = math.sqrt(sum(a * a for a in v1))
    norm_b = math.sqrt(sum(b * b for b in v2))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


class SemanticCache:
    def __init__(self, threshold: float = 0.90):
        self.threshold = threshold
        # List of tuples: (prompt, embedding, response)
        self.entries: List[Tuple[str, List[float], str]] = []

    def lookup(self, query_embedding: List[float]) -> Optional[Tuple[str, float]]:
        best_match = None
        highest_score = -1.0

        for prompt, emb, response in self.entries:
            sim = cosine_similarity(query_embedding, emb)
            if sim > highest_score:
                highest_score = sim
                best_match = response

        if highest_score >= self.threshold and best_match:
            return best_match, highest_score
        return None

    def store(self, prompt: str, embedding: List[float], response: str) -> None:
        self.entries.append((prompt, embedding, response))


# Verification
cache = SemanticCache(threshold=0.90)
cache.store("What is Value at Risk?", [1.0, 0.0, 0.0], "VaR measures potential financial loss.")

# Query 1: Highly similar vector ([0.99, 0.05, 0.0])
hit = cache.lookup([0.99, 0.05, 0.0])
assert hit is not None
assert hit[0] == "VaR measures potential financial loss."
assert hit[1] > 0.95

# Query 2: Dissimilar vector ([0.0, 1.0, 0.0])
miss = cache.lookup([0.0, 1.0, 0.0])
assert miss is None
```

## Likely follow-ups

- What are the risks of semantic cache false positives when user queries have subtle semantic differences (e.g. "Buy 100 AAPL" vs "Sell 100 AAPL")?
- How do you tune the similarity threshold between false-positive risk and cache-hit rate?

---

[← Q0830](../../batch_09_genai_services_fastapi/0830_read_consistency_models_in_nosql_state_stores_for_genai_apps/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0832 →](../../batch_09_genai_services_fastapi/0832_semantic_cache_invalidation_strategies_and_cache_hit/README.md)
