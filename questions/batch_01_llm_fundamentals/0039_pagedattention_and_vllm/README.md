# Q0039 · PagedAttention and vLLM

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Inference serving | Medium |

## Question

What is PagedAttention, and why did it significantly improve LLM serving throughput?

## Answer

- Problem: KV caches were allocated contiguously for the maximum sequence length, which wasted a lot of GPU memory through over-reservation and fragmentation, and limited batch size.
- PagedAttention, introduced by vLLM, stores the KV cache in fixed-size blocks (pages), like OS virtual memory. A block table maps each sequence's logical blocks to physical blocks allocated on demand.
- Benefits: near-zero waste, so more concurrent sequences and higher throughput. Copy-on-write sharing of common prefix blocks makes parallel sampling, beam search and shared system prompts cheap. It also enables prefix caching and swapping or preemption of sequences.

Related serving features to mention: continuous batching, chunked prefill, automatic prefix caching, speculative decoding, tensor and pipeline parallelism, and OpenAI-compatible HTTP endpoints. vLLM is relevant if the bank self-hosts open-weight models, for data residency or cost, alongside hosted Azure OpenAI and Bedrock.

## Likely follow-ups

- How does prefix caching on a self-hosted server relate to provider-side prompt caching?

---

[← Q0038](../../batch_01_llm_fundamentals/0038_online_softmax_recurrence/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0040 →](../../batch_01_llm_fundamentals/0040_structure_prompts_for_provider_prompt_caching/README.md)
