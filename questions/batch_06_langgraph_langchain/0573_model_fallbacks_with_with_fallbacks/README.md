# Q0573 · Model fallbacks with with_fallbacks

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | LangChain | Medium |

## Question

Use `with_fallbacks` so a chat model call fails over to a backup model or deployment when the primary raises, and show that with fake models.

## Answer

```python
from langchain_core.language_models.fake_chat_models import FakeListChatModel


class UnavailableModel(FakeListChatModel):
    def _call(self, *args, **kwargs):
        raise TimeoutError("primary deployment timed out")


primary = UnavailableModel(responses=["unused"])
backup = FakeListChatModel(responses=["Answer from the backup deployment."])
resilient = primary.with_fallbacks([backup], exceptions_to_handle=(TimeoutError, ConnectionError))
assert resilient.invoke("London hotel cap?").content == "Answer from the backup deployment."


class BadRequestModel(FakeListChatModel):
    def _call(self, *args, **kwargs):
        raise ValueError("invalid request: content too long")


strict = BadRequestModel(responses=["x"]).with_fallbacks([backup], exceptions_to_handle=(TimeoutError,))
try:
    strict.invoke("hi")
    raise AssertionError
except ValueError:
    pass
```

Restrict `exceptions_to_handle` to availability errors. A bad request (context too long, a content-filter block) would fail on the backup too, or worse, bypass a safety decision. On a platform, fallbacks usually live in the LLM gateway (for example Azure OpenAI deployment A, then deployment B in another region, then a Bedrock model), with prompts compatible across the fallback models.

## Likely follow-ups

- Why shouldn't a content-filter rejection trigger a fallback to another provider?

---

[← Q0572](../../batch_06_langgraph_langchain/0572_error_handling_strategy_in_langgraph/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0574 →](../../batch_06_langgraph_langchain/0574_lcel_basics_composing_runnables/README.md)
