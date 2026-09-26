# Q0687 · Layered memory in personal assistants: working, episodic, semantic

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | Personal AI assistants | Hard |

## Question

Explain the tripartite memory model (Working, Episodic, Semantic) for Personal AI Assistants and write Python code implementing memory retrieval across these layers.

## Answer

A personal assistant requires three distinct memory systems:
1. Working Memory: The immediate context window containing current turn messages and active scratchpad tools. Ephemeral and bounded.
2. Episodic Memory: Searchable historical logs of past conversations and tasks (e.g. "What did we decide about the EUR hedge last Thursday?"). Stored in vector or document databases.
3. Semantic Memory: Long-term structured facts and user preferences (e.g. "User prefers financial values in millions, base currency GBP, timezone London"). Stored in key-value or graph databases.

```python
from typing import Any, Dict, List, Optional


class TripartiteMemoryManager:
    def __init__(self):
        self.working_memory: List[str] = []
        self.episodic_archive: List[Dict[str, str]] = []
        self.semantic_profile: Dict[str, Any] = {}

    def set_user_preference(self, key: str, value: Any) -> None:
        self.semantic_profile[key] = value

    def add_working_turn(self, user_msg: str, assistant_msg: str) -> None:
        self.working_memory.append(f"User: {user_msg}")
        self.working_memory.append(f"Assistant: {assistant_msg}")

    def archive_session(self, session_date: str) -> None:
        self.episodic_archive.append({
            "date": session_date,
            "transcript": "\n".join(self.working_memory),
        })
        self.working_memory.clear()

    def assemble_prompt_context(self) -> str:
        pref_str = ", ".join(f"{k}={v}" for k, v in self.semantic_profile.items())
        return "User Profile: [" + pref_str + "]\nRecent History:\n" + "\n".join(self.working_memory)


mem = TripartiteMemoryManager()
mem.set_user_preference("currency", "GBP")
mem.set_user_preference("desk", "FX Derivatives")
mem.add_working_turn("Check USD spread", "Spread is 0.5 bps.")

prompt_ctx = mem.assemble_prompt_context()
assert "currency=GBP" in prompt_ctx
assert "Spread is 0.5 bps" in prompt_ctx

mem.archive_session("2026-09-26")
assert len(mem.working_memory) == 0
assert len(mem.episodic_archive) == 1
```

## Likely follow-ups

- How does GDPR "Right to be Forgotten" impact episodic and semantic memory?
- How do you update semantic memory automatically from conversational cues without hallucination?

---

[← Q0686](../../batch_07_mcp_a2a_skills_assistants/0686_architecture_of_an_enterprise_personal_ai_assistant/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0688 →](../../batch_07_mcp_a2a_skills_assistants/0688_semantic_profile_store_for_user_preferences_and_entity/README.md)
