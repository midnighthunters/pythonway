# Q0034 · Model weight memory by precision

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Inference capacity | Easy |

## Question

Write a function that estimates GPU memory for the model weights at a given precision, and decide which configurations fit on one 80 GB GPU with 20% headroom for the KV cache and activations.

## Answer

```python
BYTES = {"fp32": 4, "bf16": 2, "fp16": 2, "fp8": 1, "int8": 1, "int4": 0.5}


def weight_gb(params_billions: float, precision: str) -> float:
    return params_billions * 1e9 * BYTES[precision] / 1e9


def fits(params_billions: float, precision: str, gpu_gb: float = 80, headroom: float = 0.2) -> bool:
    return weight_gb(params_billions, precision) <= gpu_gb * (1 - headroom)


assert weight_gb(70, "bf16") == 140
assert weight_gb(70, "int4") == 35
assert not fits(70, "bf16") and not fits(70, "fp8") and fits(70, "int4")
assert fits(8, "bf16") and weight_gb(8, "bf16") == 16
```

The rule of thumb is parameters × bytes per parameter. A 70B model needs about 140 GB in BF16 (two or more GPUs with tensor parallelism), about 70 GB in FP8, or about 35 GB in 4-bit.

Remember the extras: KV cache (usually the big one), activations, CUDA context and framework overhead. For MoE models, all experts must be resident even though only a few are active per token.

## Likely follow-ups

- What quality risks come with 4-bit quantisation, and how would you evaluate them?
- Why do MoE models need memory for all parameters but compute for only the active ones?

---

[← Q0033](../../batch_01_llm_fundamentals/0033_continuous_batching_and_throughput/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0035 →](../../batch_01_llm_fundamentals/0035_symmetric_int8_quantization/README.md)
