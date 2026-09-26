# Q0188 · Structured outputs versus regex post-processing

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Structured output | Easy |

## Question

A colleague extracts fields from model prose using regexes. When is that acceptable, and why is structured output usually better?

## Answer

Regex on prose is brittle. The model can vary its phrasing, ordering or number formatting, or add caveats, and each model upgrade can break the patterns. Failures are silent (no match means a missing value) or wrong (the wrong number matched).

Structured outputs give you an explicit contract (schema), enforced types and enums, clear failure modes (validation errors), and easy evolution.

Regex is still appropriate for:
- Validating well-defined formats inside structured fields (IBANs, dates, ISO codes).
- Parsing your own tags or markers (`<answer>`, `STATUS:`).
- Post-checks on free text (numbers in a summary must exist in the source, citations present).
- Deterministic extraction from the source document itself, where the format is known (for example a statement's header).

## Likely follow-ups

- Give an example where a deterministic parser should replace the LLM entirely.

---

[← Q0187](../../batch_02_prompting_context_structured_output/0187_tolerant_parsing_of_older_payloads/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0189 →](../../batch_02_prompting_context_structured_output/0189_validate_parallel_tool_calls_independently/README.md)
