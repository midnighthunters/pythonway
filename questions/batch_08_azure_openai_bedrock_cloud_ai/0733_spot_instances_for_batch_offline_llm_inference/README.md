# Q0733 · Spot instances for batch offline LLM inference

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | Elastic Compute | Medium |

## Question

How do enterprise data platforms leverage cloud Spot instances (AWS Spot / Azure Spot VMs) for batch LLM evaluation and offline RAG ingestion at 70% cost reduction?

## Answer

Cloud providers sell surplus compute capacity as Spot instances at up to 70%–90% discounts compared to on-demand pricing.

Tradeoff & The Eviction Mechanism:
- Cloud providers can reclaim Spot instances with a 30-second (Azure) or 2-minute (AWS) eviction notice when demand spikes.

Architecture for Spot Batch Inference:
1. Workload Suitability:
   - Perfect for offline, asynchronous workloads: nightly trade break batch analysis, RAG embedding generation, model evaluation benchmarking, synthetic data generation.
2. Stateless Worker Architecture:
   - Workers pull task IDs from a durable queue (AWS SQS / Azure Service Bus) with visibility timeouts.
   - If a Spot VM is terminated mid-task, the visibility timeout expires, and another worker automatically claims the task.
3. Checkpoint Resumption:
   - Results are committed to persistent object storage (S3 / Azure Blob) after every small batch.

## Likely follow-ups

- Why are Spot instances unsuitable for real-time interactive trading assistants?
- How does AWS EC2 Fleet mix Spot and On-Demand instances to guarantee baseline capacity?

---

[← Q0732](../../batch_08_azure_openai_bedrock_cloud_ai/0732_implementing_a_queue_depth_autoscaling_simulator_in_python/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0734 →](../../batch_08_azure_openai_bedrock_cloud_ai/0734_checkpoint_resumption_for_long_running_batch_inference/README.md)
