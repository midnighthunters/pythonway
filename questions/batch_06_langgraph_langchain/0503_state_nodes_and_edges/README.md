# Q0503 · State, nodes and edges

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | LangGraph foundations | Easy |

## Question

Explain LangGraph's core concepts (state, reducers, nodes, edges, supersteps) in a few sentences each.

## Answer

- State: a typed schema (TypedDict, dataclass or Pydantic model) shared by all nodes. It is the single source of truth for a run and is what gets checkpointed.
- Reducers: per-key functions that decide how updates merge into the state. Without one, a node's value overwrites the key. With `Annotated[list, operator.add]`, updates are appended. `add_messages` merges messages by id.
- Nodes: functions (sync or async) that receive the state (plus optional config, runtime context and store) and return a partial update. They can also return a `Command` to update and route in one step.
- Edges: normal edges (always go A to B), conditional edges (a function picks the next node or nodes), and the `START` and `END` entry and exit points.
- Supersteps: execution proceeds in discrete steps, and nodes scheduled together run in parallel within one step. A checkpoint is saved after each superstep, which is what makes resume and time travel work.

## Likely follow-ups

- Why do parallel nodes that write the same key need a reducer?

---

[← Q0502](../../batch_06_langgraph_langchain/0502_langgraph_versus_langchain/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0504 →](../../batch_06_langgraph_langchain/0504_your_first_stategraph/README.md)
