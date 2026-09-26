# Q0276 · Chunk boundary problems

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Chunking | Medium |

## Question

What goes wrong at chunk boundaries, and how do you mitigate it?

## Answer

Problems:
- An answer split across two chunks: neither chunk alone matches strongly, or the model sees half the rule ("capped at 180 GBP" in one chunk, "except in December" in the next).
- Lost antecedents: "This limit" or "the above exceptions" without the preceding context.
- Tables and lists split mid-structure. Headings separated from their content.
- Overlap duplicates leading to repeated content in the prompt.

Mitigations:
- Structure-aware chunking (sections, list and table boundaries), with the heading path carried on every chunk.
- Modest overlap, or sentence-window and parent-child expansion at query time.
- Contextual headers (document title, section, a one-line summary).
- Retrieve neighbouring chunks when a hit sits near a boundary, and merge adjacent hits from the same document in order.
- Evaluate with questions whose answers span boundaries.

## Likely follow-ups

- How would you automatically find questions whose answers span chunk boundaries?

---

[← Q0275](../../batch_03_rag_retrieval/0275_exact_match_routing_for_identifiers/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0277 →](../../batch_03_rag_retrieval/0277_compare_chunking_strategies_with_an_evaluation/README.md)
