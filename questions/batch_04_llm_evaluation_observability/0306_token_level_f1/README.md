# Q0306 · Token-level F1

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | Metrics | Easy |

## Question

Implement SQuAD-style token F1 between a predicted and a gold answer, and explain what it rewards.

## Answer

```python
import re
import string
from collections import Counter


def normalize_tokens(s: str) -> list[str]:
    s = "".join(ch for ch in s.lower() if ch not in set(string.punctuation))
    return re.sub(r"\b(a|an|the)\b", " ", s).split()


def token_f1(pred: str, gold: str) -> float:
    p, g = normalize_tokens(pred), normalize_tokens(gold)
    if not p or not g:
        return float(p == g)
    common = sum((Counter(p) & Counter(g)).values())
    if common == 0:
        return 0.0
    precision, recall = common / len(p), common / len(g)
    return 2 * precision * recall / (precision + recall)


assert abs(token_f1("the cat sat down", "cat sat") - 0.8) < 1e-12
assert token_f1("Treasury", "treasury") == 1.0
assert token_f1("", "") == 1.0 and token_f1("x", "") == 0.0
```

It gives partial credit for overlapping words, which is useful for short extractive answers. It ignores word order and meaning, so "approved" and "not approved" overlap heavily. Don't use it as the main metric for long generative answers.

## Likely follow-ups

- Construct a case where token F1 is high but the answer is wrong.

---

[← Q0305](../../batch_04_llm_evaluation_observability/0305_exact_and_normalised_match/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0307 →](../../batch_04_llm_evaluation_observability/0307_rouge_l_with_longest_common_subsequence/README.md)
