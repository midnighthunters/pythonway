# Q0078 · Alternatives to quadratic attention

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Architectures | Medium |

## Question

What alternatives to full quadratic attention exist, and what do they trade away?

## Answer

- Sparse or local patterns (sliding window, block-sparse, dilated, global tokens): O(n·w) cost. They risk missing long-range dependencies unless mixed with global layers.
- Linear attention and kernel approximations: rewrite softmax attention so it can be computed in O(n). Historically weaker at precise recall ("find this exact phrase").
- State space models and recurrent designs (Mamba-style SSMs, RWKV, modern linear RNNs): constant memory per token and fast long-sequence inference, but weaker at exact copying and retrieval from far back.
- Hybrids that interleave attention and SSM or linear layers aim to get most of the quality with far less memory.
- System-level fixes without changing the maths: FlashAttention (exact, IO-aware), paged KV cache, KV-cache compression or eviction, and context parallelism.

For an application engineer, the practical questions are long-context quality on your own tasks (multi-needle recall), latency and cost, not the architecture label.

## Likely follow-ups

- Why are pure recurrent models weaker at "copy this exact string from 50k tokens ago"?

---

[← Q0077](../../batch_01_llm_fundamentals/0077_sliding_window_attention_mask/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0079 →](../../batch_01_llm_fundamentals/0079_bigram_language_model_with_smoothing/README.md)
