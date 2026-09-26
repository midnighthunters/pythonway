# Q0918 · Tree of Attacks with Pruning and automated red teaming defense

| Section | Topic | Difficulty |
|---|---|---|
| AI Security, Guardrails & Responsible AI in a Bank | Prompt injection defense | Hard |

## Question

Explain the Tree of Attacks with Pruning (TAP) jailbreak methodology, and write Python code simulating a stateful evaluator pruning jailbreak candidate branches.

## Answer

Tree of Attacks with Pruning (TAP) is an automated red-teaming technique where an attacker LLM recursively generates adversarial prompt variations in a tree structure, pruning branches that trigger basic filters and expanding branches that move closer to bypassing guardrails.

Defenses require stateful monitoring that detects rapid iterative prompt rephrasing across a session.

```python
from typing import List, Dict


class SessionAttackDetector:
    def __init__(self, similarity_threshold: float = 0.8, max_attempts: int = 3):
        self.user_history: Dict[str, List[str]] = {}
        self.max_attempts = max_attempts

    def record_and_evaluate(self, user_id: str, prompt: str, is_filtered: bool) -> bool:
        """Returns True if user exhibits automated iterative attack behavior."""
        if user_id not in self.user_history:
            self.user_history[user_id] = []

        if is_filtered:
            self.user_history[user_id].append(prompt)

        # Flag if user triggers filter repeatedly in short succession
        if len(self.user_history[user_id]) >= self.max_attempts:
            return True  # Rate-limit / ban user
        return False


detector = SessionAttackDetector(max_attempts=3)
u_id = "user_attacker_10"

# Attacker tries 3 iterative variants of jailbreak
assert detector.record_and_evaluate(u_id, "Attempt 1: Ignore rules", is_filtered=True) is False
assert detector.record_and_evaluate(u_id, "Attempt 2: Act as DAN", is_filtered=True) is False
# 3rd attempt triggers lock out
assert detector.record_and_evaluate(u_id, "Attempt 3: Dev mode bypass", is_filtered=True) is True
```

## Likely follow-ups

- How do automated red-teaming frameworks like PyRIT and Promptfoo automate TAP?
- How does IP-reputation and session finger-printing mitigate distributed TAP attacks?

---

[← Q0917](../../batch_10_ai_security_responsible_ai/0917_context_window_stuffing_and_denial_of_service_via_prompt/README.md) · [AI Security, Guardrails & Responsible AI in a Bank index](../README.md) · [All sections](../../README.md) · [Q0919 →](../../batch_10_ai_security_responsible_ai/0919_virtual_persona_and_roleplay_jailbreak_defenses/README.md)
