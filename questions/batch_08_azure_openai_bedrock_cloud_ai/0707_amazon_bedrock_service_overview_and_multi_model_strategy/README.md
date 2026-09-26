# Q0707 · Amazon Bedrock service overview and multi-model strategy

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | AWS Bedrock | Easy |

## Question

What is Amazon Bedrock, and what architectural advantages does it offer for enterprise multi-model AI strategies?

## Answer

Amazon Bedrock is a fully managed AWS service providing access to leading foundation models (FMs) from multiple AI providers—including Anthropic (Claude 3.5 Sonnet, Claude 3 Opus/Haiku), Meta (Llama 3), Mistral AI, Cohere, and Amazon (Titan)—through a single unified API.

Enterprise Advantages:
1. Multi-Model Agnostic Architecture:
   - Applications can switch between model families (e.g. using lightweight Llama 3 for classification, and Claude 3.5 Sonnet for complex multi-agent financial reasoning) without rewriting custom SDK integration code.
2. Data Governance & Security:
   - Encrypted at rest using AWS Key Management Service (KMS) Customer-Managed Keys (CMK) and in transit via TLS 1.3.
   - Customer data is never used to train base models and never leaves the customer's chosen AWS Region or sovereign boundary.
3. Native AWS Integration:
   - Tight coupling with AWS IAM for granular per-model permissions, AWS CloudTrail for immutable audit trails, and Amazon CloudWatch for metric monitoring.
4. Serverless & Managed:
   - No infrastructure provisioning, GPU cluster management, or patching required.

## Likely follow-ups

- How does Amazon Bedrock model access differ from deploying models on Amazon SageMaker?
- How does AWS IAM govern which internal teams can invoke specific model ARNs?

---

[← Q0706](../../batch_08_azure_openai_bedrock_cloud_ai/0706_azure_api_management_as_an_ai_gateway/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0708 →](../../batch_08_azure_openai_bedrock_cloud_ai/0708_amazon_bedrock_converse_api_unified_abstraction/README.md)
