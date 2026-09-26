# Q0397 · Evaluating an MCP tool server

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | Agent evaluation | Medium |

## Question

Your team publishes an MCP server that many agents on the platform will use. How do you evaluate it?

## Answer

- Protocol conformance: discovery (`server/discover` in the 2026-07-28 revision), list results (deterministic ordering, cache hints), error codes, schemas valid under JSON Schema 2020-12, and behaviour across the supported protocol versions. Use the official inspector tools and conformance tests.
- Tool usability by models: a set of natural-language tasks run through several agent models, measuring tool-selection accuracy, argument validity, and task success. Poor names and descriptions show up as mis-selection, so iterate on them.
- Correctness and robustness: unit and integration tests of each tool, including invalid arguments, pagination, large results and timeouts.
- Security: authorisation per request (OAuth resource-server behaviour, audience and resource indicators), least privilege, input validation, prompt-injection resistance of tool outputs (returning untrusted content marked as such), and rate limits.
- Performance: latency percentiles, concurrency, and cost.
- Observability: trace-context propagation, structured errors, and usage metrics per client.

## Likely follow-ups

- How would you detect that a tool description change made models pick the wrong tool?

---

[← Q0396](../../batch_04_llm_evaluation_observability/0396_evaluating_code_fix_agents/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0398 →](../../batch_04_llm_evaluation_observability/0398_evaluating_across_languages/README.md)
