# Q0141 · Map-reduce summarisation

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Summarisation | Medium |

## Question

Implement map-reduce summarisation for documents longer than the context: pack paragraphs into chunks, summarise each chunk (map), and summarise the combined summaries (reduce), recursing if needed with a level limit.

## Answer

```python
from typing import Callable


def chunk_paragraphs(paragraphs: list[str], max_chars: int) -> list[str]:
    chunks, cur = [], ""
    for p in paragraphs:
        if cur and len(cur) + len(p) + 1 > max_chars:
            chunks.append(cur)
            cur = p
        else:
            cur = f"{cur}\n{p}" if cur else p
    if cur:
        chunks.append(cur)
    return chunks


def map_reduce_summarize(paragraphs: list[str], summarize: Callable[[str], str], max_chars: int,
                         max_levels: int = 5) -> tuple[str, int]:
    level, calls = paragraphs, 0
    for _ in range(max_levels):
        chunks = chunk_paragraphs(level, max_chars)
        summaries = [summarize(c) for c in chunks]
        calls += len(summaries)
        if len(summaries) == 1:
            return summaries[0], calls
        level = summaries
    raise RuntimeError("summaries are not shrinking; check chunk size or the summariser")


def fake_summarize(chunk: str) -> str:
    return " | ".join(line.split(".")[0] for line in chunk.split("\n"))


paras = [f"Point {i}. Supporting detail that is long enough to matter {i}." for i in range(1, 7)]
summary, calls = map_reduce_summarize(paras, fake_summarize, max_chars=130)
assert summary.startswith("Point 1") and "Point 6" in summary
assert calls == 4
```

Here, 6 paragraphs become 3 chunks (3 map calls), plus 1 reduce call. The map calls are independent, so run them in parallel. The trade-off is that cross-chunk context is lost. The refine pattern (next question) keeps more continuity but is sequential.

## Likely follow-ups

- How would you make sure an important figure mentioned in chunk 2 survives the reduce step?

---

[← Q0140](../../batch_02_prompting_context_structured_output/0140_summarisation_prompt_design/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0142 →](../../batch_02_prompting_context_structured_output/0142_refine_summarisation/README.md)
