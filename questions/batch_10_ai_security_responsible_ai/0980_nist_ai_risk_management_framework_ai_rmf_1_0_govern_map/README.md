# Q0980 · NIST AI Risk Management Framework (AI RMF 1.0): Govern, Map, Measure, Manage

| Section | Topic | Difficulty |
|---|---|---|
| AI Security, Guardrails & Responsible AI in a Bank | Model risk management | Easy |

## Question

Explain the four core functions of the NIST AI Risk Management Framework (AI RMF 1.0), and write Python code implementing a risk profile registry.

## Answer

The National Institute of Standards and Technology (NIST) AI RMF 1.0 organizes AI governance across four functions:
1. **GOVERN**: Cultivates a culture of risk management; defines policies, roles, and accountability.
2. **MAP**: Contextualizes AI risks within the specific business process, identifying stakeholders and impacts.
3. **MEASURE**: Employs quantitative and qualitative metrics to evaluate trustworthiness, bias, and accuracy.
4. **MANAGE**: Allocates resources to track and mitigate prioritized risks on an ongoing basis.

```python
from typing import Dict, List


class NISTRiskProfileRegistry:
    def __init__(self):
        self.risks: Dict[str, dict] = {}

    def register_risk(self, risk_id: str, function: str, description: str, mitigation: str) -> None:
        assert function in ("GOVERN", "MAP", "MEASURE", "MANAGE")
        self.risks[risk_id] = {
            "function": function,
            "description": description,
            "mitigation": mitigation,
            "status": "ACTIVE",
        }


registry = NISTRiskProfileRegistry()
registry.register_risk(
    risk_id="RISK-01",
    function="MEASURE",
    description="Hallucination in loan debt service coverage calculation.",
    mitigation="Automated numeric grounding verification and dual-LLM cross check.",
)

assert "RISK-01" in registry.risks
assert registry.risks["RISK-01"]["function"] == "MEASURE"
```

## Likely follow-ups

- How does NIST AI RMF compare with ISO/IEC 42001?
- How does the MAP function evaluate secondary and unintended societal impacts?

---

[← Q0979](../../batch_10_ai_security_responsible_ai/0979_eu_ai_act_high_risk_classification_and_compliance_for/README.md) · [AI Security, Guardrails & Responsible AI in a Bank index](../README.md) · [All sections](../../README.md) · [Q0981 →](../../batch_10_ai_security_responsible_ai/0981_iso_iec_42001_artificial_intelligence_management_system/README.md)
