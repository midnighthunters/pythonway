# Q0129 · Repair common JSON errors conservatively

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Output parsing | Medium |

## Question

Write a conservative JSON repair that removes trailing commas (outside strings) and strips a BOM or code fences, then parses. Explain why you would not "fix" single quotes or unquoted keys automatically.

## Answer

```python
import json


def remove_trailing_commas(s: str) -> str:
    out, in_str, esc = [], False, False
    i = 0
    while i < len(s):
        ch = s[i]
        if in_str:
            out.append(ch)
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
        elif ch == '"':
            in_str = True
            out.append(ch)
        elif ch == ",":
            j = i + 1
            while j < len(s) and s[j] in " \t\r\n":
                j += 1
            if j < len(s) and s[j] in "}]":
                i += 1
                continue
            out.append(ch)
        else:
            out.append(ch)
        i += 1
    return "".join(out)


def repair_json(raw: str):
    s = raw.lstrip("\ufeff").strip()
    if s.startswith("```"):
        s = s.split("\n", 1)[1] if "\n" in s else ""
        s = s.rsplit("```", 1)[0]
    return json.loads(remove_trailing_commas(s))


assert repair_json('{"a": [1, 2,], "b": {"c": 3,},}') == {"a": [1, 2], "b": {"c": 3}}
assert repair_json('```json\n{"note": "a, }"}\n```') == {"note": "a, }"}
assert repair_json('\ufeff{"x": 1}') == {"x": 1}
```

Why stay conservative: single-quote or unquoted-key "fixes" can change meaning when strings contain apostrophes or colons, and silently guessing corrupts data. Anything beyond unambiguous fixes should fail and trigger a retry. Log every repair, because rising repair rates signal a prompt or model regression.

## Likely follow-ups

- Why is `ast.literal_eval` a tempting but risky way to parse Python-looking output?

---

[← Q0128](../../batch_02_prompting_context_structured_output/0128_extract_json_from_a_chatty_model_response/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0130 →](../../batch_02_prompting_context_structured_output/0130_constrain_classification_labels_with_literal/README.md)
