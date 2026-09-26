# Q0731 · Autoscaling inference pods with KEDA based on queue depth

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | Elastic Compute | Hard |

## Question

Why is CPU/memory-based autoscaling ineffective for LLM inference pods, and how does Kubernetes Event-driven Autoscaling (KEDA) scale based on queue depth?

## Answer

Why Standard HPA Fails for LLMs:
- LLM inference pods allocate 95% of GPU VRAM at startup for model weights and the KV cache. Memory utilization is permanently at ~95% regardless of whether the pod is idle or actively processing requests.
- CPU utilization is negligible because computation occurs on the GPU.
- Result: Standard CPU/Memory Horizontal Pod Autoscaler (HPA) cannot detect traffic spikes.

KEDA Solution:
- KEDA queries external metrics: active request queue depth on the AI gateway (or Prometheus `vllm:num_requests_waiting` metric).
- If pending requests in the queue exceed the target threshold (e.g. 10 waiting requests per pod), KEDA triggers pod scale-out.
- When the queue drains to 0, KEDA scales pods down after a stabilization cooldown window.

## Likely follow-ups

- Why must scale-down cooldown windows be generous (e.g. 5–10 minutes) for GPU workloads?
- How does cluster autoscaler provision underlying cloud GPU VM instances (e.g. Azure NDv5 or AWS p5) when pods scale out?

---

[← Q0730](../../batch_08_azure_openai_bedrock_cloud_ai/0730_tensorrt_llm_optimization_for_nvidia_gpus/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0732 →](../../batch_08_azure_openai_bedrock_cloud_ai/0732_implementing_a_queue_depth_autoscaling_simulator_in_python/README.md)
