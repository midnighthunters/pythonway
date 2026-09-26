# Q0701 · Azure OpenAI service overview and enterprise benefits

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | Azure OpenAI | Easy |

## Question

What is Azure OpenAI Service, and why do enterprise financial institutions choose it over direct public OpenAI API endpoints?

## Answer

Azure OpenAI Service provides REST and SDK access to OpenAI's language models (GPT-4o, GPT-4, o1, embeddings) hosted directly within Microsoft Azure's secure cloud infrastructure.

Key reasons enterprise banks (like JPMorganChase) deploy on Azure OpenAI:
1. Enterprise Security & Isolation:
   - Models run inside the bank's dedicated Azure Virtual Network (VNet) with Private Endpoints. Public internet ingress can be completely disabled.
   - Integration with Microsoft Entra ID (formerly Azure AD) for Role-Based Access Control (RBAC) and Managed Identities, eliminating shared API keys.
2. Data Privacy & Zero Data Retention:
   - Microsoft contractually guarantees that customer prompts and completions are never used to train or improve any models.
   - Regulated financial institutions can qualify for modified content filtering and exemption from the default 30-day asynchronous prompt logging store (Zero Data Retention / ZDR).
3. Predictable Throughput & SLAs:
   - Supports Provisioned Throughput Units (PTUs) providing dedicated model capacity with strict latency SLAs and zero 429 noisy-neighbor throttling.
4. Compliance & Certifications:
   - Adheres to SOC 2 Type II, ISO 27001, HIPAA, and PCI-DSS compliance frameworks required by global financial regulators (PRA, FINRA, SEC).

## Likely follow-ups

- What is the difference between standard pay-as-you-go deployments and Provisioned Throughput Units (PTUs)?
- How does Azure's data boundary ensure compliance with UK and EU data residency laws?

---

[← Q0700](../../batch_07_mcp_a2a_skills_assistants/0700_end_to_end_integration_test_of_an_mcp_tool_within_an_a2a/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0702 →](../../batch_08_azure_openai_bedrock_cloud_ai/0702_azure_openai_deployment_types_standard_global_standard_and/README.md)
