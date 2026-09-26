# Q0559 · TypedDict, dataclass or Pydantic state

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | State design | Easy |

## Question

How do you choose between TypedDict, dataclass and Pydantic models for LangGraph state?

## Answer

- TypedDict: the most common choice. It is lightweight, nodes return plain dicts, it works naturally with reducers via `Annotated`, and has no runtime validation (types are for static checking only).
- Dataclass: attribute access and default values, still light. It is good when you want defaults and a clear structure without validation overhead.
- Pydantic `BaseModel`: runtime validation and coercion of inputs, rich constraints and nice error messages. It suits trust boundaries (inputs from external callers). The cost is overhead, and some subtleties in how node outputs are validated compared with inputs.

Common practice: TypedDict for the internal graph state, Pydantic models for external input and output contracts (FastAPI request bodies, tool arguments, structured LLM outputs), validated explicitly where data enters. Whatever you choose, keep the state JSON-serialisable for checkpointing.

## Likely follow-ups

- Why must state stay JSON-serialisable?

---

[← Q0558](../../batch_06_langgraph_langchain/0558_compile_time_validation_errors/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0560 →](../../batch_06_langgraph_langchain/0560_what_gets_serialised_in_checkpoints/README.md)
