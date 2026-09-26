# Q0753 · Fine-tuning models on Azure OpenAI with custom enterprise datasets

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | Azure OpenAI | Medium |

## Question

When is fine-tuning appropriate versus RAG on Azure OpenAI, and what validation steps must financial datasets pass before fine-tuning?

## Answer

Fine-Tuning vs RAG Decision Matrix:
- RAG: Use when the model needs access to dynamic, up-to-date factual data (policies, live market prices, customer account records) or when citations and source grounding are required.
- Fine-Tuning: Use when the model needs to learn a specialized *style, tone, syntax, or complex structured output format* (e.g. converting natural language into proprietary bank query languages, or strict compliance redaction formats). Fine-tuning does NOT reliably teach new facts.

Dataset Validation Requirements:
1. Training Format: JSONL containing conversational message arrays (`system`, `user`, `assistant`).
2. Data Quality & PII Cleansing: 100% of real customer PII (names, account numbers, social security numbers) must be scrubbed or pseudonymized.
3. Balance & Distribution: Adequate representation across edge cases, avoiding bias towards common classes.
4. Validation Split: A strictly separated hold-out validation set (10%–20%) to measure validation loss and detect catastrophic forgetting of base model reasoning.

## Likely follow-ups

- What is catastrophic forgetting, and how can fine-tuning degrade general reasoning?
- How does Azure OpenAI isolate customer fine-tuned model weights from other tenants?

---

[← Q0752](../../batch_08_azure_openai_bedrock_cloud_ai/0752_asynchronous_file_batch_analysis_pipeline_with_azure_openai/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0754 →](../../batch_08_azure_openai_bedrock_cloud_ai/0754_preparing_jsonl_training_data_for_azure_openai_fine_tuning/README.md)
