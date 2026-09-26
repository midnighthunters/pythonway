# Q0843 · Tenant-based quota enforcement and tiered subscription rate limits

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | Rate limiting and quotas | Medium |

## Question

Write Python code implementing a multi-tenant quota manager supporting tiered service levels (Bronze, Silver, Gold) with daily spend and concurrency caps.

## Answer

In enterprise LLM platforms, different lines of business or subscription tiers require differentiated service levels to ensure fair sharing of shared cloud GPU clusters.

```python
from typing import Dict, Optional


class TenantTier:
    def __init__(self, name: str, max_concurrent: int, daily_token_quota: int):
        self.name = name
        self.max_concurrent = max_concurrent
        self.daily_token_quota = daily_token_quota


TIERS = {
    "BRONZE": TenantTier("Bronze", max_concurrent=2, daily_token_quota=10_000),
    "GOLD": TenantTier("Gold", max_concurrent=20, daily_token_quota=1_000_000),
}


class TenantQuotaManager:
    def __init__(self):
        # tenant_id -> {"tier": str, "active_concurrency": int, "tokens_consumed_today": int}
        self.tenants: Dict[str, Dict] = {}

    def register_tenant(self, tenant_id: str, tier_name: str) -> None:
        self.tenants[tenant_id] = {
            "tier": TIERS[tier_name],
            "active_concurrency": 0,
            "tokens_consumed_today": 0,
        }

    def acquire_slot(self, tenant_id: str, estimated_tokens: int) -> bool:
        tenant = self.tenants.get(tenant_id)
        if not tenant:
            return False
        tier = tenant["tier"]

        # Check concurrency
        if tenant["active_concurrency"] >= tier.max_concurrent:
            return False

        # Check daily quota
        if tenant["tokens_consumed_today"] + estimated_tokens > tier.daily_token_quota:
            return False

        tenant["active_concurrency"] += 1
        return True

    def release_slot(self, tenant_id: str, actual_tokens: int) -> None:
        tenant = self.tenants[tenant_id]
        tenant["active_concurrency"] = max(0, tenant["active_concurrency"] - 1)
        tenant["tokens_consumed_today"] += actual_tokens


mgr = TenantQuotaManager()
mgr.register_tenant("desk_fx_small", "BRONZE")

# First 2 concurrent slots succeed
assert mgr.acquire_slot("desk_fx_small", 100) is True
assert mgr.acquire_slot("desk_fx_small", 100) is True

# 3rd concurrent slot rejected for Bronze tier
assert mgr.acquire_slot("desk_fx_small", 100) is False

# Releasing slot frees concurrency
mgr.release_slot("desk_fx_small", actual_tokens=150)
assert mgr.acquire_slot("desk_fx_small", 100) is True
```

## Likely follow-ups

- How do you reset daily token quotas at midnight UTC across distributed databases?
- What alerting should fire when a department hits 80% and 95% of its monthly token budget?

---

[← Q0842](../../batch_09_genai_services_fastapi/0842_token_bucket_algorithm_for_managing_llm_token_rate_limits/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0844 →](../../batch_09_genai_services_fastapi/0844_per_request_token_budgeting_and_hard_cutoff_limits_in/README.md)
