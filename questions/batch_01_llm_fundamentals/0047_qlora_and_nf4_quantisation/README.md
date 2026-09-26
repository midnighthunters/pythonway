# Q0047 · QLoRA and NF4 quantisation

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Fine-tuning | Medium |

## Question

What does QLoRA add on top of LoRA, and what are the practical risks when using it for an enterprise fine-tune?

## Answer

QLoRA ingredients:
- The base model is frozen and quantised to 4-bit NormalFloat (NF4), a data type whose levels are spaced for normally distributed weights.
- Double quantisation: the quantisation constants are themselves quantised to save more memory.
- Paged optimizers move optimizer state to CPU memory on spikes, avoiding out-of-memory errors.
- LoRA adapters are kept in BF16. The forward pass dequantises the base weights on the fly, and gradients flow only into the adapters.

Result: fine-tuning 30–70B models fits on one or two GPUs, with quality usually close to 16-bit LoRA on many tasks.

Risks and practices:
- Quality: evaluate against a 16-bit baseline on your own task set, and watch for regressions on general abilities (catastrophic forgetting).
- Merging adapters into a quantised base can lose accuracy. Many teams merge into the full-precision base and then re-quantise for serving.
- Data governance: training data must be approved (no client PII without a lawful basis), versioned and reproducible. Model risk management expects documented training runs.
- Serving: plan how the adapter will run (vLLM multi-LoRA, or merged weights), and the licence of the base model.

## Likely follow-ups

- When would you choose QLoRA over a hosted fine-tuning API?

---

[← Q0046](../../batch_01_llm_fundamentals/0046_lora_forward_pass_and_parameter_savings/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0048 →](../../batch_01_llm_fundamentals/0048_fine_tune_rag_or_prompt/README.md)
