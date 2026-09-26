# Q0305 · Exact and normalised match

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | Metrics | Easy |

## Question

Implement exact match with SQuAD-style normalisation (lowercase, strip punctuation and articles, collapse whitespace), and explain when exact match is the right metric.

## Answer

```python
import re
import string


def normalize_answer(s: str) -> str:
    s = s.lower()
    s = "".join(ch for ch in s if ch not in set(string.punctuation))
    s = re.sub(r"\b(a|an|the)\b", " ", s)
    return " ".join(s.split())


def exact_match(pred: str, gold: str | list[str]) -> bool:
    golds = [gold] if isinstance(gold, str) else gold
    return any(normalize_answer(pred) == normalize_answer(g) for g in golds)


assert exact_match("The Treasury team.", "treasury team")
assert exact_match("180 GBP", ["£180", "180 GBP"])
assert not exact_match("180 USD", "180 GBP")
```

Use exact match for closed answers: labels, ids, dates, amounts, yes/no and short extractive answers. Normalise units and formats in code first (for example parse amounts to Decimal). For free-text answers, use token F1, key-point coverage or judges instead.

## Likely follow-ups

- Why does stripping punctuation break comparisons of amounts such as "1,800" and "18.00"?

---

[← Q0304](../../batch_04_llm_evaluation_observability/0304_evaluation_dataset_schema/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0306 →](../../batch_04_llm_evaluation_observability/0306_token_level_f1/README.md)
