# Q0060 · Budget max_tokens against the context window

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Context management | Easy |

## Question

Write a helper that picks `max_tokens` for a request given the model's context window, output cap, prompt size, the desired output and a safety margin. Fail clearly if the prompt doesn't fit.

## Answer

```python
def plan_max_tokens(context_window: int, prompt_tokens: int, desired_output: int,
                    model_output_cap: int, safety_margin: int = 0) -> int:
    room = context_window - prompt_tokens - safety_margin
    if room <= 0:
        raise ValueError(f"prompt ({prompt_tokens} tokens) does not fit; trim context first")
    return min(desired_output, model_output_cap, room)


assert plan_max_tokens(128_000, 10_000, 4_000, 16_384) == 4_000
assert plan_max_tokens(128_000, 126_000, 4_000, 16_384, safety_margin=500) == 1_500
assert plan_max_tokens(128_000, 1_000, 50_000, 16_384) == 16_384
try:
    plan_max_tokens(8_192, 8_192, 100, 4_096)
    raise AssertionError
except ValueError:
    pass
```

Why the margin: your token count may differ slightly from the provider's (templates, tool schemas, image tokens). Why not always ask for the maximum: some gateways and rate limiters reserve quota based on `max_tokens`, so oversized values waste throughput, and a runaway response costs more.

## Likely follow-ups

- Where do you get the context window and output cap for 20 models (a capability registry)?

---

[← Q0059](../../batch_01_llm_fundamentals/0059_grammar_constrained_decoding_with_token_masks/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0061 →](../../batch_01_llm_fundamentals/0061_choosing_an_embedding_model/README.md)
