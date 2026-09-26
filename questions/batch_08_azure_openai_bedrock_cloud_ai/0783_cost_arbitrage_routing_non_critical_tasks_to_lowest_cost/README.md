# Q0783 · Cost arbitrage: routing non-critical tasks to lowest-cost provider

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | Multi-Cloud AI Gateways | Medium |

## Question

How does an AI gateway perform cost and latency arbitrage across foundation models (e.g. GPT-4o, Claude 3.5 Sonnet, Llama 3 70B, GPT-4o-mini)?

## Answer

Arbitrage Strategy:
Not every prompt requires expensive frontier models ($15–$30/M tokens). An intelligent gateway analyzes query complexity and SLA requirements to route to the lowest-cost capable model:

1. Task Classification:
   - Tier 1 (Lightweight / High-Volume): Sentiment classification, PII redaction, entity extraction. Routed to GPT-4o-mini, Bedrock Haiku, or Llama 3 8B (~$0.15–$0.50/M tokens).
   - Tier 2 (Standard Enterprise): RAG question answering, email drafting, summarizing news. Routed to Llama 3 70B or GPT-4o standard (~$2–$5/M tokens).
   - Tier 3 (Complex Analytical): Complex financial modeling, legal contract reconciliation, multi-step agent debate. Routed to Claude 3.5 Sonnet or o1 (~$15–$60/M tokens).
2. Cost Savings:
   - Reduces overall enterprise AI spend by 60%–75% compared to routing all queries to frontier models.

## Likely follow-ups

- How can a small classifier model route queries with minimal latency overhead (< 20ms)?
- What fallback triggers if a lightweight model returns an empty or unparseable JSON response?

---

[← Q0782](../../batch_08_azure_openai_bedrock_cloud_ai/0782_high_availability_multi_provider_client_with_retry_and/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0784 →](../../batch_08_azure_openai_bedrock_cloud_ai/0784_cost_vs_quality_routing_engine_in_python/README.md)
