# Q0438 · Summarise tool outputs between steps

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Context engineering | Medium |

## Question

Implement context compaction for an agent: keep the latest N tool results verbatim, and replace older ones with short summaries, so the context stays bounded without losing key facts.

## Answer

```python
from typing import Callable


def compact_tool_history(messages: list[dict], keep_recent: int, summarize: Callable[[str], str]) -> list[dict]:
    tool_idx = [i for i, m in enumerate(messages) if m["role"] == "tool"]
    old = set(tool_idx[:-keep_recent]) if keep_recent else set(tool_idx)
    out = []
    for i, m in enumerate(messages):
        if i in old and not m.get("summarized"):
            out.append({**m, "content": summarize(m["content"]), "summarized": True})
        else:
            out.append(m)
    return out


msgs = [{"role": "user", "content": "Investigate break BRK-9"},
        {"role": "tool", "name": "get_trade", "content": "trade T1 qty 1000 px 101.2 ... (4,000 chars)"},
        {"role": "tool", "name": "get_confirm", "content": "confirm C7 qty 1000 px 101.25 ... (3,000 chars)"},
        {"role": "tool", "name": "get_fx", "content": "GBPUSD 1.2710"}]
summ = lambda s: s.split("...")[0].strip()
out = compact_tool_history(msgs, keep_recent=1, summarize=summ)
assert out[1]["content"] == "trade T1 qty 1000 px 101.2" and out[1]["summarized"]
assert out[3]["content"] == "GBPUSD 1.2710" and "summarized" not in out[3]
assert compact_tool_history(out, 1, lambda s: "!!")[1]["content"] == "trade T1 qty 1000 px 101.2"
```

Already-summarised messages aren't summarised again, so repeated compaction doesn't erode them. Keep the full outputs in external state (referenced by id), so the agent can re-fetch details if a summary turns out to be insufficient. Summaries must preserve identifiers and numbers exactly.

## Likely follow-ups

- How would you let the agent recover a detail lost in a summary?

---

[← Q0437](../../batch_05_agentic_patterns_orchestration/0437_scratchpads_and_working_notes/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0439 →](../../batch_05_agentic_patterns_orchestration/0439_sub_agents_to_isolate_context/README.md)
