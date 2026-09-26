# Q0713 · Amazon Bedrock Agents and AgentCore

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | AWS Bedrock | Medium |

## Question

Describe the architecture of Amazon Bedrock Agents. How do Action Groups and OpenAPI schemas enable autonomous tool execution?

## Answer

Amazon Bedrock Agents orchestrates autonomous multi-step reasoning by combining foundation models with enterprise APIs and data sources.

Components:
1. Orchestrator Loop:
   - Automatically generates a dynamic ReAct (Reason + Act) plan, breaks down user inquiries into sequential steps, and determines tool invocations.
2. Action Groups:
   - Define actions the agent can take. Each action group is defined by:
     - An OpenAPI 3.0 JSON/YAML specification declaring API paths and parameter schemas.
     - An AWS Lambda function that executes the business logic (e.g. querying a DynamoDB table or calling an internal payment service).
3. Knowledge Bases Integration:
   - Directly associates one or more Knowledge Bases to provide grounding context without writing custom retriever code.
4. Memory Retention:
   - Automatically maintains conversational state across user sessions.

## Likely follow-ups

- How does Bedrock Agents handle missing parameters required by an Action Group?
- What are the advantages of Bedrock Agents over custom LangGraph loops in AWS-heavy environments?

---

[← Q0712](../../batch_08_azure_openai_bedrock_cloud_ai/0712_amazon_bedrock_knowledge_bases_and_vector_indexing/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0714 →](../../batch_08_azure_openai_bedrock_cloud_ai/0714_handling_http_429_too_many_requests_with_exponential/README.md)
