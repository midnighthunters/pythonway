# Q0157 · Instruction drift in long conversations

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Context engineering | Medium |

## Question

After 40 turns, the assistant stops following its formatting and policy rules. Why, and what do you change?

## Answer

Why:
- The system prompt is far from the current turn, and recent conversation dominates attention.
- Earlier assistant turns that bent the rules act as de facto examples, so the model imitates its own history.
- Trimming or summarisation may have dropped the instructions or key constraints.
- The user may have gradually steered it (multi-turn jailbreak patterns).

Fixes:
- Always keep the system prompt, and never trim it.
- Re-inject a short reminder of the critical rules near the end of the context for long sessions.
- Summarise history into facts and state, not a style-setting transcript, and remove off-policy assistant turns from the carried history.
- Enforce formats with structured outputs and validators, and policies with code and guardrails, so drift can't cause harm.
- Test with long-conversation evaluation scripts, not just single turns.

## Likely follow-ups

- How would you build an evaluation that catches multi-turn drift?

---

[← Q0156](../../batch_02_prompting_context_structured_output/0156_context_distraction_and_poisoning/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0158 →](../../batch_02_prompting_context_structured_output/0158_what_to_store_in_long_term_memory/README.md)
