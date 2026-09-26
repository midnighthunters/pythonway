# Q0112 · Teach the model to say I don't know

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Reliability | Medium |

## Question

How do you get an assistant to abstain instead of guessing when the sources don't contain the answer? Show the prompt text and how you'd verify it works.

## Answer

Prompt elements:
- "Answer only using the numbered sources. If they don't contain the answer, reply exactly: `I couldn't find this in the available documents.` and suggest where to look."
- "Don't use outside knowledge for policy, numbers or dates."
- Give an example of an unanswerable question and the abstention reply.
- For structured outputs, add a field such as `"answerable": boolean` or an `"insufficient_evidence"` status, so abstention is machine-checkable.

Verification:
- Build an evaluation set with 20–30% unanswerable questions (answerable-looking questions whose answers aren't in the corpus).
- Measure the abstention rate on unanswerable questions (it should be high) and the false-abstention rate on answerable ones (it should be low). Track both, because tuning for one hurts the other.
- Re-test after model or prompt changes, since abstention behaviour shifts between versions.

## Likely follow-ups

- What is the business cost of too many false abstentions?

---

[← Q0111](../../batch_02_prompting_context_structured_output/0111_prompt_chaining_with_validation_between_steps/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0113 →](../../batch_02_prompting_context_structured_output/0113_controlling_output_length/README.md)
