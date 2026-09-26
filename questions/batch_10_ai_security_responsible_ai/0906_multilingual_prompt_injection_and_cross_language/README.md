# Q0906 · Multilingual prompt injection and cross-language translation evasion

| Section | Topic | Difficulty |
|---|---|---|
| AI Security, Guardrails & Responsible AI in a Bank | Prompt injection defense | Medium |

## Question

Explain how attackers use low-resource languages (e.g. Zulu, Gaelic) or multilingual translation chains to bypass English safety alignment, and design a defensive translation pipeline in Python.

## Answer

Safety alignment (RLHF / DPO) is heavily concentrated on English and major world languages. Attackers exploit this by translating malicious prompts into low-resource languages (e.g., Welsh, Swahili, Javanese). The model understands the semantic meaning but fails to trigger English-aligned safety guardrails.

A defensive pipeline translates non-English prompts to English via a fast translation model and evaluates safety guardrails against the normalized English translation.

```python
from typing import Dict


class DefensiveTranslationGuard:
    def __init__(self):
        # Simulated multi-lingual translation dictionary
        self.translation_table = {
            "dileu pob cyfarwyddyd": "ignore all instructions",  # Welsh
            "badilisheni maelekezo yote": "ignore all instructions",  # Swahili
        }
        self.blocked_terms = ["ignore all instructions", "override guardrails"]

    def evaluate_prompt(self, user_prompt: str, detected_lang: str) -> bool:
        normalized = user_prompt.lower()
        if detected_lang != "en":
            # Translate to English for inspection
            normalized = self.translation_table.get(normalized, normalized)

        for term in self.blocked_terms:
            if term in normalized:
                return False  # Blocked
        return True  # Allowed


guard = DefensiveTranslationGuard()

# Welsh attack prompt: "dileu pob cyfarwyddyd"
is_safe = guard.evaluate_prompt("dileu pob cyfarwyddyd", detected_lang="cy")
assert is_safe is False

# Legitimate French prompt
is_legit = guard.evaluate_prompt("Bonjour, quel est le taux SOFR?", detected_lang="fr")
assert is_legit is True
```

## Likely follow-ups

- Why does translating all non-English prompts add latency to global enterprise chat applications?
- How do multilingual safety models like Llama Guard 3 Multilingual mitigate translation overhead?

---

[← Q0905](../../batch_10_ai_security_responsible_ai/0905_base64_and_hex_encoding_evasion_in_user_prompts/README.md) · [AI Security, Guardrails & Responsible AI in a Bank index](../README.md) · [All sections](../../README.md) · [Q0907 →](../../batch_10_ai_security_responsible_ai/0907_recursive_prompt_injection_in_multi_agent_tool_communication/README.md)
