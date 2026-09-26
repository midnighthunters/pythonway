# Q0721 · Customer-Managed Keys with Azure Key Vault and AWS KMS

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | Cloud AI Compliance | Hard |

## Question

How do Customer-Managed Encryption Keys (CMEK / Bring Your Own Key) secure cloud AI workloads, and what happens when a key is revoked?

## Answer

Enterprise banks mandate that all data at rest—including custom fine-tuned model weights, cached prompt embeddings, and temporary training checkpoints—be encrypted using keys owned and managed exclusively by the bank in Hardware Security Modules (HSMs) via Azure Key Vault or AWS Key Management Service (KMS).

Mechanisms:
1. Envelope Encryption:
   - Data is encrypted with an ephemeral Data Encryption Key (DEK).
   - The DEK is encrypted (wrapped) with the bank's Key Encryption Key (KEK) stored inside Azure Key Vault / AWS KMS HSMs.
   - The cloud AI service must call `kms:Decrypt` or Key Vault `unwrapKey` to use the DEK.
2. Crypto-Shredding / Key Revocation:
   - If a regulatory incident, security compromise, or vendor termination occurs, the bank can immediately disable or delete the KEK in its HSM.
   - Without the KEK, the cloud provider's GPUs and storage cannot unwrap the DEK, instantly and irreversibly rendering all model checkpoints and data unreadable across all cloud storage tiers without waiting for disk overwrites.

## Likely follow-ups

- What latency impact does envelope encryption have on active LLM inference?
- How do automated key rotation policies prevent service disruption in cloud AI pipelines?

---

[← Q0720](../../batch_08_azure_openai_bedrock_cloud_ai/0720_zero_data_retention_agreements_in_regulated_cloud_ai/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0722 →](../../batch_08_azure_openai_bedrock_cloud_ai/0722_data_residency_and_sovereignty_in_the_uk_and_eu/README.md)
