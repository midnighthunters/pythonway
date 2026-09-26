# Q0737 · Speculative decoding: draft model plus target model acceleration

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | GPU Serving | Hard |

## Question

How does speculative decoding accelerate LLM inference? Explain the draft-target verification mechanism.

## Answer

The Bottleneck in Autoregressive LLMs:
Autoregressive decoding is memory-bandwidth bound: generating 1 token requires loading all 70 billion parameters from GPU HBM to the compute cores. Arithmetic intensity is very low.

Speculative Decoding Mechanism:
1. Small Draft Model:
   - A lightweight, fast draft model (e.g. Llama-3-8B) quickly generates $K$ speculative candidate tokens (e.g. $K=4$) in parallel.
2. Large Target Model:
   - The large target model (e.g. Llama-3-70B) runs a single forward pass over all $K$ candidate tokens simultaneously.
   - Because the target model evaluates $K$ tokens in parallel, it takes roughly the same time as generating 1 token.
3. Verification & Acceptance:
   - The target model accepts tokens whose probability matches or exceeds the draft distribution, and rejects the first divergent token, generating a correct replacement.
   - Result: Generates 2x to 3x more tokens per second with zero loss in target model output distribution mathematically.

## Likely follow-ups

- Under what conditions does speculative decoding fail to provide a speedup?
- What is the difference between model-based speculative decoding and Medusa / multi-head speculation?

---

[← Q0736](../../batch_08_azure_openai_bedrock_cloud_ai/0736_implementing_a_multi_lora_adapter_router_in_python/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0738 →](../../batch_08_azure_openai_bedrock_cloud_ai/0738_simulating_speculative_decoding_acceptance_logic_in_python/README.md)
