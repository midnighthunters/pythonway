# Q0183 · Require exact quotes and verify them

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Grounding | Medium |

## Question

For high-stakes answers, require the model to support claims with exact quotes in the form `"quote" [n]`. Write a verifier that checks each quote appears in the cited source.

## Answer

```python
import re

QUOTE = re.compile(r'"([^"]{8,})"\s*\[(\d+)\]')


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.replace("\u201c", '"').replace("\u201d", '"')).strip().lower()


def verify_quotes(answer: str, sources: dict[int, str]) -> list[tuple[str, int, bool]]:
    return [(q, int(n), _norm(q) in _norm(sources.get(int(n), ""))) for q, n in QUOTE.findall(answer)]


sources = {1: "Hotel stays are capped at GBP 180 per night in London.", 2: "Economy class for flights under 6 hours."}
ans = ('The cap is "capped at GBP 180 per night" [1], and short flights must be '
       '"economy class for flights under 6 hours" [2]. Also "business class is always allowed" [2].')
results = verify_quotes(ans, sources)
assert [ok for _, _, ok in results] == [True, True, False]
```

Quotes are much easier to verify automatically than paraphrases, and easy for users to check. The UI can highlight the quote in the source. Flag or regenerate answers with failed quotes.

## Likely follow-ups

- What's the downside of forcing quotes for every claim?

---

[← Q0182](../../batch_02_prompting_context_structured_output/0182_resolve_conflicting_policy_versions/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0184 →](../../batch_02_prompting_context_structured_output/0184_extract_action_items_from_emails/README.md)
