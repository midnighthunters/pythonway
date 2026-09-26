# Q0046 · LoRA forward pass and parameter savings

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Fine-tuning | Medium |

## Question

Implement a LoRA linear layer `y = xW + (α/r) · x A B`, with W frozen, and compute the fraction of trainable parameters. Show that merging the adapter gives identical outputs.

## Answer

LoRA freezes the pretrained weight and learns a low-rank update ΔW = AB with rank r ≪ d. B is initialised to zero, so training starts exactly from the base model. After training, ΔW can be merged into W (zero inference overhead), or kept separate so many adapters share one base model.

```python
import numpy as np


class LoRALinear:
    def __init__(self, w: np.ndarray, r: int, alpha: float, rng: np.random.Generator):
        d_in, d_out = w.shape
        self.w = w
        self.a = rng.normal(scale=0.01, size=(d_in, r))
        self.b = np.zeros((r, d_out))
        self.scale = alpha / r

    def __call__(self, x: np.ndarray) -> np.ndarray:
        return x @ self.w + self.scale * (x @ self.a) @ self.b

    def merged(self) -> np.ndarray:
        return self.w + self.scale * self.a @ self.b

    def trainable_fraction(self) -> float:
        return (self.a.size + self.b.size) / (self.w.size + self.a.size + self.b.size)


rng = np.random.default_rng(0)
w = rng.normal(size=(4096, 4096))
layer = LoRALinear(w, r=16, alpha=32, rng=rng)
x = rng.normal(size=(2, 4096))
assert np.allclose(layer(x), x @ w)
layer.b = rng.normal(scale=0.01, size=layer.b.shape)
assert np.allclose(layer(x), x @ layer.merged())
assert layer.trainable_fraction() < 0.008
```

Under 1% of the parameters are trainable here. That means small checkpoints, low optimizer memory and fast task switching.

QLoRA goes further: the frozen base is quantised to 4-bit (NF4) and gradients flow into higher-precision LoRA adapters, so large models can be fine-tuned on a single GPU.

## Likely follow-ups

- Which layers do you typically attach LoRA to (attention projections, MLP)?
- How would you serve 50 LoRA adapters for 50 business units on one base model?

---

[← Q0045](../../batch_01_llm_fundamentals/0045_implement_the_dpo_loss/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0047 →](../../batch_01_llm_fundamentals/0047_qlora_and_nf4_quantisation/README.md)
