# Q0123 · JSON mode, structured outputs and function calling

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Structured output | Medium |

## Question

Compare "JSON mode", schema-enforced structured outputs, and function or tool calling for getting machine-readable output. Which would you use for data extraction in production?

## Answer

- Prompt-only ("reply in JSON"): no guarantees. It fails occasionally with prose, code fences or truncation.
- JSON mode: the output is guaranteed to be syntactically valid JSON, but not to match your schema (missing fields, wrong types).
- Structured outputs with a strict schema: constrained decoding enforces your JSON Schema (required fields, types, enums). This is the strongest guarantee for extraction, but there are schema-feature limits (some keywords aren't supported, and all fields may need to be required with `additionalProperties: false`).
- Tool or function calling: the model chooses to call a tool with arguments matching its schema. It is best when the model must decide which action to take, or several of them. With strict mode, the arguments follow the schema too.

Production choice for extraction: structured outputs with a strict schema generated from a Pydantic model, then validate again with Pydantic for business rules (ranges, cross-field checks). Handle refusals and truncation explicitly. On providers without strict mode, use tool calling with a single forced tool, plus validation and retry.

## Likely follow-ups

- What does schema enforcement not protect you from? (Wrong but well-formed values.)

---

[← Q0122](../../batch_02_prompting_context_structured_output/0122_parse_and_validate_citations_in_answers/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0124 →](../../batch_02_prompting_context_structured_output/0124_extract_data_into_a_validated_pydantic_model/README.md)
