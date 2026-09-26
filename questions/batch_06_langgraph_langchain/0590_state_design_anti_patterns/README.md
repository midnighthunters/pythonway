# Q0590 · State design anti-patterns

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | State design | Medium |

## Question

What LangGraph state-design mistakes do you see often, and how do you fix them?

## Answer

- A giant untyped `dict` blob: no reducers and unclear ownership. Use a typed schema with explicit reducers per key.
- Overwrite keys written by parallel nodes: this causes `InvalidUpdateError`, or silent last-write-wins with custom merges. Add reducers, or separate keys per branch.
- Storing huge payloads (full documents, raw API responses, base64 files) in the state: checkpoints bloat and replays slow down. Store references and fetch on demand.
- Secrets or tokens in the state: they get checkpointed, traced and leaked. Pass handles through the runtime context instead.
- Non-serialisable objects (clients, open files, lambdas) in the state: checkpointing fails or is unsafe. Keep them out of the state and inject them.
- Parsing the transcript for control flow (regexes over messages): fragile. Keep structured fields (status, plan, counters).
- Unbounded message growth: add trimming, summarisation and RemoveMessage.
- Duplicate accumulation through subgraphs or retries with `operator.add`: design idempotent reducers (keyed merges) or explicit mapping.
- No schema versioning: plan migrations before the first production deploy.

## Likely follow-ups

- Why are keyed-merge reducers safer than list append for results?

---

[← Q0589](../../batch_06_langgraph_langchain/0589_migrating_from_langchain_0_x_to_1_x/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0591 →](../../batch_06_langgraph_langchain/0591_performance_tuning_for_langgraph_apps/README.md)
