# Q0119 · Rolling summary memory

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Context engineering | Medium |

## Question

Implement conversation memory that keeps the last K messages verbatim and folds older messages into a running summary produced by an LLM, updating it incrementally.

## Answer

```python
from typing import Callable


class RollingMemory:
    def __init__(self, summarize: Callable[[str, list[dict]], str], keep_last: int = 4) -> None:
        self.summarize = summarize
        self.keep_last = keep_last
        self.summary = ""
        self.recent: list[dict] = []

    def add(self, message: dict) -> None:
        self.recent.append(message)
        if len(self.recent) > self.keep_last:
            overflow = self.recent[:-self.keep_last]
            self.recent = self.recent[-self.keep_last:]
            self.summary = self.summarize(self.summary, overflow)

    def context(self) -> list[dict]:
        prefix = [{"role": "system", "content": f"Conversation summary so far: {self.summary}"}] if self.summary else []
        return prefix + self.recent


def fake_summarize(previous: str, messages: list[dict]) -> str:
    facts = [m["content"] for m in messages if m["role"] == "user"]
    return "; ".join(filter(None, [previous, *facts]))


mem = RollingMemory(fake_summarize, keep_last=2)
for i, (role, text) in enumerate([("user", "I'm in London"), ("assistant", "Noted"),
                                  ("user", "Book Tuesday"), ("assistant", "Which time?"),
                                  ("user", "9am")]):
    mem.add({"role": role, "content": text})
ctx = mem.context()
assert ctx[0]["content"] == "Conversation summary so far: I'm in London; Book Tuesday"
assert [m["content"] for m in ctx[1:]] == ["Which time?", "9am"]
```

Risks: summaries drop details (exact amounts, ids, dates) and can introduce errors that then persist. Mitigate by extracting key facts into structured memory as well, keeping the original transcript in storage for audit, and testing summaries for faithfulness. Summarise asynchronously so users don't wait.

## Likely follow-ups

- Which details must never be lost by summarisation in a banking assistant?

---

[← Q0118](../../batch_02_prompting_context_structured_output/0118_trim_conversation_history_without_breaking_tool_pairs/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0120 →](../../batch_02_prompting_context_structured_output/0120_compact_large_tool_outputs/README.md)
