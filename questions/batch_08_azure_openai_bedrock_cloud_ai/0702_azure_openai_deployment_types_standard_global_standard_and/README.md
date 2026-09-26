# Q0702 · Azure OpenAI deployment types: Standard, Global Standard, and Provisioned

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | Azure OpenAI | Medium |

## Question

Compare Azure OpenAI deployment types: Regional Standard, Global Standard, Data Zone Standard, and Provisioned Throughput (PTU). When should an enterprise use each?

## Answer

Azure OpenAI provides four distinct deployment tiers:

1. Regional Standard:
   - Capacity is anchored to a single geographic data center (e.g. `uksouth` or `eastus`).
   - Strict data residency: prompts and completions never leave the specified region.
   - Tradeoff: Lowest quota limits; vulnerable to regional capacity crunches during peak hours.
   - Use Case: Highly sensitive customer data where UK/EU data sovereignty strictly forbids cross-border data transfer.

2. Global Standard:
   - Single endpoint that dynamically routes requests to Microsoft Azure data centers globally with available capacity.
   - Pros: Highest default TPM (Tokens Per Minute) and RPM quotas; significantly lower rate of 429 throttling.
   - Tradeoff: Data in transit may be processed outside the originating region (though still encrypted and not retained).
   - Use Case: Internal research tools, code assistants, or anonymized batch summarization jobs.

3. Data Zone Standard:
   - Balances quota scalability with legal residency: dynamically routes requests across data centers strictly within a legal geographic zone (e.g. EU Data Zone).
   - Use Case: GDPR-regulated European banking workloads.

4. Provisioned Throughput Units (PTU):
   - Dedicated compute capacity reserved for the tenant in monthly or yearly commitments.
   - Predictable hourly cost regardless of token volume; zero noisy-neighbor rate limiting; guaranteed latency SLAs.
   - Use Case: High-volume trading desk assistants and customer-facing core banking APIs.

## Likely follow-ups

- How does PTU overage bursting operate when a sudden market event spikes volume?
- What metrics determine when switching from pay-as-you-go to PTUs becomes cost-effective?

---

[← Q0701](../../batch_08_azure_openai_bedrock_cloud_ai/0701_azure_openai_service_overview_and_enterprise_benefits/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0703 →](../../batch_08_azure_openai_bedrock_cloud_ai/0703_azure_entra_id_and_managed_identity_authentication/README.md)
