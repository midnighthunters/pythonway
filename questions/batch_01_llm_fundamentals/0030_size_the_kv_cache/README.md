# Q0030 · Size the KV cache

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Inference capacity | Medium |

## Question

Write a function that estimates KV-cache memory: `2 (K and V) × layers × kv_heads × head_dim × bytes_per_value × tokens × batch`. Use it to compare multi-head attention with grouped-query attention for a 70B-class model.

## Answer

```python
def kv_cache_bytes(layers: int, kv_heads: int, head_dim: int, tokens: int, batch: int = 1,
                   bytes_per_value: float = 2.0) -> float:
    return 2 * layers * kv_heads * head_dim * bytes_per_value * tokens * batch


GIB = 1024 ** 3
# Illustrative 70B-class shape: 80 layers, 64 query heads, head_dim 128, fp16 cache.
mha = kv_cache_bytes(layers=80, kv_heads=64, head_dim=128, tokens=8192)
gqa = kv_cache_bytes(layers=80, kv_heads=8, head_dim=128, tokens=8192)
assert round(mha / GIB) == 20
assert round(gqa / GIB, 1) == 2.5
assert mha / gqa == 8
per_token_gqa = kv_cache_bytes(80, 8, 128, tokens=1)
assert per_token_gqa == 327_680
```

How to read the result: with full multi-head attention, a single 8k-token sequence needs about 20 GiB of cache. GQA with 8 KV heads cuts that to about 2.5 GiB, which is why most modern models use GQA. Those gigabytes, plus the weights, decide how many concurrent sequences fit on a GPU.

Further levers: FP8 or INT8 KV cache, paged allocation (vLLM PagedAttention), prefix sharing, and sliding-window layers.

## Likely follow-ups

- How many concurrent 8k sequences fit on an 80 GB GPU after 35 GB of 4-bit weights?
- Why does KV-cache size, not FLOPs, often cap throughput?

---

[← Q0029](../../batch_01_llm_fundamentals/0029_kv_cache_incremental_decoding/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0031 →](../../batch_01_llm_fundamentals/0031_mqa_and_gqa/README.md)
