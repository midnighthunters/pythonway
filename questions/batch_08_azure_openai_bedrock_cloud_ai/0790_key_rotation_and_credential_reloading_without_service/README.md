# Q0790 · Key rotation and credential reloading without service restart

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | Multi-Cloud AI Gateways | Medium |

## Question

How does an AI gateway rotate client secrets, OAuth signing certificates, or Managed Identity tokens with zero downtime and without restarting running pods?

## Answer

Zero-Downtime Secret Rotation:
1. Dual-Key Overlap Period:
   - Cloud Key Vaults (Azure Key Vault / AWS KMS) support key versioning.
   - During key rotation, the new key (Version B) is activated while the old key (Version A) remains valid for a 24-to-72-hour grace period.
2. Background Polling / Push Notification:
   - The gateway runs a background thread that periodically polls Key Vault for secret version changes, or listens to Azure Event Grid / AWS EventBridge rotation events.
3. Atomic In-Memory Pointer Swap:
   - When a new secret is fetched, it is validated and stored in memory. The gateway swaps an atomic pointer (e.g. `threading.Lock` or atomic reference) so new requests immediately use Version B while in-flight requests finish with Version A.
   - Eliminates container restarts, connection drops, and cache invalidation spikes.

## Likely follow-ups

- What failure modes occur if an old secret is revoked before all distributed gateway pods pick up the new secret?
- How do Managed Identities eliminate manual secret rotation entirely?

---

[← Q0789](../../batch_08_azure_openai_bedrock_cloud_ai/0789_fast_token_counter_and_budget_validator_in_python/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0791 →](../../batch_08_azure_openai_bedrock_cloud_ai/0791_in_memory_rotating_secret_provider_in_python/README.md)
