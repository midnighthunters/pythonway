# Q0960 · Preventing cross-tenant data bleed in shared vector databases

| Section | Topic | Difficulty |
|---|---|---|
| AI Security, Guardrails & Responsible AI in a Bank | PII and DLP | Hard |

## Question

Explain how cross-tenant data bleed occurs in shared vector indexes, and write Python code demonstrating tenant namespace partitioning and query isolation.

## Answer

In multi-tenant SaaS or corporate shared platforms, if embeddings from Tenant A (e.g. Asset Management) and Tenant B (e.g. Commercial Banking) are indexed in the same vector collection without strict namespace partitioning, an approximate nearest neighbor (ANN) search can retrieve Tenant A's documents for Tenant B's users.

Defenses:
1. **Namespace Isolation**: Each tenant writes and queries a completely separate vector namespace (e.g. `index.query(namespace=tenant_id)`).
2. **Metadata Partitioning**: Mandatory metadata filter `tenant_id == current_tenant` enforced at the database driver level.

```python
from typing import Dict, List


class IsolatedVectorStore:
    def __init__(self):
        # Maps namespace (tenant_id) -> list of document records
        self._namespaces: Dict[str, List[dict]] = {}

    def insert(self, tenant_id: str, doc_id: str, text: str) -> None:
        if tenant_id not in self._namespaces:
            self._namespaces[tenant_id] = []
        self._namespaces[tenant_id].append({"doc_id": doc_id, "text": text})

    def query(self, tenant_id: str, query_text: str) -> List[dict]:
        # Enforce strict namespace lookup: impossible to access other tenants
        return self._namespaces.get(tenant_id, [])


store = IsolatedVectorStore()
store.insert("tenant_wealth", "doc_w1", "Private wealth portfolio strategy")
store.insert("tenant_ib", "doc_ib1", "Confidential IPO pipeline")

# Wealth query
wealth_results = store.query("tenant_wealth", "strategy")
assert len(wealth_results) == 1
assert wealth_results[0]["doc_id"] == "doc_w1"

# IB cannot be retrieved from wealth query
assert all(r["doc_id"] != "doc_ib1" for r in wealth_results)
```

## Likely follow-ups

- What are the resource cost differences between separate vector collections vs shared collections with metadata filtering?
- How do vector databases like Pinecone and Qdrant implement multi-tenant namespace partitioning?

---

[← Q0959](../../batch_10_ai_security_responsible_ai/0959_attribute_based_access_control_in_semantic_search/README.md) · [AI Security, Guardrails & Responsible AI in a Bank index](../README.md) · [All sections](../../README.md) · [Q0961 →](../../batch_10_ai_security_responsible_ai/0961_customer_banking_secrecy_regulations_glba_gdpr_art_9_nydfs/README.md)
