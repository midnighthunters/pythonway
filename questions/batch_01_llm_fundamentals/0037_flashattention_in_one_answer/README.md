# Q0037 · FlashAttention in one answer

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Inference performance | Medium |

## Question

What problem does FlashAttention solve, and does it change the model's outputs?

## Answer

- Standard attention materialises the n×n score matrix in GPU high-bandwidth memory (HBM), so memory traffic and memory use are O(n²). GPUs are usually limited by memory bandwidth, not arithmetic.
- FlashAttention tiles Q, K and V into blocks that fit in on-chip SRAM and computes softmax incrementally with an "online softmax" (a running max and running sum per row). It never writes the full matrix to HBM, and recomputes pieces in the backward pass rather than storing them.
- Result: exact attention (the same maths, up to floating-point rounding), much less memory traffic, O(n) extra memory, and large speed-ups for long sequences. Later versions improved parallelism and added FP8 on newer GPUs.

It is an IO-aware kernel optimisation, not an approximation. Contrast it with sparse or linear attention, which change the maths.

## Likely follow-ups

- Implement the online softmax recurrence for a stream of scores.
- Why is recomputation in the backward pass cheaper than storing the activations?

---

[← Q0036](../../batch_01_llm_fundamentals/0036_speculative_decoding/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0038 →](../../batch_01_llm_fundamentals/0038_online_softmax_recurrence/README.md)
