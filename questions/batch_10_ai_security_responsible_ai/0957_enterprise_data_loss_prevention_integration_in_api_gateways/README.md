# Q0957 · Enterprise Data Loss Prevention integration in API Gateways

| Section | Topic | Difficulty |
|---|---|---|
| AI Security, Guardrails & Responsible AI in a Bank | PII and DLP | Hard |

## Question

Explain how enterprise Data Loss Prevention (DLP) engines (e.g. Symantec DLP, Nightfall, AWS Macie) integrate into GenAI API Gateways, and write Python code implementing an asynchronous DLP inspection gate.

## Answer

In financial enterprises, all outbound traffic exiting to cloud model endpoints passes through a DLP proxy. The proxy scans prompts for:
1. Customer financial records (account numbers, credit cards).
2. Intellectual property and source code.
3. Employee PII and executive personal data.

If a DLP rule is triggered, the gateway blocks the request and emits a security event to Splunk.

```python
from typing import Dict, List


class DLPInspectionResult:
    def __init__(self, is_blocked: bool, violations: List[str]):
        self.is_blocked = is_blocked
        self.violations = violations


class MockDLPGateway:
    def __init__(self):
        self.restricted_terms = ["CONFIDENTIAL_TRADE_SECRET", "INTERNAL_ONLY_PROPRIETARY", "MNPI_PROJECT_ZEUS"]

    def inspect_payload(self, text: str) -> DLPInspectionResult:
        violations = []
        for term in self.restricted_terms:
            if term in text:
                violations.append(f"DLP_POLICY_BREACH: {term}")

        is_blocked = len(violations) > 0
        return DLPInspectionResult(is_blocked, violations)


dlp = MockDLPGateway()

# Clean prompt
r_clean = dlp.inspect_payload("Calculate standard deviation of S&P 500 returns.")
assert r_clean.is_blocked is False
assert len(r_clean.violations) == 0

# Violating prompt
r_violating = dlp.inspect_payload("Summarize MNPI_PROJECT_ZEUS acquisition target valuation.")
assert r_violating.is_blocked is True
assert "MNPI_PROJECT_ZEUS" in r_violating.violations[0]
```

## Likely follow-ups

- What latency SLA is typical for enterprise DLP inspection (typically < 30ms)?
- How does DLP inspection handle streaming SSE token streams?

---

[← Q0956](../../batch_10_ai_security_responsible_ai/0956_ner_based_pii_detection_using_transformer_models/README.md) · [AI Security, Guardrails & Responsible AI in a Bank index](../README.md) · [All sections](../../README.md) · [Q0958 →](../../batch_10_ai_security_responsible_ai/0958_entitlement_aware_rag_document_metadata_acl_filtering_at/README.md)
