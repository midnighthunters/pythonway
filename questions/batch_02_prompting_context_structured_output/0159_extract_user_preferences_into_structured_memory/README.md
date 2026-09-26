# Q0159 · Extract user preferences into structured memory

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Memory | Medium |

## Question

Implement memory updates where the LLM proposes preference updates as JSON. Accept only known keys, and only when the supporting quote actually appears in the user's own message, so the model can't invent memories.

## Answer

```python
from typing import Literal

from pydantic import BaseModel, Field


class Preference(BaseModel):
    key: Literal["home_office", "seat", "language", "dietary"]
    value: str = Field(min_length=1, max_length=60)
    source_quote: str = Field(min_length=3)


class PreferenceUpdate(BaseModel):
    preferences: list[Preference] = Field(default_factory=list, max_length=5)


def apply_memory_update(memory: dict[str, str], proposal_json: str, user_message: str) -> list[str]:
    accepted = []
    for p in PreferenceUpdate.model_validate_json(proposal_json).preferences:
        if p.source_quote.lower() in user_message.lower():
            memory[p.key] = p.value
            accepted.append(p.key)
    return accepted


memory: dict[str, str] = {}
msg = "I usually work from the Canary Wharf office and I prefer aisle seats."
proposal = ('{"preferences": ['
            '{"key": "home_office", "value": "Canary Wharf", "source_quote": "work from the Canary Wharf office"},'
            '{"key": "seat", "value": "aisle", "source_quote": "prefer aisle seats"},'
            '{"key": "dietary", "value": "vegan", "source_quote": "I am vegan"}]}')
assert apply_memory_update(memory, proposal, msg) == ["home_office", "seat"]
assert memory == {"home_office": "Canary Wharf", "seat": "aisle"}
```

Only extract from the user's own messages, never from documents or tool results, which is what stops memory poisoning. Show the user what was saved.

## Likely follow-ups

- How would you handle conflicting updates ("aisle" last month, "window" today)?

---

[← Q0158](../../batch_02_prompting_context_structured_output/0158_what_to_store_in_long_term_memory/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0160 →](../../batch_02_prompting_context_structured_output/0160_deduplicate_memory_facts/README.md)
