# Q0776 · Validating Bedrock IAM policy statements in Python

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | AWS Bedrock | Medium |

## Question

Write Python code that inspects an IAM policy dictionary and validates that only permitted `InvokeModel` actions and European regional resources are present.

## Answer

```python
from typing import Any, Dict, List


class BedrockPolicyValidator:
    ALLOWED_ACTIONS = {"bedrock:InvokeModel", "bedrock:InvokeModelWithResponseStream"}

    @classmethod
    def validate_policy(cls, policy_doc: Dict[str, Any]) -> bool:
        for stmt in policy_doc.get("Statement", []):
            if stmt.get("Effect") == "Allow":
                actions = stmt.get("Action", [])
                if isinstance(actions, str):
                    actions = [actions]
                if not all(a in cls.ALLOWED_ACTIONS for a in actions):
                    return False

                resources = stmt.get("Resource", [])
                if isinstance(resources, str):
                    resources = [resources]
                # Enforce EU resource boundaries
                for r in resources:
                    if not ("eu-" in r or "inference-profile/eu." in r):
                        return False
        return True


valid_policy = {
    "Statement": [
        {
            "Effect": "Allow",
            "Action": ["bedrock:InvokeModel", "bedrock:InvokeModelWithResponseStream"],
            "Resource": ["arn:aws:bedrock:eu-central-1::foundation-model/anthropic.claude-3-5-sonnet"],
        }
    ]
}

assert BedrockPolicyValidator.validate_policy(valid_policy) is True

bad_policy = {
    "Statement": [
        {
            "Effect": "Allow",
            "Action": ["bedrock:*"],
            "Resource": ["arn:aws:bedrock:us-east-1::foundation-model/titan"],
        }
    ]
}
assert BedrockPolicyValidator.validate_policy(bad_policy) is False
```

## Likely follow-ups

- How does AWS IAM Access Analyzer statically prove that an IAM policy does not grant external access?
- What are Service Control Policies (SCPs), and how do they enforce cloud-wide AI boundaries?

---

[← Q0775](../../batch_08_azure_openai_bedrock_cloud_ai/0775_iam_policies_for_least_privilege_bedrock_model_access/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0777 →](../../batch_08_azure_openai_bedrock_cloud_ai/0777_bedrock_cloudtrail_event_logging_for_compliance_audits/README.md)
