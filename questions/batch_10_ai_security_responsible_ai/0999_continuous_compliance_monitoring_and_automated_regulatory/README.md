# Q0999 · Continuous compliance monitoring and automated regulatory reporting

| Section | Topic | Difficulty |
|---|---|---|
| AI Security, Guardrails & Responsible AI in a Bank | Model risk management | Medium |

## Question

Write Python code implementing an automated compliance dashboard metric aggregator that summarizes daily prompt injection attempts, PII redaction volumes, and hallucination rates for executive risk committees.

## Answer

Executive risk committees and regulatory examiners require periodic reports on AI risk telemetry. The aggregator compiles events from API gateways, guardrails, and audit logs into structured compliance metrics.

```python
from typing import Dict, List


class ComplianceMetricsAggregator:
    def __init__(self):
        self.total_requests = 0
        self.injection_blocks = 0
        self.pii_redactions = 0
        self.hallucination_flags = 0

    def record_transaction(self, blocked_injection: bool, redacted_pii: bool, hallucination: bool):
        self.total_requests += 1
        if blocked_injection:
            self.injection_blocks += 1
        if redacted_pii:
            self.pii_redactions += 1
        if hallucination:
            self.hallucination_flags += 1

    def generate_executive_report(self) -> dict:
        total = max(1, self.total_requests)
        return {
            "total_volume": self.total_requests,
            "injection_attempt_pct": round((self.injection_blocks / total) * 100, 2),
            "pii_redaction_pct": round((self.pii_redactions / total) * 100, 2),
            "hallucination_rate_pct": round((self.hallucination_flags / total) * 100, 2),
            "risk_status": "NORMAL" if (self.injection_blocks / total) < 0.05 else "ELEVATED",
        }


aggregator = ComplianceMetricsAggregator()
aggregator.record_transaction(blocked_injection=False, redacted_pii=True, hallucination=False)
aggregator.record_transaction(blocked_injection=True, redacted_pii=False, hallucination=False)
aggregator.record_transaction(blocked_injection=False, redacted_pii=False, hallucination=False)

report = aggregator.generate_executive_report()
assert report["total_volume"] == 3
assert report["pii_redaction_pct"] == 33.33
assert report["injection_attempt_pct"] == 33.33
assert report["risk_status"] == "ELEVATED"
```

## Likely follow-ups

- How do these aggregated metrics feed into Governance, Risk, and Compliance (GRC) tools like Archer?
- What are the mandatory quarterly reporting metrics under PRA SS1/23?

---

[← Q0998](../../batch_10_ai_security_responsible_ai/0998_third_party_foundation_model_risk_assessment_and_vendor/README.md) · [AI Security, Guardrails & Responsible AI in a Bank index](../README.md) · [All sections](../../README.md) · [Q1000 →](../../batch_10_ai_security_responsible_ai/1000_complete_enterprise_ai_security_and_responsible_governance/README.md)
