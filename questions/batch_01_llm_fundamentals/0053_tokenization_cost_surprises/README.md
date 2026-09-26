# Q0053 · Tokenization cost surprises

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Tokenization | Easy |

## Question

Give examples of inputs that tokenize much less efficiently than English prose, and explain the operational impact.

## Answer

- Non-Latin scripts and some languages: several tokens per word, so the same message costs more and fits less context. Multilingual fairness matters for a global workforce.
- Numbers, IDs and hashes: long digit strings or UUIDs fragment into many tokens, and models handle arithmetic on them poorly.
- Code and JSON: indentation, braces and quoted keys inflate counts. Pretty-printed JSON can cost 20–40% more than compact JSON.
- Whitespace-heavy and table-like text (CSV exports, PDFs extracted with layout).
- Base64 and encoded blobs, which are terrible for both cost and model understanding.

Impact: quota (tokens per minute) and cost forecasting, context overflows, and truncated outputs. Mitigate by counting tokens with the model's tokenizer before sending, compacting JSON, summarising or converting tables, and never sending binary blobs as text.

## Likely follow-ups

- How would you forecast the monthly token spend for a new use case?

---

[← Q0052](../../batch_01_llm_fundamentals/0052_matryoshka_embedding_truncation/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0054 →](../../batch_01_llm_fundamentals/0054_truncate_text_to_a_token_budget/README.md)
