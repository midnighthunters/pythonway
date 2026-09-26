# Q0659 · A2A Server-Sent Events (SSE) streaming of task progress

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | A2A protocol | Medium |

## Question

Explain how A2A uses Server-Sent Events (SSE) for real-time task progress streaming. What event types are standard in A2A streaming?

## Answer

Clients connect to `GET /tasks/{id}/events` to receive real-time updates as an agent executes.

Standard A2A Event Types:
1. `status_change`: Emitted when the task transitions between states (`submitted` -> `working` -> `completed`).
2. `part_stream`: Emitted for token-by-token or chunk-by-chunk streaming of a `TextPart` or `DataPart`.
3. `part_complete`: Emitted when a specific output part is fully produced.
4. `heartbeat`: Periodic keep-alive event to prevent corporate proxy connection drops.
5. `error`: Emitted when an operational or model failure occurs.

SSE Frame Format:
```
event: status_change
data: {"task_id": "tsk-1", "status": "working", "timestamp": "2026-09-26T16:00:00Z"}

event: part_stream
data: {"task_id": "tsk-1", "index": 0, "delta": "Analyzing portfolio holdings..."}

event: part_complete
data: {"task_id": "tsk-1", "index": 0, "part": {"type": "text", "text": "Analyzing portfolio holdings... Done."}}
```

## Likely follow-ups

- How does the client reconnect without missing events if the network drops?
- What is the difference between A2A SSE event streaming and raw OpenAI LLM token streaming?

---

[← Q0658](../../batch_07_mcp_a2a_skills_assistants/0658_handling_the_needs_input_state_in_a2a_tasks/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0660 →](../../batch_07_mcp_a2a_skills_assistants/0660_parsing_a2a_streaming_event_frames_in_python/README.md)
