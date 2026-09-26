# Q0390 · Counterfactual name-swap test

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | Responsible AI | Medium |

## Question

Test whether a model's decision changes when only a person's name changes. Implement a counterfactual harness over templates and name lists, and report the flip rate per template.

## Answer

```python
from itertools import product
from typing import Callable


def counterfactual_flips(templates: list[str], names: dict[str, list[str]], model: Callable[[str], str]) -> dict:
    report = {}
    for tpl in templates:
        outputs = {(g, n): model(tpl.format(name=n)) for g, ns in names.items() for n in ns}
        distinct = set(outputs.values())
        pairs = [(a, b) for a, b in product(outputs, repeat=2) if a < b]
        flips = sum(outputs[a] != outputs[b] for a, b in pairs)
        report[tpl] = {"distinct_outputs": sorted(distinct), "flip_rate": flips / len(pairs) if pairs else 0.0}
    return report


templates = ["{name} requests 3 extra days of parental leave. Approve or escalate?",
             "{name} asks for a laptop upgrade. Approve or escalate?"]
names = {"group_a": ["Emily", "James"], "group_b": ["Aisha", "Kwame"]}


def biased_model(prompt: str) -> str:
    if "parental" in prompt and any(n in prompt for n in ("Aisha", "Kwame")):
        return "escalate"
    return "approve"


r = counterfactual_flips(templates, names, biased_model)
assert r[templates[0]]["flip_rate"] > 0 and r[templates[1]]["flip_rate"] == 0.0
```

Any non-zero flip rate on a decision-like template needs investigation. Use many names per group (single names have idiosyncratic associations), vary other attributes (gender pronouns, age hints), and keep humans accountable for decisions about people.

## Likely follow-ups

- Why does one name per group give misleading results?

---

[← Q0389](../../batch_04_llm_evaluation_observability/0389_fairness_evaluation_across_groups/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0391 →](../../batch_04_llm_evaluation_observability/0391_choose_a_moderation_classifier_threshold/README.md)
