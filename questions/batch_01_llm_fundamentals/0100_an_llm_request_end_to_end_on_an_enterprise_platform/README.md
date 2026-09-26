# Q0100 · An LLM request end to end on an enterprise platform

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Platform architecture | Hard |

## Question

Trace a single chat request on an enterprise platform like LLM Suite from the user's browser to the model and back. Name every component and what it's responsible for.

## Answer

1. Client: the web app authenticates the user (SSO, Entra ID or OIDC) and opens a streaming connection (SSE or WebSocket) to the API.
2. API gateway or edge: TLS, WAF, authentication token validation, coarse rate limiting, request size limits.
3. Chat or orchestration service (for example FastAPI): loads the conversation state (NoSQL store), applies the user's entitlements, and selects the assistant or agent configuration and prompt version.
4. Pre-processing guardrails: input normalisation, PII detection or redaction as policy requires, prompt-injection and jailbreak classifiers, data-classification checks.
5. Retrieval or tools, if needed: entitlement-filtered search over indexes, MCP tool calls through a governed gateway, with per-tool authorisation.
6. LLM gateway: model routing (capability, cost, region, quota), per-tenant quotas and token budgeting, retries and fallbacks across Azure OpenAI and Bedrock deployments, prompt caching, and cost metering.
7. Provider: model inference, provider-side content filtering, streamed tokens.
8. Post-processing: output guardrails (content filters, PII leakage, citation checks, schema validation) applied incrementally to the stream or on completion.
9. Response streaming back to the client, with citations and a trace id.
10. Persistence and observability: conversation store, audit log (who, what, which model and version, sources, tools), traces and metrics (TTFT, tokens, cost, errors), and asynchronous feedback capture for evaluation.

Cross-cutting: secrets management, private networking to providers, multi-region failover, kill switches, and change management for prompts and models.

## Likely follow-ups

- Where would you put the guardrails so streaming still feels fast?
- Which of these components would you make shared platform services, and which would you leave to application teams?

---

[← Q0099](../../batch_01_llm_fundamentals/0099_continue_generation_past_the_output_limit/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md)
