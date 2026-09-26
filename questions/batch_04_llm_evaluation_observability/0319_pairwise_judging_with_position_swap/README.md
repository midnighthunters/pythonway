# Q0319 · Pairwise judging with position swap

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | Model-graded evaluation | Medium |

## Question

Implement pairwise comparison of two answers with an LLM judge that runs both orderings, and only declares a winner when both orderings agree, to cancel position bias.

## Answer

```python
from typing import Callable


def pairwise(question: str, a: str, b: str, judge: Callable[[str, str, str], str]) -> str:
    first = judge(question, a, b)
    second = judge(question, b, a)
    second_mapped = {"first": "second", "second": "first", "tie": "tie"}[second]
    if first == second_mapped and first != "tie":
        return "A" if first == "first" else "B"
    return "tie"


def biased_judge(q: str, x: str, y: str) -> str:
    if len(x) > 3 * len(y):
        return "first"
    if len(y) > 3 * len(x):
        return "second"
    return "first"


assert pairwise("q", "short", "slightly longer", biased_judge) == "tie"
assert pairwise("q", "a thorough and correct answer", "no", biased_judge) == "A"
assert pairwise("q", "no", "a thorough and correct answer", biased_judge) == "B"
```

This judge always prefers the first position unless the difference is large. Swapping the order exposes the bias, and the inconsistent verdict becomes a tie instead of a false win. Report the win rate with ties, and the inconsistency rate, which is itself a measure of judge reliability.

## Likely follow-ups

- What does a high inconsistency rate tell you about the two systems being compared?

---

[← Q0318](../../batch_04_llm_evaluation_observability/0318_judge_prompt_with_rubric_and_structured_verdict/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0320 →](../../batch_04_llm_evaluation_observability/0320_known_biases_of_llm_judges/README.md)
