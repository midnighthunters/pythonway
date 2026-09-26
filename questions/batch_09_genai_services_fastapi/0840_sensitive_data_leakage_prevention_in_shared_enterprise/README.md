# Q0840 · Sensitive data leakage prevention in shared enterprise semantic caches

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | Semantic caching | Hard |

## Question

Explain the risk of cross-tenant data leakage in shared semantic caches, and write Python code enforcing strict tenant isolation and role-based ACLs in cache retrieval.

## Answer

In multi-tenant banking applications (e.g. Wealth Management vs Investment Banking), sharing a semantic cache across departments risks catastrophic data leakage:
If an Investment Banker asks: *"What is the projected EBITDA for Project Falcon?"* and the response is cached, a Wealth Management user asking a similar question must **never** receive that cached response.

Enforcement rules:
1. Always scope cache keys with `tenant_id` and `department_id`.
2. Evaluate Access Control Lists (ACLs) and security classification tags prior to returning cached hits.

```python
from typing import Dict, List, Optional


class SecureTenantCache:
    def __init__(self):
        # tenant_id -> list of records
        self.store: Dict[str, List[Dict]] = {}

    def put(self, tenant_id: str, allowed_roles: List[str], prompt: str, response: str) -> None:
        if tenant_id not in self.store:
            self.store[tenant_id] = []
        self.store[tenant_id].append({
            "prompt": prompt,
            "response": response,
            "allowed_roles": set(allowed_roles),
        })

    def get(self, tenant_id: str, user_role: str, prompt: str) -> Optional[str]:
        # Rule 1: Strict tenant isolation
        records = self.store.get(tenant_id, [])
        for rec in records:
            if rec["prompt"] == prompt:
                # Rule 2: Role entitlement check
                if user_role in rec["allowed_roles"] or "PUBLIC" in rec["allowed_roles"]:
                    return rec["response"]
                else:
                    return None  # Entitlement denial
        return None


cache = SecureTenantCache()
cache.put("tenant_ib", ["MD", "VP"], "Project Falcon EBITDA", "$450M projected FY26")

# Valid access by Vice President
assert cache.get("tenant_ib", "VP", "Project Falcon EBITDA") == "$450M projected FY26"

# Denied access by Analyst in same tenant
assert cache.get("tenant_ib", "ANALYST", "Project Falcon EBITDA") is None

# Denied access by another tenant
assert cache.get("tenant_wealth", "VP", "Project Falcon EBITDA") is None
```

## Likely follow-ups

- How does Chinese Wall compliance (ethical wall) apply to AI caches in investment banks?
- Why should PII-scrubbed prompts be used for cross-tenant universal caches?

---

[← Q0839](../../batch_09_genai_services_fastapi/0839_streaming_responses_from_a_semantic_cache_with_synthetic/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0841 →](../../batch_09_genai_services_fastapi/0841_sliding_window_rate_limiting_middleware_using_redis_lua/README.md)
