# Q0724 · Cloud egress cost optimization and dedicated network peering

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | Cloud AI Architecture | Medium |

## Question

How do enterprise banks optimize cloud egress costs and latency when connecting on-premises systems to cloud LLMs via Azure ExpressRoute and AWS Direct Connect?

## Answer

Transmitting multi-megabyte document chunks and high-frequency streaming responses over the public internet incurs significant egress fees ($0.08–$0.12 per GB) and unpredictable network latency.

Optimization Strategies:
1. Dedicated Private Peering:
   - Azure ExpressRoute and AWS Direct Connect establish dedicated 10 Gbps / 100 Gbps fiber circuits between bank data centers and cloud VPCs/VNets.
   - Bypasses public internet, providing deterministic sub-5ms round-trip latency and discounted private data transfer rates.
2. In-Cloud Processing & Summarization:
   - Perform heavy RAG document chunking and vector search directly inside the cloud region rather than streaming large raw PDFs from on-premises to the cloud on every query.
   - Return only concise summaries and answers over the egress link.
3. Compression Middleware:
   - Enable Gzip / Brotli compression or binary encoding (MessagePack / Protocol Buffers) on SSE event streams.

## Likely follow-ups

- Why is streaming SSE over public internet connections prone to connection resets compared to ExpressRoute?
- How does AWS PrivateLink differ from AWS Direct Connect?

---

[← Q0723](../../batch_08_azure_openai_bedrock_cloud_ai/0723_disaster_recovery_active_active_versus_active_passive_multi/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0725 →](../../batch_08_azure_openai_bedrock_cloud_ai/0725_continuous_batching_vs_static_batching_in_llm_inference/README.md)
