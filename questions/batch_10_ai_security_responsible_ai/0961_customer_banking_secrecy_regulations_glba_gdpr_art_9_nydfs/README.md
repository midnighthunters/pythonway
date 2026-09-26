# Q0961 · Customer banking secrecy regulations (GLBA, GDPR Art. 9, NYDFS 23 NYCRR 500)

| Section | Topic | Difficulty |
|---|---|---|
| AI Security, Guardrails & Responsible AI in a Bank | PII and DLP | Medium |

## Question

Explain customer banking secrecy laws (GLBA Safeguards Rule, GDPR Article 9, NYDFS 23 NYCRR 500) and how they govern GenAI architectures in financial services.

## Answer

1. **Gramm-Leach-Bliley Act (GLBA) Safeguards Rule**:
   - Mandates that financial institutions protect Nonpublic Personal Information (NPI) of consumers.
   - Requires encryption of all customer data in transit and at rest.
   - Imposes vendor risk management on cloud AI providers.
2. **GDPR Article 9 (Special Categories of Personal Data)**:
   - Prohibits processing biometric data, political opinions, or health data without explicit consent.
   - Grants EU citizens the "Right to Explanation" for automated decisions.
3. **NYDFS 23 NYCRR 500 (Cybersecurity Requirements for Financial Services)**:
   - Requires multi-factor authentication, rigorous access controls, audit trails, and 72-hour cybersecurity incident reporting.

```python
# no-run
# Regulatory Compliance Checklist for GenAI Microservices
COMPLIANCE_REQUIREMENTS = {
    "GLBA": {
        "encryption_in_transit": "TLS 1.3 mandated",
        "encryption_at_rest": "AES-256 GCM with KMS rotation",
        "npi_masking": "Customer SSN/Account numbers masked before cloud LLM ingestion",
    },
    "NYDFS_23_NYCRR_500": {
        "mfa_required": True,
        "audit_retention_years": 7,
        "incident_notification_window_hours": 72,
    },
    "GDPR": {
        "right_to_be_forgotten": "Purge customer embeddings and chat logs within 30 days of request",
        "zero_data_retention_agreement": "Signed cloud provider commitment preventing model retraining on customer data",
    },
}
```

## Likely follow-ups

- How does the Zero Data Retention (ZDR) agreement with Microsoft Azure OpenAI fulfill GLBA obligations?
- What are the regulatory penalties for failing to report a GenAI data breach under NYDFS 500?

---

[← Q0960](../../batch_10_ai_security_responsible_ai/0960_preventing_cross_tenant_data_bleed_in_shared_vector/README.md) · [AI Security, Guardrails & Responsible AI in a Bank index](../README.md) · [All sections](../../README.md) · [Q0962 →](../../batch_10_ai_security_responsible_ai/0962_redacting_pii_before_public_cloud_llm_calls_zero_data/README.md)
