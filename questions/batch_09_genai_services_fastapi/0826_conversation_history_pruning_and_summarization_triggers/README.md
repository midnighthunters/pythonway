# Q0826 · Conversation history pruning and summarization triggers

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | NoSQL state stores | Medium |

## Question

Write Python code that monitors conversation token length in persistent storage, automatically triggering recursive conversation summarization when message history exceeds a token threshold.

## Answer

As user conversations expand, blindly loading full thread history into prompt context triggers LLM context window overflows and inflates inference latency. An automated compaction mechanism summarizes older turns while keeping recent turns intact.

```python
from typing import Dict, List


def estimate_tokens(text: str) -> int:
    return len(text) // 4  # Standard fast approximation


class ConversationBufferManager:
    def __init__(self, max_tokens: int = 50, keep_recent: int = 2):
        self.max_tokens = max_tokens
        self.keep_recent = keep_recent
        self.summary: str = ""
        self.messages: List[Dict[str, str]] = []

    def add_message(self, role: str, content: str) -> None:
        self.messages.append({"role": role, "content": content})
        self._compact_if_needed()

    def _compact_if_needed(self) -> None:
        total_tokens = sum(estimate_tokens(m["content"]) for m in self.messages)
        if total_tokens > self.max_tokens and len(self.messages) > self.keep_recent:
            # Messages to summarize
            to_summarize = self.messages[:-self.keep_recent]
            self.messages = self.messages[-self.keep_recent:]

            # Simulate LLM summarization
            summarized_snippets = [f"{m['role']}: {m['content']}" for m in to_summarize]
            new_summary = " | ".join(summarized_snippets)
            if self.summary:
                self.summary += " ; " + new_summary
            else:
                self.summary = new_summary

    def get_prompt_context(self) -> List[Dict[str, str]]:
        context = []
        if self.summary:
            context.append({"role": "system", "content": f"Prior Summary: {self.summary}"})
        context.extend(self.messages)
        return context


mgr = ConversationBufferManager(max_tokens=15, keep_recent=1)
mgr.add_message("user", "Calculate Greek Delta for Option Portfolio A.")
mgr.add_message("assistant", "Delta is 0.65.")
mgr.add_message("user", "Now calculate Gamma.")

ctx = mgr.get_prompt_context()
assert len(ctx) >= 2
assert ctx[0]["role"] == "system"
assert "Prior Summary" in ctx[0]["content"]
assert ctx[-1]["content"] == "Now calculate Gamma."
```

## Likely follow-ups

- How do you preserve system prompt instructions and safety guardrails during automated compaction?
- What are the risks of hallucination compounding when an LLM repeatedly summarizes previous summaries?

---

[← Q0825](../../batch_09_genai_services_fastapi/0825_implementing_an_async_key_value_checkpoint_saver_for_agent/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0827 →](../../batch_09_genai_services_fastapi/0827_multi_region_active_active_replication_for_conversation/README.md)
