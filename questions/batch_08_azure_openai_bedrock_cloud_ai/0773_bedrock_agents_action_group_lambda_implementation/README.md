# Q0773 · Bedrock Agents action group Lambda implementation

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | AWS Bedrock | Medium |

## Question

Describe the anatomy of an AWS Lambda function handling an Amazon Bedrock Agent Action Group request, including payload parsing and response serialization.

## Answer

When an agent invokes an Action Group, Bedrock dispatches an event to the configured Lambda function:

Event Payload Structure:
- `actionGroup`: Name of the action group.
- `apiPath`: The matched OpenAPI path (e.g. `/accounts/{id}/balance`).
- `httpMethod`: `GET`, `POST`, etc.
- `parameters`: List of parameter objects (`{"name": "id", "type": "string", "value": "123"}`).
- `requestBody`: JSON body content if applicable.

Response Contract:
The Lambda must return an exact JSON schema containing `messageVersion: "1.0"` and a `response` object containing `actionGroup`, `apiPath`, `httpMethod`, `httpStatusCode`, and `responseBody`.

## Likely follow-ups

- How does the Lambda communicate business execution errors back to the Bedrock Agent?
- What IAM execution role permissions does the Lambda require?

---

[← Q0772](../../batch_08_azure_openai_bedrock_cloud_ai/0772_reciprocal_rank_fusion_for_bedrock_knowledge_bases/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0774 →](../../batch_08_azure_openai_bedrock_cloud_ai/0774_formatting_bedrock_agent_lambda_response_payloads_in_python/README.md)
