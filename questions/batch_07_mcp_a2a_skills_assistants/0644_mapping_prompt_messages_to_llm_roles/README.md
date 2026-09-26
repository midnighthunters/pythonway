# Q0644 · Mapping prompt messages to LLM roles

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | MCP prompts | Medium |

## Question

How are MCP prompt message roles (`user`, `assistant`) mapped into LangChain and standard OpenAI chat message formats?

## Answer

MCP prompt messages declare a `role` of either `"user"` or `"assistant"`.

Mapping rules:
- `role: "user"` maps to OpenAI `{"role": "user"}` and LangChain `HumanMessage(content=...)`.
- `role: "assistant"` maps to OpenAI `{"role": "assistant"}` and LangChain `AIMessage(content=...)`.
- System instructions in MCP prompts are typically conveyed either as a `user` message with instructions or mapped to `SystemMessage(content=...)` if supported by client convention.

```python
from typing import Any, Dict, List
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage


def convert_mcp_prompt_to_langchain(mcp_messages: List[Dict[str, Any]]) -> List[BaseMessage]:
    lc_messages: List[BaseMessage] = []
    for msg in mcp_messages:
        role = msg.get("role")
        content_obj = msg.get("content", {})
        text = content_obj.get("text", "")

        if role == "user":
            lc_messages.append(HumanMessage(content=text))
        elif role == "assistant":
            lc_messages.append(AIMessage(content=text))
    return lc_messages


mcp_msgs = [
    {"role": "user", "content": {"type": "text", "text": "What is the policy?"}},
    {"role": "assistant", "content": {"type": "text", "text": "Policy is 100% collateralized."}},
]

converted = convert_mcp_prompt_to_langchain(mcp_msgs)
assert len(converted) == 2
assert isinstance(converted[0], HumanMessage)
assert isinstance(converted[1], AIMessage)
assert converted[1].content == "Policy is 100% collateralized."
```

## Likely follow-ups

- What should a client do if an MCP message contains an unsupported role?
- How are multimodal prompt contents (e.g. attached images) translated to LangChain messages?

---

[← Q0643](../../batch_07_mcp_a2a_skills_assistants/0643_getting_prompt_messages_with_prompts_get_and_arguments/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0645 →](../../batch_07_mcp_a2a_skills_assistants/0645_embedding_resource_content_into_mcp_prompt_messages/README.md)
