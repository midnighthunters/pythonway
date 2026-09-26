# Q0254 · GraphRAG and knowledge graphs

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Advanced retrieval | Medium |

## Question

What is GraphRAG, and when does a knowledge graph help beyond vector search?

## Answer

- GraphRAG approaches extract entities and relationships from the corpus into a graph (for example Policy → applies_to → Entity, Control → mitigates → Risk). Some also detect communities and summarise them hierarchically, which supports global questions ("what are the main themes across all audit findings?").
- At query time, you link the entities in the question to graph nodes, traverse neighbours (multi-hop), and bring the connected facts and their source chunks into the context.

It helps with multi-hop and relational questions, aggregation and "sensemaking" across many documents, disambiguation (which "Apollo" project), and explainable paths.

Costs: LLM-based extraction over the corpus is expensive and noisy, and the graph needs maintenance as documents change, plus schema design and entity resolution. Many enterprise teams get most of the value from structured metadata plus hybrid search, and add a graph for specific domains (controls and risks, org structures, entity hierarchies) where the relationships already exist in systems of record.

## Likely follow-ups

- Where in a bank do high-quality graphs already exist, so you don't need LLM extraction?

---

[← Q0253](../../batch_03_rag_retrieval/0253_iterative_retrieval_tool_loop/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0255 →](../../batch_03_rag_retrieval/0255_entity_co_occurrence_graph_expansion/README.md)
