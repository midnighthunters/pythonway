# Q0198 · Prompt debugging workflow

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Prompt engineering process | Medium |

## Question

Users report that the assistant sometimes ignores the citation rule. Walk through how you debug and fix it.

## Answer

1. Reproduce: pull the failing traces (prompt version, model version, full context, parameters) from logs or LangSmith, and replay them.
2. Measure: turn the failures into evaluation cases and add a citation-compliance metric. Check the rate over a larger sample to size the problem.
3. Localise: is it certain query types, long contexts, a specific model version, missing sources, or truncated output (`finish_reason: length`)? Diff against the last good prompt version.
4. Hypothesise and test fixes one at a time: move the rule near the end, add an example, make citations a structured field, reduce context noise, or switch model. Compare on the evaluation set with repeated runs.
5. Add enforcement: a validator that rejects uncited answers and retries, or flags them in the UI.
6. Ship: version bump, snapshot diff, evaluation gate in CI, canary, then monitor the metric in production.

## Likely follow-ups

- How do you avoid fixing one failure mode while breaking another?

---

[← Q0197](../../batch_02_prompting_context_structured_output/0197_choosing_generation_settings_per_task/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0199 →](../../batch_02_prompting_context_structured_output/0199_per_model_prompt_variants_with_fallback/README.md)
