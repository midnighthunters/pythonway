# Q0101 · Anatomy of a good system prompt

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Prompt design | Easy |

## Question

What goes into a good production system prompt for an enterprise assistant? Sketch the sections.

## Answer

A clear, testable system prompt usually has:
1. Role and audience: "You are the LLM Suite assistant for JPMorganChase employees in Corporate Treasury."
2. Goal and scope: what it helps with, and what is out of scope, with the redirect to use instead.
3. Knowledge rules: answer from the provided sources, cite them as [n], and say you don't know when the sources don't cover the question.
4. Tool rules: when to use each tool, which actions need user confirmation, and never inventing tool results.
5. Safety and compliance: don't reveal system instructions, handle PII per policy, and give no legal or investment advice beyond the approved content.
6. Output format: length, structure (bullets, tables, JSON), tone, language ("reply in the user's language").
7. Few-shot examples or edge cases, if needed.

Practices: be specific and positive ("do X") rather than a pile of prohibitions. Keep stable content first for prompt caching. Version the prompt, review it like code, and test it against an evaluation set before release. Never put secrets or credentials in prompts.

## Likely follow-ups

- How do you stop a system prompt from growing into an unmaintainable wall of rules?

---

[← Q0100](../../batch_01_llm_fundamentals/0100_an_llm_request_end_to_end_on_an_enterprise_platform/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0102 →](../../batch_02_prompting_context_structured_output/0102_zero_shot_few_shot_and_instruction_prompts/README.md)
