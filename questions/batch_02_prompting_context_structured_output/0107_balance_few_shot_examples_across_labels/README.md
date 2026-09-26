# Q0107 · Balance few-shot examples across labels

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Few-shot | Easy |

## Question

Write a function that picks k few-shot examples for a classifier prompt, round-robin across labels, so no label dominates, with deterministic output.

## Answer

Majority-label bias is real: if most examples in the prompt say "approve", the model leans towards "approve".

```python
from collections import defaultdict
from itertools import cycle


def balanced_examples(examples: list[dict], k: int) -> list[dict]:
    by_label: dict[str, list[dict]] = defaultdict(list)
    for ex in examples:
        by_label[ex["label"]].append(ex)
    labels = sorted(by_label)
    picked: list[dict] = []
    for label in cycle(labels):
        if len(picked) == k or not any(by_label.values()):
            break
        if by_label[label]:
            picked.append(by_label[label].pop(0))
    return picked


data = [{"text": f"t{i}", "label": "approve"} for i in range(6)] + [
    {"text": "r1", "label": "reject"}, {"text": "e1", "label": "escalate"}]
out = balanced_examples(data, 5)
assert [e["label"] for e in out] == ["approve", "escalate", "reject", "approve", "approve"]
assert len(balanced_examples(data, 100)) == len(data)
```

Also shuffle the final order (with a fixed seed) or interleave labels, because a run of the same label at the end creates recency bias.

## Likely follow-ups

- When would you intentionally reflect the real class distribution instead?

---

[← Q0106](../../batch_02_prompting_context_structured_output/0106_select_few_shot_examples_by_similarity_with_diversity/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0108 →](../../batch_02_prompting_context_structured_output/0108_few_shot_order_and_recency_effects/README.md)
