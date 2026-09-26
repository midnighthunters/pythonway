# Q0160 · Deduplicate memory facts

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Memory | Medium |

## Question

Memories accumulate near-duplicates ("prefers aisle seats", "Prefers aisle seat."). Write a deduplicator that normalises text, treats near matches (similarity ≥ 0.9) as duplicates, and keeps the most recent version.

## Answer

```python
import re
from difflib import SequenceMatcher


def _norm(s: str) -> str:
    return re.sub(r"[^a-z0-9 ]", "", re.sub(r"\s+", " ", s.lower())).strip()


def dedupe_memories(items: list[dict], threshold: float = 0.9) -> list[dict]:
    """items: {'text': str, 'ts': int}. Returns unique items, newest wins, ordered by ts."""
    kept: list[dict] = []
    for item in sorted(items, key=lambda m: m["ts"], reverse=True):
        n = _norm(item["text"])
        if all(SequenceMatcher(None, n, _norm(k["text"])).ratio() < threshold for k in kept):
            kept.append(item)
    return sorted(kept, key=lambda m: m["ts"])


mems = [{"text": "Prefers aisle seats", "ts": 1}, {"text": "prefers aisle seat.", "ts": 5},
        {"text": "Works from Canary Wharf", "ts": 2}, {"text": "Prefers window seats", "ts": 3}]
out = dedupe_memories(mems)
assert [m["text"] for m in out] == ["Works from Canary Wharf", "Prefers window seats", "prefers aisle seat."]
```

This is O(n²), which is fine for per-user memory sizes. "Aisle" versus "window" survives because it is a conflict, not a duplicate. Conflicts need a resolution rule (the most recent explicit statement wins, or ask the user). At scale, use embeddings for candidate duplicates and an LLM or rules to merge.

## Likely follow-ups

- Why is string similarity a poor detector of contradictory memories?

---

[← Q0159](../../batch_02_prompting_context_structured_output/0159_extract_user_preferences_into_structured_memory/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0161 →](../../batch_02_prompting_context_structured_output/0161_account_for_every_token_in_a_request/README.md)
