# Q0703 · Azure Entra ID and Managed Identity authentication

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | Azure OpenAI | Medium |

## Question

Why are static API keys prohibited in enterprise cloud AI deployments, and write Python code authenticating with Azure OpenAI using Azure Managed Identity (`DefaultAzureCredential`).

## Answer

Static API keys present severe operational risks: they can be accidentally committed to Git repositories, leaked in log files, shared across developers without accountability, and require disruptive manual key rotations.

Azure Managed Identity links the application's runtime identity directly to its Azure compute resource (VM, AKS pod, Azure Function). The runtime fetches short-lived OAuth 2.0 tokens from Entra ID automatically.

```python
from unittest.mock import MagicMock


class MockAzureTokenProvider:
    def __init__(self, token: str = "mock-jwt-token-12345"):
        self.token = token

    def get_bearer_token(self) -> str:
        # In real code: DefaultAzureCredential().get_token("https://cognitiveservices.azure.com/.default").token
        return self.token


class SecureAzureOpenAIClient:
    def __init__(self, endpoint: str, token_provider: MockAzureTokenProvider):
        self.endpoint = endpoint
        self.token_provider = token_provider

    def build_headers(self) -> dict:
        token = self.token_provider.get_bearer_token()
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }


provider = MockAzureTokenProvider("eyJhbGciOiJSUzI1NiIs...")
client = SecureAzureOpenAIClient("https://jpmc-openai-prod.openai.azure.com", provider)
headers = client.build_headers()

assert "Bearer eyJhbGci" in headers["Authorization"]
assert headers["Content-Type"] == "application/json"
```

## Likely follow-ups

- What Entra ID RBAC role is required to grant inference permissions without granting configuration rights?
- How does workload identity federation work when hosting Python apps in Kubernetes (AKS)?

---

[← Q0702](../../batch_08_azure_openai_bedrock_cloud_ai/0702_azure_openai_deployment_types_standard_global_standard_and/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0704 →](../../batch_08_azure_openai_bedrock_cloud_ai/0704_azure_openai_content_safety_filters_and_custom_blocklists/README.md)
