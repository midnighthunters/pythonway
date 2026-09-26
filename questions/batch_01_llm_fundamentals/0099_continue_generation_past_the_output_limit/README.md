# Q0099 · Continue generation past the output limit

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Long outputs | Medium |

## Question

A report needs more tokens than the model's output cap. Implement a continuation loop: call the model, and while `finish_reason == "length"`, ask it to continue, stitching chunks and removing any overlap the model repeats.

## Answer

```python
def stitch(a: str, b: str, max_overlap: int = 200, min_overlap: int = 3) -> str:
    for k in range(min(len(a), len(b), max_overlap), min_overlap - 1, -1):
        if a.endswith(b[:k]):
            return a + b[k:]
    return a + b


def generate_long(call, prompt: str, max_rounds: int = 10) -> tuple[str, str]:
    text = ""
    for _ in range(max_rounds):
        chunk, reason = call(prompt, text)
        text = stitch(text, chunk)
        if reason != "length":
            return text, reason
    return text, "max_rounds"


TARGET = "The quick brown fox jumps over the lazy dog. Then it rests in the shade."


def fake_call(prompt: str, so_far: str) -> tuple[str, str]:
    start = max(0, len(so_far) - 3)
    chunk = TARGET[start:start + 13]
    return chunk, "stop" if start + 13 >= len(TARGET) else "length"


assert generate_long(fake_call, "write") == (TARGET, "stop")
assert stitch("abcdef", "defgh") == "abcdefgh"
assert stitch("abc", "xyz") == "abcxyz"
```

The `min_overlap` guard stops accidental one- or two-character matches from eating real text.

In practice, first check whether you need one giant generation. Generating section by section from an outline is more controllable and parallelisable, and each section can be validated. Also cap the total rounds and cost.

## Likely follow-ups

- Why is section-by-section generation usually better for long reports?

---

[← Q0098](../../batch_01_llm_fundamentals/0098_small_language_models_for_platform_tasks/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0100 →](../../batch_01_llm_fundamentals/0100_an_llm_request_end_to_end_on_an_enterprise_platform/README.md)
