# Q0041 · Mixture of experts routing

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Architectures | Medium |

## Question

Explain mixture-of-experts (MoE) layers and implement a top-2 router that sends each token to its two highest-scoring experts and combines their outputs with renormalised gate weights.

## Answer

An MoE layer replaces one FFN with E expert FFNs. A router scores the experts per token, and only the top-k run. Total parameters are large, but active parameters (and FLOPs) per token are small. Challenges include load balancing (an auxiliary loss, capacity limits), all-to-all communication across GPUs, and needing memory for every expert.

```python
import numpy as np


def moe_top2(x: np.ndarray, router_w: np.ndarray, experts: list) -> tuple[np.ndarray, np.ndarray]:
    logits = x @ router_w
    top2 = np.argsort(-logits, axis=-1)[:, :2]
    out = np.zeros_like(x)
    for t in range(x.shape[0]):
        sel = logits[t, top2[t]]
        gates = np.exp(sel - sel.max())
        gates /= gates.sum()
        for g, e in zip(gates, top2[t]):
            out[t] += g * experts[e](x[t])
    return out, top2


rng = np.random.default_rng(0)
d, num_experts = 4, 4
experts = [lambda v, s=s: v * s for s in (1.0, 2.0, 3.0, 4.0)]
x = rng.normal(size=(3, d))
router = np.zeros((d, num_experts))
router[:, 3] = 10.0
router[:, 2] = 5.0
x = np.abs(x)
out, chosen = moe_top2(x, router, experts)
assert all(set(c) == {2, 3} for c in chosen.tolist())
assert np.all((out > 3 * x) & (out < 4 * x))
```

With these weights every token routes to experts 2 and 3, and the output is a gate-weighted blend of 3x and 4x.

## Likely follow-ups

- Why do MoE models have high memory needs but lower per-token compute?
- What goes wrong if the router sends most tokens to one expert?

---

[← Q0040](../../batch_01_llm_fundamentals/0040_structure_prompts_for_provider_prompt_caching/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0042 →](../../batch_01_llm_fundamentals/0042_reasoning_models_and_test_time_compute/README.md)
