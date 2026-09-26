# Q0832 · Semantic cache invalidation strategies and cache-hit threshold tuning

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | Semantic caching | Hard |

## Question

Explain semantic cache invalidation strategies when underlying knowledge bases or system prompts change, and write Python code simulating targeted namespace invalidation.

## Answer

Unlike exact key-value caches where invalidating `cache:user:123` is trivial, semantic caches store un-keyed vectors.

Invalidation strategies include:
1. **Namespace / Tenant Partitioning**: Tagging cache entries with `model_version`, `prompt_template_hash`, and `knowledge_base_version`.
2. **TTL Expiration**: Forcing entries to expire after a maximum TTL (e.g. 24 hours).
3. **Targeted Invalidation by Metadata Tag**: Deleting all entries referencing a modified financial entity or regulatory policy.

```python
from typing import Dict, List, Optional


class TaggedSemanticCache:
    def __init__(self):
        self.cache: List[Dict] = []

    def put(self, prompt: str, response: str, tags: List[str], model_version: str) -> None:
        self.cache.append({
            "prompt": prompt,
            "response": response,
            "tags": set(tags),
            "model_version": model_version,
            "valid": True,
        })

    def invalidate_by_tag(self, tag: str) -> int:
        count = 0
        for item in self.cache:
            if tag in item["tags"] and item["valid"]:
                item["valid"] = False
                count += 1
        return count

    def get_valid_entries(self) -> List[Dict]:
        return [item for item in self.cache if item["valid"]]


cache = TaggedSemanticCache()
cache.put("Explain SOFR rate calculation", "SOFR is published by NY Fed...", ["rates", "sofr"], "gpt-4o-v1")
cache.put("Explain Euribor calculation", "Euribor is benchmark rate...", ["rates", "euribor"], "gpt-4o-v1")
cache.put("Explain Credit Default Swaps", "A CDS is a financial swap...", ["derivatives"], "gpt-4o-v1")

# SOFR methodology updated: invalidate 'sofr' tag
invalidated_count = cache.invalidate_by_tag("sofr")
assert invalidated_count == 1
assert len(cache.get_valid_entries()) == 2
```

## Likely follow-ups

- Why is invalidating vector embeddings more computationally expensive than invalidating Redis strings?
- How does changing the system prompt affect the validity of a shared semantic cache?

---

[← Q0831](../../batch_09_genai_services_fastapi/0831_redis_vector_similarity_search_for_semantic_prompt_response/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0833 →](../../batch_09_genai_services_fastapi/0833_exact_sha_256_caching_versus_semantic_vector_caching_trade/README.md)
