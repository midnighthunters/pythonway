# Q0044 · Pre-training, SFT and preference tuning

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Training pipeline | Medium |

## Question

Describe the stages that turn a base model into a chat assistant, and what each stage changes.

## Answer

1. Pre-training: next-token prediction on trillions of tokens of web, code and books. It produces broad knowledge and skills, but the model just continues text and doesn't follow instructions reliably.
2. Supervised fine-tuning (SFT, instruction tuning): train on curated prompt-response pairs, often with chat templates and tool-call examples. It teaches format, instruction following and tool use.
3. Preference optimisation: RLHF (train a reward model on human comparisons, then optimise with PPO), or direct methods such as DPO on chosen and rejected pairs. It shapes helpfulness, harmlessness, tone and refusals.
4. Reinforcement learning with verifiable rewards: reward correct maths, passing unit tests and successful tool trajectories. This is the main driver of reasoning models.
5. Safety tuning and red-teaming loops, then evaluation and release.

For enterprise teams, you mostly consume steps 1–4 from vendors. What you might do is lightweight SFT or LoRA on narrow tasks, preference data from user feedback for evaluation, and prompt and RAG engineering. Most "make it know our data" needs are solved by retrieval, not training.

## Likely follow-ups

- Why does SFT alone often produce an over-eager, verbose assistant?

---

[← Q0043](../../batch_01_llm_fundamentals/0043_estimate_training_compute_with_6nd/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0045 →](../../batch_01_llm_fundamentals/0045_implement_the_dpo_loss/README.md)
