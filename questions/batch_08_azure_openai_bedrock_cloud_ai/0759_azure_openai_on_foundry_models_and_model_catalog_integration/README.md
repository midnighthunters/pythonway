# Q0759 · Azure OpenAI on Foundry Models and model catalog integration

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | Azure OpenAI | Medium |

## Question

What is Azure AI Foundry (formerly Azure AI Studio), and how does its model catalog unify proprietary OpenAI models with open models like Llama 3 and Mistral?

## Answer

Azure AI Foundry is Microsoft's unified enterprise GenAI development and governance platform.

Key Capabilities:
1. Comprehensive Model Catalog:
   - Houses frontier proprietary models (OpenAI GPT-4o, o1, o3-mini) alongside open-weight and partner models (Meta Llama 3, Mistral Large, Cohere, DeepSeek) through Models-as-a-Service (MaaS).
2. Pay-As-You-Go API Consumption (MaaS):
   - Open models are served serverlessly via managed endpoints billed on per-token consumption, eliminating the need to provision dedicated GPU virtual machines.
3. Unified SDK & Endpoint Interface:
   - Uses the Azure AI Inference SDK, providing an identical chat completion schema across OpenAI, Meta, and Mistral models.
4. Centralized Safety & Evaluation:
   - Applies Azure AI Content Safety filters and automated benchmark evaluation runs uniformly across all deployed models.

## Likely follow-ups

- How does deploying a model via MaaS differ from deploying on self-managed AKS GPU clusters?
- What are the SLA differences between Azure OpenAI and MaaS partner models?

---

[← Q0758](../../batch_08_azure_openai_bedrock_cloud_ai/0758_custom_log_analytics_query_parser_for_azure_openai/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0760 →](../../batch_08_azure_openai_bedrock_cloud_ai/0760_data_zone_standard_architecture_and_legal_boundary/README.md)
