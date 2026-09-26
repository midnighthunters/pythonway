# Q0768 · Custom Model Import in Amazon Bedrock

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | AWS Bedrock | Medium |

## Question

What is Custom Model Import (CMI) in Amazon Bedrock, and how does it allow banks to serve proprietary fine-tuned weights serverlessly?

## Answer

Custom Model Import (CMI) allows enterprise organizations to import their own custom foundation models—fine-tuned outside Bedrock (e.g. on internal SageMaker GPU clusters, on-prem H100 clusters, or via Hugging Face)—directly into Amazon Bedrock.

Capabilities & Process:
1. Supported Architectures: Open architectures including Llama, Mistral, and Flan-T5 in safetensors format.
2. S3 Ingestion: Model weights and tokenizer files are uploaded to an encrypted S3 bucket.
3. Automated Serverless Packaging:
   - Bedrock validates weights and deploys the model into a fully managed, serverless inference infrastructure.
4. Unified Access:
   - The imported custom model receives a standard Bedrock model ARN.
   - Applications invoke it using the exact same Converse API, Guardrails, and IAM permission policies as commercial foundation models.

## Likely follow-ups

- What are the pricing mechanics for Custom Model Import compared to on-demand base models?
- How does Bedrock verify the structural integrity of imported model weight tensors?

---

[← Q0767](../../batch_08_azure_openai_bedrock_cloud_ai/0767_provisioned_throughput_cost_vs_on_demand_breakeven/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0769 →](../../batch_08_azure_openai_bedrock_cloud_ai/0769_bedrock_guardrails_contextual_grounding_evaluation/README.md)
