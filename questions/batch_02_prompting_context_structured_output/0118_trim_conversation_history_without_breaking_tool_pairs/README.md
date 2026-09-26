# Q0118 · Trim conversation history without breaking tool pairs

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Context engineering | Hard |

## Question

Trim chat history to a token budget: always keep system messages, keep the most recent turns, and never separate an assistant message that made tool calls from the tool-result messages that answer it (APIs reject orphaned tool results).

## Answer

Approach: group the messages into atomic units (an assistant tool-call message plus its following tool messages form one unit), then add units from newest to oldest while they fit.

```python
from typing import Callable


def group_units(messages: list[dict]) -> list[list[dict]]:
    units: list[list[dict]] = []
    for m in messages:
        if m["role"] == "tool" and units and (units[-1][0].get("tool_calls")):
            units[-1].append(m)
        else:
            units.append([m])
    return units


def trim_history(messages: list[dict], budget: int, count: Callable[[dict], int]) -> list[dict]:
    system = [m for m in messages if m["role"] == "system"]
    rest = [m for m in messages if m["role"] != "system"]
    used = sum(count(m) for m in system)
    if used > budget:
        raise ValueError("system prompt alone exceeds budget")
    kept: list[list[dict]] = []
    for unit in reversed(group_units(rest)):
        cost = sum(count(m) for m in unit)
        if used + cost > budget:
            break
        kept.append(unit)
        used += cost
    return system + [m for unit in reversed(kept) for m in unit]


def words(m: dict) -> int:
    return len(m.get("content", "").split()) + 1


msgs = [
    {"role": "system", "content": "be helpful"},
    {"role": "user", "content": "old question one two three"},
    {"role": "assistant", "content": "", "tool_calls": [{"id": "c1"}]},
    {"role": "tool", "tool_call_id": "c1", "content": "result a b"},
    {"role": "assistant", "content": "answer"},
    {"role": "user", "content": "new question"},
]
out = trim_history(msgs, budget=13, count=words)
assert [m["role"] for m in out] == ["system", "assistant", "tool", "assistant", "user"]
out = trim_history(msgs, budget=9, count=words)
assert [m["role"] for m in out] == ["system", "assistant", "user"]
```

With budget 9, the tool pair doesn't fit, so both of its messages are dropped together rather than leaving an orphaned tool result.

Improvements: summarise dropped turns instead of discarding them, pin important messages, and count tokens with the provider's tokenizer, including tool schemas.

## Likely follow-ups

- Why might you prefer to keep the first user message (the original task) even when trimming?

---

[← Q0117](../../batch_02_prompting_context_structured_output/0117_allocate_a_token_budget_across_context_sections/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0119 →](../../batch_02_prompting_context_structured_output/0119_rolling_summary_memory/README.md)
