# Q0740 · Implementing prompt prefix cache matching in Python

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | GPU Serving | Medium |

## Question

Write Python code implementing an exact prefix cache matcher that extracts reusable cached token counts between incoming queries.

## Answer

```python
from typing import List, Tuple


class PrefixCacheIndex:
    def __init__(self):
        self._cached_prefixes: List[List[str]] = []

    def register_prefix(self, tokens: List[str]) -> None:
        self._cached_prefixes.append(tokens)

    def find_longest_cached_prefix(self, query_tokens: List[str]) -> int:
        max_shared = 0
        for cached in self._cached_prefixes:
            shared = 0
            for c_tok, q_tok in zip(cached, query_tokens):
                if c_tok == q_tok:
                    shared += 1
                else:
                    break
            if shared > max_shared:
                max_shared = shared
        return max_shared


index = PrefixCacheIndex()
system_policy = ["System:", "You", "are", "a", "bank", "assistant", "Policy:", "Strict"]
index.register_prefix(system_policy)

# Query starts with exact same 8 tokens, followed by user question
incoming = system_policy + ["User:", "What", "is", "VaR?"]
shared_count = index.find_longest_cached_prefix(incoming)

assert shared_count == 8  # First 8 tokens hit KV cache
```

## Likely follow-ups

- How does prefix matching interact with PagedAttention block boundaries?
- How should least-recently-used (LRU) eviction manage GPU cache memory across tenants?

---

[← Q0739](../../batch_08_azure_openai_bedrock_cloud_ai/0739_prefix_caching_and_prompt_caching_across_multi_turn_sessions/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0741 →](../../batch_08_azure_openai_bedrock_cloud_ai/0741_triton_inference_server_for_multi_model_serving/README.md)
