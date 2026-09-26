# Q0722 · Data residency and sovereignty in the UK and EU

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | Cloud AI Compliance | Medium |

## Question

How do UK Prudential Regulation Authority (PRA) rules and EU GDPR govern data residency for GenAI workloads, and how are cloud architectures structured to comply?

## Answer

Under GDPR Article 44–49 and UK PRA Supervisory Statement SS2/21 (Outsourcing and third-party risk management):
1. Geographic In-Country Processing:
   - Customer financial records and personally identifiable information (PII) must not be transferred outside the UK or European Economic Area (EEA) without specific adequacy decisions or Standard Contractual Clauses (SCCs).
2. Cloud AI Boundary Enforcement:
   - Azure OpenAI: Deployments must be pinned to `uksouth` (London) / `ukwest` (Cardiff) or EU Data Boundary regions (Frankfurt, Dublin, Paris, Amsterdam). Global endpoints must be disabled via Azure Policy.
   - AWS Bedrock: Inference profile ARNs must be prefixed with `eu.` (e.g. `eu.anthropic.claude-3-5-sonnet`) to ensure cross-region failover remains strictly within Frankfurt, Ireland, and Paris.
3. Sub-processor Verification:
   - Third-party model providers (e.g. Anthropic, OpenAI) must operate under signed Data Protection Agreements (DPAs) guaranteeing that processing occurs solely within authorized data center boundaries.

## Likely follow-ups

- What constitutes an "international transfer" when invoking an LLM hosted in another jurisdiction?
- How does client-side token pseudonymization enable using non-EU models while remaining compliant?

---

[← Q0721](../../batch_08_azure_openai_bedrock_cloud_ai/0721_customer_managed_keys_with_azure_key_vault_and_aws_kms/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0723 →](../../batch_08_azure_openai_bedrock_cloud_ai/0723_disaster_recovery_active_active_versus_active_passive_multi/README.md)
