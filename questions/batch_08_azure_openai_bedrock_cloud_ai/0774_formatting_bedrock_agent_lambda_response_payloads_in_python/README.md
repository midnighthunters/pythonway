# Q0774 · Formatting Bedrock Agent Lambda response payloads in Python

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | AWS Bedrock | Medium |

## Question

Write Python code that formats a compliant response dictionary for an Amazon Bedrock Agent Action Group Lambda invocation.

## Answer

```python
import json
from typing import Any, Dict


def build_bedrock_agent_response(
    action_group: str,
    api_path: str,
    http_method: str,
    http_status: int,
    body_data: Dict[str, Any],
) -> Dict[str, Any]:
    return {
        "messageVersion": "1.0",
        "response": {
            "actionGroup": action_group,
            "apiPath": api_path,
            "httpMethod": http_method,
            "httpStatusCode": http_status,
            "responseBody": {
                "application/json": {
                    "body": json.dumps(body_data)
                }
            },
        },
    }


res = build_bedrock_agent_response(
    action_group="TradingServiceActionGroup",
    api_path="/trades/check_limit",
    http_method="POST",
    http_status=200,
    body_data={"within_limit": True, "available_usd": 500000.0},
)

assert res["messageVersion"] == "1.0"
assert res["response"]["httpStatusCode"] == 200
parsed_body = json.loads(res["response"]["responseBody"]["application/json"]["body"])
assert parsed_body["within_limit"] is True
```

## Likely follow-ups

- What happens if the `responseBody` exceeds the maximum Bedrock payload size?
- Can binary attachments (e.g. generated PDF reports) be returned from Action Group Lambdas?

---

[← Q0773](../../batch_08_azure_openai_bedrock_cloud_ai/0773_bedrock_agents_action_group_lambda_implementation/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0775 →](../../batch_08_azure_openai_bedrock_cloud_ai/0775_iam_policies_for_least_privilege_bedrock_model_access/README.md)
