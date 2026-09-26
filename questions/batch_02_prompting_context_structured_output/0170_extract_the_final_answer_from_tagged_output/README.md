# Q0170 · Extract the final answer from tagged output

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Output parsing | Easy |

## Question

The prompt asks the model to put its final answer in `<answer>...</answer>`. Write an extractor that uses the last complete answer block, and raises if there is none.

## Answer

```python
import re

ANSWER = re.compile(r"<answer>(.*?)</answer>", re.S | re.I)


def extract_answer(text: str) -> str:
    matches = ANSWER.findall(text)
    if not matches:
        raise ValueError("no <answer> block found")
    return matches[-1].strip()


out = "Let me work it out... <answer>draft</answer> Actually, correcting: <answer>\n42 days\n</answer>"
assert extract_answer(out) == "42 days"
try:
    extract_answer("<answer>unterminated")
    raise AssertionError
except ValueError:
    pass
```

Using the last block handles models that self-correct. Tags are easier for models to follow than "the final line", and easier for you to parse. With structured outputs you'd use a JSON field instead.

## Likely follow-ups

- What should happen if the model outputs two different answers in two blocks?

---

[← Q0169](../../batch_02_prompting_context_structured_output/0169_combined_citation_and_abstention_template/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0171 →](../../batch_02_prompting_context_structured_output/0171_strip_scratchpad_content_before_display/README.md)
