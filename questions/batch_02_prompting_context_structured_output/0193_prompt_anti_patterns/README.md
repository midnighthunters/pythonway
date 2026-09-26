# Q0193 · Prompt anti-patterns

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Prompt design | Easy |

## Question

List the prompt anti-patterns you'd flag in a code review.

## Answer

- Secrets or internal URLs in prompts, or user data concatenated into the system role.
- Contradictory rules ("be brief" and "explain in detail"), or rule lists so long nobody knows which ones matter.
- Vague success criteria ("make it good"), and no output format for machine-consumed results.
- Relying on the prompt for security ("never show salaries to non-managers").
- No abstention path, so the model must answer whatever it knows.
- Examples containing real customer or employee data.
- Timestamps or random ids at the top of the prompt (breaks caching), and non-deterministic tool ordering.
- `str.format` on templates with JSON braces or user-controlled templates.
- Prompt changes shipped without an evaluation run, version bump or snapshot diff.
- The same prompt for every model family without testing.
- Asking the model to do arithmetic or date maths that code should do.

## Likely follow-ups

- Which of these would you block a merge for?

---

[← Q0192](../../batch_02_prompting_context_structured_output/0192_design_outputs_for_evaluation/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0194 →](../../batch_02_prompting_context_structured_output/0194_review_this_prompt/README.md)
