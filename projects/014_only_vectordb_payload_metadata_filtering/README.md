# Project 014: Metadata Payloads, Namespaces & Boolean Filtering

> **Stage**: Stage 1: Pure Fundamentals  
> **Difficulty**: 3.0 / 10 (Intermediate)  
> **Primary Pillars**: `VectorDB`  
> **Auxiliary Disciplines**: `Guardrails`  

---

## 🎯 Learning Objective
Execute multi-tenant pre-filtering with MongoDB-style boolean expressions (`$eq`, `$in`, `$gt`, `$and`, `$or`, `$not`) and tenant namespace guardrails. Prevent cross-tenant data leakage and eliminate the catastrophic **Recall Collapse** vulnerability caused by naive post-filtering in production Vector Databases.

---

## 🧠 Key Concepts Covered
- **Metadata Payloads**: Associating rich, structured JSON attributes (tenant ID, department, timestamps, security clearance) with dense vector records.
- **Pre-filtering vs Post-filtering**:
  - *Post-filtering*: Evaluating vector distances globally and filtering the top-K afterwards.
  - *Pre-filtering*: Evaluating boolean predicates FIRST to build candidate masks before distance computation.
- **Recall Collapse**: A failure mode in post-filtering where top global results belong to other partitions, leaving the user with zero matching records despite valid matches existing in the index.
- **Boolean Filter AST Engine**: A recursive parser supporting comparison operators (`$eq`, `$ne`, `$gt`, `$gte`, `$lt`, `$lte`, `$in`, `$nin`, `$contains`) and logical connectors (`$and`, `$or`, `$not`).
- **Tenant Guardrails**: Programmatic security layers that intercept queries and inject non-bypassable tenant isolation predicates to eliminate data leakage.

---

## 🏗️ Architecture & Control Flow
```text
User Query + Context (Tenant: 'Acme', Clearance: 1)
                     │
                     ▼
┌──────────────────────────────────────────────┐
│          TenantGuardrail Layer               │  Validates auth, blocks spoofing,
│                                              │  injects mandatory tenant clauses
└──────────────────────┬───────────────────────┘
                       │
             Secure Boolean AST Filter
                       │
       ┌───────────────┴───────────────┐
       ▼                               ▼
[PRE-FILTERING PATH]           [POST-FILTERING PATH]
(Security Gold Standard)       (Recall Collapse Flaw)
       │                               │
1. Scan metadata payloads      1. Compute global top-K
   to build candidate mask        across ALL tenants
       │                               │
2. Evaluate vector distances   2. Discard items that
   ONLY on candidate subset       fail tenant filter
       │                               │
3. Return guaranteed Top-K     3. If top-K belonged to
   authorized documents           others -> ZERO RESULTS!
       │                               │
       └───────────────┬───────────────┘
                       │
                       ▼
       ┌───────────────────────────────┐
       │     Groq LLM Synthesis        │  Generates grounded response using
       │  (Zero Leakage Enforcement)   │  strictly authorized documents
       └───────────────────────────────┘
```

---

## 📂 Project Structure
```text
014_only_vectordb_payload_metadata_filtering/
├── README.md              # Project specifications, self-quiz & stretch challenge
├── requirements.txt       # Dependencies for this project
├── config.py              # Groq model and environment configuration
├── main.py                # Boolean filter engine, pre/post filtering & guardrail RAG
└── test_verification.py   # Automated assertion tests
```

---

## 🚀 Execution & Verification Guide

### 1. Run Main Demonstration
```bash
python main.py
```

### 2. Run Automated Verification Tests
```bash
python test_verification.py
```

---

## 📝 Self-Assessment Interview Quiz (Test Your Understanding)

1. **Why does post-filtering cause "Recall Collapse" in multi-tenant or categorical vector search?**
   * *Answer*: In post-filtering, the index retrieves the global $K$ nearest vectors based solely on distance. If another tenant or unselected category has dense vector clusters closer to the query, all $K$ slots will be occupied by those foreign vectors. When the post-filter drops them, zero results remain for the user, even if the database contains hundreds of relevant records within the authorized tenant.

2. **How do modern vector databases optimize pre-filtering to avoid scanning every metadata payload?**
   * *Answer*: Modern vector databases (e.g. Qdrant, Pinecone, Milvus) maintain payload inverted indices (B-trees, Roaring Bitmaps, or inverted postings). The filter engine executes set intersections on bitmaps in sub-millisecond time to produce an active ID bitset, which is then used as a lookup mask during HNSW graph traversal (Single-Stage Filtered HNSW) or flat matrix indexing.

3. **What attack vector arises if user-supplied filter dictionaries are passed directly to a vector store without a guardrail layer?**
   * *Answer*: If user-supplied JSON filters are passed unsanitized, an attacker can perform "Metadata Injection" (e.g., passing `{"tenant_id": {"$ne": "own_tenant"}}` or overriding the tenant parameter with a target competitor's ID). A Tenant Guardrail strictly intercepts the query at the application boundary, validates identity tokens, and enforces top-level non-overridable `$and` clauses.

---

## 🏆 Stretch Challenge
**Task**: Implement a **Single-Stage Filtered Graph Traversal**: update the `HNSWIndex` from Project 013 so that during beam search on Layer 0, the neighbor exploration checks the payload candidate bitmask before pushing candidates into the evaluation queue, bypassing distance computations for disallowed tenants entirely.
