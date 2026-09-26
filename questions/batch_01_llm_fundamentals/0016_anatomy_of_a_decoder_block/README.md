# Q0016 · Anatomy of a decoder block

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Transformers | Medium |

## Question

Walk through one decoder-only transformer block, and say where most parameters and most inference compute go.

## Answer

A typical modern block (pre-norm):
1. `h = x + Attention(RMSNorm(x))`: multi-head (often grouped-query) causal self-attention with RoPE on Q and K.
2. `out = h + FFN(RMSNorm(h))`: a feed-forward network, usually a gated variant (SwiGLU) that expands to about 3–4× the model width and back.

Where the parameters are: roughly two-thirds sit in the FFN matrices and one-third in the attention projections, plus the embedding and output matrices (large when the vocabulary is big).

Where inference cost goes:
- Prefill (processing the prompt) is compute-bound matrix multiplication over all tokens at once.
- Decode (one token at a time) is dominated by reading the weights and the KV cache from GPU memory, so it is memory-bandwidth bound.
- Attention over long contexts grows with sequence length. The KV cache grows linearly with context and batch size.

Mixture-of-experts models replace the FFN with many expert FFNs and a router, so only a fraction of the parameters are active per token.

## Likely follow-ups

- Why does decode speed barely improve with a faster GPU compute unit but improve with more memory bandwidth?
- What does SwiGLU add over a plain ReLU FFN?

---

[← Q0015](../../batch_01_llm_fundamentals/0015_layernorm_versus_rmsnorm/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0017 →](../../batch_01_llm_fundamentals/0017_encoder_decoder_and_encoder_decoder_models/README.md)
