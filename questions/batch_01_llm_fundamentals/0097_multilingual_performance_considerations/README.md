# Q0097 · Multilingual performance considerations

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Global users | Medium |

## Question

LLM Suite users work in many languages. What changes when you support non-English users?

## Answer

- Quality varies by language. Models are usually strongest in English, so evaluate each major language separately, including for retrieval.
- Tokenization efficiency: some languages cost several times more tokens per sentence, which affects cost, latency and context.
- Retrieval: use multilingual embedding models, or translate queries. BM25 needs language-aware analysers (stemming, segmentation for languages without spaces).
- Mixed-language documents and queries (English policy, French question) need cross-lingual retrieval and instructions on the answer language.
- Safety and guardrails: content filters and PII detectors must work in each language, because attackers switch languages to evade filters.
- Formatting and locale: dates, number formats (1.234,56 versus 1,234.56) and currency, which is critical for financial content.
- Regulatory and HR content may exist in local-language versions. Retrieve the right jurisdiction's version.

## Likely follow-ups

- How would you evaluate an assistant in five languages without five times the labelling effort?

---

[← Q0096](../../batch_01_llm_fundamentals/0096_parse_tool_calls_from_raw_model_text/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0098 →](../../batch_01_llm_fundamentals/0098_small_language_models_for_platform_tasks/README.md)
