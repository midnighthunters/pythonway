# Q0142 · Refine summarisation

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Summarisation | Medium |

## Question

Implement the "refine" summarisation pattern, where the running summary is updated chunk by chunk, and compare it with map-reduce.

## Answer

```python
from typing import Callable


def refine_summarize(chunks: list[str], first: Callable[[str], str],
                     refine: Callable[[str, str], str]) -> tuple[str, int]:
    if not chunks:
        raise ValueError("no chunks")
    summary, calls = first(chunks[0]), 1
    for chunk in chunks[1:]:
        summary = refine(summary, chunk)
        calls += 1
    return summary, calls


def fake_first(chunk: str) -> str:
    return chunk.split(".")[0]


def fake_refine(summary: str, chunk: str) -> str:
    return f"{summary}; {chunk.split('.')[0]}"


s, calls = refine_summarize(["Revenue up 5%. Detail.", "Costs flat. Detail.", "Outlook cautious. Detail."],
                            fake_first, fake_refine)
assert s == "Revenue up 5%; Costs flat; Outlook cautious" and calls == 3
```

Comparison:
- Refine is sequential (slow for long documents) and keeps narrative continuity, but can drift or let early content dominate or be overwritten.
- Map-reduce is parallel, fast and scalable, but loses cross-chunk context and can duplicate points.
- Long-context models can often summarise a whole 100–200 page document in one call. Compare that on quality and cost before building chunked pipelines.

## Likely follow-ups

- Which pattern would you pick for a 300-page regulatory filing with a 30-second SLA?

---

[← Q0141](../../batch_02_prompting_context_structured_output/0141_map_reduce_summarisation/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0143 →](../../batch_02_prompting_context_structured_output/0143_faithful_summaries_of_financial_documents/README.md)
