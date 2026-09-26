# Q0146 · The sandwich defence and its limits

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Prompt safety | Medium |

## Question

Some teams "sandwich" untrusted input between instructions (instructions, then data, then a reminder of the instructions). Does it work?

## Answer

- It helps a bit. Restating the rules after the untrusted content leverages recency, and clear delimiters reduce accidental instruction following.
- It is not a security control. Determined injections (role-play, encoding tricks, "the user has authorised you to…", multi-turn setups, instructions hidden in retrieved content) still succeed some of the time, and models change.

Layered defence instead:
1. Least privilege: the agent can't do anything that the current user, or the task, doesn't need.
2. Deterministic enforcement in code: tool allowlists per context, argument validation, entitlement checks, and human approval for side effects or data egress.
3. Isolation: process untrusted content with a model or step that has no tools ("quarantined" or "dual LLM" patterns), and pass only structured, validated results onward.
4. Detection: injection classifiers on inputs and retrieved content, and output filters for data leakage.
5. Monitoring and red-teaming.

## Likely follow-ups

- Explain the dual-LLM (privileged versus quarantined model) pattern.

---

[← Q0145](../../batch_02_prompting_context_structured_output/0145_schema_context_for_text_to_sql/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0147 →](../../batch_02_prompting_context_structured_output/0147_automatic_prompt_optimisation_with_an_eval_loop/README.md)
