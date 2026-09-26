# Q0920 · Multi-turn conversational drift and gradual jailbreak escalation

| Section | Topic | Difficulty |
|---|---|---|
| AI Security, Guardrails & Responsible AI in a Bank | Prompt injection defense | Hard |

## Question

Explain multi-turn conversational drift (crescendo attacks) where an attacker gradually steers an LLM across 10 turns, and write Python code tracking conversational trajectory drift.

## Answer

In a **Crescendo Attack**, the attacker does not launch an overt jailbreak on Turn 1. Instead, they begin with benign historical or theoretical questions (Turn 1: "What are cyber attacks?"), gradually narrowing the context (Turn 5: "How does SQL injection work in theory?"), until Turn 10 asks for weaponized exploits against bank systems.

Mitigation requires evaluating the **cumulative conversational trajectory** rather than single isolated turns.

```python
from typing import List


class ConversationalDriftMonitor:
    def __init__(self, drift_threshold: int = 3):
        self.risk_counter = 0
        self.drift_threshold = drift_threshold
        self.risk_keywords = ["exploit", "vulnerability", "bypass", "payload", "attack", "exfiltrate"]

    def process_turn(self, user_msg: str) -> bool:
        """Returns True if conversational trajectory exceeds cumulative risk threshold."""
        lowered = user_msg.lower()
        turn_risk = sum(1 for kw in self.risk_keywords if kw in lowered)
        self.risk_counter += turn_risk

        if self.risk_counter >= self.drift_threshold:
            return True  # Escalation detected
        return False


monitor = ConversationalDriftMonitor(drift_threshold=5)

# Turn 1: Benign
assert monitor.process_turn("Tell me about software engineering.") is False
# Turn 2: Borderline
assert monitor.process_turn("What is a software vulnerability?") is False  # counter = 1
# Turn 3: Escalating
assert monitor.process_turn("How do attackers bypass authentication with an exploit?") is False  # counter = 1 + 3 = 4

# Turn 4: Breaches cumulative threshold
assert monitor.process_turn("Give me an exploit payload") is True
```

## Likely follow-ups

- Why does stateless API design make detecting multi-turn crescendo attacks difficult?
- How does session-level summarization expose conversational drift to moderation models?

---

[← Q0919](../../batch_10_ai_security_responsible_ai/0919_virtual_persona_and_roleplay_jailbreak_defenses/README.md) · [AI Security, Guardrails & Responsible AI in a Bank index](../README.md) · [All sections](../../README.md) · [Q0921 →](../../batch_10_ai_security_responsible_ai/0921_multimodal_prompt_injection_in_images_and_visual_typography/README.md)
