# Q0720 · Zero Data Retention agreements in regulated cloud AI

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | Cloud AI Compliance | Hard |

## Question

What is a Zero Data Retention (ZDR) agreement with cloud AI providers (Microsoft Azure and AWS), and why is it mandatory for Tier-1 banks?

## Answer

Default Cloud AI Logging Behavior:
By default, commercial cloud AI services (including standard Azure OpenAI instances) log customer prompt and completion payloads for up to 30 days in asynchronous abuse-monitoring data stores accessible to vendor human security personnel.

Why ZDR is Mandatory for Banks:
1. Bank Secrecy & GLBA / GDPR: Prompts frequently contain Non-Public Personal Information (NPI), material non-public financial information (MNPI), or proprietary trading calculations. Storing unencrypted customer financial data in vendor abuse stores breaches financial confidentiality laws.
2. Zero Data Retention (ZDR) Terms:
   - Microsoft Azure and AWS contractually disable prompt and completion logging entirely.
   - Data exists purely in ephemeral GPU/CPU RAM for the duration of inference computation and is purged immediately upon completion of the HTTP stream.
   - Vendor employees have zero access to customer payloads under any circumstances.
3. Requirements to Qualify:
   - Formal application demonstrating regulated status; deployment inside dedicated VNets; agreement to deploy customer-side content safety guardrails.

## Likely follow-ups

- What audits verify that a cloud provider adheres to Zero Data Retention?
- Does ZDR apply to embeddings stored in cloud vector databases?

---

[← Q0719](../../batch_08_azure_openai_bedrock_cloud_ai/0719_streaming_responses_time_to_first_token_vs_throughput/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0721 →](../../batch_08_azure_openai_bedrock_cloud_ai/0721_customer_managed_keys_with_azure_key_vault_and_aws_kms/README.md)
