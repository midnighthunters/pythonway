# Q0775 · IAM policies for least-privilege Bedrock model access

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | AWS Bedrock | Medium |

## Question

Construct an AWS IAM policy enforcing least-privilege access, permitting an application to invoke only Claude 3.5 Sonnet in European inference profiles while denying model modification.

## Answer

In enterprise AWS architectures, application roles must never be granted `bedrock:*`. They should be restricted to specific model invocation actions and target ARNs.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowClaudeEUInferenceOnly",
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream"
      ],
      "Resource": [
        "arn:aws:bedrock:eu-central-1::foundation-model/anthropic.claude-3-5-sonnet-*",
        "arn:aws:bedrock:*:*:inference-profile/eu.anthropic.claude-3-5-sonnet-*"
      ]
    },
    {
      "Sid": "DenyModelCustomizationAndAdmin",
      "Effect": "Deny",
      "Action": [
        "bedrock:CreateModelCustomizationJob",
        "bedrock:StopModelCustomizationJob",
        "bedrock:DeleteCustomModel"
      ],
      "Resource": "*"
    }
  ]
}
```

## Likely follow-ups

- Why should IAM policies include both the raw model ARN and the inference-profile ARN?
- How can `aws:PrincipalTag` enforce department-level access control on Bedrock models?

---

[← Q0774](../../batch_08_azure_openai_bedrock_cloud_ai/0774_formatting_bedrock_agent_lambda_response_payloads_in_python/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0776 →](../../batch_08_azure_openai_bedrock_cloud_ai/0776_validating_bedrock_iam_policy_statements_in_python/README.md)
