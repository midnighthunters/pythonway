# Q0705 · Private Endpoints and network isolation in Azure OpenAI

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | Azure OpenAI | Medium |

## Question

Describe how Azure Private Endpoints and Virtual Network (VNet) service endpoints secure Azure OpenAI resources. What network boundaries are enforced?

## Answer

In financial production environments, cloud resources must not have public IP addresses or route traffic over the public internet.

Network Architecture:
1. Disabling Public Access:
   - The Azure OpenAI resource has `publicNetworkAccess: "Disabled"` enforced via Azure Policy.
2. Private Endpoint Deployment:
   - A Private Endpoint creates a virtual network interface (NIC) with a private IP address (e.g. `10.240.12.55`) inside the bank's dedicated subnet.
3. Private DNS Zones:
   - Azure Private DNS Zone (`privatelink.openai.azure.com`) overrides public DNS resolution, resolving `jpmc-ai.openai.azure.com` directly to the internal private IP address.
4. On-Premises Connectivity:
   - Bank workstations and on-prem trading engines connect across dedicated Azure ExpressRoute connections directly to the VNet private IP, ensuring complete traffic isolation from the public internet.

## Likely follow-ups

- How does Azure Private Link prevent data exfiltration compared to standard firewall IP whitelisting?
- What routing configurations are required for multi-region active-active private endpoints?

---

[← Q0704](../../batch_08_azure_openai_bedrock_cloud_ai/0704_azure_openai_content_safety_filters_and_custom_blocklists/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0706 →](../../batch_08_azure_openai_bedrock_cloud_ai/0706_azure_api_management_as_an_ai_gateway/README.md)
