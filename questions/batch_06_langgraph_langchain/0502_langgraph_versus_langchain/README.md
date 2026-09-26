# Q0502 · LangGraph versus LangChain

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | LangGraph foundations | Easy |

## Question

How do LangChain and LangGraph relate in the 1.x releases, and when do you use each?

## Answer

- LangChain provides the building blocks and a high-level agent API: chat-model interfaces for many providers, messages, tools, prompts, structured output, retrievers, and `create_agent` (a prebuilt tool-calling agent loop with middleware for things like human-in-the-loop, summarisation and PII handling).
- LangGraph is the lower-level runtime: graphs, state, checkpointing, interrupts and streaming. LangChain 1.x agents are built on it, so they inherit persistence and streaming.

Use `create_agent` when a standard tool-calling loop fits and middleware covers your customisation. Drop to LangGraph when you need a custom control flow: multi-step workflows with agentic nodes, custom approval points, parallel branches, multi-agent topologies, or strict deterministic sections. Many production systems mix them: a LangGraph workflow whose nodes include `create_agent` agents as subgraphs.

## Likely follow-ups

- What customisation would push you from `create_agent` to a hand-built graph?

---

[← Q0501](../../batch_06_langgraph_langchain/0501_what_langgraph_is_and_why_use_it/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0503 →](../../batch_06_langgraph_langchain/0503_state_nodes_and_edges/README.md)
