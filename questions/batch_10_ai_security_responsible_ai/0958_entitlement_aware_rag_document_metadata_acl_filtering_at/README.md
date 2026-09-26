# Q0958 · Entitlement-aware RAG: document metadata ACL filtering at retrieval time

| Section | Topic | Difficulty |
|---|---|---|
| AI Security, Guardrails & Responsible AI in a Bank | PII and DLP | Hard |

## Question

Explain Entitlement-Aware RAG in enterprise banking, and write Python code implementing pre-filtering of vector search results based on user access control lists (ACLs).

## Answer

In a corporate bank, a Wealth Management analyst and an Investment Banker might query the same RAG knowledge base. If the vector index contains Merger & Acquisition (M&A) deal documents, the Wealth Management user must **never** see those chunks in their retrieval results, even if their query is semantically identical.

**Pre-Filtering vs Post-Filtering**:
- **Post-filtering**: Retrieve top-k (e.g. 50), then discard unauthorized docs. Flaw: if all top-50 results are confidential M&A docs, the user receives 0 results!
- **Pre-filtering (Standard)**: Pass the user's ACL groups directly into the vector database filter query (`$in: user_groups`). Only authorized documents are scored and returned.

```python
from typing import Dict, List, Set


class DocumentChunk:
    def __init__(self, doc_id: str, content: str, allowed_groups: Set[str], score: float):
        self.doc_id = doc_id
        self.content = content
        self.allowed_groups = allowed_groups
        self.score = score


def entitlement_filtered_search(
    chunks: List[DocumentChunk], user_groups: Set[str], top_k: int = 2
) -> List[DocumentChunk]:
    """Pre-filters candidate vector chunks to those authorized for user_groups."""
    eligible = [c for c in chunks if bool(c.allowed_groups & user_groups or "PUBLIC" in c.allowed_groups)]
    # Sort by vector similarity score
    eligible.sort(key=lambda c: c.score, reverse=True)
    return eligible[:top_k]


corpus = [
    DocumentChunk("doc_1", "Project Falcon M&A Target ($5B)", {"GROUP_M_AND_A"}, 0.95),
    DocumentChunk("doc_2", "Public Treasury Yield Commentary", {"PUBLIC"}, 0.88),
    DocumentChunk("doc_3", "Wealth Management Asset Allocation", {"GROUP_WEALTH"}, 0.82),
]

user_wealth_analyst = {"GROUP_WEALTH"}
results = entitlement_filtered_search(corpus, user_wealth_analyst, top_k=2)

assert len(results) == 2
assert results[0].doc_id == "doc_2"  # Public doc
assert results[1].doc_id == "doc_3"  # Wealth doc
assert all(r.doc_id != "doc_1" for r in results)  # M&A doc strictly excluded!
```

## Likely follow-ups

- How do Pinecone, Qdrant, and Milvus implement metadata payload filtering alongside HNSW graphs?
- What performance penalty occurs when metadata filtering prunes 99% of vector candidates?

---

[← Q0957](../../batch_10_ai_security_responsible_ai/0957_enterprise_data_loss_prevention_integration_in_api_gateways/README.md) · [AI Security, Guardrails & Responsible AI in a Bank index](../README.md) · [All sections](../../README.md) · [Q0959 →](../../batch_10_ai_security_responsible_ai/0959_attribute_based_access_control_in_semantic_search/README.md)
