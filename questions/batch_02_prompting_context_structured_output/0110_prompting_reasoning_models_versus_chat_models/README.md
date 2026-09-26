# Q0110 · Prompting reasoning models versus chat models

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Prompt design | Medium |

## Question

How should you prompt a reasoning model differently from a standard chat model?

## Answer

- State the goal, constraints and success criteria, and let the model plan. Detailed step-by-step scripts and "think step by step" add little and can even hurt.
- Fewer or no few-shot examples at first. Add them only if the output format needs it.
- Provide all the relevant context up front, clearly delimited. Say what "done" looks like (for example "return JSON matching this schema", "list assumptions").
- Use the effort or budget controls instead of prose for "think harder". Expect higher latency and hidden reasoning tokens that are billed.
- Don't ask it to reveal its chain of thought. Ask for a concise rationale or evidence if you need an explanation.
- For agents, reasoning models are good at planning and tool selection, so give them well-described tools and let them decide.

Standard chat models benefit more from explicit decomposition, examples and step-by-step instructions.

## Likely follow-ups

- When is a cheaper chat model with a decomposed prompt chain better than one reasoning-model call?

---

[← Q0109](../../batch_02_prompting_context_structured_output/0109_role_prompting_and_personas/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0111 →](../../batch_02_prompting_context_structured_output/0111_prompt_chaining_with_validation_between_steps/README.md)
