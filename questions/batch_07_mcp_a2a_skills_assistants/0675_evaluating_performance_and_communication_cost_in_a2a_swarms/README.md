# Q0675 · Evaluating performance and communication cost in A2A swarms

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | A2A orchestration | Medium |

## Question

How do you measure and optimize the communication overhead (tokens, latency, cost) in an A2A multi-agent swarm?

## Answer

In multi-agent systems, agents exchanging verbose conversational messages incur quadratic communication overhead.

Optimization techniques:
1. Structured Data vs Free Text: Enforce `DataPart` (JSON) exchanges rather than conversational dialogue between worker agents.
2. Summary Propagation: When worker agents complete tasks, pass executive summaries rather than entire execution transcripts.
3. Message Filtering: Gate peer-to-peer broadcasts through relevance filters.
4. Token & Cost Metering: Track prompt/completion tokens consumed per agent in the trace context.

Metrics to track:
- Messages Per Task: Ratio of total A2A messages to resolved user tasks.
- Token Amplification Factor: Total tokens consumed across all sub-agents divided by the initial user prompt tokens.
- P99 End-to-End Latency: Wall-clock time from task submission to final result.

## Likely follow-ups

- What is the risk of "infinite agent gossip" in unconstrained swarms?
- How does capping max task delegation hops control cost?

---

[← Q0674](../../batch_07_mcp_a2a_skills_assistants/0674_tracing_multi_agent_a2a_message_chains_with_correlation_ids/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0676 →](../../batch_07_mcp_a2a_skills_assistants/0676_what_is_an_agent_skill_and_how_does_it_differ_from_a_tool/README.md)
