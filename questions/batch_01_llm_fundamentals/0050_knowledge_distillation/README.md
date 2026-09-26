# Q0050 · Knowledge distillation

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Model optimisation | Medium |

## Question

What is knowledge distillation, and implement the distillation loss (KL divergence between temperature-softened teacher and student distributions).

## Answer

A smaller student model is trained to mimic a larger teacher. You can match its soft probability distributions (richer signal than hard labels), or train on teacher-generated outputs, often called synthetic data or sequence-level distillation. It is used to make cheaper and faster models for high-volume tasks such as classification, routing and extraction.

```python
import numpy as np


def softmax(x, t=1.0):
    z = x / t
    z = z - z.max(-1, keepdims=True)
    e = np.exp(z)
    return e / e.sum(-1, keepdims=True)


def distillation_kl(teacher_logits, student_logits, temperature: float = 2.0) -> float:
    p = softmax(teacher_logits, temperature)
    q = softmax(student_logits, temperature)
    kl = (p * (np.log(p + 1e-12) - np.log(q + 1e-12))).sum(-1)
    return float(kl.mean() * temperature ** 2)


t = np.array([[4.0, 1.0, 0.5]])
assert distillation_kl(t, t) < 1e-9
assert distillation_kl(t, np.array([[0.0, 0.0, 0.0]])) > distillation_kl(t, np.array([[3.0, 1.0, 0.5]]))
```

The T² factor keeps the gradient magnitudes comparable across temperatures.

Governance note: check model licences and provider terms. Some prohibit using their outputs to train competing models.

## Likely follow-ups

- Why do soft labels carry more information than the teacher's argmax?

---

[← Q0049](../../batch_01_llm_fundamentals/0049_catastrophic_forgetting/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0051 →](../../batch_01_llm_fundamentals/0051_bi_encoders_versus_cross_encoders/README.md)
