# Q0834 · Multi-tier caching architecture: L1 in-memory LRU and L2 distributed Redis

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | Semantic caching | Medium |

## Question

Write Python code implementing a multi-tier cache: an in-memory L1 LRU cache backed by an L2 distributed cache, tracking hits, misses, and cache promotion.

## Answer

In high-throughput microservices, multi-tier caching reduces network round trips to Redis.
- **L1 (Local Memory / LRU)**: Sub-microsecond access, capped at local RAM limits.
- **L2 (Distributed Redis)**: Shared across all horizontally scaled FastAPI pods, 1-2 ms network latency.

```python
from collections import OrderedDict
from typing import Any, Dict, Optional


class MultiTierCache:
    def __init__(self, l1_capacity: int = 2):
        self.l1_capacity = l1_capacity
        self.l1: OrderedDict[str, Any] = OrderedDict()
        self.l2: Dict[str, Any] = {}  # Simulates distributed Redis
        self.stats = {"l1_hits": 0, "l2_hits": 0, "misses": 0}

    def get(self, key: str) -> Optional[Any]:
        # Check L1
        if key in self.l1:
            self.stats["l1_hits"] += 1
            self.l1.move_to_end(key)
            return self.l1[key]

        # Check L2
        if key in self.l2:
            self.stats["l2_hits"] += 1
            val = self.l2[key]
            # Promote to L1
            self._put_l1(key, val)
            return val

        self.stats["misses"] += 1
        return None

    def _put_l1(self, key: str, val: Any) -> None:
        self.l1[key] = val
        self.l1.move_to_end(key)
        if len(self.l1) > self.l1_capacity:
            self.l1.popitem(last=False)  # Evict oldest LRU item

    def put(self, key: str, val: Any) -> None:
        self._put_l1(key, val)
        self.l2[key] = val


cache = MultiTierCache(l1_capacity=2)
cache.put("k1", "v1")
cache.put("k2", "v2")

# L1 hit
assert cache.get("k1") == "v1"
assert cache.stats["l1_hits"] == 1

# Insert k3: evicts k2 from L1 (k1 was moved to end on get)
cache.put("k3", "v3")

# k2 is now an L2 hit and gets promoted back to L1
assert cache.get("k2") == "v2"
assert cache.stats["l2_hits"] == 1
```

## Likely follow-ups

- What cache stampede problem arises when an entry expires from both L1 and L2 simultaneously?
- How do you synchronize L1 invalidation across multiple FastAPI worker containers?

---

[← Q0833](../../batch_09_genai_services_fastapi/0833_exact_sha_256_caching_versus_semantic_vector_caching_trade/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0835 →](../../batch_09_genai_services_fastapi/0835_handling_temperature_and_non_determinism_in_semantic_cache/README.md)
