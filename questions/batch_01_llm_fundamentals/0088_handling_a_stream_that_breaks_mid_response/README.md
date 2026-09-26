# Q0088 · Handling a stream that breaks mid-response

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Streaming reliability | Medium |

## Question

A streamed completion disconnects after 60% of the answer. What should the client and the service do?

## Answer

- You can't resume a provider stream from the middle. The in-flight generation is lost, and MCP's 2026-07-28 revision similarly removed SSE resumability, so clients re-issue the request.
- Options:
  1. Retry the whole request (idempotently) and replace the partial text. This is the simplest and correct option for short answers.
  2. Continue: send the partial answer back as an assistant prefix or with "continue from here", then stitch the continuation. It is cheaper for long outputs but risks seams and duplication.
  3. Show the partial answer with an "interrupted, retry?" UI.
- Service side: detect client disconnects and cancel the upstream call (don't keep paying for tokens nobody reads). Log partial usage for billing. Emit a terminal event (`error`, or `done` with `finish_reason`) so clients can tell completion from truncation.
- Tool-using agents: never re-run side-effecting tool calls on retry. Checkpoint agent state (LangGraph checkpointers) so you resume from the last completed step, not from scratch.

## Likely follow-ups

- How does a LangGraph checkpointer change the retry story for a long agent run?

---

[← Q0087](../../batch_01_llm_fundamentals/0087_batch_inference_apis_for_offline_workloads/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0089 →](../../batch_01_llm_fundamentals/0089_explaining_llm_limitations_to_business_stakeholders/README.md)
