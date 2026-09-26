# Q0070 · Data, tensor and pipeline parallelism

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Distributed inference | Medium |

## Question

Explain data, tensor and pipeline parallelism for large models, and which one you'd use to serve a model that doesn't fit on one GPU.

## Answer

- Data parallelism: full model copies on each GPU, each processing different requests or batches. It scales throughput but needs the model to fit on one device. In training, gradients are all-reduced across copies (ZeRO/FSDP additionally shard optimizer state and weights).
- Tensor parallelism: split each layer's weight matrices across GPUs, where each computes part of every matmul and they exchange activations every layer. It needs fast interconnect (NVLink) and cuts per-token latency. It is the usual choice within a node for serving.
- Pipeline parallelism: put different layers on different GPUs and stream micro-batches through the stages. The communication need is lower, so it works across nodes, but it adds pipeline bubbles and latency.
- Expert parallelism (for MoE) places different experts on different GPUs, with all-to-all routing.

Serving a 70B model in BF16: tensor parallelism across 2–4 GPUs in one node, with data-parallel replicas of that group for throughput.

## Likely follow-ups

- Why is tensor parallelism across nodes usually a bad idea?

---

[← Q0069](../../batch_01_llm_fundamentals/0069_concurrency_planning_with_little_s_law/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0071 →](../../batch_01_llm_fundamentals/0071_self_consistency_majority_voting/README.md)
