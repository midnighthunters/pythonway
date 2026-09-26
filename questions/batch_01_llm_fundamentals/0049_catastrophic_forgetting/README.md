# Q0049 · Catastrophic forgetting

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Fine-tuning | Medium |

## Question

What is catastrophic forgetting in fine-tuning, and how do you detect and limit it?

## Answer

- Fine-tuning on a narrow dataset shifts the weights towards that task, and the model can lose general abilities it had: instruction following, safety behaviour, reasoning, or other languages.
- Detection: run a regression suite alongside the task evaluation, covering general benchmarks relevant to you, safety and refusal tests, and formatting and tool-call tests. Compare against the base model.
- Mitigation:
  - Parameter-efficient tuning (LoRA with a modest rank) changes fewer weights.
  - Lower learning rate and fewer epochs, with early stopping on a held-out set.
  - Mix general instruction data into the fine-tuning set (replay).
  - Keep the adapter separate, so the base model still serves other traffic.
  - Regularise towards the reference model (the KL term in preference tuning).

## Likely follow-ups

- Why is a safety regression after fine-tuning especially important in a bank?

---

[← Q0048](../../batch_01_llm_fundamentals/0048_fine_tune_rag_or_prompt/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0050 →](../../batch_01_llm_fundamentals/0050_knowledge_distillation/README.md)
