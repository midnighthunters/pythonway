# Q0951 · Microsoft Presidio architecture: Analyzers, Recognizers, and Anonymizers

| Section | Topic | Difficulty |
|---|---|---|
| AI Security, Guardrails & Responsible AI in a Bank | PII and DLP | Medium |

## Question

Explain the modular architecture of Microsoft Presidio (Analyzer Engine, Pattern Recognizers, and Anonymizer Engine), and write Python code implementing an in-memory PII pipeline.

## Answer

Microsoft Presidio provides an enterprise-grade framework for detecting and anonymizing PII:
1. **Analyzer Engine**: Orchestrates multiple pattern recognizers, contextual word scoring, and NLP models (spaCy / Stanza) to identify entity types (NAME, EMAIL, SSN, PHONE) with confidence scores.
2. **Pattern Recognizers**: Specific rules, regular expressions, and checksum validators (e.g. Luhn algorithm for credit cards).
3. **Anonymizer Engine**: Transforms detected entities via redaction (`<REDACTED>`), masking (`***-**-1234`), synthetic replacement, or encryption.

```python
import re
from typing import Dict, List, Tuple


class SimplePIIEntity:
    def __init__(self, entity_type: str, start: int, end: int, score: float, text: str):
        self.entity_type = entity_type
        self.start = start
        self.end = end
        self.score = score
        self.text = text


class SimplePresidioAnalyzer:
    def __init__(self):
        self.recognizers = [
            ("EMAIL_ADDRESS", re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b")),
            ("US_SSN", re.compile(r"\b\d{3}-\d{2}-\d{4}\b")),
        ]

    def analyze(self, text: str) -> List[SimplePIIEntity]:
        results = []
        for entity_type, pattern in self.recognizers:
            for match in pattern.finditer(text):
                results.append(
                    SimplePIIEntity(
                        entity_type=entity_type,
                        start=match.start(),
                        end=match.end(),
                        score=0.95,
                        text=match.group(),
                    )
                )
        return results


class SimplePresidioAnonymizer:
    @staticmethod
    def anonymize(text: str, entities: List[SimplePIIEntity]) -> str:
        # Sort entities backwards to replace by index without offsetting
        sorted_entities = sorted(entities, key=lambda e: e.start, reverse=True)
        res = text
        for ent in sorted_entities:
            res = res[: ent.start] + f"<{ent.entity_type}>" + res[ent.end :]
        return res


analyzer = SimplePresidioAnalyzer()
anonymizer = SimplePresidioAnonymizer()

raw_text = "Client John Doe email is john.doe@jpmchase.com and SSN is 123-45-6789."
ents = analyzer.analyze(raw_text)
assert len(ents) == 2

anon_text = anonymizer.anonymize(raw_text, ents)
assert "john.doe@jpmchase.com" not in anon_text
assert "123-45-6789" not in anon_text
assert "<EMAIL_ADDRESS>" in anon_text
assert "<US_SSN>" in anon_text
```

## Likely follow-ups

- How does Presidio's context word enhancement increase confidence when words like "SSN" precede numbers?
- How do custom recognizers implement Luhn checksum validation for credit cards?

---

[← Q0950](../../batch_10_ai_security_responsible_ai/0950_auditing_agent_action_intents_before_tool_execution/README.md) · [AI Security, Guardrails & Responsible AI in a Bank index](../README.md) · [All sections](../../README.md) · [Q0952 →](../../batch_10_ai_security_responsible_ai/0952_custom_banking_pii_recognizers_iban_ssn_credit_card_cusip/README.md)
