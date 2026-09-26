# Q0757 · Azure Monitor and Application Insights for LLM latency alerting

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | Azure OpenAI | Medium |

## Question

What key metrics from Azure OpenAI should be monitored in Azure Monitor and Application Insights? What alert thresholds indicate degraded service?

## Answer

Key Metrics to Monitor:
1. `AzureOpenAIRequests`: Total request count segmented by deployment and HTTP status code. Alert on 4xx (especially 429) and 5xx spikes (> 1% error rate over 5 minutes).
2. `ProcessedPromptTokens` & `GeneratedTokens`: Real-time token throughput measuring workload spikes against provisioned TPM.
3. `Time To First Token (TTFT)`: End-to-end latency to first streamed chunk. Alert if P95 TTFT exceeds 1.5 seconds.
4. `ProvisionedManagedUtilizationPct` (for PTUs): Capacity utilization percentage. Alert when utilization sustains above 80% to plan capacity expansion before drops occur.
5. `ContentSafetyBlocks`: Sudden spike indicates potential jailbreak testing or prompt injection attack on internal applications.

## Likely follow-ups

- How do Log Analytics Kusto (KQL) queries correlate 429 errors with specific client IP addresses?
- What automated remediation actions can an Azure Alert trigger via Logic Apps or webhooks?

---

[← Q0756](../../batch_08_azure_openai_bedrock_cloud_ai/0756_simulating_a_dynamic_tpm_quota_allocator_in_python/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0758 →](../../batch_08_azure_openai_bedrock_cloud_ai/0758_custom_log_analytics_query_parser_for_azure_openai/README.md)
