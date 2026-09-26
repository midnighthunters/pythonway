# Q0058 · Sources of non-determinism in LLM APIs

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Reliability | Medium |

## Question

Temperature is 0 but you get different outputs for the same prompt. Why, and what should an evaluation pipeline do about it?

## Answer

Causes:
- Floating-point non-associativity. GPU kernels sum in different orders depending on batch composition, parallelism and hardware, so near-tied logits can flip the argmax. One flip changes every token after it.
- Dynamic batching with other users' requests, and different replicas or hardware behind the endpoint.
- Silent model or version updates when you use a floating alias instead of a pinned version.
- MoE routing sensitivity, speculative decoding, and some providers ignoring or overriding sampling parameters for reasoning models.

```python
import numpy as np

a = (1e16 + 1.0) - 1e16
b = (1e16 - 1e16) + 1.0
assert a == 0.0 and b == 1.0
logits_order1 = np.array([a, 0.5])
logits_order2 = np.array([b, 0.5])
assert np.argmax(logits_order1) == 1 and np.argmax(logits_order2) == 0
```

The same maths in a different summation order flips the chosen token.

For evaluations: pin model versions, run each case several times and report the mean and variance (or pass@k and pass^k), use tolerant scorers (semantic or rubric rather than exact match), and store the seed, model version and parameters with every result. Use a seed parameter where offered, but treat it as best effort.

## Likely follow-ups

- How many repeats do you need to distinguish a 2-point accuracy change?

---

[← Q0057](../../batch_01_llm_fundamentals/0057_stop_sequences_across_streamed_chunks/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0059 →](../../batch_01_llm_fundamentals/0059_grammar_constrained_decoding_with_token_masks/README.md)
