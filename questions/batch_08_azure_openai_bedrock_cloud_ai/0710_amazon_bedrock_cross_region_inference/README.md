# Q0710 · Amazon Bedrock Cross-Region Inference

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | AWS Bedrock | Medium |

## Question

What is Amazon Bedrock Cross-Region Inference (CRI), and how does it prevent 429 throttling while maintaining regulatory compliance?

## Answer

During market volatility or peak business hours, a single AWS region (e.g. `us-east-1`) can experience high utilization, resulting in HTTP 429 Too Many Requests errors.

Amazon Bedrock Cross-Region Inference (CRI):
1. Mechanism:
   - Instead of targeting a specific regional model ID, applications invoke an Inference Profile ARN (e.g. `us.anthropic.claude-3-5-sonnet-20241022-v2:0` or `eu.anthropic.claude-3-5-sonnet-20241022-v2:0`).
   - Bedrock automatically and dynamically routes requests across multiple underlying AWS data centers within the specified geographic boundary (e.g. between `us-east-1`, `us-east-2`, and `us-west-2`).
2. Resilience & Quota Pooling:
   - Effectively pools TPM and RPM quotas across regions, virtually eliminating 429 throttling spikes with zero code changes in the calling application.
3. Sovereign Data Boundaries:
   - European banks utilize EU-specific inference profiles (`eu.*`) ensuring that compute and data in transit remain strictly within EU boundaries (e.g. Frankfurt, Ireland, Paris), maintaining GDPR compliance.

## Likely follow-ups

- Does Cross-Region Inference incur additional data transfer charges?
- What latency difference might be observed when a request routes across regions?

---

[← Q0709](../../batch_08_azure_openai_bedrock_cloud_ai/0709_tool_calling_in_the_amazon_bedrock_converse_api/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0711 →](../../batch_08_azure_openai_bedrock_cloud_ai/0711_amazon_bedrock_guardrails_and_pii_masking/README.md)
