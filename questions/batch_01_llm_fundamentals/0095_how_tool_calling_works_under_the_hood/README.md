# Q0095 · How tool calling works under the hood

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Tool use | Medium |

## Question

What actually happens when a model "calls a function"? Describe the loop between your code, the API and the model.

## Answer

1. You send messages plus tool definitions (name, description, JSON Schema of parameters). The provider injects these into the prompt in the format the model was trained on.
2. The model, fine-tuned on tool-use data, decides to emit a structured tool call (special tokens or JSON) instead of or alongside text. The API parses it and returns `tool_calls` with ids and JSON arguments, with `finish_reason` / `stop_reason` indicating tool use.
3. Your code validates the arguments (never trust them blindly), checks permissions, executes the tool, and appends a tool-result message linked by the call id.
4. You call the model again with the result, and it either calls more tools or writes the final answer.

Key points: the model never executes anything. Your code does, so authorisation, validation, timeouts and idempotency are your responsibility. Descriptions and schemas are prompts, so clear names and descriptions measurably improve tool selection. Parallel tool calls can arrive in one turn. Arguments may be invalid JSON or violate the schema, so handle and report errors back to the model.

MCP standardises how tools are discovered and invoked across servers. The model-level loop stays the same.

## Likely follow-ups

- What should you send back to the model when a tool call fails validation?

---

[← Q0094](../../batch_01_llm_fundamentals/0094_why_cosine_similarity_thresholds_don_t_transfer/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0096 →](../../batch_01_llm_fundamentals/0096_parse_tool_calls_from_raw_model_text/README.md)
