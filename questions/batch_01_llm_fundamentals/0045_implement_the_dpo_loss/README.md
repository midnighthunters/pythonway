# Q0045 · Implement the DPO loss

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Preference optimisation | Hard |

## Question

Implement the Direct Preference Optimization loss for a batch, given sequence log-probabilities under the policy and a frozen reference model for the chosen and rejected responses.

## Answer

DPO optimises `-log σ(β[(log π(y_w) - log π_ref(y_w)) - (log π(y_l) - log π_ref(y_l))])`. It raises the likelihood of preferred responses relative to the reference, and lowers it for rejected ones, without training a separate reward model. β controls how far the policy may drift from the reference.

```python
import numpy as np


def log_sigmoid(x: np.ndarray) -> np.ndarray:
    return -np.logaddexp(0.0, -x)


def dpo_loss(pol_chosen, pol_rejected, ref_chosen, ref_rejected, beta: float = 0.1):
    margin = (np.asarray(pol_chosen) - ref_chosen) - (np.asarray(pol_rejected) - ref_rejected)
    losses = -log_sigmoid(beta * margin)
    reward_acc = float((margin > 0).mean())
    return float(losses.mean()), reward_acc


loss_equal, acc = dpo_loss([-10.0], [-10.0], [-10.0], [-10.0])
assert np.isclose(loss_equal, np.log(2)) and acc == 0.0
good, acc_good = dpo_loss([-5.0, -6.0], [-20.0, -18.0], [-10.0, -10.0], [-10.0, -10.0])
bad, _ = dpo_loss([-20.0], [-5.0], [-10.0], [-10.0])
assert good < np.log(2) < bad and acc_good == 1.0
assert np.isfinite(dpo_loss([1e4], [-1e4], [0.0], [0.0])[0])
```

`np.logaddexp` keeps `log σ` stable for large margins. The naive `np.log(1 / (1 + np.exp(-x)))` overflows.

Starting value: when the policy equals the reference, the loss is ln 2 ≈ 0.693. This is a useful sanity check in training logs.

## Likely follow-ups

- Why doesn't DPO need a separate reward model?
- What is reward hacking, and how does β mitigate drift?

---

[← Q0044](../../batch_01_llm_fundamentals/0044_pre_training_sft_and_preference_tuning/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0046 →](../../batch_01_llm_fundamentals/0046_lora_forward_pass_and_parameter_savings/README.md)
