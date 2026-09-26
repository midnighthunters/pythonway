# Q0777 · Bedrock CloudTrail event logging for compliance audits

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | AWS Bedrock | Medium |

## Question

What audit events does AWS CloudTrail record for Amazon Bedrock invocations, and what fields are required for financial regulatory reporting?

## Answer

Under FINRA, SEC Rule 17a-4, and PRA SS1/23, all interactions with AI systems must be auditable.

CloudTrail Audit Fields for Bedrock:
1. `eventName`: `InvokeModel`, `InvokeModelWithResponseStream`, `CreateKnowledgeBase`, `UpdateAgent`.
2. `userIdentity`: Detailed IAM principal (User ARN, AssumedRole, Session Name, federated corporate identity).
3. `eventTime`: UTC timestamp of the invocation.
4. `requestParameters`: Model ID, inference profile ARN, guardrail ID, and guardrail version.
5. `sourceIPAddress` & `userAgent`: Client source IP and calling SDK/application identity.
6. `responseElements`: HTTP status code, request ID.
7. Data Protection: Prompt and completion texts are NOT logged in standard CloudTrail events by default, preserving privacy while proving that the invocation occurred.

## Likely follow-ups

- How does Amazon Bedrock Model Invocation Logging export full prompt/completion logs to S3 when explicitly enabled?
- How can S3 Object Lock enforce Write-Once-Read-Many (WORM) compliance on model audit logs?

---

[← Q0776](../../batch_08_azure_openai_bedrock_cloud_ai/0776_validating_bedrock_iam_policy_statements_in_python/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0778 →](../../batch_08_azure_openai_bedrock_cloud_ai/0778_parsing_cloudtrail_bedrock_event_logs_in_python/README.md)
