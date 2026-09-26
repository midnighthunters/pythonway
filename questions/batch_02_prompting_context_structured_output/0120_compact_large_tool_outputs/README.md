# Q0120 · Compact large tool outputs

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Context engineering | Medium |

## Question

Tools often return huge JSON payloads. Write a compactor that keeps the structure but caps list lengths and string lengths, recording how much was omitted, so the model sees a representative, bounded result.

## Answer

```python
import json
from typing import Any


def compact(value: Any, max_items: int = 3, max_str: int = 80) -> Any:
    if isinstance(value, dict):
        return {k: compact(v, max_items, max_str) for k, v in value.items()}
    if isinstance(value, list):
        items = [compact(v, max_items, max_str) for v in value[:max_items]]
        if len(value) > max_items:
            items.append(f"... {len(value) - max_items} more items omitted")
        return items
    if isinstance(value, str) and len(value) > max_str:
        return value[:max_str] + f"... [{len(value) - max_str} chars omitted]"
    return value


payload = {"account": "GB00-TEST", "transactions": [{"id": i, "memo": "x" * 200} for i in range(50)]}
small = compact(payload)
assert len(small["transactions"]) == 4
assert small["transactions"][-1] == "... 47 more items omitted"
assert small["transactions"][0]["memo"].endswith("[120 chars omitted]")
assert len(json.dumps(small)) < len(json.dumps(payload)) / 10
```

Better still: design tools to return what the model needs (filters, pagination, summaries, a `total_count`) and let the agent request the next page. Keep the full payload outside the context (in state or a store), referenced by an id, so later steps or the UI can use it.

## Likely follow-ups

- When is it dangerous to compact tool results (for example, the model then under-reports totals)?

---

[← Q0119](../../batch_02_prompting_context_structured_output/0119_rolling_summary_memory/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0121 →](../../batch_02_prompting_context_structured_output/0121_where_to_place_documents_and_the_question/README.md)
