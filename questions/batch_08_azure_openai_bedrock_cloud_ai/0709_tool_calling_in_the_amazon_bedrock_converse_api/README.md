# Q0709 · Tool calling in the Amazon Bedrock Converse API

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | AWS Bedrock | Medium |

## Question

Write Python code that defines a tool configuration for the Amazon Bedrock Converse API and extracts tool use requests from a simulated model response.

## Answer

In the Bedrock Converse API, tool calling is configured via the `toolConfig` parameter:
- `tools`: A list of tool definitions, each having a `toolSpec` containing `name`, `description`, and `inputSchema` with a JSON Schema `json` object.
- The model responds with `stopReason: "tool_use"` and a content block of type `toolUse` containing `toolUseId`, `name`, and `input`.

```python
from typing import Any, Dict, List, Optional


class BedrockToolHandler:
    @staticmethod
    def make_tool_spec(name: str, description: str, properties: Dict[str, Any], required: List[str]) -> Dict[str, Any]:
        return {
            "toolSpec": {
                "name": name,
                "description": description,
                "inputSchema": {
                    "json": {
                        "type": "object",
                        "properties": properties,
                        "required": required,
                    }
                },
            }
        }

    @staticmethod
    def extract_tool_calls(response_output: Dict[str, Any]) -> List[Dict[str, Any]]:
        message = response_output.get("message", {})
        calls = []
        for block in message.get("content", []):
            if "toolUse" in block:
                tu = block["toolUse"]
                calls.append({"id": tu["toolUseId"], "name": tu["name"], "args": tu["input"]})
        return calls


spec = BedrockToolHandler.make_tool_spec(
    name="get_fx_rate",
    description="Fetches spot FX rate",
    properties={"pair": {"type": "string"}},
    required=["pair"],
)
assert spec["toolSpec"]["name"] == "get_fx_rate"

mock_response = {
    "stopReason": "tool_use",
    "message": {
        "role": "assistant",
        "content": [
            {"text": "Let me check the live rate."},
            {"toolUse": {"toolUseId": "call_123", "name": "get_fx_rate", "input": {"pair": "EURUSD"}}},
        ],
    },
}

extracted = BedrockToolHandler.extract_tool_calls(mock_response)
assert len(extracted) == 1
assert extracted[0]["name"] == "get_fx_rate"
assert extracted[0]["args"]["pair"] == "EURUSD"
```

## Likely follow-ups

- How does the application send the tool execution result back to the Converse API in the next turn?
- Can multiple tool calls be returned in a single Converse response?

---

[← Q0708](../../batch_08_azure_openai_bedrock_cloud_ai/0708_amazon_bedrock_converse_api_unified_abstraction/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0710 →](../../batch_08_azure_openai_bedrock_cloud_ai/0710_amazon_bedrock_cross_region_inference/README.md)
