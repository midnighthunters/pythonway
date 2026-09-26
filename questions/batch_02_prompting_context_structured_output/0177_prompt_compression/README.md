# Q0177 · Prompt compression

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Cost optimisation | Medium |

## Question

Prompts are getting long and expensive. What prompt-compression options exist, and what are their risks?

## Answer

Options, from safest to riskiest:
1. Remove waste: duplicated instructions, verbose tool descriptions, pretty-printed JSON, boilerplate in retrieved chunks (headers, footers, navigation text).
2. Retrieve less: better reranking, a tighter top-k, deduplication, filtering by metadata.
3. Summarise history and tool outputs into facts and state.
4. Use structured compact formats (CSV or tables instead of verbose JSON) for tabular data.
5. Prompt caching: doesn't shorten the prompt, but makes the stable prefix cheaper and faster.
6. Learned compression (token-dropping methods such as LLMLingua-style approaches): large savings, but they can drop negations, numbers or qualifiers.

Risks: losing critical details (amounts, "not", dates), degraded citations, and harder debugging. Evaluate any compression on quality metrics, not just token counts. Keep originals for audit.

## Likely follow-ups

- Which content should never go through lossy compression?

---

[← Q0176](../../batch_02_prompting_context_structured_output/0176_style_guide_compliance/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0178 →](../../batch_02_prompting_context_structured_output/0178_token_efficient_data_formats_in_prompts/README.md)
