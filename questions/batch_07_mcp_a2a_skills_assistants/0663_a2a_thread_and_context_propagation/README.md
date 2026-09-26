# Q0663 · A2A thread and context propagation

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | A2A protocol | Medium |

## Question

How does the A2A protocol propagate conversation threads, security principals, and distributed tracing headers across deep agent delegation hierarchies?

## Answer

When Agent A delegates to Agent B, which delegates to Agent C, end-to-end tracing and access context must be preserved.

A2A specifies a `context` block in task requests:
1. `thread_id` / `session_id`: Preserves the conversational thread back to the human user.
2. `initiator`: The authenticated human user or system identity (e.g. `user_id: "u123456@jpmc.com"`), enabling downstream agents to check user entitlements.
3. `traceparent` (W3C Trace Context): Distributed tracing header (`version-trace_id-parent_id-flags`) passed across all A2A hops.
4. `delegation_depth`: Integer counter incremented at each hop to detect infinite loops.

```python
from typing import Any, Dict


class A2AContextManager:
    @staticmethod
    def propagate(incoming_context: Dict[str, Any], next_span_id: str) -> Dict[str, Any]:
        depth = incoming_context.get("delegation_depth", 0)
        if depth >= 5:
            raise RecursionError(f"Delegation depth limit exceeded: {depth}")

        return {
            "session_id": incoming_context.get("session_id"),
            "initiator": incoming_context.get("initiator"),
            "traceparent": f"00-{incoming_context.get('trace_id', '123')}-{next_span_id}-01",
            "delegation_depth": depth + 1,
        }


ctx = {"session_id": "sess-1", "initiator": "alice", "trace_id": "abc456", "delegation_depth": 1}
next_ctx = A2AContextManager.propagate(ctx, "span999")

assert next_ctx["delegation_depth"] == 2
assert "span999" in next_ctx["traceparent"]
assert next_ctx["initiator"] == "alice"
```

## Likely follow-ups

- Why must `delegation_depth` have a hard threshold?
- How do security gateways prevent an untrusted agent from spoofing the `initiator` field?

---

[← Q0662](../../batch_07_mcp_a2a_skills_assistants/0662_a2a_task_cancellation_and_compensation/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0664 →](../../batch_07_mcp_a2a_skills_assistants/0664_a2a_task_idempotency_with_client_tokens/README.md)
