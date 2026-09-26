# Q0108 · Few-shot order and recency effects

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Few-shot | Medium |

## Question

The same few-shot examples give different accuracy depending on their order. Why, and how do you make prompts robust to it?

## Answer

Known effects:
- Recency: the examples closest to the query have more influence.
- Majority label: skewed example labels shift predictions.
- Surface copying: the model copies phrasing, length or entities from examples, and sometimes leaks example content into answers.

Mitigations:
- Pick diverse, representative examples, balanced across labels, and similar to the query (dynamic selection).
- Put crisp instructions and label definitions before the examples. For modern instruction-tuned models, good definitions often matter more than examples.
- Test order sensitivity: run the evaluation with several shuffles and report the variance. High variance means the prompt is brittle.
- Keep examples obviously synthetic (fake names and amounts), so they aren't mistaken for real data.
- Prefer structured output with an enum, so drifted wording can't break parsing.

## Likely follow-ups

- How would you detect that the model is copying details from the examples into real answers?

---

[← Q0107](../../batch_02_prompting_context_structured_output/0107_balance_few_shot_examples_across_labels/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0109 →](../../batch_02_prompting_context_structured_output/0109_role_prompting_and_personas/README.md)
