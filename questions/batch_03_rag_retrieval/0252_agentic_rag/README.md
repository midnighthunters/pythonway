# Q0252 · Agentic RAG

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Agentic retrieval | Medium |

## Question

What is agentic RAG, and when is it worth the extra cost over a single retrieve-then-generate pass?

## Answer

Agentic RAG gives the model retrieval tools (search, fetch a document, list sections, query SQL) and lets it decide iteratively what to look up, reflect on what it found, and stop when it has enough.

Worth it for:
- Multi-hop questions (policy A references procedure B, which defines C).
- Comparisons across sources ("how do the UK and US parental leave policies differ?").
- Research-style tasks that need several searches with refinement.
- Heterogeneous sources (docs plus SQL plus APIs).

Costs and risks: several LLM calls (latency and cost), loops and over-searching, harder evaluation (trajectories), and more prompt-injection surface through retrieved content feeding tool decisions.

Controls: step and token budgets, deduplicating repeat queries, entitlement-filtered tools, returning evidence with ids, and evaluating both final answers and trajectories. Route simple questions to single-pass RAG and escalate only when needed.

## Likely follow-ups

- How would you decide per query whether to use single-pass or agentic RAG?

---

[← Q0251](../../batch_03_rag_retrieval/0251_conversational_rag_memory/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0253 →](../../batch_03_rag_retrieval/0253_iterative_retrieval_tool_loop/README.md)
