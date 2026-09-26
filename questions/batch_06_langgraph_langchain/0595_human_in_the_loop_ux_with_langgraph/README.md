# Q0595 · Human-in-the-loop UX with LangGraph

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | UX | Medium |

## Question

Design the user experience for approvals in a LangGraph-powered assistant: what the reviewer sees, how decisions flow back, and how to handle delays.

## Answer

- The request card shows exactly what will happen: the tool and its concrete arguments (amount, recipient, email body), the reason and evidence (the agent's summary plus citations), the risk tier, and who requested it. Never show only the agent's paraphrase.
- Decisions: approve, edit (with validated fields), reject with a reason (fed back to the agent), or respond (answer a question). This maps onto an `interrupt()` payload and a `Command(resume=...)` value, or the HITL middleware's decisions.
- Routing: send the approval to the right person (the requester for personal actions, a second approver for four-eyes controls) via the app, email or Teams, with deep links. Queue views for approvers.
- Delays: runs wait durably (checkpointed), with reminders, expiry (auto-reject after N hours, with the user told), and a status visible to the requester ("waiting for Tom's approval").
- Audit: every decision logged with the approver's identity, time, the original and edited arguments, and the trace id.
- Safety: re-validate at resume time (the balance may have changed), and make the resume endpoint authorised and idempotent (a double click can't execute twice).

## Likely follow-ups

- Why re-validate at resume time rather than trusting the state at the time of the interrupt?

---

[← Q0594](../../batch_06_langgraph_langchain/0594_side_effects_and_replays_in_langgraph/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0596 →](../../batch_06_langgraph_langchain/0596_evaluate_a_langgraph_agent/README.md)
