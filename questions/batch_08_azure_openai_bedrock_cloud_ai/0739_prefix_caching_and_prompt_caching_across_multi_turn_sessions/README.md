# Q0739 · Prefix caching and prompt caching across multi-turn sessions

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | GPU Serving | Medium |

## Question

Explain how prefix caching (prompt caching) works in modern cloud providers (Anthropic Claude, Azure OpenAI, vLLM) and how it slashes latency and cost.

## Answer

In multi-turn chat assistants and RAG systems, large context prefixes (system prompts, detailed API schemas, 50-page financial policy documents) are repeated across successive requests.

Prompt Caching Mechanism:
1. KV Cache Reuse:
   - The engine hashes sequential blocks of the input prompt.
   - When a new request arrives sharing the exact same initial token sequence as a previous request, the engine skips the expensive prefill computation for those tokens.
   - It directly reuses the existing KV cache stored in GPU VRAM.
2. Benefits:
   - Latency: Cuts TTFT (Time To First Token) by up to 80%.
   - Cost: Major cloud providers offer up to a 50%–90% price discount on cached input tokens (e.g. Anthropic prompt caching).
3. Requirements:
   - Caching requires exact prefix matches from token 0; dynamic variables (timestamps, user IDs) must be placed at the very end of the prompt.

## Likely follow-ups

- Why does placing a dynamic timestamp at the beginning of a system prompt destroy prompt caching?
- What is the minimum token threshold required for cloud providers to activate prompt caching?

---

[← Q0738](../../batch_08_azure_openai_bedrock_cloud_ai/0738_simulating_speculative_decoding_acceptance_logic_in_python/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0740 →](../../batch_08_azure_openai_bedrock_cloud_ai/0740_implementing_prompt_prefix_cache_matching_in_python/README.md)
