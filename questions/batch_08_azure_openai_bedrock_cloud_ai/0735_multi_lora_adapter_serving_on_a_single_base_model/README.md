# Q0735 · Multi-LoRA adapter serving on a single base model

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | Elastic Compute | Hard |

## Question

What is Multi-LoRA serving, and how does it allow a single GPU cluster to host dozens of fine-tuned domain models concurrently?

## Answer

The Enterprise Challenge:
Different bank desks require specialized fine-tuned models: Credit Risk, Legal Contracts, FX Trading, Wealth Advisory. Deploying separate 70B parameter models for each desk would require dozens of expensive GPU clusters.

Multi-LoRA Solution:
1. Shared Base Model:
   - A single base model (e.g. Llama 3 70B in FP8) is loaded once into GPU VRAM (occupying ~35 GB).
2. Lightweight LoRA Adapters:
   - Each domain desk trains low-rank adapter weights (rank $r=8$ or $16$), which occupy only 50 MB to 200 MB per adapter.
   - Dozens of adapters are stored in CPU RAM or SSD storage.
3. Dynamic In-Flight Swapping:
   - Frameworks like vLLM and S-LoRA dynamically load the requested adapter weights into the GPU Tensor Core calculation for specific sequences within a continuous batch.
   - Sequence A uses the `legal_adapter`, while Sequence B in the same batch uses the `credit_adapter`.

## Likely follow-ups

- What latency overhead does switching LoRA adapters introduce per batch iteration?
- How does S-LoRA manage adapter memory paging in GPU VRAM?

---

[← Q0734](../../batch_08_azure_openai_bedrock_cloud_ai/0734_checkpoint_resumption_for_long_running_batch_inference/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0736 →](../../batch_08_azure_openai_bedrock_cloud_ai/0736_implementing_a_multi_lora_adapter_router_in_python/README.md)
