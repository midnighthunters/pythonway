# Q0143 · Faithful summaries of financial documents

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Summarisation | Medium |

## Question

A summary of a quarterly risk report will be read by senior management. How do you make sure it is faithful, especially the numbers?

## Answer

- Extract, then write: first extract the key figures into a structured table (metric, value, period, page), validated against the source text, then generate the narrative from that table. Numbers in the prose must come from the table.
- Instruct the model to preserve exact values and units and never compute new figures unless asked. Where derived values are needed, compute them in code.
- Post-generation checks: every number in the summary must appear in the source or the extracted table (a regex check). Citations to pages or sections. Negations and caveats checked by an NLI or judge model.
- Evaluate with a checklist of must-include points per document type, plus faithfulness scoring on a sample, reviewed by domain experts.
- UX and controls: label it "AI-generated draft", link to the sources, require human sign-off before distribution, and keep an audit trail of versions.

## Likely follow-ups

- Write the regex-based check that finds numbers in a summary that aren't in the source.

---

[← Q0142](../../batch_02_prompting_context_structured_output/0142_refine_summarisation/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0144 →](../../batch_02_prompting_context_structured_output/0144_read_only_guardrails_for_text_to_sql/README.md)
