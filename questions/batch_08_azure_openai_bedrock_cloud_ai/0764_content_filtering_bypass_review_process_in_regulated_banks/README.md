# Q0764 · Content filtering bypass review process in regulated banks

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | Azure OpenAI | Medium |

## Question

Under what circumstances can a bank request an exemption from Azure OpenAI default content filtering, and what internal controls replace it?

## Answer

Why Banks Request Exemption:
Certain legitimate financial applications generate content that triggers standard content safety filters:
- Anti-Money Laundering (AML) & Sanctions: Analyzing dark-web narcotics transactions, arms trafficking communications, or terrorist financing dossiers.
- Fraud & Cyber Threat Intelligence: Analyzing phishing emails containing malicious language or scam tactics.
- Legal & Dispute Resolution: Analyzing harassment lawsuits or whistleblower transcripts.

Microsoft Exemption Criteria & Compensating Controls:
1. Formal Approval Application: Demonstrating regulated entity status and specific high-risk business justification.
2. In-House Compensating Guardrails:
   - The bank must implement its own internal content filtering pipeline (e.g. NeMo Guardrails, custom BERT classification, regex blocklists) tailored specifically to the use case.
3. Access Restricted to Vetted Staff:
   - Endpoints are restricted strictly to authorized AML investigators via Entra ID group membership.
4. Comprehensive Audit Logging:
   - 100% of unfiltered prompts and completions are immutably archived for internal compliance audit.

## Likely follow-ups

- What liability does a bank assume when operating with modified content filtering?
- Does modified content filtering also grant an exemption from Zero Data Retention?

---

[← Q0763](../../batch_08_azure_openai_bedrock_cloud_ai/0763_azure_openai_token_bucket_rate_limiter_with_burst_multiplier/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0765 →](../../batch_08_azure_openai_bedrock_cloud_ai/0765_disaster_recovery_runbook_automated_regional_failover_for/README.md)
