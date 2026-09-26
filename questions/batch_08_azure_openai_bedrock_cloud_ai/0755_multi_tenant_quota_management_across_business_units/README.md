# Q0755 · Multi-tenant quota management across business units

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | Azure OpenAI | Medium |

## Question

How do enterprise cloud AI platform teams allocate and enforce TPM and RPM quotas across dozens of internal business units sharing a centralized Azure OpenAI resource?

## Answer

Centralized Quota Problem:
An enterprise Azure OpenAI subscription has a finite regional quota (e.g. 2,000,000 Tokens Per Minute). If one algorithmic trading team runs an unthrottled batch job, they consume 100% of the quota, starving high-priority wealth management chat assistants.

Enterprise Quota Governance Architecture:
1. Virtual Quotas at AI Gateway:
   - The central AI Gateway (APIM or custom FastAPI proxy) defines a virtual quota matrix mapping `tenant_id` to guaranteed TPM and RPM caps.
2. Tiered Priority Queues:
   - High-Priority (Real-time Trading & Client Chat): Guaranteed minimum TPM slice that cannot be preempted.
   - Low-Priority (Batch RAG Ingestion & Backtesting): Shared opportunistic pool that throttles automatically during trading hours.
3. Fair-Share Token Bucket:
   - Distributed Redis token buckets enforce per-tenant quotas across all gateway worker instances.

## Likely follow-ups

- How does the gateway handle an application that exceeds its allocated TPM slice?
- What metrics trigger an alert to request an Azure quota increase?

---

[← Q0754](../../batch_08_azure_openai_bedrock_cloud_ai/0754_preparing_jsonl_training_data_for_azure_openai_fine_tuning/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0756 →](../../batch_08_azure_openai_bedrock_cloud_ai/0756_simulating_a_dynamic_tpm_quota_allocator_in_python/README.md)
