# Q0171 · Strip scratchpad content before display

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Output handling | Medium |

## Question

A prompt lets the model think in `<thinking>` tags before answering. Write a display filter that removes complete thinking blocks and any unclosed trailing block (which happens when a response is cut off or still streaming).

## Answer

```python
import re

BLOCK = re.compile(r"<thinking>.*?</thinking>", re.S | re.I)
OPEN_TAIL = re.compile(r"<thinking>.*\Z", re.S | re.I)


def visible_text(text: str) -> str:
    return OPEN_TAIL.sub("", BLOCK.sub("", text)).strip()


assert visible_text("<thinking>check policy §4</thinking>The limit is £50.") == "The limit is £50."
assert visible_text("Answer first. <thinking>still reasoning about") == "Answer first."
assert visible_text("<THINKING>a</THINKING>x<thinking>b</thinking>y") == "xy"
```

Why hide it: scratchpads can contain half-formed reasoning, restated system instructions, or sensitive intermediate data, and they confuse users. With native reasoning models, use the provider's separate reasoning channel instead of prompt tags. For audit, store the scratchpad separately under access control if policy requires, rather than showing it.

## Likely follow-ups

- How do you apply this filter to a token stream without flicker?

---

[← Q0170](../../batch_02_prompting_context_structured_output/0170_extract_the_final_answer_from_tagged_output/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0172 →](../../batch_02_prompting_context_structured_output/0172_structured_plans_with_dependency_validation/README.md)
