# Q0055 · Padding side for batched generation

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Inference | Medium |

## Question

Why do inference stacks use left padding for batched generation but right padding for training? What breaks if you get it wrong?

## Answer

- Generation appends new tokens at the end of every sequence. With right padding, the pad tokens sit between the prompt and the new tokens, so the model "continues" from padding. Left padding puts every sequence's last real token in the final position, so all rows can take the next token together.
- Training doesn't generate, and loss is masked on pads, so right padding is simpler there.
- Left padding needs a correct attention mask and matching position ids, so real tokens start at position 0 or are offset consistently. Otherwise RoPE positions are wrong.
- Symptoms of getting it wrong: fine output at batch size 1 but garbage or repetition in batches, and results that depend on which other requests were batched with yours.

Hosted APIs (Azure OpenAI, Bedrock) hide this. It matters when you self-host with Hugging Face `generate` or build a custom batcher.

## Likely follow-ups

- How do continuous-batching servers avoid padding altogether?

---

[← Q0054](../../batch_01_llm_fundamentals/0054_truncate_text_to_a_token_budget/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0056 →](../../batch_01_llm_fundamentals/0056_render_a_chat_template_safely/README.md)
