# Q0181 · Source metadata for grounding

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Grounding | Medium |

## Question

What metadata should accompany each retrieved chunk in the prompt, and why?

## Answer

Include, compactly:
- A stable id for citations ([1] or `doc-123#p4`).
- Title and section heading, so the model understands context and users can verify.
- Source system and owner (for example "HR Policy Portal"), which signals authority.
- Effective date or version, and a status such as superseded or draft, which helps resolve conflicts and staleness.
- Jurisdiction or business line where policies vary ("UK", "US", "Corporate Treasury").
- Page or URL for deep links in the UI.

Tell the model how to use it: "prefer the most recent effective version; if sources conflict, say so and cite both". Keep entitlement and classification metadata out of the model's view where it isn't needed, but use it in retrieval filtering. Too much metadata wastes tokens, so include only what changes the answer or the citation.

## Likely follow-ups

- How would you handle a question where the UK and US policies differ?

---

[← Q0180](../../batch_02_prompting_context_structured_output/0180_inject_the_current_date_and_time_zone/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0182 →](../../batch_02_prompting_context_structured_output/0182_resolve_conflicting_policy_versions/README.md)
