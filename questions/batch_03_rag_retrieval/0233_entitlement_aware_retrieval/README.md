# Q0233 · Entitlement-aware retrieval

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Security | Hard |

## Question

Implement retrieval where each chunk has `allowed_groups`. Filter by the user's groups before ranking, deny chunks with no ACL by default, and make sure the result count and scores never reveal inaccessible documents.

## Answer

```python
from typing import Callable


def secure_retrieve(query: str, chunks: list[dict], user_groups: set[str],
                    score: Callable[[str, str], float], k: int) -> list[dict]:
    visible = [c for c in chunks if c.get("allowed_groups") and user_groups & set(c["allowed_groups"])]
    ranked = sorted(visible, key=lambda c: (-score(query, c["text"]), c["id"]))
    return [{"id": c["id"], "text": c["text"]} for c in ranked[:k] if score(query, c["text"]) > 0]


def overlap(q: str, t: str) -> float:
    return len(set(q.lower().split()) & set(t.lower().split()))


chunks = [
    {"id": "hr-1", "text": "salary bands for vice president", "allowed_groups": ["hr-comp"]},
    {"id": "pol-1", "text": "travel policy for vice president grade", "allowed_groups": ["all-staff"]},
    {"id": "orphan", "text": "salary bands draft", "allowed_groups": []},
]
assert [c["id"] for c in secure_retrieve("vice president salary bands", chunks, {"all-staff"}, overlap, 5)] == ["pol-1"]
assert [c["id"] for c in secure_retrieve("salary bands", chunks, {"hr-comp", "all-staff"}, overlap, 5)] == ["hr-1"]
```

Principles:
- Filter inside the search (pre-filter or filtered ANN), never after generation. The model must never see what the user can't.
- Deny by default: a missing ACL means no access, not public access.
- Sync ACLs from the source systems (group memberships change daily), resolve nested groups, and re-check at query time for highly sensitive sources.
- Don't leak through side channels: counts ("12 results, 11 hidden"), scores, suggestions, caches or logs.

## Likely follow-ups

- How would you handle a user whose group membership was revoked five minutes ago?

---

[← Q0232](../../batch_03_rag_retrieval/0232_extract_metadata_filters_from_queries/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0234 →](../../batch_03_rag_retrieval/0234_why_entitlements_must_filter_before_generation/README.md)
