# Q0717 · Semantic caching at the AI gateway layer

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | Cloud AI Gateways | Medium |

## Question

How does semantic caching differ from exact-match caching for LLM requests? Write Python code implementing an in-memory cosine-similarity cache for LLM completions.

## Answer

Traditional exact-match caching (hashing prompt strings) fails for GenAI because slight variations ("What is the EURUSD rate?" vs "What's the current EUR/USD spot rate?") produce different cache keys.

Semantic caching embeds the incoming query into a vector and searches a vector store for previously answered queries with high cosine similarity (e.g. similarity $\ge 0.95$). If a match is found, the cached completion is returned instantly, saving 100% of LLM inference cost and reducing latency from 2 seconds to 10 milliseconds.

```python
import math
from typing import Any, Dict, List, Optional, Tuple


def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    dot = sum(a * b for a, b in zip(v1, v2))
    norm1 = math.sqrt(sum(a * a for a in v1))
    norm2 = math.sqrt(sum(b * b for b in v2))
    return dot / (norm1 * norm2) if norm1 and norm2 else 0.0


class SemanticCache:
    def __init__(self, similarity_threshold: float = 0.90):
        self.threshold = similarity_threshold
        self._entries: List[Tuple[str, List[float], str]] = []  # (query, vector, answer)

    def lookup(self, query_vec: List[float]) -> Optional[Tuple[str, float]]:
        best_match = None
        best_score = -1.0
        for query, vec, ans in self._entries:
            sim = cosine_similarity(query_vec, vec)
            if sim > best_score:
                best_score = sim
                best_match = ans

        if best_score >= self.threshold:
            return best_match, best_score
        return None

    def store(self, query: str, query_vec: List[float], answer: str) -> None:
        self._entries.append((query, query_vec, answer))


cache = SemanticCache(similarity_threshold=0.90)
cache.store("What is London hotel cap?", [1.0, 0.0, 0.0], "London cap is £180.")

# Query with near-identical vector (sim = 0.96)
hit = cache.lookup([0.96, 0.28, 0.0])
assert hit is not None
assert hit[0] == "London cap is £180."

# Dissimilar query (sim = 0.0)
miss = cache.lookup([0.0, 1.0, 0.0])
assert miss is None
```

## Likely follow-ups

- What are the risks of semantic cache poisoning?
- Why must queries containing time-sensitive data (e.g. stock prices) bypass semantic caches?

---

[← Q0716](../../batch_08_azure_openai_bedrock_cloud_ai/0716_token_counting_and_cost_metering_per_tenant/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0718 →](../../batch_08_azure_openai_bedrock_cloud_ai/0718_weighted_round_robin_load_balancing_across_cloud_llm_regions/README.md)
