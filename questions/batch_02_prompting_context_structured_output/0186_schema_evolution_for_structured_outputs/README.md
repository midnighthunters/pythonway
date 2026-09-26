# Q0186 · Schema evolution for structured outputs

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Structured output | Medium |

## Question

Downstream systems consume your extraction JSON. How do you evolve the schema safely over time?

## Answer

- Version the schema explicitly (`schema_version` in the payload, and in the prompt or model configuration) and keep a changelog.
- Prefer additive changes: new optional fields with defaults. Consumers ignore unknown fields.
- Breaking changes (rename, type change, new required field) get a new major version. Run both versions in parallel with dual-write or translation, migrate consumers, then retire the old version.
- Readers should be tolerant: accept the old field names via aliases, and fill defaults.
- Contract tests between the producer (prompt, schema and model) and consumers.
- Re-run the evaluation on schema changes. Adding a field can change the model's accuracy on the other fields.
- For stored historical outputs, either migrate them or keep version-aware readers.

## Likely follow-ups

- Why can adding one new field reduce accuracy on existing fields?

---

[← Q0185](../../batch_02_prompting_context_structured_output/0185_chunked_extraction_over_long_documents/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0187 →](../../batch_02_prompting_context_structured_output/0187_tolerant_parsing_of_older_payloads/README.md)
