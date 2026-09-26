# Q0964 · Membership Inference Attacks: detecting private records in model weights

| Section | Topic | Difficulty |
|---|---|---|
| AI Security, Guardrails & Responsible AI in a Bank | PII and DLP | Hard |

## Question

Explain Membership Inference Attacks (MIA) against fine-tuned LLMs, and write Python code implementing loss-threshold membership inference.

## Answer

In a Membership Inference Attack, an attacker determines whether a specific individual's confidential record (e.g. "Trader John Doe traded $50M in swap contracts") was part of the model's private training dataset.

Because models typically achieve lower training loss (higher log-likelihood / lower perplexity) on training data than on unseen test data, an attacker can infer membership by thresholding prediction loss.

```python
import math
from typing import List


class MembershipInferenceTester:
    def __init__(self, loss_threshold: float = 0.5):
        self.loss_threshold = loss_threshold

    def calculate_cross_entropy_loss(self, predicted_probs: List[float]) -> float:
        # Loss = -sum(log(p)) / N
        return -sum(math.log(max(1e-12, p)) for p in predicted_probs) / len(predicted_probs)

    def infer_membership(self, token_probs: List[float]) -> bool:
        loss = self.calculate_cross_entropy_loss(token_probs)
        # Low loss indicates model likely memorized the sequence during training
        return loss < self.loss_threshold


mia = MembershipInferenceTester(loss_threshold=0.3)

# Sample 1: Model predicted target tokens with high confidence (likely training member)
training_sample_probs = [0.85, 0.90, 0.92, 0.88]
assert mia.infer_membership(training_sample_probs) is True

# Sample 2: Model uncertain on unseen data (non-member)
unseen_sample_probs = [0.30, 0.40, 0.25, 0.35]
assert mia.infer_membership(unseen_sample_probs) is False
```

## Likely follow-ups

- How does Differential Privacy mathematically bound the success rate of Membership Inference Attacks?
- What is the Likelihood Ratio Attack (LiRA) for MIA?

---

[← Q0963](../../batch_10_ai_security_responsible_ai/0963_differential_privacy_in_fine_tuning_and_synthetic_dataset/README.md) · [AI Security, Guardrails & Responsible AI in a Bank index](../README.md) · [All sections](../../README.md) · [Q0965 →](../../batch_10_ai_security_responsible_ai/0965_model_inversion_attacks_reconstructing_private_inputs_from/README.md)
