# Q0806 · Testing GenAI endpoints with FastAPI TestClient and mocking

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | FastAPI foundations | Medium |

## Question

Write Python code using FastAPI's `TestClient` and `unittest.mock` to unit-test a chat route by mocking the underlying LLM call without network access.

## Answer

```python
from unittest.mock import MagicMock
from fastapi import FastAPI
from fastapi.testclient import TestClient


class LLMService:
    def generate(self, prompt: str) -> str:
        # Real implementation calls Azure OpenAI / Bedrock
        raise NotImplementedError("Real network call disabled in unit tests")


app = FastAPI()
llm_service = LLMService()


@app.post("/chat")
def chat_endpoint(payload: dict):
    reply = llm_service.generate(payload["prompt"])
    return {"reply": reply}


# Unit Test with Mock
mock_llm = MagicMock()
mock_llm.generate.return_value = "Mocked market analysis response."

# Patch instance on app module
llm_service.generate = mock_llm.generate

client = TestClient(app)
response = client.post("/chat", json={"prompt": "Summarize market"})

assert response.status_code == 200
assert response.json()["reply"] == "Mocked market analysis response."
mock_llm.generate.assert_called_once_with("Summarize market")
```

## Likely follow-ups

- How does `pytest.fixture` structure reusable mock fixtures across a test suite?
- How do you mock asynchronous streaming generators in FastAPI tests?

---

[← Q0805](../../batch_09_genai_services_fastapi/0805_global_exception_handler_for_model_provider_errors/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0807 →](../../batch_09_genai_services_fastapi/0807_server_sent_events_streaming_with_streamingresponse/README.md)
