# Q0762 · Azure Policy enforcement: preventing public IP creation on AI endpoints

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | Cloud AI Architecture | Medium |

## Question

How does Azure Policy enforce enterprise security governance to ensure no cloud AI resource is accidentally created with public internet access enabled?

## Answer

Azure Policy acts as a guardrail at the Azure Resource Manager (ARM) control plane, evaluating resource definitions before creation.

Policy Definition Mechanism:
1. `Deny` Effect on Public Network Access:
   - A custom policy rule inspects all resources of type `Microsoft.CognitiveServices/accounts` where `kind == "OpenAI"`.
   - If the property `properties.publicNetworkAccess` is not explicitly set to `"Disabled"`, the ARM deployment is instantly rejected with HTTP 403 Forbidden.
2. Mandatory Private Endpoints:
   - Another policy mandates that any cognitive service account must have an associated `privateEndpointConnections` resource linked to an approved bank VNet subnet.
3. Continuous Compliance Auditing:
   - Azure Policy continuously scans the entire cloud subscription and flags any non-compliant drift in security dashboards.

## Likely follow-ups

- How does Azure Policy prevent developers from bypassing rules during local CLI testing?
- Can Azure Policy automatically remediate a non-compliant resource by disabling public access?

---

[← Q0761](../../batch_08_azure_openai_bedrock_cloud_ai/0761_network_routing_expressroute_versus_public_internet_latency/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0763 →](../../batch_08_azure_openai_bedrock_cloud_ai/0763_azure_openai_token_bucket_rate_limiter_with_burst_multiplier/README.md)
