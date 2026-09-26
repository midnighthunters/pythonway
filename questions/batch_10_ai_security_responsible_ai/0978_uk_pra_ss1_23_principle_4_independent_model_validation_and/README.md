# Q0978 · UK PRA SS1/23 Principle 4: Independent Model Validation and Challenger Models

| Section | Topic | Difficulty |
|---|---|---|
| AI Security, Guardrails & Responsible AI in a Bank | Model risk management | Hard |

## Question

Explain PRA SS1/23 Principle 4 (Independent Model Validation), and write Python code comparing the outputs of a primary champion model against an independent challenger model.

## Answer

Principle 4 mandates that model validation must be conducted by an independent team with technical competence and no financial stake in the model's commercial deployment.

A core methodology is **Challenger Model Testing**: The primary model (e.g. GPT-4o) and an independent challenger model (e.g. Claude 3.5 Sonnet or an internal open-weight Llama-3-70B) are evaluated on identical test datasets. Divergences in predictions flag model instability or blind spots.

```python
from typing import List, Dict


def evaluate_champion_challenger(
    test_cases: List[str], champion_outputs: List[str], challenger_outputs: List[str]
) -> dict:
    total = len(test_cases)
    exact_matches = 0
    divergent_cases = []

    for i in range(total):
        if champion_outputs[i] == challenger_outputs[i]:
            exact_matches += 1
        else:
            divergent_cases.append({
                "case": test_cases[i],
                "champion": champion_outputs[i],
                "challenger": challenger_outputs[i],
            })

    agreement_rate = exact_matches / total if total > 0 else 0.0
    return {
        "total_evaluated": total,
        "agreement_rate": round(agreement_rate, 4),
        "divergent_cases": divergent_cases,
    }


cases = ["Classify risk: Client liquidity ratio = 0.8", "Classify risk: Client debt-to-equity = 1.2"]
champ = ["HIGH_RISK", "MODERATE_RISK"]
chall = ["HIGH_RISK", "LOW_RISK"]  # Divergence on case 2

report = evaluate_champion_challenger(cases, champ, chall)
assert report["total_evaluated"] == 2
assert report["agreement_rate"] == 0.50
assert len(report["divergent_cases"]) == 1
assert report["divergent_cases"][0]["champion"] == "MODERATE_RISK"
```

## Likely follow-ups

- Why must challenger models have different training lineage or architecture than champion models?
- How does the Model Risk Office resolve persistent disagreements between champion and challenger models?

---

[← Q0977](../../batch_10_ai_security_responsible_ai/0977_uk_pra_ss1_23_model_risk_management_principles_for_banks/README.md) · [AI Security, Guardrails & Responsible AI in a Bank index](../README.md) · [All sections](../../README.md) · [Q0979 →](../../batch_10_ai_security_responsible_ai/0979_eu_ai_act_high_risk_classification_and_compliance_for/README.md)
