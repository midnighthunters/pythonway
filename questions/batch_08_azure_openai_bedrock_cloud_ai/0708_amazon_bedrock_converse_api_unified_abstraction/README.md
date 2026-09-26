# Q0708 · Amazon Bedrock Converse API unified abstraction

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | AWS Bedrock | Medium |

## Question

What is the Amazon Bedrock Converse API, and write Python code that formats a multi-turn conversation with system prompts conforming to the Converse API schema.

## Answer

The Amazon Bedrock Converse API (`converse` and `converse_stream`) provides a unified, consistent message abstraction across all Bedrock foundation models.

Before the Converse API, each provider had proprietary request formats (e.g. Anthropic used `prompt`/`messages` with specific keys; Meta used raw prompt strings; Cohere used different parameter names). The Converse API unifies:
- `modelId`: The model identifier or inference profile ARN.
- `messages`: List of message objects with `role` (`user` or `assistant`) and `content` blocks.
- `system`: List of system prompt text blocks.
- `inferenceConfig`: Standardized `temperature`, `topP`, and `maxTokens`.

```python
from typing import Any, Dict, List


class BedrockConverseFormatter:
    @staticmethod
    def build_request(
        model_id: str,
        system_instruction: str,
        conversation: List[tuple],
        max_tokens: int = 1000,
        temperature: float = 0.2,
    ) -> Dict[str, Any]:
        messages = []
        for role, text in conversation:
            messages.append({"role": role, "content": [{"text": text}]})

        return {
            "modelId": model_id,
            "system": [{"text": system_instruction}],
            "messages": messages,
            "inferenceConfig": {
                "maxTokens": max_tokens,
                "temperature": temperature,
            },
        }


req = BedrockConverseFormatter.build_request(
    model_id="anthropic.claude-3-5-sonnet-20241022-v2:0",
    system_instruction="You are a JPMorganChase credit risk assistant.",
    conversation=[
        ("user", "What is the net gearing ratio for Borrower X?"),
        ("assistant", "Borrower X's net gearing ratio is 1.45x."),
        ("user", "Is this within covenant limits?"),
    ],
    max_tokens=500,
    temperature=0.0,
)

assert req["modelId"] == "anthropic.claude-3-5-sonnet-20241022-v2:0"
assert req["system"][0]["text"] == "You are a JPMorganChase credit risk assistant."
assert len(req["messages"]) == 3
assert req["messages"][0]["role"] == "user"
assert req["inferenceConfig"]["temperature"] == 0.0
```

## Likely follow-ups

- How does the Converse API standardize tool calling across different model families?
- How are image and document attachments formatted within `content` blocks?

---

[← Q0707](../../batch_08_azure_openai_bedrock_cloud_ai/0707_amazon_bedrock_service_overview_and_multi_model_strategy/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0709 →](../../batch_08_azure_openai_bedrock_cloud_ai/0709_tool_calling_in_the_amazon_bedrock_converse_api/README.md)
