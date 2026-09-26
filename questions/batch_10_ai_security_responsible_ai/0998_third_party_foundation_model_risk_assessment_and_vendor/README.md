# Q0998 · Third-party foundation model risk assessment and vendor dependency governance

| Section | Topic | Difficulty |
|---|---|---|
| AI Security, Guardrails & Responsible AI in a Bank | Model risk management | Easy |

## Question

What governance controls must a bank enforce when consuming third-party foundation models (OpenAI, Anthropic, AWS Bedrock), and write Python code evaluating vendor risk criteria.

## Answer

When consuming external SaaS or cloud foundation models, banks cannot inspect internal training weights or datasets directly. Therefore, vendor risk management enforces contractual and technical controls:
1. **Zero Data Retention (ZDR)**: Provider commits never to log customer prompts or use customer data for model retraining.
2. **Dedicated Cloud Tenants / Private Endpoints**: Routing traffic exclusively over AWS PrivateLink or Azure ExpressRoute.
3. **SOC 2 Type II and ISO 27001 Certification**: Verified independent security audits.
4. **Service Level Agreements (SLAs)**: Guarantees on availability, latency, and notification of model deprecation (minimum 6 months notice).

```python
from typing import Dict, List


def evaluate_vendor_ai_compliance(vendor_attestation: Dict[str, bool]) -> dict:
    mandatory_criteria = [
        "zero_data_retention_agreement_signed",
        "private_networking_supported",
        "soc2_type2_certified",
        "no_training_on_customer_data",
    ]
    missing = [c for c in mandatory_criteria if not vendor_attestation.get(c, False)]
    return {
        "approved": len(missing) == 0,
        "missing_mandatory_controls": missing,
    }


vendor_ok = {
    "zero_data_retention_agreement_signed": True,
    "private_networking_supported": True,
    "soc2_type2_certified": True,
    "no_training_on_customer_data": True,
}

assert evaluate_vendor_ai_compliance(vendor_ok)["approved"] is True

vendor_bad = {
    "zero_data_retention_agreement_signed": False,  # Missing ZDR!
    "private_networking_supported": True,
    "soc2_type2_certified": True,
    "no_training_on_customer_data": False,
}
res = evaluate_vendor_ai_compliance(vendor_bad)
assert res["approved"] is False
assert len(res["missing_mandatory_controls"]) == 2
```

## Likely follow-ups

- What is the operational risk when a cloud vendor deprecates a model version without notice?
- How do multi-provider architectures mitigate vendor lock-in?

---

[← Q0997](../../batch_10_ai_security_responsible_ai/0997_disaster_recovery_and_emergency_kill_switches_for/README.md) · [AI Security, Guardrails & Responsible AI in a Bank index](../README.md) · [All sections](../../README.md) · [Q0999 →](../../batch_10_ai_security_responsible_ai/0999_continuous_compliance_monitoring_and_automated_regulatory/README.md)
