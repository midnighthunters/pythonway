# Q0800 · Comprehensive end-to-end integration test of a multi-cloud AI gateway

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | Multi-Cloud AI Gateways | Hard |

## Question

Write an end-to-end integration test in Python simulating an AI Gateway that validates tenant authentication, checks token budgets, invokes a primary cloud AI endpoint, and logs an audit record.

## Answer

```python
from typing import Any, Dict


class MockCloudEndpoint:
    def complete(self, prompt: str) -> Dict[str, Any]:
        return {
            "text": f"Completed: {prompt}",
            "usage": {"prompt_tokens": 50, "completion_tokens": 20},
        }


class ProductionAIGateway:
    def __init__(self, cloud_endpoint: MockCloudEndpoint, valid_api_keys: set):
        self.endpoint = cloud_endpoint
        self.valid_keys = valid_api_keys
        self.audit_log = []

    def handle_request(self, auth_header: str, prompt: str) -> Dict[str, Any]:
        # Step 1: Validate Authentication
        if not auth_header.startswith("Bearer ") or auth_header[7:] not in self.valid_keys:
            return {"status": "error", "code": 401, "message": "Unauthorized"}

        tenant_key = auth_header[7:]

        # Step 2: Invoke Cloud Provider
        res = self.endpoint.complete(prompt)

        # Step 3: Record Audit
        audit_entry = {
            "tenant": tenant_key,
            "prompt": prompt,
            "tokens": res["usage"]["prompt_tokens"] + res["usage"]["completion_tokens"],
        }
        self.audit_log.append(audit_entry)

        return {
            "status": "success",
            "output": res["text"],
            "tokens_used": audit_entry["tokens"],
        }


# End-to-end test execution
cloud = MockCloudEndpoint()
gateway = ProductionAIGateway(cloud, valid_api_keys={"jpmc-app-key-alpha"})

# Unauthorized call
bad_res = gateway.handle_request("Bearer bad-key", "Hello")
assert bad_res["status"] == "error"
assert bad_res["code"] == 401

# Authorized call
good_res = gateway.handle_request("Bearer jpmc-app-key-alpha", "Summarize trade report")
assert good_res["status"] == "success"
assert "Completed: Summarize trade report" in good_res["output"]
assert good_res["tokens_used"] == 70

# Verify audit trail recorded
assert len(gateway.audit_log) == 1
assert gateway.audit_log[0]["tenant"] == "jpmc-app-key-alpha"
assert gateway.audit_log[0]["tokens"] == 70
```

## Likely follow-ups

- How would you structure chaos testing to simulate intermittent cloud network partitions?
- How do contract tests prevent breaking changes when cloud providers update API versions?

---

[← Q0799](../../batch_08_azure_openai_bedrock_cloud_ai/0799_cryptographic_audit_batch_signer_in_python/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md)
