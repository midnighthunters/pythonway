# Q0085 · Agent latency budget with parallel stages

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Latency engineering | Medium |

## Question

An agent turn runs a planner call, then three tool calls, then a final answer call. Write a function that computes turn latency for sequential versus parallel stages, and use it to decide what to parallelise.

## Answer

```python
import math


def pipeline_latency(stages: list[list[float]]) -> float:
    """Each stage is a list of step latencies that run in parallel."""
    return sum(max(stage) for stage in stages if stage)


sequential = [[1.2], [0.8], [0.8], [0.8], [2.0]]
parallel_tools = [[1.2], [0.8, 0.8, 0.8], [2.0]]
assert math.isclose(pipeline_latency(sequential), 5.6)
assert math.isclose(pipeline_latency(parallel_tools), 4.0)
assert math.isclose(pipeline_latency([[1.2], [0.8, 3.5, 0.8], [2.0]]), 6.7)
```

The last case shows that a parallel stage is only as fast as its slowest call, so add per-tool timeouts.

Levers: run independent tool calls in parallel (models can emit several tool calls in one turn), stream the final answer, use a smaller model for planning or routing, cache tool results, cut round trips by giving the model better tools, and set a total deadline with graceful degradation.

## Likely follow-ups

- How would you enforce a 10-second end-to-end deadline across nested async calls?

---

[← Q0084](../../batch_01_llm_fundamentals/0084_fp16_versus_bf16_overflow/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0086 →](../../batch_01_llm_fundamentals/0086_pack_texts_into_embedding_batches/README.md)
