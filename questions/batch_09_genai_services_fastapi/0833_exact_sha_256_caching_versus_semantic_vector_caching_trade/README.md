# Q0833 · Exact SHA-256 caching versus semantic vector caching trade-offs

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | Semantic caching | Easy |

## Question

Compare exact string/hash caching (SHA-256) versus semantic vector caching for GenAI services, and write Python code implementing exact hash cache key generation.

## Answer

| Attribute | Exact Hash Caching (SHA-256) | Semantic Vector Caching |
|---|---|---|
| **Lookup Latency** | < 0.5 ms (O(1) hash lookup) | 5 - 25 ms (embedding API call + vector ANN search) |
| **Lookup Cost** | $0.00 (No embedding model call) | Embedding model token cost per request |
| **Hit Rate** | Low (only matches identical character strings) | High (matches rephrased or synonymous queries) |
| **False Positive Rate** | 0.0% (Deterministic match) | 1 - 5% (Depends on cosine threshold tuning) |
| **Implementation Complexity** | Simple Redis GET/SET | Vector index (HNSW/IVF), embedding pipeline, threshold tuning |

```python
import hashlib
import json
from typing import Dict, List


def generate_exact_cache_key(messages: List[Dict[str, str]], model: str, temperature: float) -> str:
    payload = {
        "model": model,
        "temperature": temperature,
        "messages": messages,
    }
    serialized = json.dumps(payload, sort_keys=True)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


req1 = [{"role": "user", "content": "What is the capital of France?"}]
key1 = generate_exact_cache_key(req1, "gpt-4o", 0.0)
key2 = generate_exact_cache_key(req1, "gpt-4o", 0.0)
key3 = generate_exact_cache_key(req1, "gpt-4o", 0.7)

assert key1 == key2
assert key1 != key3  # Different temperature must yield distinct cache key
```

## Likely follow-ups

- Why should you always sort JSON keys when hashing request payloads?
- Can you combine exact hash caching (L1) and semantic caching (L2) in a multi-tier cache?

---

[← Q0832](../../batch_09_genai_services_fastapi/0832_semantic_cache_invalidation_strategies_and_cache_hit/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0834 →](../../batch_09_genai_services_fastapi/0834_multi_tier_caching_architecture_l1_in_memory_lru_and_l2/README.md)
