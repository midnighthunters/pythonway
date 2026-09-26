# Q0725 · Continuous batching vs static batching in LLM inference engines

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | GPU Serving | Medium |

## Question

Explain the difference between static batching and continuous batching (iteration-level scheduling) in LLM inference engines like vLLM and TensorRT-LLM.

## Answer

Batching is critical for maximizing GPU memory bandwidth and compute utilization.

1. Static Batching:
   - Collects $N$ incoming requests, pads them to the length of the longest prompt, and generates tokens until the longest sequence completes.
   - Flaws: Shorter sequences finish early but idle on the GPU while waiting for the longest sequence to complete ("padding waste"). New requests arriving during generation must wait for the entire batch to complete.
2. Continuous Batching (Iteration-Level Scheduling):
   - Operates at the granularity of individual decoding iterations rather than whole sequences.
   - As soon as sequence $A$ emits an EOS (End of Sequence) token, its allocated GPU memory is immediately reclaimed.
   - A newly arrived sequence $B$ is inserted into the running batch on the very next token iteration without waiting.
   - Impact: Increases GPU throughput by 4x to 8x and slashes queueing delays.

## Likely follow-ups

- How does continuous batching handle the difference between prefill iterations and decode iterations?
- What scheduling algorithm decides priority when the GPU runs out of KV cache memory during continuous batching?

---

[← Q0724](../../batch_08_azure_openai_bedrock_cloud_ai/0724_cloud_egress_cost_optimization_and_dedicated_network_peering/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0726 →](../../batch_08_azure_openai_bedrock_cloud_ai/0726_pagedattention_and_kv_cache_memory_allocation/README.md)
