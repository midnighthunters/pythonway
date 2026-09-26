# Q0255 · Entity co-occurrence graph expansion

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Advanced retrieval | Medium |

## Question

Build a lightweight entity co-occurrence graph from chunk annotations, and use it to expand a query's entities to strongly related ones before retrieval.

## Answer

```python
from collections import defaultdict
from itertools import combinations


def build_graph(chunk_entities: dict[str, set[str]]) -> dict[str, dict[str, int]]:
    g: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for ents in chunk_entities.values():
        for a, b in combinations(sorted(ents), 2):
            g[a][b] += 1
            g[b][a] += 1
    return g


def expand(entities: set[str], g: dict, min_weight: int = 2) -> set[str]:
    out = set(entities)
    for e in entities:
        out |= {n for n, w in g.get(e, {}).items() if w >= min_weight}
    return out


def retrieve_by_entities(entities: set[str], chunk_entities: dict[str, set[str]]) -> list[str]:
    return sorted(cid for cid, ents in chunk_entities.items() if ents & entities)


ce = {"c1": {"POL-31", "POL-12"}, "c2": {"POL-31", "POL-12", "UK"}, "c3": {"POL-31", "UK"},
      "c4": {"POL-31", "UK"}, "c5": {"Canteen"}}
g = build_graph(ce)
assert expand({"POL-12"}, g) == {"POL-12", "POL-31"}
assert retrieve_by_entities(expand({"POL-12"}, g), ce) == ["c1", "c2", "c3", "c4"]
assert expand({"Canteen"}, g) == {"Canteen"}
```

Entities could come from an NER model, from the metadata in the source systems, or from an LLM pass at ingestion. Expansion boosts recall for related concepts, so rerank afterwards to protect precision.

## Likely follow-ups

- How would you stop hub entities (like "UK") from expanding every query?

---

[← Q0254](../../batch_03_rag_retrieval/0254_graphrag_and_knowledge_graphs/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0256 →](../../batch_03_rag_retrieval/0256_route_between_rag_and_sql/README.md)
