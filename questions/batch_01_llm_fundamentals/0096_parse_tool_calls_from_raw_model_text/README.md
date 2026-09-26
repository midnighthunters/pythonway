# Q0096 · Parse tool calls from raw model text

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Tool use | Medium |

## Question

A self-hosted model emits tool calls as `<tool_call>{json}</tool_call>` inside its text. Write a parser that extracts every call, validates the JSON and tool name against an allowlist, and collects errors rather than crashing.

## Answer

```python
import json
import re

TOOL_RE = re.compile(r"<tool_call>(.*?)</tool_call>", re.S)


def parse_tool_calls(text: str, allowed: set[str]) -> tuple[list[tuple[str, dict]], list[str]]:
    calls, errors = [], []
    for m in TOOL_RE.finditer(text):
        try:
            obj = json.loads(m.group(1).strip())
        except json.JSONDecodeError as e:
            errors.append(f"invalid JSON: {e.msg}")
            continue
        name, args = obj.get("name"), obj.get("arguments", {})
        if name not in allowed:
            errors.append(f"unknown tool: {name!r}")
        elif not isinstance(args, dict):
            errors.append(f"arguments for {name} must be an object")
        else:
            calls.append((name, args))
    return calls, errors


text = ('Let me check. <tool_call>{"name": "get_fx_rate", "arguments": {"pair": "GBPUSD", '
        '"opts": {"date": "2026-09-25"}}}</tool_call> and <tool_call>{"name": "rm_rf", "arguments": {}}'
        '</tool_call> <tool_call>{bad json}</tool_call>')
calls, errors = parse_tool_calls(text, {"get_fx_rate"})
assert calls == [("get_fx_rate", {"pair": "GBPUSD", "opts": {"date": "2026-09-25"}})]
assert errors[0] == "unknown tool: 'rm_rf'" and errors[1].startswith("invalid JSON")
```

Capturing everything between the tags and then parsing it handles nested braces. A regex like `\{.*?\}` would stop at the first closing brace. Next steps: validate the arguments against each tool's JSON Schema, and return errors to the model as tool results so it can self-correct.

## Likely follow-ups

- How would you handle a tool call split across streamed chunks?

---

[← Q0095](../../batch_01_llm_fundamentals/0095_how_tool_calling_works_under_the_hood/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0097 →](../../batch_01_llm_fundamentals/0097_multilingual_performance_considerations/README.md)
