# Q0043 · Estimate training compute with 6ND

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Scaling | Medium |

## Question

Use the approximation training FLOPs ≈ 6 × parameters × tokens to estimate compute and GPU-days for a model, and explain the Chinchilla compute-optimal rule.

## Answer

- The forward pass costs about 2N FLOPs per token and the backward pass about 4N, so training costs about 6ND.
- Chinchilla (2022) found that, for a fixed compute budget, loss is minimised with roughly 20 training tokens per parameter. Earlier large models were undertrained.
- Modern practice deliberately "over-trains" smaller models far beyond 20 tokens per parameter, because inference cost dominates over the model's lifetime.

```python
def train_flops(params: float, tokens: float) -> float:
    return 6 * params * tokens


def gpu_days(flops: float, peak_flops: float, mfu: float) -> float:
    return flops / (peak_flops * mfu) / 86_400


chinchilla_tokens = 20 * 70e9
f = train_flops(70e9, chinchilla_tokens)
assert f == 5.88e23
days = gpu_days(f, peak_flops=1e15, mfu=0.4)
assert 17_000 < days < 17_050
assert train_flops(8e9, 15e12) / train_flops(70e9, 1.4e12) > 1.2
```

About 17,000 GPU-days at 40% utilisation of an illustrative 1 PFLOP/s accelerator. The last line shows an over-trained 8B model on 15T tokens uses more compute than a Chinchilla-optimal 70B.

For an application team, the takeaway is that pre-training is out of scope. Fine-tuning and inference economics are what you manage.

## Likely follow-ups

- What is MFU, and why is 40–50% considered good?

---

[← Q0042](../../batch_01_llm_fundamentals/0042_reasoning_models_and_test_time_compute/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0044 →](../../batch_01_llm_fundamentals/0044_pre_training_sft_and_preference_tuning/README.md)
