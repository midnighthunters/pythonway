# Q0109 · Role prompting and personas

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Prompt design | Easy |

## Question

Does "You are an expert financial analyst" actually improve answers? When are personas useful?

## Answer

- A persona mostly sets tone, vocabulary and assumed audience. On modern models it gives little reliable accuracy gain on its own.
- What helps more is concrete context: the audience ("a treasury operations analyst"), the task and success criteria, domain constraints ("use IFRS terminology"), and examples.
- Useful cases: consistent voice for a branded assistant, and simulating a reviewer ("act as a strict code reviewer and list security issues"), where the persona implies a checklist.
- Risks: over-confident personas ("you are always right") increase unwarranted certainty. Personas that impersonate real people or regulated roles ("you are a licensed lawyer") create compliance issues.

Measure it. If the persona doesn't move evaluation metrics, keep the prompt shorter.

## Likely follow-ups

- How would you A/B test whether a persona line helps?

---

[← Q0108](../../batch_02_prompting_context_structured_output/0108_few_shot_order_and_recency_effects/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0110 →](../../batch_02_prompting_context_structured_output/0110_prompting_reasoning_models_versus_chat_models/README.md)
