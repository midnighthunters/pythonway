# Q0093 · Memory needed to fine-tune

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Fine-tuning | Medium |

## Question

Estimate GPU memory for full fine-tuning versus LoRA versus QLoRA of a 7B model with Adam in mixed precision (excluding activations).

## Answer

Rule of thumb for full fine-tuning with Adam in mixed precision: BF16 weights (2 bytes) + BF16 gradients (2) + FP32 master weights (4) + Adam m and v (4 + 4), so about 16 bytes per parameter. LoRA freezes the base (2 bytes per parameter in BF16, or about 0.5 in 4-bit) and pays the full 16 bytes only for the small adapter.

```python
def full_ft_gb(params_b: float) -> float:
    return params_b * 16


def lora_gb(params_b: float, adapter_params_m: float, base_bytes: float = 2.0) -> float:
    return params_b * base_bytes + adapter_params_m / 1000 * 16


assert full_ft_gb(7) == 112
assert round(lora_gb(7, adapter_params_m=20), 2) == 14.32
assert round(lora_gb(7, adapter_params_m=20, base_bytes=0.5), 2) == 3.82
```

So roughly 112 GB (multi-GPU, sharded with FSDP or ZeRO), about 14 GB for LoRA, and about 4 GB for QLoRA, plus activations. Activations grow with batch size × sequence length and are reduced with gradient checkpointing (recompute them in the backward pass) and smaller micro-batches with gradient accumulation.

## Likely follow-ups

- How does gradient checkpointing trade compute for memory?

---

[← Q0092](../../batch_01_llm_fundamentals/0092_vocabulary_size_trade_offs/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0094 →](../../batch_01_llm_fundamentals/0094_why_cosine_similarity_thresholds_don_t_transfer/README.md)
