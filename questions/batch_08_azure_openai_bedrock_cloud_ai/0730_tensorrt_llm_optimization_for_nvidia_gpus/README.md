# Q0730 · TensorRT-LLM optimization for NVIDIA GPUs

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | GPU Serving | Medium |

## Question

What is NVIDIA TensorRT-LLM, and how does it optimize LLM inference pipelines compared to vanilla PyTorch?

## Answer

TensorRT-LLM is an open-source library that compiles and optimizes LLM architectures specifically for NVIDIA GPU hardware (Ampere, Hopper, Blackwell).

Optimizations:
1. Kernel Fusion:
   - Merges multiple consecutive operations (e.g. LayerNorm, GEMM, GeLU activation, and bias addition) into a single GPU kernel, eliminating round-trips to GPU global memory (HBM).
2. FlashAttention-v2 & FMHA:
   - Highly optimized fused multi-head attention kernels maximizing Tensor Core utilization.
3. In-Flight Batching:
   - Hardware-optimized iteration-level scheduling directly inside C++ runtimes.
4. FP8 Matrix Multiplication:
   - Dedicated Hopper Tensor Core kernels utilizing FP8 transformer engines.
5. Multi-GPU Tensor Parallelism:
   - Optimized NCCL communication primitives that overlap computation with inter-GPU communication over NVLink.

## Likely follow-ups

- What are the operational tradeoffs of compiling TensorRT-LLM engines ahead-of-time (AOT)?
- How does TensorRT-LLM integrate with Triton Inference Server?

---

[← Q0729](../../batch_08_azure_openai_bedrock_cloud_ai/0729_vllm_architecture_and_deployment_on_kubernetes/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0731 →](../../batch_08_azure_openai_bedrock_cloud_ai/0731_autoscaling_inference_pods_with_keda_based_on_queue_depth/README.md)
