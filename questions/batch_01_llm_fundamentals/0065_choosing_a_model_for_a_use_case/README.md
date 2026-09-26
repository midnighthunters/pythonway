# Q0065 · Choosing a model for a use case

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Model selection | Medium |

## Question

A team asks which model to use for their new assistant. Walk through how you decide.

## Answer

1. Define the task and success criteria, and build a small evaluation set of 50–200 real examples with expected outputs or rubrics.
2. Hard constraints first: data classification and approved models or regions, context length, modality, tool calling or structured outputs, latency SLO and budget.
3. Shortlist 2–4 models across tiers (a fast small model, a strong general model, a reasoning model if the task is multi-step).
4. Evaluate on your set: quality, TTFT and total latency (p50/p95), cost per task, refusal and safety behaviour, and variance across runs.
5. Choose on the quality–cost–latency frontier. Often a mix works best: a small model for classification and routing, a strong one for generation.
6. Operationalise it: pin versions, add a fallback model, monitor it, and re-evaluate when providers release or deprecate models.

On a model-agnostic platform, this is a repeatable process with a capability registry and an evaluation harness, not a one-off opinion.

## Likely follow-ups

- How do you avoid over-fitting the choice to a tiny evaluation set?

---

[← Q0064](../../batch_01_llm_fundamentals/0064_model_cascade_by_confidence/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0066 →](../../batch_01_llm_fundamentals/0066_open_weight_versus_hosted_models_in_a_bank/README.md)
