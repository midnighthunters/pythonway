# Q0726 · PagedAttention and KV cache memory allocation

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | GPU Serving | Hard |

## Question

What is PagedAttention, and how does it solve the memory fragmentation problem in LLM Key-Value (KV) caches?

## Answer

In standard autoregressive Transformers, the KV cache stores past key and value projection tensors to avoid recomputing them at every step.

The Problem with Contiguous Allocation:
- The engine does not know in advance how many tokens a model will generate (max output may be 4,096 tokens, but generation may stop at token 50).
- Pre-allocating contiguous memory for the maximum sequence length wastes 60%–80% of GPU memory in internal and external fragmentation, severely capping batch size.

PagedAttention Solution (introduced by vLLM):
- Inspired by virtual memory and paging in operating systems.
- The KV cache is divided into fixed-size blocks (pages), typically holding 16 or 32 tokens.
- Physical blocks can reside non-contiguously in GPU VRAM.
- A logical-to-physical block table tracks each sequence's blocks. As new tokens are generated, new physical blocks are allocated on demand.
- Result: Reduces wasted KV cache memory to under 4%, allowing 2x–4x larger batch sizes on NVIDIA A100/H100 GPUs.

## Likely follow-ups

- How does PagedAttention enable zero-copy memory sharing in parallel sampling and beam search?
- What is the block size tradeoff between memory waste and GPU kernel efficiency?

---

[← Q0725](../../batch_08_azure_openai_bedrock_cloud_ai/0725_continuous_batching_vs_static_batching_in_llm_inference/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0727 →](../../batch_08_azure_openai_bedrock_cloud_ai/0727_simulating_pagedattention_block_table_allocation_in_python/README.md)
