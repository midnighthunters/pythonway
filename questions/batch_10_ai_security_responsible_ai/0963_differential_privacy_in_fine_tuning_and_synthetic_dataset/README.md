# Q0963 · Differential Privacy in fine-tuning and synthetic dataset generation

| Section | Topic | Difficulty |
|---|---|---|
| AI Security, Guardrails & Responsible AI in a Bank | PII and DLP | Hard |

## Question

Explain Differential Privacy (DP-SGD) in fine-tuning language models, and write Python code implementing DP gradient clipping and Gaussian noise injection.

## Answer

When fine-tuning an LLM on proprietary bank customer records, standard training risks memorizing individual customer data.

**Differentially Private Stochastic Gradient Descent (DP-SGD)** provides a mathematical privacy guarantee ($\epsilon, \delta$):
1. **Per-sample Gradient Clipping**: Clips the L2-norm of each sample's gradient to a threshold $C$, bounding any single individual's influence.
2. **Noise Addition**: Adds calibrated Gaussian noise $\mathcal{N}(0, \sigma^2 C^2 I)$ to the aggregated gradient.

```python
import math
import random
from typing import List


def dp_clip_and_noise_gradients(
    gradients: List[float], max_norm: float = 1.0, noise_multiplier: float = 0.5
) -> List[float]:
    # 1. Compute L2 norm
    l2_norm = math.sqrt(sum(g ** 2 for g in gradients))

    # 2. Clip gradient if it exceeds max_norm
    scaling_factor = min(1.0, max_norm / (l2_norm + 1e-6))
    clipped = [g * scaling_factor for g in gradients]

    # 3. Add Gaussian noise (simulated with random.gauss)
    sigma = noise_multiplier * max_norm
    noisy_gradients = [g + random.gauss(0, sigma) for g in clipped]

    return noisy_gradients


raw_grads = [3.0, 4.0]  # L2 norm = 5.0
dp_grads = dp_clip_and_noise_gradients(raw_grads, max_norm=1.0, noise_multiplier=0.0)  # zero noise test

# Clipped norm must equal max_norm (1.0)
clipped_norm = math.sqrt(sum(g ** 2 for g in dp_grads))
assert abs(clipped_norm - 1.0) < 1e-4
```

## Likely follow-ups

- What is the privacy budget $\epsilon$ (epsilon), and how does model utility degrade as $\epsilon \to 0$?
- How does the Opacus library integrate DP-SGD into PyTorch fine-tuning loops?

---

[← Q0962](../../batch_10_ai_security_responsible_ai/0962_redacting_pii_before_public_cloud_llm_calls_zero_data/README.md) · [AI Security, Guardrails & Responsible AI in a Bank index](../README.md) · [All sections](../../README.md) · [Q0964 →](../../batch_10_ai_security_responsible_ai/0964_membership_inference_attacks_detecting_private_records_in/README.md)
