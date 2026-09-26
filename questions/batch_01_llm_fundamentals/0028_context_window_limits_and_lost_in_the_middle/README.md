# Q0028 · Context window limits and lost in the middle

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Context | Medium |

## Question

What limits the context window, and why doesn't a 1M-token window remove the need for retrieval?

## Answer

Limits:
- Attention compute grows quadratically in sequence length during prefill, and the KV cache memory grows linearly with context times batch size.
- Models are trained and evaluated on certain lengths, so quality typically degrades before the advertised maximum.
- Provider limits apply: maximum input tokens, maximum output tokens, and tokens-per-minute quotas.

Why long context doesn't replace retrieval:
- Cost and latency: every token is billed and processed on every call. Prefill of a very large prompt can take seconds to tens of seconds.
- Quality: "lost in the middle" effects mean facts placed in the middle of long contexts are used less reliably than those at the start or end, and irrelevant text distracts the model.
- Entitlements: you can't put a whole document store in the prompt, because users may only see what they're entitled to. Retrieval is where that filtering happens.
- Freshness and scale: corporate corpora are far larger than any window.

Use long context for whole-document tasks (analysing one long contract). Use retrieval for large or permissioned corpora. Prompt caching makes a large, stable prefix much cheaper.

## Likely follow-ups

- How would you test whether a model really uses information from the middle of a long prompt (needle-in-a-haystack, multi-needle tests)?

---

[← Q0027](../../batch_01_llm_fundamentals/0027_why_llms_hallucinate/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0029 →](../../batch_01_llm_fundamentals/0029_kv_cache_incremental_decoding/README.md)
