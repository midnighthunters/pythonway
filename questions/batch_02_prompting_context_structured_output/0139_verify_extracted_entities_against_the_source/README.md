# Q0139 · Verify extracted entities against the source

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Grounding | Medium |

## Question

The model extracts account numbers, names and amounts from an email. Write a check that each extracted value appears verbatim in the source (after whitespace normalisation) and flags the ones that don't, since those are likely hallucinated.

## Answer

```python
import re


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip().lower()


def verify_entities(source: str, entities: list[dict]) -> tuple[list[dict], list[dict]]:
    haystack = _norm(source)
    verified, suspicious = [], []
    for e in entities:
        (verified if _norm(e["value"]) in haystack else suspicious).append(e)
    return verified, suspicious


email = "Hi team,\nPlease refund  GBP 125.00 to account 12-34-56 87654321 for Jane   Doe.\nThanks"
ents = [{"type": "amount", "value": "GBP 125.00"}, {"type": "account", "value": "12-34-56 87654321"},
        {"type": "name", "value": "Jane Doe"}, {"type": "account", "value": "12-34-56 87654322"}]
ok, bad = verify_entities(email, ents)
assert [e["value"] for e in ok] == ["GBP 125.00", "12-34-56 87654321", "Jane Doe"]
assert bad == [{"type": "account", "value": "12-34-56 87654322"}]
```

The fake account number differs by one digit, which is exactly the kind of error people miss. Ask the model to return values exactly as written (a `source_text` field) and normalise them separately afterwards. Verbatim checks don't work for derived values (for example "total of all refunds"), which need arithmetic checks instead.

## Likely follow-ups

- How would you handle values the model legitimately reformats, such as dates?

---

[← Q0138](../../batch_02_prompting_context_structured_output/0138_self_reported_confidence_pitfalls/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0140 →](../../batch_02_prompting_context_structured_output/0140_summarisation_prompt_design/README.md)
