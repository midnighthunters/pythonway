# Q0977 · UK PRA SS1/23 Model Risk Management principles for banks: Principle 3

| Section | Topic | Difficulty |
|---|---|---|
| AI Security, Guardrails & Responsible AI in a Bank | Model risk management | Hard |

## Question

Explain UK Prudential Regulation Authority (PRA) Supervisory Statement SS1/23 Principle 3 (Model Development), and write Python code implementing an automated Model Card metadata validator.

## Answer

PRA SS1/23 sets explicit standards for UK banks regarding Model Risk Management. Principle 3 mandates:
1. A clear model development lifecycle with documented business rationale and use case constraints.
2. Documented dataset provenance, quality, and representation bias.
3. Explicit identification of model limitations, failure modes, and operational boundary conditions.
4. Formal documentation via Model Cards and Technical Specifications.

```python
from typing import Dict, List


class SS123ModelCardValidator:
    REQUIRED_SECTIONS = [
        "model_id",
        "intended_use",
        "prohibited_use",
        "training_data_provenance",
        "known_limitations",
        "performance_metrics",
        "governance_signoff",
    ]

    @classmethod
    def validate_card(cls, card: Dict[str, str]) -> Dict[str, bool]:
        missing = [s for s in cls.REQUIRED_SECTIONS if s not in card or not card[s].strip()]
        return {
            "compliant": len(missing) == 0,
            "missing_sections": missing,
        }


card = {
    "model_id": "JPMC-LLM-CREDIT-V1",
    "intended_use": "Drafting commercial lending assessment memos for human underwriting review.",
    "prohibited_use": "Automated loan rejections without human credit officer approval.",
    "training_data_provenance": "SEC 10-K filings (2018-2025) and anonymized historical credit memos.",
    "known_limitations": "Underperforms on non-standard lease contracts and private equity debt structures.",
    "performance_metrics": "Hallucination rate < 0.8%, Factual recall 96.4%.",
    "governance_signoff": "Approved by Model Risk Office on 2026-03-15.",
}

res = SS123ModelCardValidator.validate_card(card)
assert res["compliant"] is True
assert len(res["missing_sections"]) == 0
```

## Likely follow-ups

- What are the capital adequacy penalties for banks failing to comply with PRA SS1/23?
- How does Principle 3 address third-party external foundation models (e.g. OpenAI, Anthropic)?

---

[← Q0976](../../batch_10_ai_security_responsible_ai/0976_federal_reserve_sr_11_7_and_occ_2011_12_model_risk/README.md) · [AI Security, Guardrails & Responsible AI in a Bank index](../README.md) · [All sections](../../README.md) · [Q0978 →](../../batch_10_ai_security_responsible_ai/0978_uk_pra_ss1_23_principle_4_independent_model_validation_and/README.md)
