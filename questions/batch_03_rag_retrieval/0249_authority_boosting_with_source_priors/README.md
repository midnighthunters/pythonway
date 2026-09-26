# Q0249 · Authority boosting with source priors

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Ranking | Medium |

## Question

The same topic appears in an official policy, a team wiki and a Teams chat export. Implement source-authority priors in ranking, and explain how to set them.

## Answer

```python
PRIORS = {"policy_portal": 1.0, "procedure_library": 0.9, "team_wiki": 0.7, "chat_export": 0.4}


def authority_rank(results: list[dict], priors: dict[str, float] = PRIORS, default: float = 0.5) -> list[dict]:
    scored = [{**r, "final": r["score"] * priors.get(r["source"], default)} for r in results]
    return sorted(scored, key=lambda r: (-r["final"], r["id"]))


results = [{"id": "chat-9", "source": "chat_export", "score": 0.92},
           {"id": "pol-7", "source": "policy_portal", "score": 0.81},
           {"id": "wiki-3", "source": "team_wiki", "score": 0.85}]
assert [r["id"] for r in authority_rank(results)] == ["pol-7", "wiki-3", "chat-9"]
assert authority_rank([{"id": "x", "source": "unknown", "score": 1.0}])[0]["final"] == 0.5
```

Set priors with the domain owners (which sources are authoritative for which questions), then tune them on labelled queries. Show the source type in citations so users can judge. Better still, keep unofficial sources out of the index for policy assistants, or separate them clearly ("community content").

## Likely follow-ups

- Should a chat message ever outrank an official policy?

---

[← Q0248](../../batch_03_rag_retrieval/0248_recency_boosting_with_time_decay/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0250 →](../../batch_03_rag_retrieval/0250_semantic_cache_keys_with_entitlements/README.md)
