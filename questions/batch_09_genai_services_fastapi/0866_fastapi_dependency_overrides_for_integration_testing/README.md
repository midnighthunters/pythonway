# Q0866 · FastAPI dependency overrides for integration testing without live cloud services

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | FastAPI foundations | Easy |

## Question

Write Python code demonstrating FastAPI dependency overrides (`app.dependency_overrides`) to mock a cloud LLM client during automated test execution.

## Answer

Production microservices rely on FastAPI dependency injection (`Depends`) to inject cloud model clients or database sessions. In CI/CD pipelines, swapping these dependencies with fast, deterministic mocks eliminates cloud costs, API quotas, and network flakiness.

```python
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

app = FastAPI()


class RealAzureOpenAIClient:
    def call_gpt4(self, prompt: str) -> str:
        # In production: makes outbound HTTPS request to Azure endpoint
        raise NotImplementedError("Real cloud service unavailable in CI")


def get_llm_client() -> RealAzureOpenAIClient:
    return RealAzureOpenAIClient()


@app.get("/ask")
def ask(prompt: str, client: RealAzureOpenAIClient = Depends(get_llm_client)):
    return {"answer": client.call_gpt4(prompt)}


# Test suite
class MockLLMClient:
    def call_gpt4(self, prompt: str) -> str:
        return f"Mock answer for: {prompt}"


test_client = TestClient(app)

# Inject mock dependency
app.dependency_overrides[get_llm_client] = lambda: MockLLMClient()

res = test_client.get("/ask?prompt=TestVaR")
assert res.status_code == 200
assert res.json()["answer"] == "Mock answer for: TestVaR"

# Clean up override
app.dependency_overrides.clear()
```

## Likely follow-ups

- Why should you always clear `app.dependency_overrides` after test fixtures complete?
- How does dependency injection simplify testing database transactions with rollback?

---

[← Q0865](../../batch_09_genai_services_fastapi/0865_asynchronous_generator_cancellation_and_memory_cleanup_on/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0867 →](../../batch_09_genai_services_fastapi/0867_sub_applications_and_api_versioning_with_apirouter/README.md)
