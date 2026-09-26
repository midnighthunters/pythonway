# Q0161 · Account for every token in a request

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Context engineering | Medium |

## Question

Write a request token-accounting function covering system prompt, messages, tool schemas (as serialised JSON) and images, which reports a per-section breakdown and whether the request fits the context window with the reserved output.

## Answer

```python
import json
from typing import Callable


def request_token_report(system: str, messages: list[dict], tools: list[dict], images: list[tuple[int, int]],
                         context_window: int, reserved_output: int, count: Callable[[str], int],
                         image_tokens: Callable[[int, int], int]) -> dict:
    breakdown = {
        "system": count(system),
        "messages": sum(count(m["content"]) + 4 for m in messages),
        "tools": count(json.dumps(tools, separators=(",", ":"))),
        "images": sum(image_tokens(w, h) for w, h in images),
    }
    total = sum(breakdown.values())
    return {**breakdown, "total": total, "fits": total + reserved_output <= context_window,
            "headroom": context_window - reserved_output - total}


approx = lambda s: max(1, len(s) // 4)
report = request_token_report(
    system="x" * 400, messages=[{"role": "user", "content": "y" * 200}],
    tools=[{"name": "search", "parameters": {"type": "object"}}], images=[(1024, 1024)],
    context_window=2_000, reserved_output=500, count=approx, image_tokens=lambda w, h: 765)
assert report["system"] == 100 and report["messages"] == 54 and report["images"] == 765
assert report["total"] == 100 + 54 + report["tools"] + 765 and report["fits"] is True
```

Tool schemas are the hidden cost. Twenty verbose tools can be thousands of tokens on every call. Per-message overhead (role markers, template tokens) and images add up too. Use the provider's token-counting endpoint or tokenizer where available, and track this breakdown in telemetry to spot bloat.

## Likely follow-ups

- Which section would you shrink first when the headroom goes negative?

---

[← Q0160](../../batch_02_prompting_context_structured_output/0160_deduplicate_memory_facts/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0162 →](../../batch_02_prompting_context_structured_output/0162_system_prompt_confidentiality/README.md)
