# Q0344 · Property-based fuzzing of output parsers

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | Testing | Medium |

## Question

Fuzz a label parser that extracts a known label from model output. Properties: it never raises, it returns either None or a valid label, and it finds the label when it's wrapped in typical noise.

## Answer

```python
import random
import re
import string

LABELS = ["billing", "access", "other"]


def parse_label(text: str, labels: list[str] = LABELS) -> str | None:
    found = {l for l in labels if re.search(rf"\b{l}\b", text, re.I)}
    return found.pop() if len(found) == 1 else None


rng = random.Random(0)
alphabet = string.printable + "éü中😀\u200b"
for _ in range(2_000):
    s = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 40)))
    out = parse_label(s)
    assert out is None or out in LABELS

wrappers = ['{"label": "%s"}', "Label: **%s**", "  %s.  ", "The answer is %s!", "```\n%s\n```"]
for label in LABELS:
    for w in wrappers:
        for variant in (label, label.upper(), label.title()):
            assert parse_label(w % variant) == label
assert parse_label("billing or access?") is None
```

Returning None when two labels appear is deliberate, since ambiguity shouldn't be resolved by accident. Use the `hypothesis` library for real property-based testing (shrinking to minimal failing examples). The idea is the same: state invariants, then generate many inputs.

## Likely follow-ups

- What invariant would you test for a partial-JSON streaming parser?

---

[← Q0343](../../batch_04_llm_evaluation_observability/0343_record_and_replay_llm_calls/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0345 →](../../batch_04_llm_evaluation_observability/0345_pytest_fixtures_for_llm_applications/README.md)
