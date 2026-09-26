# Q0156 · Context distraction and poisoning

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Context engineering | Medium |

## Question

What are context distraction, confusion and poisoning in agents, and how do you prevent them?

## Answer

- Distraction: long contexts full of marginally relevant material. The model latches onto irrelevant details, repeats past actions, or ignores the current instruction.
- Confusion: too many similar tools or overlapping documents, so the model picks the wrong one.
- Clash: contradictory information, such as an old policy version and a new one, or an early wrong assumption the model keeps honouring.
- Poisoning: an error (a hallucinated fact or a bad tool result) enters the context and is treated as truth in later steps. Adversarial poisoning is prompt injection in retrieved content or tool results.

Prevention:
- Retrieve less but better (rerank, deduplicate, filter by recency and authority).
- Load only the relevant tools.
- Prune or summarise stale tool outputs, and keep state in structured fields rather than transcripts.
- Isolate sub-tasks in sub-agents with fresh contexts, returning concise results.
- Validate tool outputs before adding them, and mark provenance.
- Allow resets: re-plan from the goal and verified facts when progress stalls.

## Likely follow-ups

- How would you detect that an agent is looping because of a poisoned context?

---

[← Q0155](../../batch_02_prompting_context_structured_output/0155_assemble_the_system_prompt_per_user_role/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0157 →](../../batch_02_prompting_context_structured_output/0157_instruction_drift_in_long_conversations/README.md)
