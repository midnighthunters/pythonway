# B0020 · Model-agnostic platform challenges

| Section | Topic | Difficulty |
|---|---|---|
| Behavioural, Role & JPMorganChase | Platform strategy | Medium |

## Question

What does "model-agnostic" mean for a platform like LLM Suite, and what makes it hard?

## Answer

Meaning: features and integrations don't depend on one model or provider. An abstraction layer routes each request to a model (for example a GPT model on Azure OpenAI or a Claude model on Bedrock) based on capability, cost, latency and policy.

What makes it hard:

- API differences: message formats, tool-calling schemas, structured-output support, streaming event shapes, token accounting.
- Behavioural differences: a prompt tuned for one model degrades on another, so you need per-model prompt variants plus evaluations.
- Capability gaps: context length, vision, reasoning controls, prompt caching.
- Quotas, limits and error semantics differ (429s, content-filter responses).
- Every model update needs regression evaluation.

Techniques: a canonical internal request/response schema, provider adapters, a capability registry, routing policies, evaluation gates and feature flags.

## Likely follow-ups

- How would you design the adapter layer?
- What do you do with a model that doesn't support tool calling?

---

[← B0019](../../behavioural_questions/0019_build_versus_buy_an_enterprise_llm_platform/README.md) · [Behavioural, Role & JPMorganChase index](../README.md) · [All sections](../../README.md) · [B0021 →](../../behavioural_questions/0021_measuring_success_of_an_internal_genai_platform/README.md)
