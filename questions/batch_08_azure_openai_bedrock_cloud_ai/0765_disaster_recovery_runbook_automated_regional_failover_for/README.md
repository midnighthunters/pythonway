# Q0765 · Disaster Recovery runbook: automated regional failover for Azure OpenAI

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | Cloud AI Architecture | Hard |

## Question

Detail the automated steps executed by an enterprise cloud AI gateway when a primary Azure OpenAI region suffers an unplanned regional outage.

## Answer

Disaster Recovery Runbook Steps:

1. Detection Phase:
   - Health probes running every 5 seconds detect 3 consecutive failed health pings or a sudden surge in HTTP 503/504 errors (> 15% of traffic over 30 seconds).
   - Gateway trips the regional Circuit Breaker to `OPEN`.
2. Traffic Drainage & Shift Phase:
   - The global router (Azure Front Door or AWS Route 53 Anycast) drains in-flight connections and shifts 100% of new ingress traffic to the secondary region (e.g. `westeurope`).
3. Quota Rebalancing:
   - The gateway automatically triggers an Azure API call or automated script to increase secondary deployment provisioned limits or enables secondary burst buffers.
   - Low-priority asynchronous batch workloads are paused to preserve secondary capacity for real-time customer assistants.
4. Recovery & Health Verification:
   - Gateway probes primary region in `HALF_OPEN` state. Once 50 consecutive probe requests succeed with P95 latency < 800ms, traffic is gradually restored (10% -> 50% -> 100%).

## Likely follow-ups

- How do you prevent split-brain states during intermittent regional network flappings?
- What are the recovery time objectives (RTO) and recovery point objectives (RPO) for stateful agent workflows?

---

[← Q0764](../../batch_08_azure_openai_bedrock_cloud_ai/0764_content_filtering_bypass_review_process_in_regulated_banks/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0766 →](../../batch_08_azure_openai_bedrock_cloud_ai/0766_amazon_bedrock_provisioned_throughput_model_units_and/README.md)
