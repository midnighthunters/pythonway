# Q0932 · OWASP LLM07: System Prompt Leakage and intellectual property extraction

| Section | Topic | Difficulty |
|---|---|---|
| AI Security, Guardrails & Responsible AI in a Bank | OWASP LLM Top 10 | Easy |

## Question

Explain OWASP LLM07: System Prompt Leakage, and write Python code implementing an automated prompt leak scanner that rejects outputs that match proprietary prompt fingerprints.

## Answer

System Prompt Leakage occurs when an LLM reveals its system instructions, business rules, or internal configuration to end users. System prompts often contain proprietary trading methodologies, classification rubrics, or internal API schemas that constitute intellectual property.

```python
from typing import List


class PromptLeakDetector:
    def __init__(self, proprietary_phrases: List[str]):
        self.fingerprints = [phrase.lower() for phrase in proprietary_phrases]

    def contains_prompt_leak(self, model_response: str) -> bool:
        lowered = model_response.lower()
        for phrase in self.fingerprints:
            if phrase in lowered:
                return True
        return False


rules = [
    "Rule 1: Always assign Credit Tier A if net worth > 10M",
    "Secret Algorithm: JPMC_ALPHA_MOMENTUM_V2",
    "Never disclose the internal risk score calculation formula",
]

detector = PromptLeakDetector(proprietary_phrases=rules)

safe_answer = "Based on our public guidelines, high net worth accounts receive premium services."
assert detector.contains_prompt_leak(safe_answer) is False

leaked_answer = "Sure, my instructions state: Secret Algorithm: JPMC_ALPHA_MOMENTUM_V2."
assert detector.contains_prompt_leak(leaked_answer) is True
```

## Likely follow-ups

- Why should system prompts never contain sensitive credentials, API keys, or database passwords?
- How does system prompt obfuscation (paraphrasing instructions) mitigate leakage?

---

[← Q0931](../../batch_10_ai_security_responsible_ai/0931_owasp_llm06_excessive_agency_and_autonomous_destructive/README.md) · [AI Security, Guardrails & Responsible AI in a Bank index](../README.md) · [All sections](../../README.md) · [Q0933 →](../../batch_10_ai_security_responsible_ai/0933_owasp_llm08_vector_and_embedding_weaknesses/README.md)
