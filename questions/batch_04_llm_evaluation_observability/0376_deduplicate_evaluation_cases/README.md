# Q0376 · Deduplicate evaluation cases

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | Datasets | Easy |

## Question

A golden set assembled from logs has many near-duplicate questions that over-weight some intents. Deduplicate them with normalisation and a similarity threshold, keeping the first occurrence.

## Answer

```python
import re
from difflib import SequenceMatcher


def dedupe_cases(questions: list[str], threshold: float = 0.9) -> list[str]:
    kept, norms = [], []
    for q in questions:
        n = " ".join(re.findall(r"[a-z0-9]+", q.lower()))
        if any(SequenceMatcher(None, n, k).ratio() >= threshold for k in norms):
            continue
        kept.append(q)
        norms.append(n)
    return kept


qs = ["What is the London hotel cap?", "what's the London hotel cap", "What is the London hotel cap??",
      "What is the Paris hotel cap?", "How do I file expenses?"]
assert dedupe_cases(qs) == ["What is the London hotel cap?", "What is the Paris hotel cap?", "How do I file expenses?"]
```

Notice that "London" and "Paris" survive as distinct cases. They need different answers even though they're textually similar. Keep the duplicate counts as frequency weights if you want the evaluation to reflect traffic, but report unweighted results too.

## Likely follow-ups

- When should near-duplicate cases be kept deliberately?

---

[← Q0375](../../batch_04_llm_evaluation_observability/0375_check_for_evaluation_leakage/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0377 →](../../batch_04_llm_evaluation_observability/0377_stratified_sampling_for_evaluation_sets/README.md)
