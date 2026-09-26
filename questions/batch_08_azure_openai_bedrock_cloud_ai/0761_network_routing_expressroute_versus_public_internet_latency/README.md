# Q0761 · Network routing: ExpressRoute versus public internet latency

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | Cloud AI Architecture | Medium |

## Question

Analyze the network latency and jitter profiles of invoking cloud AI APIs over Azure ExpressRoute versus the public internet for high-frequency banking systems.

## Answer

Performance Analysis:

1. Public Internet Ingress:
   - Packets traverse multiple public Autonomous Systems (AS) and ISP peering points.
   - Latency: Unpredictable variance (40ms to 180ms round-trip).
   - Jitter: High packet jitter and packet loss during peak consumer internet hours, causing streaming SSE chunk stalls.
   - Security: Encrypted via TLS, but IP addresses and traffic volumes are visible to internet monitors.

2. Azure ExpressRoute Dedicated Circuit:
   - Private Layer-3 point-to-point fiber connection directly connecting bank on-premises data centers to Microsoft's global backbone.
   - Latency: Deterministic sub-5ms round-trip latency to local Azure cloud regions (e.g. London data center to `uksouth`).
   - Jitter: Near-zero packet jitter; strictly enforced SLA on bandwidth and uptime (99.95%+).
   - Resilience: ExpressRoute circuits are provisioned in redundant active-active pairs across geographically separated meet-me facilities.

## Likely follow-ups

- How does MTU (Maximum Transmission Unit) configuration on ExpressRoute impact large document transfer speed?
- What is the difference between ExpressRoute Private Peering and Microsoft Peering?

---

[← Q0760](../../batch_08_azure_openai_bedrock_cloud_ai/0760_data_zone_standard_architecture_and_legal_boundary/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0762 →](../../batch_08_azure_openai_bedrock_cloud_ai/0762_azure_policy_enforcement_preventing_public_ip_creation_on/README.md)
