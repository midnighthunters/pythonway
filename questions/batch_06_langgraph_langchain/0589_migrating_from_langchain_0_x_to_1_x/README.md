# Q0589 · Migrating from LangChain 0.x to 1.x

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | Migration | Medium |

## Question

What were the big changes between LangChain 0.x and 1.x, and how would you plan a migration for a large internal codebase?

## Answer

Big changes (at a high level):
- A slimmer core `langchain` package focused on agents (`create_agent`, middleware), with legacy chains and many older abstractions moved to `langchain-classic` (or deprecated).
- Agents run on LangGraph, and LangGraph reached 1.x with a stable runtime API.
- Standardised message content blocks (reasoning, citations, multimodal) across providers.
- Continued use of provider integration packages (`langchain-openai`, `langchain-aws` and others), and the removal of long-deprecated APIs.

Migration plan:
1. Inventory usage: legacy chains (`LLMChain`, `RetrievalQA`), old agents (`AgentExecutor`), memory classes and callbacks.
2. Install with a pinned `langchain-classic` as a bridge, so the code keeps working while you port.
3. Replace legacy chains with LCEL or small LangGraph graphs, and agents with `create_agent` or custom graphs. Move memory to checkpointers and the Store.
4. Test with fake models and the evaluation suites at each step. Watch message-format and tool-call differences.
5. Roll out service by service behind flags, and pin versions in lockfiles, with dependency and security review.

## Likely follow-ups

- Why is a temporary compatibility package useful in large migrations?

---

[← Q0588](../../batch_06_langgraph_langchain/0588_migrating_from_create_react_agent_to_create_agent/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0590 →](../../batch_06_langgraph_langchain/0590_state_design_anti_patterns/README.md)
