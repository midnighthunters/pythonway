# Q0955 · Handling PII in unstructured multi-turn chat dialogues

| Section | Topic | Difficulty |
|---|---|---|
| AI Security, Guardrails & Responsible AI in a Bank | PII and DLP | Medium |

## Question

Explain the challenge of coreference resolution in multi-turn PII redaction (e.g. Turn 1: "John Smith", Turn 2: "his account"), and write Python code maintaining a session entity registry.

## Answer

In multi-turn chat, an attacker or user introduces PII in Turn 1 ("My name is Robert Vance"), but uses pronouns in Turn 2 ("What is my balance?"). If Turn 1's entity is pseudonymized to `CLIENT_1`, the session entity registry must map subsequent pronouns and references consistently across conversation turns.

```python
from typing import Dict, List


class MultiTurnEntityRegistry:
    def __init__(self):
        # Maps session_id -> {original_entity: pseudonym}
        self.sessions: Dict[str, Dict[str, str]] = {}

    def get_or_create_pseudonym(self, session_id: str, entity_name: str) -> str:
        if session_id not in self.sessions:
            self.sessions[session_id] = {}

        session_store = self.sessions[session_id]
        if entity_name not in session_store:
            idx = len(session_store) + 1
            session_store[entity_name] = f"PERSON_{idx}"

        return session_store[entity_name]


registry = MultiTurnEntityRegistry()
# Turn 1
p1 = registry.get_or_create_pseudonym("sess_101", "Robert Vance")
assert p1 == "PERSON_1"

# Turn 2: Same session resolves to same pseudonym
p2 = registry.get_or_create_pseudonym("sess_101", "Robert Vance")
assert p2 == "PERSON_1"

# Different session gets new pseudonym
p_other = registry.get_or_create_pseudonym("sess_999", "Robert Vance")
assert p_other == "PERSON_1"  # Scoped per session
```

## Likely follow-ups

- How does neural coreference resolution (e.g. AllenNLP, FastCoref) link pronouns to named entities?
- How long should session entity registries be persisted in Redis?

---

[← Q0954](../../batch_10_ai_security_responsible_ai/0954_irreversible_pii_masking_redaction_and_synthetic_data/README.md) · [AI Security, Guardrails & Responsible AI in a Bank index](../README.md) · [All sections](../../README.md) · [Q0956 →](../../batch_10_ai_security_responsible_ai/0956_ner_based_pii_detection_using_transformer_models/README.md)
