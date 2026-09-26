# Q0956 · NER-based PII detection using Transformer models

| Section | Topic | Difficulty |
|---|---|---|
| AI Security, Guardrails & Responsible AI in a Bank | PII and DLP | Medium |

## Question

Explain Named Entity Recognition (NER) using spaCy or HuggingFace Transformers for PII detection, and write Python code evaluating entity span overlaps.

## Answer

Regex patterns fail to identify unstructured PII such as person names, company names, or addresses (e.g. "Meeting with Nikhil Goyal at 270 Park Avenue"). NER models analyze token embeddings and surrounding syntactic context to classify tokens into entity categories (`PER`, `ORG`, `LOC`).

```python
from typing import Dict, List, Tuple


class MockNERToken:
    def __init__(self, text: str, label: str, start: int, end: int):
        self.text = text
        self.label = label
        self.start = start
        self.end = end


def detect_pii_entities_spans(text: str) -> List[MockNERToken]:
    # Mocking NER prediction spans for person names
    entities = []
    if "Nikhil Goyal" in text:
        idx = text.index("Nikhil Goyal")
        entities.append(MockNERToken("Nikhil Goyal", "PERSON", idx, idx + 12))
    return entities


doc = "Senior Engineer Nikhil Goyal reviewed the risk model."
spans = detect_pii_entities_spans(doc)

assert len(spans) == 1
assert spans[0].text == "Nikhil Goyal"
assert spans[0].label == "PERSON"
assert doc[spans[0].start : spans[0].end] == "Nikhil Goyal"
```

## Likely follow-ups

- What are the trade-offs between speed and accuracy of small spaCy models (`en_core_web_sm`) vs RoBERTa-NER?
- How do you handle overlapping entity spans produced by multiple recognizers?

---

[← Q0955](../../batch_10_ai_security_responsible_ai/0955_handling_pii_in_unstructured_multi_turn_chat_dialogues/README.md) · [AI Security, Guardrails & Responsible AI in a Bank index](../README.md) · [All sections](../../README.md) · [Q0957 →](../../batch_10_ai_security_responsible_ai/0957_enterprise_data_loss_prevention_integration_in_api_gateways/README.md)
