# Q0116 · What context engineering means

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Context engineering | Medium |

## Question

People say "context engineering" has replaced "prompt engineering". What does it mean in practice for an agentic platform?

## Answer

Context engineering is deciding what information goes into the model's context window at each step, in what form and in what order, under a token budget. Most agent failures are context failures (missing, stale, noisy or conflicting context), not model failures.

Components:
- Instructions: system prompt, policies, persona.
- Knowledge: retrieved documents (entitlement-filtered), with metadata and citations.
- Tools: which tool definitions are loaded (a subset, not all 200), and how results are summarised back.
- Memory: short-term history (trimmed or summarised) and long-term user preferences or facts.
- State: task plan, intermediate results, scratch notes, and handoff summaries between agents.
- Structure: delimiters, ordering, and the stable prefix kept first for caching.

Techniques: budget allocation per section, summarisation and compaction, just-in-time retrieval (let the agent fetch details via tools instead of stuffing everything), isolating sub-tasks in sub-agents with their own clean context, and pruning stale tool outputs.

## Likely follow-ups

- What does "context rot" look like in a long-running agent, and how do you fix it?

---

[← Q0115](../../batch_02_prompting_context_structured_output/0115_measure_prompt_robustness_to_paraphrase/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0117 →](../../batch_02_prompting_context_structured_output/0117_allocate_a_token_budget_across_context_sections/README.md)
