# Q0982 · Technology Controls Agenda and internal audit controls in JPMorganChase

| Section | Topic | Difficulty |
|---|---|---|
| AI Security, Guardrails & Responsible AI in a Bank | Model risk management | Medium |

## Question

Explain JPMorganChase's Technology Controls Agenda (TCA) and write Python code implementing an automated controls compliance verification check for GenAI microservices.

## Answer

JPMorganChase's Technology Controls Agenda (TCA) governs all software systems operating within the firm. For GenAI and LLM Suite services, TCA mandates:
1. **Access Control**: Zero Trust architecture, Least Privilege, Entra ID / CyberArk credential management.
2. **Data Protection**: Encryption in transit (TLS 1.3), encryption at rest (KMS envelope encryption), and automated PII masking.
3. **Change Management**: Zero unreviewed code deployments; all prompt changes tracked in Git.
4. **Vulnerability Management**: Zero critical/high CVEs in container base images.
5. **Audit Logging**: Immutable, tamper-evident logs for all transactions.

```python
from typing import Any, Dict, List


class TCAComplianceChecker:
    @staticmethod
    def audit_service_configuration(config: Dict[str, bool]) -> Dict[str, Any]:
        required_controls = [
            "tls_1_3_enforced",
            "pii_redaction_enabled",
            "gitops_prompt_versioning",
            "zero_critical_cves",
            "worm_audit_logging",
        ]
        failures = [ctrl for ctrl in required_controls if not config.get(ctrl, False)]
        return {
            "compliant": len(failures) == 0,
            "failed_controls": failures,
        }


prod_config = {
    "tls_1_3_enforced": True,
    "pii_redaction_enabled": True,
    "gitops_prompt_versioning": True,
    "zero_critical_cves": True,
    "worm_audit_logging": True,
}

audit = TCAComplianceChecker.audit_service_configuration(prod_config)
assert audit["compliant"] is True
assert len(audit["failed_controls"]) == 0
```

## Likely follow-ups

- How does Corporate Cyber Security (CCS) enforce TCA compliance across global software engineering teams?
- What are the consequences of an audit "Management Issue" (MI) raised by Internal Audit against an AI application?

---

[← Q0981](../../batch_10_ai_security_responsible_ai/0981_iso_iec_42001_artificial_intelligence_management_system/README.md) · [AI Security, Guardrails & Responsible AI in a Bank index](../README.md) · [All sections](../../README.md) · [Q0983 →](../../batch_10_ai_security_responsible_ai/0983_model_inventory_management_tiered_risk_rating_and_model/README.md)
