# Q0597 · Design a LangGraph trade-break agent

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | System design | Hard |

## Question

Sketch the LangGraph design (state, nodes, edges, interrupts, persistence) for an agent that investigates and remediates trade breaks with analyst approval.

## Answer

State: `break_id`, `break_type`, `evidence` (a keyed-merge reducer), `playbook`, `proposed_action`, `approval` (decision, approver), `status`, `audit` (append reducer), `attempts`.

Nodes:
1. `load_break` (deterministic): fetch the break record.
2. Parallel evidence nodes (`fetch_trade`, `fetch_confirm`, `fetch_ssi`, `fetch_history`), joined by `compare`.
3. `classify` (LLM plus rules): the break type with confidence. Low confidence routes to `escalate`.
4. `select_playbook` (deterministic): tolerance rules decide auto, approval or escalate.
5. `draft_action` (LLM): the amendment request or counterparty email, with the evidence.
6. `approval` (`interrupt()`): the analyst sees the evidence and the concrete action (approve, edit or reject), with four-eyes above the monetary limit.
7. `execute` (idempotent tool calls with a key from the thread and action) then `verify` (re-read the systems to confirm).
8. `escalate` or `close` with a summary.

Edges: conditional routing on confidence, playbook and approval result. A rejection goes back to `draft_action` once, then to `escalate`.

Persistence and operations: a Postgres checkpointer (runs wait hours for analysts), thread id = the break id (idempotent intake from the queue), background runs triggered by queue messages, streaming status to the analyst UI, LangSmith or OpenTelemetry traces, and an evaluation suite of historical breaks with known resolutions.

## Likely follow-ups

- Which nodes must never call an LLM, and why?

---

[← Q0596](../../batch_06_langgraph_langchain/0596_evaluate_a_langgraph_agent/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0598 →](../../batch_06_langgraph_langchain/0598_design_a_langgraph_personal_assistant/README.md)
