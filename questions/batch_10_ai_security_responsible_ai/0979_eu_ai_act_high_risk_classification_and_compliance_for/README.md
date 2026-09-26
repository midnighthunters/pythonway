# Q0979 · EU AI Act high-risk classification and compliance for financial services

| Section | Topic | Difficulty |
|---|---|---|
| AI Security, Guardrails & Responsible AI in a Bank | Model risk management | Medium |

## Question

Explain how the European Union AI Act classifies AI systems in banking (Credit Scoring, Risk Evaluation) as High-Risk, and outline mandatory compliance requirements.

## Answer

Under Annex III of the EU Artificial Intelligence Act:
- **High-Risk AI Systems**: AI systems used to evaluate the creditworthiness of natural persons or establish their credit score, and AI used for risk assessment and pricing in life/health insurance.
- **Mandatory Requirements (Articles 9-15)**:
  1. **Risk Management System (Art. 9)**: Continuous identification and mitigation of known and foreseeable risks.
  2. **Data Governance (Art. 10)**: Training/validation datasets must be relevant, representative, and free of discriminatory bias.
  3. **Technical Documentation & Logging (Art. 11-12)**: Automatic logging of events to ensure traceability and auditability.
  4. **Human Oversight (Art. 14)**: Built-in human-machine interfaces enabling human operators to override or stop the system (Kill Switch).
  5. **Accuracy, Robustness & Cybersecurity (Art. 15)**: Resilient against adversarial attacks and prompt injection.

```python
# no-run
# EU AI Act High-Risk Classification Decision Tree
def classify_eu_ai_act_risk(use_case: str) -> str:
    if use_case in ["credit_scoring_retail", "loan_origination_evaluation", "employment_candidate_screening"]:
        return "HIGH_RISK"  # Mandatory CE mark, Conformity Assessment, Annex III
    elif use_case in ["customer_facing_chatbot", "content_generation"]:
        return "TRANSPARENCY_RISK"  # Must disclose user is interacting with AI (Art. 52)
    elif use_case in ["social_scoring", "subliminal_manipulation", "real_time_biometric_surveillance"]:
        return "PROHIBITED"  # Strictly banned under Article 5
    return "MINIMAL_RISK"
```

## Likely follow-ups

- What are the maximum financial penalties under the EU AI Act (up to €35M or 7% of global annual turnover)?
- How do General Purpose AI (GPAI) model rules (e.g. systemic risk obligations) apply to foundation model providers?

---

[← Q0978](../../batch_10_ai_security_responsible_ai/0978_uk_pra_ss1_23_principle_4_independent_model_validation_and/README.md) · [AI Security, Guardrails & Responsible AI in a Bank index](../README.md) · [All sections](../../README.md) · [Q0980 →](../../batch_10_ai_security_responsible_ai/0980_nist_ai_risk_management_framework_ai_rmf_1_0_govern_map/README.md)
