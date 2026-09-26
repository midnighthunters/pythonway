# Q0989 · Bias and fairness testing in credit scoring and loan recommendation LLM assistants

| Section | Topic | Difficulty |
|---|---|---|
| AI Security, Guardrails & Responsible AI in a Bank | Model risk management | Medium |

## Question

Explain Disparate Impact and Equal Opportunity fairness metrics under the Equal Credit Opportunity Act (ECOA), and write Python code calculating the Disparate Impact Ratio.

## Answer

Under the US Equal Credit Opportunity Act (ECOA) and Consumer Financial Protection Bureau (CFPB) rules:
Creditors cannot discriminate based on race, sex, age, or marital status.
- **Disparate Impact (Four-Fifths / 80% Rule)**: The approval rate for a protected demographic group must be at least 80% of the approval rate for the highest group:
  $$\text{Disparate Impact Ratio} = \frac{P(\text{Approve} \mid \text{Protected Group})}{P(\text{Approve} \mid \text{Reference Group})} \ge 0.80$$

```python
from typing import List, Dict


def calculate_disparate_impact_ratio(
    protected_approvals: int, protected_total: int, reference_approvals: int, reference_total: int
) -> float:
    rate_protected = protected_approvals / protected_total if protected_total > 0 else 0.0
    rate_reference = reference_approvals / reference_total if reference_total > 0 else 0.0

    if rate_reference == 0:
        return 1.0

    di_ratio = rate_protected / rate_reference
    return round(di_ratio, 4)


# Reference group: 80 approved out of 100 (80% rate)
# Protected group A: 70 approved out of 100 (70% rate) -> 70 / 80 = 0.875 >= 0.80 (Compliant)
ratio_pass = calculate_disparate_impact_ratio(70, 100, 80, 100)
assert ratio_pass == 0.875
assert ratio_pass >= 0.80

# Protected group B: 50 approved out of 100 (50% rate) -> 50 / 80 = 0.625 < 0.80 (Violation)
ratio_fail = calculate_disparate_impact_ratio(50, 100, 80, 100)
assert ratio_fail == 0.625
assert ratio_fail < 0.80
```

## Likely follow-ups

- Why cannot proxy variables (like zip code or university name) be used in credit recommendation prompts?
- How does demographic parity differ from predictive equality in algorithmic fairness?

---

[← Q0988](../../batch_10_ai_security_responsible_ai/0988_evaluating_hallucination_and_factual_consistency_using_rag/README.md) · [AI Security, Guardrails & Responsible AI in a Bank index](../README.md) · [All sections](../../README.md) · [Q0990 →](../../batch_10_ai_security_responsible_ai/0990_toxicity_hate_speech_and_brand_reputation_filtering_using/README.md)
