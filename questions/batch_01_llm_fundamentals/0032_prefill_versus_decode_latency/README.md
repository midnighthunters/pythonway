# Q0032 · Prefill versus decode latency

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Inference performance | Medium |

## Question

Explain time to first token (TTFT) and time per output token (TPOT). Write a function that estimates end-to-end latency, and use it to show which optimisation helps a long-answer workload.

## Answer

- Prefill processes the whole prompt in parallel and is compute-bound. TTFT ≈ queueing + network + prefill time, which grows with prompt length.
- Decode generates tokens one by one and is memory-bandwidth bound. TPOT is roughly constant per token for a given batch.
- End-to-end latency ≈ TTFT + output_tokens × TPOT.

```python
def e2e_latency_ms(prompt_tokens: int, output_tokens: int, prefill_tok_per_s: float,
                   tpot_ms: float, overhead_ms: float = 50.0) -> float:
    ttft = overhead_ms + prompt_tokens / prefill_tok_per_s * 1000
    return ttft + output_tokens * tpot_ms


base = e2e_latency_ms(2_000, 800, prefill_tok_per_s=10_000, tpot_ms=20)
assert base == 50 + 200 + 16_000
faster_prefill = e2e_latency_ms(2_000, 800, prefill_tok_per_s=20_000, tpot_ms=20)
shorter_output = e2e_latency_ms(2_000, 400, prefill_tok_per_s=10_000, tpot_ms=20)
assert base - faster_prefill == 100
assert base - shorter_output == 8_000
```

The numbers are illustrative. In this long-answer workload, decode dominates, so the big wins are fewer output tokens (concise instructions, structured output, `max_tokens`), a faster or smaller model, and streaming to improve perceived latency. For RAG with huge prompts and short answers, prefill dominates, so prompt caching and smaller contexts win.

Always report p50, p95 and p99 for both TTFT and total latency.

## Likely follow-ups

- Why does streaming improve user experience without changing total latency?
- How would you set SLOs for TTFT and for total latency on a chat product?

---

[← Q0031](../../batch_01_llm_fundamentals/0031_mqa_and_gqa/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0033 →](../../batch_01_llm_fundamentals/0033_continuous_batching_and_throughput/README.md)
