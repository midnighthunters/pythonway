# B0010 · Most complex agentic system you have built

| Section | Topic | Difficulty |
|---|---|---|
| Behavioural, Role & JPMorganChase | GenAI experience | Hard |

## Question

Describe the most complex AI or agentic system you have built.

## Answer

Be precise, because interviewers will drill into every layer:

- Goal, and why an agent (multi-step, tool use) rather than a single prompt or a fixed workflow.
- Architecture: framework (e.g. LangGraph StateGraph), state schema, nodes and tools, routing, checkpointer (Postgres), human-in-the-loop interrupts, long-term memory store, models (Azure OpenAI, Bedrock), MCP tools.
- Reliability: step limits, retries with backoff, idempotent tools, timeouts, fallbacks, structured outputs.
- Safety: per-tool permissions, approval before side effects, prompt-injection mitigations, PII handling.
- Evaluation: golden dataset, trajectory and tool-call evaluation, LLM-as-judge calibrated against humans, online feedback.
- Operations: tracing (LangSmith/OpenTelemetry), cost per task, latency budget.
- Results and the lessons you took away.

## Likely follow-ups

- How did you prevent infinite loops?
- How did you evaluate tool-call correctness?
- What failed in production?

---

[← B0009](../../behavioural_questions/0009_biggest_technical_achievement/README.md) · [Behavioural, Role & JPMorganChase index](../README.md) · [All sections](../../README.md) · [B0011 →](../../behavioural_questions/0011_why_are_you_leaving_your_current_role/README.md)
