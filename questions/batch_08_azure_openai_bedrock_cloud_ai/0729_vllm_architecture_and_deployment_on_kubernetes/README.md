# Q0729 · vLLM architecture and deployment on Kubernetes

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | GPU Serving | Medium |

## Question

Describe the architecture of vLLM and how an enterprise AI team deploys it as a scalable microservice on Kubernetes with GPU resource limits.

## Answer

vLLM is a high-throughput, memory-efficient open-source LLM serving engine.

Key Architectural Components:
1. PagedAttention: Eliminates memory fragmentation in the KV cache.
2. Continuous Batching: Iteration-level scheduling maximizing GPU occupancy.
3. Asynchronous LLM Engine: Non-blocking Python engine using Ray or multiprocessing for distributed tensor parallelism across multiple GPUs.
4. OpenAI-Compatible API Server: Exposes `/v1/chat/completions` and `/v1/completions` endpoints with native SSE streaming.

Kubernetes Deployment Spec Highlights:
- Resources: `nvidia.com/gpu: 8` for 8x H100 SXM5 GPUs with NVLink.
- Shared Memory: Mount `emptyDir` with `medium: Memory` to `/dev/shm` (critical for PyTorch multi-GPU IPC).
- Probes: Readiness probe targeting `/health` to ensure model weights are fully loaded into VRAM before receiving live traffic.

## Likely follow-ups

- How does Tensor Parallelism (TP) divide model weights across 8 GPUs on a single node?
- When should Pipeline Parallelism (PP) be used in addition to Tensor Parallelism?

---

[← Q0728](../../batch_08_azure_openai_bedrock_cloud_ai/0728_gpu_quantization_fp8_awq_gptq_int4_for_enterprise_inference/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0730 →](../../batch_08_azure_openai_bedrock_cloud_ai/0730_tensorrt_llm_optimization_for_nvidia_gpus/README.md)
