# Q0688 · Semantic profile store for user preferences and entity memory

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | Personal AI assistants | Medium |

## Question

Write Python code for an entity-based semantic memory store that extracts and updates key facts about user preferences and counterparties.

## Answer

```python
from typing import Any, Dict, Optional


class SemanticProfileStore:
    def __init__(self):
        self._user_entities: Dict[str, Dict[str, Any]] = {}

    def upsert_entity(self, category: str, entity_id: str, attributes: Dict[str, Any]) -> None:
        key = f"{category}:{entity_id}"
        if key not in self._user_entities:
            self._user_entities[key] = {}
        self._user_entities[key].update(attributes)

    def get_entity(self, category: str, entity_id: str) -> Optional[Dict[str, Any]]:
        return self._user_entities.get(f"{category}:{entity_id}")


store = SemanticProfileStore()
store.upsert_entity("counterparty", "BARCLAYS", {"lei": "213800LBQA1Y9L22JB70", "rating": "A+"})
store.upsert_entity("counterparty", "BARCLAYS", {"credit_limit_usd": 50000000})

barclays = store.get_entity("counterparty", "BARCLAYS")
assert barclays["rating"] == "A+"
assert barclays["credit_limit_usd"] == 50000000
```

## Likely follow-ups

- How can conflicting facts in semantic memory be resolved over time?
- Should the user be allowed to view and manually edit their stored semantic profile?

---

[← Q0687](../../batch_07_mcp_a2a_skills_assistants/0687_layered_memory_in_personal_assistants_working_episodic/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0689 →](../../batch_07_mcp_a2a_skills_assistants/0689_intent_routing_between_local_tools_and_specialized_a2a/README.md)
