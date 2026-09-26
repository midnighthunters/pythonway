# Q0017 · Encoder, decoder and encoder-decoder models

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Architectures | Easy |

## Question

Compare encoder-only, decoder-only and encoder-decoder transformers, with an example use of each on an enterprise AI platform.

## Answer

- Encoder-only (BERT family): bidirectional attention, and outputs contextual embeddings rather than generating text. Good for classification, NER, embeddings and rerankers (cross-encoders). Example: a PII detector or a reranker in the RAG pipeline.
- Decoder-only (GPT, Llama, Claude-style): causal attention, generates text autoregressively. It is the general-purpose chat, agent and tool-calling model. Example: the main assistant in LLM Suite.
- Encoder-decoder (T5, BART): the encoder reads the input bidirectionally and the decoder generates while cross-attending to it. Good for translation and summarisation, and common in speech models such as Whisper.

Platform point: you rarely need one giant model for everything. Small encoders are cheap, fast and deterministic enough for classification, routing and guardrails. Reserve large decoders for generation and reasoning.

## Likely follow-ups

- Why did decoder-only models win for general-purpose assistants?
- When would you fine-tune a small encoder instead of prompting a large LLM?

---

[← Q0016](../../batch_01_llm_fundamentals/0016_anatomy_of_a_decoder_block/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0018 →](../../batch_01_llm_fundamentals/0018_greedy_decoding_loop/README.md)
