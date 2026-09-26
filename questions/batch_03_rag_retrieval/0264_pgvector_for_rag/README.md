# Q0264 · pgvector for RAG

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Infrastructure | Medium |

## Question

Show how you'd store and query chunks with pgvector, including metadata filtering and entitlement filtering in SQL, and discuss when Postgres is enough.

## Answer

```sql
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE chunks (
    chunk_id      text PRIMARY KEY,
    doc_id        text NOT NULL,
    jurisdiction  text,
    acl_groups    text[] NOT NULL,
    effective     date,
    content       text NOT NULL,
    embedding     vector(1024) NOT NULL
);

CREATE INDEX ON chunks USING hnsw (embedding vector_cosine_ops);
CREATE INDEX ON chunks USING gin (acl_groups);

-- $1 = query embedding, $2 = the user's groups (text[]), $3 = jurisdiction
SELECT chunk_id, doc_id, content, 1 - (embedding <=> $1) AS similarity
FROM chunks
WHERE acl_groups && $2
  AND ($3::text IS NULL OR jurisdiction = $3)
ORDER BY embedding <=> $1
LIMIT 20;
```

`<=>` is cosine distance, and `&&` is array overlap for the ACL check. Everything is parameterised, never string-built.

When Postgres is enough: up to low tens of millions of vectors with moderate QPS, and when you value transactional consistency (chunks and ACLs updated atomically with document metadata), SQL filters and a single database to operate. Watch filtered HNSW recall with very selective filters (tune `hnsw.ef_search`, and consider iterative index scans in newer pgvector versions). For BM25, pair it with Postgres full-text search or an external engine.

## Likely follow-ups

- Why is updating ACLs transactionally with the chunks an advantage?

---

[← Q0263](../../batch_03_rag_retrieval/0263_opensearch_hybrid_retrieval/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0265 →](../../batch_03_rag_retrieval/0265_scaling_vector_search_to_100m_chunks/README.md)
