# Q0066 · Open-weight versus hosted models in a bank

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Model strategy | Medium |

## Question

When would a bank self-host an open-weight model instead of using hosted Azure OpenAI or Bedrock models?

## Answer

Reasons to self-host:
- Data residency or sovereignty, or no approved hosted option for a data class.
- Predictable high-volume workloads where dedicated GPUs are cheaper per token.
- Fine-tuning control, custom decoding, or access to internals (logprobs, embeddings, grammars).
- Latency or offline needs (on-premises, edge), and avoiding provider rate limits.

Reasons to use hosted models:
- Frontier quality and fast upgrades, with no GPU capacity planning or on-call for serving.
- Enterprise controls already built in (private networking, content filters, compliance attestations).
- Elastic capacity (pay-as-you-go plus provisioned throughput).

Costs of self-hosting: GPU procurement and utilisation, serving stack (vLLM or TGI), security patching, model supply-chain risk (weights provenance, licences, pickle-free safetensors), evaluation and red-teaming burden, and model-risk validation.

Typical answer: hosted for most generative use cases, and open-weight for specific high-volume, narrow or sensitive tasks, all behind the same gateway so apps don't care.

## Likely follow-ups

- How would you verify the integrity and licence of downloaded weights?

---

[← Q0065](../../batch_01_llm_fundamentals/0065_choosing_a_model_for_a_use_case/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0067 →](../../batch_01_llm_fundamentals/0067_model_version_pinning_and_deprecation/README.md)
