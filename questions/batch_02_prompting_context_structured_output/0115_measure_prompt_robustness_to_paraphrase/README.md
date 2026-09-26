# Q0115 · Measure prompt robustness to paraphrase

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Prompt testing | Medium |

## Question

Write a small harness that runs several paraphrased versions of the same instruction across a test set and reports per-variant accuracy and the agreement rate between variants.

## Answer

Brittle prompts are a production risk: an innocuous wording change or model upgrade can swing results. Measuring sensitivity makes it visible.

```python
from collections import Counter
from typing import Callable


def robustness_report(variants: dict[str, str], cases: list[tuple[str, str]],
                      llm: Callable[[str, str], str]) -> dict:
    preds = {name: [llm(tpl, x).strip().lower() for x, _ in cases] for name, tpl in variants.items()}
    accuracy = {name: sum(p == y for p, (_, y) in zip(ps, cases)) / len(cases) for name, ps in preds.items()}
    agree = 0
    for i in range(len(cases)):
        votes = Counter(ps[i] for ps in preds.values())
        agree += votes.most_common(1)[0][1] == len(variants)
    return {"accuracy": accuracy, "full_agreement": agree / len(cases)}


def fake_llm(template: str, text: str) -> str:
    if "sentiment" in template.lower():
        return "positive" if "great" in text else "negative"
    return "positive"


cases = [("great service", "positive"), ("awful wait", "negative"), ("great app", "positive")]
report = robustness_report({"v1": "Classify the sentiment:", "v2": "Is this positive or negative?"}, cases, fake_llm)
assert report["accuracy"] == {"v1": 1.0, "v2": 2 / 3}
assert report["full_agreement"] == 2 / 3
```

In real runs, also repeat each variant several times (the model isn't deterministic) and include model-version changes in the same report.

## Likely follow-ups

- What agreement rate would you accept before shipping a classifier prompt?

---

[← Q0114](../../batch_02_prompting_context_structured_output/0114_negative_instructions_and_their_pitfalls/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0116 →](../../batch_02_prompting_context_structured_output/0116_what_context_engineering_means/README.md)
