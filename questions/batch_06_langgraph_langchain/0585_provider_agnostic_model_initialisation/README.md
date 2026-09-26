# Q0585 · Provider-agnostic model initialisation

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | Model-agnostic design | Medium |

## Question

How would you initialise chat models in a way that lets the platform swap providers (Azure OpenAI, Bedrock, self-hosted) without code changes in agents?

## Answer

- Use LangChain's standard chat-model interface everywhere (`invoke`, `stream`, `bind_tools`, `with_structured_output`), so agent code depends only on `BaseChatModel`.
- Create models through a factory: LangChain's `init_chat_model("provider:model", ...)` or your own registry that maps a logical model name ("policy-qa-default") to a concrete provider, deployment, region and parameters from configuration. Agents ask for capabilities, not vendors.
- Route through the platform LLM gateway (an OpenAI-compatible or custom endpoint), so quotas, logging, guardrails and failover are central. The factory then mostly configures base URLs and credentials (Entra ID or IAM based, never keys in code).
- Keep per-model prompt variants and capability flags (tool calling, structured output, vision, context size) in the registry, and test each supported model with the contract and evaluation suites.
- Make the model choice configurable per run (through the config or context) for A/B tests and fallbacks.

## Likely follow-ups

- What breaks when you swap models even with a common interface?

---

[← Q0584](../../batch_06_langgraph_langchain/0584_read_configurable_values_inside_nodes/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0586 →](../../batch_06_langgraph_langchain/0586_using_mcp_tools_in_langgraph/README.md)
