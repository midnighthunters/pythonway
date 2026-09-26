# Q0766 · Amazon Bedrock Provisioned Throughput: Model Units and capacity reservation

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | AWS Bedrock | Medium |

## Question

What is Provisioned Throughput in Amazon Bedrock, how are Model Units (MUs) calculated, and when is it financially advantageous over On-Demand pricing?

## Answer

Amazon Bedrock Provisioned Throughput:
- Provides dedicated model compute capacity by reserving Model Units (MUs) for specific foundation models (e.g. Anthropic Claude 3.5 Sonnet).
- Guarantees zero throttling (no 429 errors from noisy neighbors) and consistent latency SLAs during peak volatility.
- Purchased under 1-month or 6-month term commitments.

Financial Breakeven Calculation:
- On-Demand Pricing: Charged per 1,000 input tokens and per 1,000 output tokens.
- Provisioned Throughput: Charged an hourly flat rate per Model Unit (e.g. ~$20–$30/hour per MU depending on model and commitment term).
- Breakeven Rule: When a trading desk generates steady sustained volume exceeding ~5,000,000–8,000,000 tokens per hour, Provisioned Throughput becomes cheaper than on-demand pay-per-token pricing while eliminating rate-limit risks.

## Likely follow-ups

- Can you dynamically autoscale Bedrock Model Units up and down based on market hours?
- What happens if traffic exceeds the throughput capacity of provisioned Model Units?

---

[← Q0765](../../batch_08_azure_openai_bedrock_cloud_ai/0765_disaster_recovery_runbook_automated_regional_failover_for/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0767 →](../../batch_08_azure_openai_bedrock_cloud_ai/0767_provisioned_throughput_cost_vs_on_demand_breakeven/README.md)
