# Q0723 · Disaster Recovery: Active-Active versus Active-Passive multi-region cloud AI

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | Cloud AI Architecture | Hard |

## Question

Compare Active-Active and Active-Passive multi-region deployment architectures for enterprise LLM services across Azure and AWS.

## Answer

Architectural Comparison:

1. Active-Passive (Warm Standby):
   - Primary region (e.g. Azure `uksouth`) handles 100% of traffic.
   - Secondary region (e.g. Azure `westeurope` or AWS `eu-west-1`) maintains provisioned capacity and warm endpoints.
   - Failover: Traffic is redirected via DNS / Global Traffic Manager upon health check failure.
   - Pros: Simpler state management, no split-brain risks, deterministic latency.
   - Cons: Idle secondary capacity incurs high reservation costs (especially for PTUs); recovery time objective (RTO) is 1–5 minutes.

2. Active-Active:
   - Both regions concurrently serve traffic (e.g. 50% `uksouth`, 50% `westeurope`) through an Anycast Global Load Balancer or Azure Front Door.
   - Health checks automatically shed load from a degraded region in milliseconds (RTO near zero).
   - Pros: Maximum utilization of provisioned throughput; instant resilience against regional cloud failures.
   - Cons: Requires distributed conversation state replication (e.g. Azure Cosmos DB with multi-region write or Redis Enterprise Active-Active CRDTs).

## Likely follow-ups

- How do you handle session affinity when a user has an active multi-turn conversation in an Active-Active setup?
- What are the cost implications of keeping provisioned PTUs warm in two regions simultaneously?

---

[← Q0722](../../batch_08_azure_openai_bedrock_cloud_ai/0722_data_residency_and_sovereignty_in_the_uk_and_eu/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0724 →](../../batch_08_azure_openai_bedrock_cloud_ai/0724_cloud_egress_cost_optimization_and_dedicated_network_peering/README.md)
