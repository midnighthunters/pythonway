# Q0140 · Summarisation prompt design

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Summarisation | Easy |

## Question

What makes a good summarisation prompt for internal documents, and what are the common failure modes?

## Answer

Specify:
- Audience and purpose: "for a Treasury manager deciding whether to escalate".
- Format and length: "5 bullets, each under 25 words, then a one-line recommendation".
- Must-keep content: figures, dates, owners, decisions, risks, action items. Say "preserve all numbers exactly as written".
- Faithfulness: "Only include information stated in the document. Mark uncertainties."
- Handling gaps: "If the document doesn't mention X, say 'not stated'."

Failure modes: invented or rounded numbers, dropping negations or caveats ("not approved" becomes "approved"), over-weighting the beginning of long documents, mixing up entities, editorialising, and skipping the key but unusual detail. Evaluate with faithfulness checks and a coverage checklist of key points.

## Likely follow-ups

- How would you evaluate whether a summary dropped a critical caveat?

---

[← Q0139](../../batch_02_prompting_context_structured_output/0139_verify_extracted_entities_against_the_source/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0141 →](../../batch_02_prompting_context_structured_output/0141_map_reduce_summarisation/README.md)
