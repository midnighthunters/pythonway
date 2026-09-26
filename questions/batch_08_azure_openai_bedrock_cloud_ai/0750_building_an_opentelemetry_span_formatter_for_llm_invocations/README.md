# Q0750 · Building an OpenTelemetry span formatter for LLM invocations

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | Cloud AI Gateways | Medium |

## Question

Write Python code that formats a standardized OpenTelemetry GenAI span dictionary from an LLM invocation response.

## Answer

```python
from typing import Any, Dict


class OpenTelemetryGenAIFormatter:
    @staticmethod
    def format_span(
        system: str, model: str, prompt_tokens: int, completion_tokens: int, finish_reason: str, temperature: float
    ) -> Dict[str, Any]:
        return {
            "name": f"chat {model}",
            "attributes": {
                "gen_ai.system": system,
                "gen_ai.request.model": model,
                "gen_ai.request.temperature": temperature,
                "gen_ai.usage.prompt_tokens": prompt_tokens,
                "gen_ai.usage.completion_tokens": completion_tokens,
                "gen_ai.response.finish_reasons": [finish_reason],
            },
        }


span = OpenTelemetryGenAIFormatter.format_span(
    system="azure_openai",
    model="gpt-4o",
    prompt_tokens=512,
    completion_tokens=128,
    finish_reason="stop",
    temperature=0.2,
)

assert span["name"] == "chat gpt-4o"
assert span["attributes"]["gen_ai.system"] == "azure_openai"
assert span["attributes"]["gen_ai.usage.prompt_tokens"] == 512
assert span["attributes"]["gen_ai.response.finish_reasons"] == ["stop"]
```

## Likely follow-ups

- How do you capture time-to-first-token (TTFT) as an OpenTelemetry span event?
- What privacy flags control whether prompt contents are recorded in traces?

---

[← Q0749](../../batch_08_azure_openai_bedrock_cloud_ai/0749_distributed_tracing_with_opentelemetry_genai_semantic/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0751 →](../../batch_08_azure_openai_bedrock_cloud_ai/0751_azure_openai_assistants_api_with_code_interpreter_in_banking/README.md)
