# Q0128 · Extract JSON from a chatty model response

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Output parsing | Medium |

## Question

Without structured outputs, models sometimes wrap JSON in prose or markdown fences. Write a robust extractor that prefers a fenced `json` block, otherwise finds the first balanced JSON object while respecting strings, and parses it.

## Answer

```python
import json
import re

FENCE = re.compile(r"```(?:json)?\s*\n(.*?)```", re.S | re.I)


def first_balanced_object(text: str) -> str | None:
    start = text.find("{")
    while start != -1:
        depth, in_str, esc = 0, False, False
        for i in range(start, len(text)):
            ch = text[i]
            if in_str:
                if esc:
                    esc = False
                elif ch == "\\":
                    esc = True
                elif ch == '"':
                    in_str = False
            elif ch == '"':
                in_str = True
            elif ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    return text[start:i + 1]
        start = text.find("{", start + 1)
    return None


def extract_json(text: str):
    m = FENCE.search(text)
    candidate = m.group(1) if m else first_balanced_object(text)
    if candidate is None:
        raise ValueError("no JSON object found")
    return json.loads(candidate)


assert extract_json('Sure!\n```json\n{"a": 1}\n```\nAnything else?') == {"a": 1}
assert extract_json('Result: {"msg": "use {braces} and \\"quotes\\"", "n": {"x": 2}} done') == {
    "msg": 'use {braces} and "quotes"', "n": {"x": 2}}
try:
    extract_json("no json here")
    raise AssertionError
except ValueError:
    pass
```

Treat this as a fallback. Structured outputs remove the need for it. Always validate the parsed object against the schema afterwards.

## Likely follow-ups

- Why can't a regex alone find balanced JSON?

---

[← Q0127](../../batch_02_prompting_context_structured_output/0127_validate_and_retry_with_error_feedback/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0129 →](../../batch_02_prompting_context_structured_output/0129_repair_common_json_errors_conservatively/README.md)
