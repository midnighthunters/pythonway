# B0019 · Build versus buy an enterprise LLM platform

| Section | Topic | Difficulty |
|---|---|---|
| Behavioural, Role & JPMorganChase | Platform strategy | Medium |

## Question

Why would a bank build its own LLM platform instead of rolling out an off-the-shelf assistant?

## Answer

Reasons to build:

- Control: data stays in firm-controlled environments with custom logging, retention and audit.
- Model agility: route each task to the best model and switch providers without retraining users.
- Integration: firm identity, entitlements, internal data sources, internal APIs and workflow systems.
- Governance: consistent guardrails, evaluation, usage policy and cost allocation per business unit.
- Differentiation: proprietary workflows and agents are strategic assets.

Costs of building: headcount, keeping pace with vendor features, consumer-grade UX expectations.

Realistic answer: hybrid. Build the platform, gateway, integrations and governance; consume models and selected tools; adopt standards (MCP, A2A) so vendor agents and tools plug in.

## Likely follow-ups

- Which components would you buy?
- How do you keep up with vendor feature velocity?

---

[← B0018](../../behavioural_questions/0018_genai_in_a_bank_versus_a_startup/README.md) · [Behavioural, Role & JPMorganChase index](../README.md) · [All sections](../../README.md) · [B0020 →](../../behavioural_questions/0020_model_agnostic_platform_challenges/README.md)
