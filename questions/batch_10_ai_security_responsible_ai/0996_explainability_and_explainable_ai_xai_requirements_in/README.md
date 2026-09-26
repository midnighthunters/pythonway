# Q0996 · Explainability and Explainable AI (XAI) requirements in automated lending

| Section | Topic | Difficulty |
|---|---|---|
| AI Security, Guardrails & Responsible AI in a Bank | Model risk management | Hard |

## Question

Explain explainability requirements under CFPB Circular 2022-03 for automated lending decisions, and write Python code generating principal adverse action reason codes.

## Answer

Under the Equal Credit Opportunity Act (ECOA) and Consumer Financial Protection Bureau (CFPB) guidance:
When a bank denies credit or takes adverse action, it must provide the consumer with specific, principal reasons for the denial (Adverse Action Notice). Using "the black-box LLM decided so" is legally invalid.

Even if an LLM is used to synthesize applicant data, the underlying decision must be tied to deterministic feature attribution (e.g. SHAP / feature importances) that maps to approved regulatory reason codes.

```python
from typing import Dict, List


class AdverseActionExplainer:
    REASON_CODES = {
        "dti_ratio": "Debt-to-income ratio exceeds allowable underwriting threshold.",
        "delinquency": "Number of delinquent past-due accounts on credit report.",
        "credit_utilization": "Revolving credit line utilization exceeds 80%.",
        "insufficient_history": "Insufficient length of established credit history.",
    }

    @classmethod
    def generate_adverse_action_reasons(
        cls, applicant_metrics: Dict[str, float], top_n: int = 2
    ) -> List[str]:
        # Identify top risk factors based on adverse thresholds
        risk_scores = []
        if applicant_metrics.get("dti", 0.0) > 0.43:
            risk_scores.append(("dti_ratio", applicant_metrics["dti"]))
        if applicant_metrics.get("utilization", 0.0) > 0.80:
            risk_scores.append(("credit_utilization", applicant_metrics["utilization"]))
        if applicant_metrics.get("delinquencies", 0) > 0:
            risk_scores.append(("delinquency", applicant_metrics["delinquencies"]))

        # Sort by severity and pick top_n
        risk_scores.sort(key=lambda x: x[1], reverse=True)
        return [cls.REASON_CODES[k] for k, _ in risk_scores[:top_n]]


applicant = {"dti": 0.52, "utilization": 0.88, "delinquencies": 2}
reasons = AdverseActionExplainer.generate_adverse_action_reasons(applicant, top_n=2)

assert len(reasons) == 2
assert "Debt-to-income ratio" in reasons[0] or "credit report" in reasons[0]
```

## Likely follow-ups

- How do SHAP (SHapley Additive exPlanations) values provide local feature attribution for credit models?
- What are the regulatory consequences of providing vague or non-specific reasons on an adverse action notice?

---

[← Q0995](../../batch_10_ai_security_responsible_ai/0995_incident_response_playbook_for_genai_security_breach/README.md) · [AI Security, Guardrails & Responsible AI in a Bank index](../README.md) · [All sections](../../README.md) · [Q0997 →](../../batch_10_ai_security_responsible_ai/0997_disaster_recovery_and_emergency_kill_switches_for/README.md)
