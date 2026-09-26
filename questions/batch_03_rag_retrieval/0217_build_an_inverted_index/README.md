# Q0217 · Build an inverted index

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Keyword search | Medium |

## Question

Implement a tiny inverted index with tokenisation, term-frequency postings, and AND/OR boolean queries.

## Answer

```python
import re
from collections import defaultdict


def tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


class InvertedIndex:
    def __init__(self) -> None:
        self.postings: dict[str, dict[str, int]] = defaultdict(dict)

    def add(self, doc_id: str, text: str) -> None:
        for term in tokenize(text):
            self.postings[term][doc_id] = self.postings[term].get(doc_id, 0) + 1

    def query(self, text: str, mode: str = "and") -> set[str]:
        sets = [set(self.postings.get(t, {})) for t in tokenize(text)]
        if not sets:
            return set()
        return set.intersection(*sets) if mode == "and" else set.union(*sets)


idx = InvertedIndex()
idx.add("d1", "Hotel cap London 180 GBP")
idx.add("d2", "Hotel booking via portal")
idx.add("d3", "Flights London economy")
assert idx.query("hotel london") == {"d1"}
assert idx.query("hotel london", mode="or") == {"d1", "d2", "d3"}
assert idx.postings["london"] == {"d1": 1, "d3": 1}
assert idx.query("") == set()
```

Real engines (Lucene in OpenSearch and Elasticsearch, and Azure AI Search) add analysers (stemming, stop words, language rules), compressed postings, positions for phrase queries, and skip lists for fast intersections.

## Likely follow-ups

- How would you support phrase queries such as "business class"?

---

[← Q0216](../../batch_03_rag_retrieval/0216_metadata_schema_for_chunks/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0218 →](../../batch_03_rag_retrieval/0218_bm25_scoring_from_scratch/README.md)
