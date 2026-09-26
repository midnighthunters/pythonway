# Q0121 · Where to place documents and the question

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Context engineering | Medium |

## Question

In a long-context prompt, should the question go before or after the documents? What ordering rules do you follow?

## Answer

Practical guidance that holds across most current models:
- Put long documents first and the specific question or instructions after them, near the end. Models attend strongly to the end of the context, and recency helps them apply the instructions to the material.
- Keep global rules in the system prompt (stable, and cacheable).
- Order retrieved chunks sensibly: the most relevant first (or first and last, which mitigates "lost in the middle"), and keep chunks from the same document together in document order when continuity matters.
- Label everything with ids, titles, dates and sources, so the model can cite and prefer the newer or authoritative version.
- Restate the key constraint briefly after the documents for very long contexts ("Answer only from the documents above, citing [n]").

Validate the ordering on your own evaluation set, because the gains differ by model.

## Likely follow-ups

- How would you test whether ordering matters for your use case?

---

[← Q0120](../../batch_02_prompting_context_structured_output/0120_compact_large_tool_outputs/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0122 →](../../batch_02_prompting_context_structured_output/0122_parse_and_validate_citations_in_answers/README.md)
