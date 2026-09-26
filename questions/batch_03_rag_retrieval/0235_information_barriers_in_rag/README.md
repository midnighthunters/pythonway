# Q0235 · Information barriers in RAG

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Security | Hard |

## Question

Banks keep information barriers (for example between private-side deal teams and public-side research and sales). Implement a barrier check as a second, independent control on top of ACL filtering, so even a misconfigured ACL can't leak across the wall.

## Answer

```python
BARRIERS = {frozenset({"private_side", "public_side"})}


def crosses_barrier(user_side: str | None, doc_side: str | None) -> bool:
    return bool(user_side and doc_side and frozenset({user_side, doc_side}) in BARRIERS)


def barrier_filter(chunks: list[dict], user: dict) -> list[dict]:
    out = []
    for c in chunks:
        acl_ok = bool(set(c.get("acl", [])) & user["groups"])
        if acl_ok and not crosses_barrier(user.get("side"), c.get("side")):
            out.append(c)
    return out


chunks = [
    {"id": "deal-memo", "side": "private_side", "acl": ["m-and-a", "all-staff"]},
    {"id": "research-note", "side": "public_side", "acl": ["research", "all-staff"]},
    {"id": "travel-policy", "side": None, "acl": ["all-staff"]},
]
analyst = {"groups": {"research", "all-staff"}, "side": "public_side"}
banker = {"groups": {"m-and-a", "all-staff"}, "side": "private_side"}
assert [c["id"] for c in barrier_filter(chunks, analyst)] == ["research-note", "travel-policy"]
assert [c["id"] for c in barrier_filter(chunks, banker)] == ["deal-memo", "travel-policy"]
```

The deal memo's ACL wrongly includes `all-staff`, but the barrier still blocks it for the public-side analyst. That is defence in depth.

Also apply barriers to caches (never share cached answers across sides), conversation memory, tools, logs and evaluation data. Wall-crossing (an approved, temporary move) should be an explicit, audited entitlement change, not a prompt instruction.

## Likely follow-ups

- How would you handle a user who is wall-crossed for one specific deal?

---

[← Q0234](../../batch_03_rag_retrieval/0234_why_entitlements_must_filter_before_generation/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0236 →](../../batch_03_rag_retrieval/0236_document_level_versus_chunk_level_security/README.md)
