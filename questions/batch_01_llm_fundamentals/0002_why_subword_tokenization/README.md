# Q0002 · Why subword tokenization

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Tokenization | Easy |

## Question

Why do LLMs use subword tokenization (BPE, WordPiece, Unigram) rather than words or characters?

## Answer

- Words: the vocabulary explodes and there is no way to represent unseen words (names, typos, code identifiers).
- Characters: sequences become about 4× longer, and attention cost grows quadratically with length. Models also have to learn spelling from scratch.
- Subwords are a compromise. Frequent words become single tokens, and rare words split into reusable pieces, so nothing is out-of-vocabulary. Byte-level BPE (GPT-style) falls back to raw bytes, so any Unicode input is encodable.

Practical consequences:
- Cost and limits are measured in tokens, not characters. English averages roughly 0.75 words per token. Other languages, code, numbers and JSON can be much less efficient.
- Different model families use different tokenizers, so token counts (and therefore cost and context usage) differ for the same text. A model-agnostic platform must count tokens per model.
- Tokenization explains odd failures: counting letters in a word, reversing strings, and arithmetic on long numbers.

## Likely follow-ups

- Why can the same prompt cost more on one provider than another?
- How would you estimate tokens without the exact tokenizer, and what error bars would you quote?

---

[← Q0001](../../batch_01_llm_fundamentals/0001_what_an_llm_actually_computes/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0003 →](../../batch_01_llm_fundamentals/0003_train_a_toy_bpe_tokenizer/README.md)
