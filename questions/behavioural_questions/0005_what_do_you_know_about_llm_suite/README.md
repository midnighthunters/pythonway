# B0005 · What do you know about LLM Suite

| Section | Topic | Difficulty |
|---|---|---|
| Behavioural, Role & JPMorganChase | JPMC & LLM Suite | Medium |

## Question

What do you know about LLM Suite, and what engineering challenges do you think it has?

## Answer

Publicly reported facts (say "publicly reported"; don't claim inside knowledge):

- JPMorganChase's proprietary GenAI platform that gives employees secure access to LLMs. Released in summer 2024; about 200,000 onboarded users within eight months; later reports cite around 250,000 employees with access.
- Model-agnostic: an abstraction layer routes work to models from providers such as OpenAI and Anthropic, so models can be swapped as they improve. It is reportedly refreshed roughly every eight weeks.
- Won American Banker's 2025 Innovation of the Year grand prize.
- Stated direction: an "AI hub for employees", connecting more internal data sources and combining GenAI with workflows so agents can carry out multi-step tasks.

Engineering challenges this implies: provider adapters and routing, entitlement-aware retrieval, guardrails, evaluation on every model change, quota and cost allocation, streaming at scale, observability, and now MCP/A2A-based integration of tools and agents.

## Likely follow-ups

- What makes a model-agnostic platform hard to build?
- How would you evaluate a new model before exposing it to users?
- What would you build next?

---

[← B0004](../../behavioural_questions/0004_why_llm_suite_engineering/README.md) · [Behavioural, Role & JPMorganChase index](../README.md) · [All sections](../../README.md) · [B0006 →](../../behavioural_questions/0006_why_corporate_technology_in_london/README.md)
