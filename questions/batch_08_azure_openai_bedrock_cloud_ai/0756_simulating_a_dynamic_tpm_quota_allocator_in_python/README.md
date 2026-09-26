# Q0756 · Simulating a dynamic TPM quota allocator in Python

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | Azure OpenAI | Medium |

## Question

Write Python code implementing a multi-tenant token quota allocator that tracks consumed tokens per minute and blocks requests exceeding tenant TPM limits.

## Answer

```python
import time
from typing import Dict, Tuple


class DynamicTPMQuotaAllocator:
    def __init__(self, tenant_limits: Dict[str, int]):
        self.tenant_limits = tenant_limits  # tenant_id -> max tokens per minute
        # Maps tenant_id -> (window_start_time, tokens_consumed)
        self._usage: Dict[str, Tuple[float, int]] = {}

    def request_tokens(self, tenant_id: str, tokens_needed: int) -> Tuple[bool, str]:
        limit = self.tenant_limits.get(tenant_id, 10000)
        now = time.time()

        if tenant_id not in self._usage:
            self._usage[tenant_id] = (now, 0)

        window_start, consumed = self._usage[tenant_id]

        # Reset window after 60 seconds (simulated with 0.1s for fast test)
        if now - window_start >= 0.1:
            window_start = now
            consumed = 0

        if consumed + tokens_needed > limit:
            return False, f"TPM quota exceeded for {tenant_id}: {consumed + tokens_needed} > {limit}"

        self._usage[tenant_id] = (window_start, consumed + tokens_needed)
        return True, "Allocated"


allocator = DynamicTPMQuotaAllocator({"equities_desk": 1000, "research_desk": 500})

# Equities desk requests 600 tokens: succeeds
ok1, _ = allocator.request_tokens("equities_desk", 600)
assert ok1 is True

# Equities desk requests another 500 tokens (total 1100 > 1000): rejected
ok2, msg = allocator.request_tokens("equities_desk", 500)
assert ok2 is False
assert "quota exceeded" in msg

# Research desk has independent quota
ok3, _ = allocator.request_tokens("research_desk", 400)
assert ok3 is True
```

## Likely follow-ups

- How does a token reservation system handle requests whose completion length is unknown before generation?
- How should unconsumed reserved tokens be returned to the pool upon stream completion?

---

[← Q0755](../../batch_08_azure_openai_bedrock_cloud_ai/0755_multi_tenant_quota_management_across_business_units/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0757 →](../../batch_08_azure_openai_bedrock_cloud_ai/0757_azure_monitor_and_application_insights_for_llm_latency/README.md)
