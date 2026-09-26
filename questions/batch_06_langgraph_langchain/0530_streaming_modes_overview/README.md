# Q0530 · Streaming modes overview

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | Streaming | Easy |

## Question

What streaming modes does LangGraph offer, and which would you use for a chat UI, a progress panel and debugging?

## Answer

- `values`: the full state after each step. Useful for debugging and simple UIs, but heavy.
- `updates`: only each node's returned update after it runs. Good for progress panels ("retrieved 5 documents", "booked seat").
- `messages`: LLM tokens as they're generated, with metadata (which node or model produced them). This is what a chat UI streams.
- `custom`: arbitrary events a node emits with `get_stream_writer()` (percent complete, tool status). Good for long tools.
- `debug`: detailed execution events for troubleshooting.

You can combine several modes (`stream_mode=["messages", "updates"]`) and receive `(mode, chunk)` tuples. With subgraphs, pass `subgraphs=True` to see events from nested graphs. For a chat front end: `messages` for tokens, plus `updates` or `custom` for status events, sent over SSE.

## Likely follow-ups

- Which mode would leak the most internal data if sent directly to a browser?

---

[← Q0529](../../batch_06_langgraph_langchain/0529_correct_an_agent_with_update_state/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0531 →](../../batch_06_langgraph_langchain/0531_stream_node_updates_to_a_client/README.md)
