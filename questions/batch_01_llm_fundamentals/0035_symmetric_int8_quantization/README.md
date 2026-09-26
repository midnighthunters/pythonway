# Q0035 · Symmetric int8 quantization

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Quantization | Medium |

## Question

Implement per-channel symmetric INT8 quantisation and dequantisation of a weight matrix, and measure the reconstruction error.

## Answer

Scale each output channel (row) by `max|w| / 127`, round to integers in [-127, 127], and multiply back to dequantise. Per-channel scales reduce the error compared with a single tensor-wide scale when rows have different ranges.

```python
import numpy as np


def quantize_int8(w: np.ndarray):
    scale = np.abs(w).max(axis=1, keepdims=True) / 127.0
    scale = np.where(scale == 0, 1.0, scale)
    q = np.clip(np.round(w / scale), -127, 127).astype(np.int8)
    return q, scale


def dequantize(q: np.ndarray, scale: np.ndarray) -> np.ndarray:
    return q.astype(np.float32) * scale


rng = np.random.default_rng(0)
w = rng.normal(size=(64, 256)).astype(np.float32)
w[0] *= 50
q, s = quantize_int8(w)
err = np.abs(dequantize(q, s) - w)
assert q.dtype == np.int8 and np.all(err <= s / 2 + 1e-6)
tensor_scale = np.abs(w).max() / 127.0
tensor_err = np.abs(np.round(w / tensor_scale) * tensor_scale - w).mean()
assert err.mean() < tensor_err
```

In LLMs, outlier activation channels make naive activation quantisation hard. Methods such as LLM.int8(), SmoothQuant, GPTQ, AWQ and FP8 formats exist to handle this.

Evaluate any quantised model on your own task evaluations, not just perplexity.

## Likely follow-ups

- Weight-only quantisation versus weight-and-activation quantisation: which helps decode speed and which helps prefill?

---

[← Q0034](../../batch_01_llm_fundamentals/0034_model_weight_memory_by_precision/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0036 →](../../batch_01_llm_fundamentals/0036_speculative_decoding/README.md)
