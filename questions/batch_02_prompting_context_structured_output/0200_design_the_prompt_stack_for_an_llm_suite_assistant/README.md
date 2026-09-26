# Q0200 · Design the prompt stack for an LLM Suite assistant

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Context engineering design | Hard |

## Question

Design the full prompt and context stack for a policy Q&A assistant used by 200,000 employees: what goes where, how it is versioned, cached, validated and evaluated.

## Answer

Layers, in order (the stable prefix first):
1. Platform system prompt (global, rarely changes): identity, safety and compliance rules, grounding and citation rules, abstention wording, and the output contract. Versioned and cached.
2. Assistant configuration (per assistant or business line): scope, tone, jurisdiction defaults, tool descriptions for only the allowed tools, and a few synthetic examples. Versioned, cached.
3. User context (per session): role or entitlement summary, language, time zone, today's date, and relevant long-term preferences.
4. Retrieved evidence (per turn): entitlement-filtered, reranked chunks with ids and metadata (title, effective date, jurisdiction), in delimited untrusted-data blocks, conflicts resolved to effective versions.
5. Conversation: a rolling summary plus the last few turns, with tool pairs intact.
6. Current user message, plus a short reminder of the output contract.

Output: a structured reply (`status`, `answer`, `citations`, optional `follow_ups`), streamed and validated (citations exist, quotes verified on high-risk routes, markdown sanitised).

Engineering:
- Budget allocator per section, token accounting in telemetry, and cache-friendly ordering.
- Prompt registry with immutable versions, snapshot tests, lint checks, and evaluation gates in CI (groundedness, citation accuracy, abstention on unanswerable questions, safety, format adherence, latency and cost).
- Canary rollout with feature flags and rollback. Prompt, model and index versions logged per trace.
- Per-model variants only where evaluations show a need.

## Likely follow-ups

- Which layer would you change first if the abstention rate doubled after a release?
- How would you let business lines customise layer 2 without breaking layer 1 guarantees?

---

[← Q0199](../../batch_02_prompting_context_structured_output/0199_per_model_prompt_variants_with_fallback/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md)
