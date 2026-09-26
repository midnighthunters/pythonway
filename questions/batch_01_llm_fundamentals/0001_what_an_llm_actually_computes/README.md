# Q0001 · What an LLM actually computes

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Foundations | Easy |

## Question

In one or two minutes, explain what a large language model computes, from input text to output text.

## Answer

- Text is split into tokens (subword units) and each token id is mapped to an embedding vector.
- A stack of transformer decoder blocks (self-attention plus feed-forward layers, with residual connections and normalisation) turns the sequence of vectors into contextual representations. Causal masking means each position only sees earlier positions.
- The final hidden state at the last position is projected to a vector of logits, one per vocabulary token. Softmax turns the logits into a probability distribution over the next token.
- A decoding strategy (greedy, temperature, top-p and so on) picks one token. It is appended to the input, and the loop repeats until a stop token, a stop sequence or `max_tokens`.
- Training objective: minimise cross-entropy on next-token prediction over huge corpora (pre-training), then instruction tuning and preference optimisation (SFT, RLHF/DPO) to make it follow instructions and be helpful and safe.

Key consequence for engineers: the model has no memory between calls. Everything it "knows" about the conversation must be in the context window, which drives cost, latency and most design decisions on a platform like LLM Suite.

## Likely follow-ups

- Why is generation sequential while the prompt can be processed in parallel?
- Where does the "knowledge" live, and why does it have a cutoff date?

---

[LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0002 →](../../batch_01_llm_fundamentals/0002_why_subword_tokenization/README.md)
