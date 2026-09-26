# Q0581 · Message types and content blocks

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | LangChain | Medium |

## Question

Describe LangChain's message types and the content they can carry, and why a standard representation matters on a model-agnostic platform.

## Answer

- `SystemMessage`: instructions from the application or operator.
- `HumanMessage`: user input: text, or multimodal content blocks (images, files, audio).
- `AIMessage`: model output, with text content, `tool_calls` (structured), `usage_metadata` (input and output tokens), `response_metadata` (finish reason, model name), and in newer versions standardised content blocks for reasoning, citations and server-side tool results. `AIMessageChunk` is the streaming fragment type, and chunks can be added together.
- `ToolMessage`: a tool result tied to a `tool_call_id`, with a status (success or error) and optional artifacts not sent to the model.
- `RemoveMessage`: a state-management instruction to delete by id (LangGraph).

Why it matters: each provider (Azure OpenAI, Bedrock Converse, others) has different wire formats for roles, tool calls, images and reasoning. Standard messages let you swap models, log usage consistently (`usage_metadata`), and write provider-independent tests. The provider integration packages handle translation.

## Likely follow-ups

- Where would you read the token usage for cost metering?

---

[← Q0580](../../batch_06_langgraph_langchain/0580_the_tool_calling_message_protocol/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0582 →](../../batch_06_langgraph_langchain/0582_fake_chat_models_for_testing/README.md)
