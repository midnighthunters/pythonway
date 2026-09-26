# Q0033 · Continuous batching and throughput

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Inference serving | Medium |

## Question

What is continuous (in-flight) batching, and why does it increase throughput compared with static batching? What is the latency trade-off?

## Answer

- Static batching waits for a batch of requests, runs them together, and finishes when the longest sequence finishes. Short requests sit idle, and new requests wait.
- Continuous batching, used by vLLM, TGI, TensorRT-LLM and SGLang, schedules at the iteration (token) level. After every decode step, finished sequences leave and waiting ones join. The GPU stays busy, and throughput (tokens per second per GPU) rises substantially.
- Supporting techniques: paged KV-cache allocation, which avoids fragmentation, and chunked prefill, which splits a long prompt so it doesn't stall everyone else's decode steps.

Trade-off: bigger batches mean higher throughput but higher per-token latency for each user. Serving systems tune the maximum batch size and the scheduling policy to hit a TPOT SLO while maximising throughput.

On a platform like LLM Suite you mostly consume hosted APIs, where this happens behind the scenes. It still shows up as latency variance under load, and as the reason provisioned throughput behaves differently from pay-as-you-go.

## Likely follow-ups

- What is head-of-line blocking in LLM serving?
- How would you choose between latency-optimised and throughput-optimised deployments for batch document processing?

---

[← Q0032](../../batch_01_llm_fundamentals/0032_prefill_versus_decode_latency/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0034 →](../../batch_01_llm_fundamentals/0034_model_weight_memory_by_precision/README.md)
