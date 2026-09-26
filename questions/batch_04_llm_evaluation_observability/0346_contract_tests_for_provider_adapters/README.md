# Q0346 · Contract tests for provider adapters

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | Testing | Medium |

## Question

A model-agnostic platform maps different provider responses into one canonical result. Write two fake provider adapters (an OpenAI-style one and a Bedrock Converse-style one) and a shared contract test that both must pass.

## Answer

```python
from dataclasses import dataclass
from typing import Literal

Finish = Literal["stop", "length", "tool_call", "content_filter"]


@dataclass(frozen=True)
class ChatResult:
    text: str
    input_tokens: int
    output_tokens: int
    finish: Finish


def from_openai_style(resp: dict) -> ChatResult:
    choice = resp["choices"][0]
    mapping = {"stop": "stop", "length": "length", "tool_calls": "tool_call", "content_filter": "content_filter"}
    return ChatResult(choice["message"].get("content") or "", resp["usage"]["prompt_tokens"],
                      resp["usage"]["completion_tokens"], mapping[choice["finish_reason"]])


def from_converse_style(resp: dict) -> ChatResult:
    blocks = resp["output"]["message"]["content"]
    text = "".join(b.get("text", "") for b in blocks)
    mapping = {"end_turn": "stop", "stop_sequence": "stop", "max_tokens": "length", "tool_use": "tool_call",
               "guardrail_intervened": "content_filter", "content_filtered": "content_filter"}
    return ChatResult(text, resp["usage"]["inputTokens"], resp["usage"]["outputTokens"], mapping[resp["stopReason"]])


def contract(result: ChatResult) -> None:
    assert isinstance(result.text, str)
    assert result.input_tokens >= 0 and result.output_tokens >= 0
    assert result.finish in ("stop", "length", "tool_call", "content_filter")


oa = {"choices": [{"message": {"content": "Hi"}, "finish_reason": "length"}],
      "usage": {"prompt_tokens": 12, "completion_tokens": 3}}
cv = {"output": {"message": {"content": [{"text": "Hi"}]}}, "stopReason": "max_tokens",
      "usage": {"inputTokens": 12, "outputTokens": 3}}
a, b = from_openai_style(oa), from_converse_style(cv)
for r in (a, b):
    contract(r)
assert a == b == ChatResult("Hi", 12, 3, "length")
```

Callers see one finish vocabulary regardless of provider, so "truncated output" is handled once. Run the same contract suite against recorded real responses from each provider, and re-run it when SDKs or APIs change.

## Likely follow-ups

- What canonical fields would you add for tool calls and reasoning tokens?

---

[← Q0345](../../batch_04_llm_evaluation_observability/0345_pytest_fixtures_for_llm_applications/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0347 →](../../batch_04_llm_evaluation_observability/0347_test_streaming_handlers_against_arbitrary_chunking/README.md)
