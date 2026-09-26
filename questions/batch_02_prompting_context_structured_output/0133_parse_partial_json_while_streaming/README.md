# Q0133 · Parse partial JSON while streaming

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Streaming structured output | Hard |

## Question

To show structured results progressively, implement `parse_partial_json(prefix)`, which returns the best-effort object for an incomplete JSON stream. Close open strings and brackets, and if that fails, fall back to the last complete element.

## Answer

```python
import json


def _scan(s: str):
    stack, in_str, esc, commas = [], False, False, []
    for i, ch in enumerate(s):
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
            continue
        if ch == '"':
            in_str = True
        elif ch in "{[":
            stack.append("}" if ch == "{" else "]")
        elif ch in "}]" and stack:
            stack.pop()
        elif ch == ",":
            commas.append(i)
    return in_str, esc, stack, commas


def _close(s: str) -> str:
    in_str, esc, stack, _ = _scan(s)
    body = s[:-1] if esc else s
    return body + ('"' if in_str else "") + "".join(reversed(stack))


def parse_partial_json(prefix: str):
    candidates = [_close(prefix)] + [_close(prefix[:c]) for c in reversed(_scan(prefix)[3])]
    for cand in candidates:
        try:
            return json.loads(cand)
        except json.JSONDecodeError:
            continue
    return None


assert parse_partial_json('{"a": 1, "b": "hel') == {"a": 1, "b": "hel"}
assert parse_partial_json('{"a": 1, "b') == {"a": 1}
assert parse_partial_json('{"items": [1, 2, 3') == {"items": [1, 2, 3]}
assert parse_partial_json('{"a": 1, "b":') == {"a": 1}
assert parse_partial_json('{"a": "x, y') == {"a": "x, y"}
assert parse_partial_json('{"a": tr') is None
```

Uses: live-render extracted fields or an agent's plan as tokens arrive. Only act on fields once they are complete (for example after the closing quote, or when the next key starts). Never trigger side effects from partial output. Libraries such as `partial-json-parser`, and some SDK helpers, do this more thoroughly.

## Likely follow-ups

- How would you know that a particular field's value is final while still streaming?

---

[← Q0132](../../batch_02_prompting_context_structured_output/0132_money_and_dates_in_structured_output/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0134 →](../../batch_02_prompting_context_structured_output/0134_discriminated_unions_for_agent_actions/README.md)
