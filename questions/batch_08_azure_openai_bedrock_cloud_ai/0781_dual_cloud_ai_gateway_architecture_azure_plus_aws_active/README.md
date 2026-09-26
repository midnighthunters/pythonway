# Q0781 · Dual-cloud AI gateway architecture: Azure plus AWS Active-Active

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | Multi-Cloud AI Gateways | Hard |

## Question

Design an Active-Active multi-cloud AI gateway architecture spanning Microsoft Azure and AWS. How is session affinity, failover, and token billing handled?

## Answer

Architecture Components:
1. Global Traffic Manager:
   - Anycast DNS / Cloudflare Enterprise routes client requests to the closest healthy cloud entry point.
2. Ingress Gateways:
   - Azure API Management (APIM) deployed in Azure `uksouth`.
   - AWS API Gateway / Envoy Proxy deployed in AWS `eu-west-2` (London).
3. Cross-Cloud Failover Mesh:
   - If Azure OpenAI hits quota or experiences 5xx errors, Azure APIM forwards the request over dedicated ExpressRoute/Direct Connect cloud interconnect directly to AWS Bedrock in `eu-west-2`, avoiding public internet hops.
4. Shared Distributed State:
   - Active-Active Redis Enterprise cluster replicated across Azure and AWS for global tenant rate-limit token buckets and semantic cache.
5. Unified Telemetry & Billing:
   - Both gateways push structured OTel events to a shared Kafka cluster, aggregating token consumption for centralized department chargebacks.

## Likely follow-ups

- What are the networking latency penalties of routing cross-cloud from Azure to AWS?
- How do you handle non-compatible parameter schemas (e.g. `max_tokens` vs `maxTokens`)?

---

[← Q0780](../../batch_08_azure_openai_bedrock_cloud_ai/0780_measuring_cri_latency_variance_and_jitter_in_python/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0782 →](../../batch_08_azure_openai_bedrock_cloud_ai/0782_high_availability_multi_provider_client_with_retry_and/README.md)
