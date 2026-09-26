# Q0927 · OWASP LLM02: Sensitive Information Disclosure and model weight inversion

| Section | Topic | Difficulty |
|---|---|---|
| AI Security, Guardrails & Responsible AI in a Bank | OWASP LLM Top 10 | Medium |

## Question

Explain OWASP LLM02: Sensitive Information Disclosure, and write Python code implementing output filtering that blocks accidental leakage of Internal System IP, API keys, and PII.

## Answer

OWASP LLM02 occurs when an LLM reveals confidential information, proprietary business algorithms, intellectual property, internal network hostnames, or Personally Identifiable Information (PII) to unauthorized users.

Defense requires post-generation output regex scrubbing and high-entropy secret scanners.

```python
import re
from typing import List, Tuple


class SensitiveDataScrubber:
    PATTERNS = [
        ("AWS_KEY", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
        ("INTERNAL_IP", re.compile(r"\b10\.\d{1,3}\.\d{1,3}\.\d{1,3}\b")),
        ("GENERIC_API_KEY", re.compile(r"\bsk-[a-zA-Z0-9]{20,}\b")),
    ]

    @classmethod
    def scrub(cls, text: str) -> Tuple[str, List[str]]:
        detections = []
        scrubbed = text
        for name, pattern in cls.PATTERNS:
            matches = pattern.findall(scrubbed)
            if matches:
                detections.append(name)
                scrubbed = pattern.sub(f"[REDACTED_{name}]", scrubbed)
        return scrubbed, detections


leaked_text = "Connect to 10.240.12.5 using key sk-abcdef1234567890abcdef"
clean, found = SensitiveDataScrubber.scrub(leaked_text)

assert "INTERNAL_IP" in found
assert "GENERIC_API_KEY" in found
assert "10.240.12.5" not in clean
assert "[REDACTED_INTERNAL_IP]" in clean
assert "[REDACTED_GENERIC_API_KEY]" in clean
```

## Likely follow-ups

- How does training data extraction (Carlini et al.) recover memorized PII from model weights?
- What role does Differential Privacy (DP-SGD) play in preventing sensitive memorization during pretraining?

---

[← Q0926](../../batch_10_ai_security_responsible_ai/0926_owasp_llm01_prompt_injection_comprehensive_taxonomy_and/README.md) · [AI Security, Guardrails & Responsible AI in a Bank index](../README.md) · [All sections](../../README.md) · [Q0928 →](../../batch_10_ai_security_responsible_ai/0928_owasp_llm03_supply_chain_vulnerabilities_in_model_hubs_and/README.md)
