# Q0965 · Model inversion attacks: reconstructing private inputs from output probabilities

| Section | Topic | Difficulty |
|---|---|---|
| AI Security, Guardrails & Responsible AI in a Bank | PII and DLP | Medium |

## Question

Explain model inversion attacks, and write Python code demonstrating how output logit temperature smoothing mitigates token probability leakage.

## Answer

Model inversion attacks exploit high-precision output token probabilities (logits) to reconstruct private training sentences or system prompts. If a model returns raw logprobs, an attacker can use beam search over token probabilities to invert the underlying private context.

Mitigation:
1. Disable raw logprob outputs in production APIs.
2. Apply temperature scaling and top-k filtering to smooth probability distributions.

```python
import math
from typing import List


def apply_temperature_smoothing(logits: List[float], temperature: float = 1.0) -> List[float]:
    """Applies temperature scaling and softmax to smooth peaky output distributions."""
    scaled = [l / max(0.01, temperature) for l in logits]
    max_l = max(scaled)
    exp_logits = [math.exp(l - max_l) for l in scaled]
    sum_exp = sum(exp_logits)
    return [e / sum_exp for e in exp_logits]


raw_logits = [5.0, 3.0, 2.0]

# At low temp (0.2), distribution is extremely peaked (reveals exact top token)
peaked_probs = apply_temperature_smoothing(raw_logits, temperature=0.2)
assert peaked_probs[0] > 0.95

# At higher temp (2.0), distribution is smoothed, reducing inversion signal
smoothed_probs = apply_temperature_smoothing(raw_logits, temperature=2.0)
assert smoothed_probs[0] < 0.70
```

## Likely follow-ups

- Why should public-facing GenAI APIs restrict access to `logprobs=True` parameters?
- How does model quantization (FP8 / INT4) impact model inversion attacks?

---

[← Q0964](../../batch_10_ai_security_responsible_ai/0964_membership_inference_attacks_detecting_private_records_in/README.md) · [AI Security, Guardrails & Responsible AI in a Bank index](../README.md) · [All sections](../../README.md) · [Q0966 →](../../batch_10_ai_security_responsible_ai/0966_right_to_be_forgotten_gdpr_art_17_deleting_customer_data/README.md)
