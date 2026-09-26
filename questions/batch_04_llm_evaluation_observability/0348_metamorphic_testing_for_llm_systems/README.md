# Q0348 · Metamorphic testing for LLM systems

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | Testing | Medium |

## Question

Without labels, you can still test relations that should hold. Implement metamorphic tests for a ticket classifier: appending irrelevant text, changing a person's name, or changing letter case must not change the label.

## Answer

```python
import re
from typing import Callable

TRANSFORMS: dict[str, Callable[[str], str]] = {
    "irrelevant_suffix": lambda t: t + " Thanks, and have a nice weekend!",
    "name_swap": lambda t: re.sub(r"\bPriya\b", "Oleksandr", t),
    "upper_case": str.upper,
}


def metamorphic_violations(classify: Callable[[str], str], inputs: list[str]) -> list[tuple[str, str]]:
    violations = []
    for text in inputs:
        base = classify(text)
        for name, t in TRANSFORMS.items():
            if classify(t(text)) != base:
                violations.append((name, text))
    return violations


def buggy_classifier(text: str) -> str:
    if "weekend" in text.lower():
        return "hr"
    return "access" if "password" in text.lower() else "other"


inputs = ["Priya cannot reset her password", "Printer on floor 3 is jammed"]
v = metamorphic_violations(buggy_classifier, inputs)
assert ("irrelevant_suffix", "Priya cannot reset her password") in v and len(v) == 2
```

The name-swap relation doubles as a fairness probe (outputs shouldn't change with names associated with different groups). Metamorphic tests scale to production traffic, because they need no labels, only relations.

## Likely follow-ups

- Which metamorphic relations would you define for a RAG answer?

---

[← Q0347](../../batch_04_llm_evaluation_observability/0347_test_streaming_handlers_against_arbitrary_chunking/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0349 →](../../batch_04_llm_evaluation_observability/0349_perturbation_robustness_tests/README.md)
