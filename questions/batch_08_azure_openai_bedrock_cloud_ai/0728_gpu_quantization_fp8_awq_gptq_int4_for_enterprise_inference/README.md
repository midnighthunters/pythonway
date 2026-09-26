# Q0728 · GPU quantization: FP8, AWQ, GPTQ, INT4 for enterprise inference

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | GPU Serving | Medium |

## Question

Compare modern GPU quantization formats (FP8, AWQ, GPTQ, INT4). What are the tradeoffs between memory footprint, latency, and perplexity degradation?

## Answer

Quantization reduces the precision of model weights and activations to fit larger models on fewer GPUs and increase memory-bandwidth throughput:

1. FP8 (8-bit Floating Point - E4M3 & E5M2):
   - Native hardware acceleration on NVIDIA Ada Lovelace, Hopper (H100), and Blackwell.
   - Near-zero perplexity loss compared to FP16. 2x speedup in matrix multiplication; cuts VRAM in half.
   - Gold standard for enterprise serving of Llama 3 70B and DeepSeek models.
2. AWQ (Activation-aware Weight Quantization - INT4):
   - Recognizes that not all weights are equally important: protects the top 1% of salient weights that correspond to large activation outliers.
   - Quantizes remaining weights to INT4. Excellent retention of reasoning and coding capabilities.
3. GPTQ (Generalized Post-Training Quantization - INT4):
   - One-shot layer-by-layer second-order error minimization. Fast execution on older Ampere (A100) GPUs.
4. Perplexity Tradeoffs:
   - Math, code, and financial calculation reasoning degrade noticeably at pure INT4 without activation protection.
   - Recommendation: Use FP8 on Hopper/Blackwell; AWQ INT4 on memory-constrained A100 clusters.

## Likely follow-ups

- What is the difference between weight-only quantization and weight-activation (W8A8 / W4A4) quantization?
- Why do activation outliers cause severe precision collapse in naive INT8 quantization?

---

[← Q0727](../../batch_08_azure_openai_bedrock_cloud_ai/0727_simulating_pagedattention_block_table_allocation_in_python/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0729 →](../../batch_08_azure_openai_bedrock_cloud_ai/0729_vllm_architecture_and_deployment_on_kubernetes/README.md)
