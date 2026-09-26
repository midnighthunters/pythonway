# Q0769 · Bedrock Guardrails contextual grounding evaluation

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | AWS Bedrock | Medium |

## Question

How does Amazon Bedrock Guardrails evaluate Contextual Grounding to eliminate hallucinations in RAG applications?

## Answer

Contextual Grounding in Bedrock Guardrails specifically combats hallucinations and off-grounding answers in RAG architectures.

Two Scoring Dimensions:
1. Grounding Score (Faithfulness):
   - Measures whether claims made in the model's generated answer are statistically grounded in and supported by the retrieved reference source passages.
   - Threshold range: 0.0 to 1.0 (default recommendation: block if score < 0.75).
2. Relevance Score (Relevance to Query):
   - Evaluates whether the generated response directly answers the user's specific query rather than offering unrelated grounded facts.

Operation:
- If an agent retrieves 3 policy chunks and synthesizes an answer containing an invented regulatory rule, the Grounding filter detects that the claim lacks source support.
- Action: Intercepts the response before transmission to the user, returning a configured standard message: `"The requested information is not supported by the reference documents."`

## Likely follow-ups

- How does contextual grounding differ from traditional LLM-as-a-judge faithfulness metrics?
- What latency overhead does contextual grounding filtering add to the response stream?

---

[← Q0768](../../batch_08_azure_openai_bedrock_cloud_ai/0768_custom_model_import_in_amazon_bedrock/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0770 →](../../batch_08_azure_openai_bedrock_cloud_ai/0770_evaluating_hallucination_scores_against_ground_truth/README.md)
