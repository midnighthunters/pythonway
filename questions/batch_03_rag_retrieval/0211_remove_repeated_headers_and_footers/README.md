# Q0211 · Remove repeated headers and footers

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Ingestion | Medium |

## Question

Given the text lines of each page of a parsed PDF, remove lines that repeat on most pages (headers and footers) and page-number lines, but keep content that merely repeats occasionally.

## Answer

```python
import math
import re
from collections import Counter

PAGE_NUM = re.compile(r"^\s*(page\s*)?\d+(\s*(of|/)\s*\d+)?\s*$", re.I)


def strip_boilerplate(pages: list[list[str]], min_fraction: float = 0.8) -> list[list[str]]:
    norm = lambda s: re.sub(r"\d+", "#", s.strip().lower())
    counts = Counter(n for page in pages for n in {norm(l) for l in page if l.strip()})
    threshold = max(2, math.ceil(min_fraction * len(pages)))
    boiler = {n for n, c in counts.items() if c >= threshold}
    return [[l for l in page if l.strip() and norm(l) not in boiler and not PAGE_NUM.match(l)] for page in pages]


pages = [
    ["JPMC Internal - Confidential", "Travel Policy v4", "Hotels are capped.", "Page 1 of 3"],
    ["JPMC Internal - Confidential", "Travel Policy v4", "Flights are economy.", "Page 2 of 3"],
    ["JPMC Internal - Confidential", "Travel Policy v4", "Hotels are capped.", "Page 3 of 3"],
]
clean = strip_boilerplate(pages)
assert clean == [["Hotels are capped."], ["Flights are economy."], ["Hotels are capped."]]
```

Replacing digits with `#` treats "Page 1" and "Page 2" as the same line. "Hotels are capped." appears on two of three pages, below the 80% threshold (3 pages), so it survives. Use a ceiling here: `int(0.6 * 3)` rounds down to 2 and would strip real content. Tune the threshold per corpus, and keep the classification label (for example "Confidential") as metadata rather than text.

## Likely follow-ups

- What could go wrong with this heuristic on a two-page document?

---

[← Q0210](../../batch_03_rag_retrieval/0210_document_parsing_challenges/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0212 →](../../batch_03_rag_retrieval/0212_tables_in_rag/README.md)
