# Q0182 · Resolve conflicting policy versions

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Grounding | Medium |

## Question

Retrieval returns several versions of the same policy. Write a function that keeps, for each policy, the latest version effective on the given date, and reports excluded versions (superseded or not yet effective).

## Answer

```python
from datetime import date


def effective_versions(docs: list[dict], as_of: date) -> tuple[list[dict], list[str]]:
    best: dict[str, dict] = {}
    for d in docs:
        if d["effective"] <= as_of:
            cur = best.get(d["policy_id"])
            if cur is None or d["effective"] > cur["effective"]:
                best[d["policy_id"]] = d
    keep = {d["doc_id"] for d in best.values()}
    return sorted(best.values(), key=lambda d: d["policy_id"]), [d["doc_id"] for d in docs if d["doc_id"] not in keep]


docs = [
    {"doc_id": "travel-v3", "policy_id": "travel", "effective": date(2025, 1, 1)},
    {"doc_id": "travel-v4", "policy_id": "travel", "effective": date(2026, 4, 1)},
    {"doc_id": "travel-v5", "policy_id": "travel", "effective": date(2027, 1, 1)},
    {"doc_id": "expenses-v2", "policy_id": "expenses", "effective": date(2026, 2, 1)},
]
kept, excluded = effective_versions(docs, date(2026, 9, 26))
assert [d["doc_id"] for d in kept] == ["expenses-v2", "travel-v4"]
assert excluded == ["travel-v3", "travel-v5"]
```

Resolving conflicts deterministically before the prompt is more reliable than asking the model to work out which version applies. Keep the "not yet effective" version available for questions such as "what's changing next year?".

## Likely follow-ups

- Where should this logic live: in the retriever, a post-filter, or the prompt?

---

[← Q0181](../../batch_02_prompting_context_structured_output/0181_source_metadata_for_grounding/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0183 →](../../batch_02_prompting_context_structured_output/0183_require_exact_quotes_and_verify_them/README.md)
