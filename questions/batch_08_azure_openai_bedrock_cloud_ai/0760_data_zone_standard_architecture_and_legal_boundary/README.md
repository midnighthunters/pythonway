# Q0760 · Data Zone Standard: architecture and legal boundary verification

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | Azure OpenAI | Medium |

## Question

How does the Azure OpenAI Data Zone Standard deployment enforce data residency while mitigating regional capacity shortages?

## Answer

The Challenge:
Regional Standard deployments (e.g. `westeurope` in Amsterdam) guarantee data residency, but during peak traffic periods, Amsterdam data centers may hit 100% capacity and return HTTP 429 errors. Global Standard solves capacity by routing anywhere globally, but violates European data sovereignty laws.

Data Zone Standard Solution:
- Microsoft groups data centers into legally defined geopolitical zones (e.g. EU Data Zone: Sweden Central, Germany West Central, France Central, Switzerland North).
- A Data Zone Standard deployment dynamically balances traffic across data centers *exclusively within that geographic zone*.
- Legal Guarantee: Customer prompts and generated tokens never exit the specified zone in transit or at rest.
- Benefit: Delivers 3x–5x higher throughput quotas than a single regional deployment while maintaining 100% compliance with EU data protection regulations.

## Likely follow-ups

- How does a bank verify through audit logs that an EU Data Zone request was not processed in the US?
- Which specific regions belong to the EU Data Zone for Azure OpenAI?

---

[← Q0759](../../batch_08_azure_openai_bedrock_cloud_ai/0759_azure_openai_on_foundry_models_and_model_catalog_integration/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0761 →](../../batch_08_azure_openai_bedrock_cloud_ai/0761_network_routing_expressroute_versus_public_internet_latency/README.md)
