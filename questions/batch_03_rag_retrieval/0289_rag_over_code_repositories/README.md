# Q0289 · RAG over code repositories

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Domain RAG | Medium |

## Question

How does RAG over source code differ from RAG over prose documents?

## Answer

- Chunking by syntax: functions, classes and modules (via tree-sitter or AST parsing), keeping signatures and docstrings with each chunk, rather than fixed-size windows.
- Retrieval signals: identifiers matter enormously, so use BM25 with code-aware tokenisation (splitting camelCase and snake_case), plus code-specific embedding models.
- Structure: the call graph, imports, references and symbol definitions. "Go to definition" style retrieval often beats similarity.
- Freshness: code changes constantly, so index per commit or branch, incrementally.
- Context assembly: include the relevant definitions and usages, file paths and line numbers, and tests.
- Security: repository permissions and secrets in code (scan and exclude them), and licence considerations.
- Agentic retrieval is common: tools such as `grep`, `read_file` and `list_symbols` let the agent explore, which is how code agents work in practice.

## Likely follow-ups

- Why do code agents often prefer grep-like tools over vector search?

---

[← Q0288](../../batch_03_rag_retrieval/0288_multi_vector_document_scoring/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0290 →](../../batch_03_rag_retrieval/0290_rag_over_email_and_chat/README.md)
