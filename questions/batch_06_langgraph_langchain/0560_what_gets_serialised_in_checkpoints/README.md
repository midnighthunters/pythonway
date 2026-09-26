# Q0560 · What gets serialised in checkpoints

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | Persistence | Medium |

## Question

What exactly is stored in a LangGraph checkpoint, and what are the implications for security, size and compatibility?

## Answer

Contents: the values of every state channel (messages, custom fields), pending writes and the next tasks, pending interrupts and their payloads, and metadata (step number, source, parent checkpoint), per thread and checkpoint id. Serialisation uses a serialiser that handles LangChain message objects and common Python types.

Implications:
- Security and privacy: checkpoints contain everything the agent saw (prompts, tool outputs, personal data, possibly secrets if you put them in the state). Encrypt them at rest, restrict access, apply retention, and include them in erasure requests. Never put credentials in the state.
- Size: one checkpoint per superstep, and full message histories replicated across checkpoints. Prune, summarise, store large payloads externally by reference, and set retention.
- Compatibility: renaming or retyping state fields breaks old checkpoints. Version the state and migrate, or keep tolerant readers.
- Custom objects: arbitrary classes may not serialise, or may deserialise unsafely. Prefer JSON-friendly data.

## Likely follow-ups

- Why is deserialising arbitrary pickled objects from checkpoints a security risk?

---

[← Q0559](../../batch_06_langgraph_langchain/0559_typeddict_dataclass_or_pydantic_state/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0561 →](../../batch_06_langgraph_langchain/0561_thread_ids_and_multi_user_safety/README.md)
