# Q0248 · Recency boosting with time decay

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Ranking | Medium |

## Question

Implement a recency boost that blends relevance with an exponential time decay (with a half-life), so newer documents win ties but a strongly relevant old document still beats a weakly relevant new one. Exempt evergreen document types.

## Answer

```python
def recency_boost(score: float, age_days: float, doc_type: str, half_life: float = 180,
                  weight: float = 0.3, evergreen: frozenset = frozenset({"policy_definition", "glossary"})) -> float:
    if doc_type in evergreen:
        return score
    decay = 0.5 ** (age_days / half_life)
    return score * ((1 - weight) + weight * decay)


new, old = recency_boost(0.8, 10, "news"), recency_boost(0.8, 720, "news")
assert new > old
assert recency_boost(0.95, 720, "news") > recency_boost(0.6, 1, "news")
assert recency_boost(0.8, 5000, "glossary") == 0.8
assert abs(recency_boost(1.0, 180, "news") - 0.85) < 1e-12
```

Multiplying keeps the boost proportional to relevance. For policies, prefer explicit version logic (the effective version) over decay: an old but current policy must not be penalised.

## Likely follow-ups

- Why is decay the wrong tool for policy versions?

---

[← Q0247](../../batch_03_rag_retrieval/0247_diagnose_a_bad_rag_answer/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0249 →](../../batch_03_rag_retrieval/0249_authority_boosting_with_source_priors/README.md)
