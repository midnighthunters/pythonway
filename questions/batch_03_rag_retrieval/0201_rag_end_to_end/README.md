# Q0201 · RAG end to end

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | RAG architecture | Easy |

## Question

Explain retrieval-augmented generation end to end, naming the offline and online stages.

## Answer

Offline (indexing):
1. Ingest documents from the source systems (SharePoint, Confluence, policy portals), with metadata and access-control lists.
2. Parse and clean them (PDF and HTML extraction, tables, OCR where needed) and remove boilerplate.
3. Chunk them into retrievable units with metadata (title, section, dates, ACLs).
4. Embed the chunks, and index them in a vector index plus a keyword (BM25) index.
5. Keep the index fresh: incremental updates, deletions and re-embedding on model change.

Online (query time):
1. Understand the query: condense it with conversation context, rewrite or expand it, extract filters.
2. Retrieve: hybrid search with entitlement and metadata filters applied inside the search.
3. Rerank the candidates with a cross-encoder and select the top k within a token budget.
4. Generate: a grounded prompt with numbered sources, instructions to cite and to abstain when the sources don't cover the question.
5. Post-process: validate citations, check groundedness, apply safety filters, stream with source links.
6. Log and evaluate: retrieval ids, scores, feedback and traces.

Why use it: it gives the model fresh, private, permissioned knowledge with citations, without retraining.

## Likely follow-ups

- Which stage would you instrument first when answers are wrong?

---

[← Q0200](../../batch_02_prompting_context_structured_output/0200_design_the_prompt_stack_for_an_llm_suite_assistant/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0202 →](../../batch_03_rag_retrieval/0202_when_not_to_use_rag/README.md)
