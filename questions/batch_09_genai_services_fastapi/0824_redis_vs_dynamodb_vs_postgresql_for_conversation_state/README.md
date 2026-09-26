# Q0824 · Redis vs DynamoDB vs PostgreSQL for conversation state

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | NoSQL state stores | Medium |

## Question

Compare Redis, AWS DynamoDB, and PostgreSQL for persisting LLM conversational state and LangGraph checkpoints across latency, durability, operational cost, and query flexibility.

## Answer

| Attribute | In-Memory Redis | AWS DynamoDB / Cosmos DB | PostgreSQL (RDS / Aurora) |
|---|---|---|---|
| **Primary Role** | Hot short-term session buffer & semantic cache | Durable serverless conversation history & checkpoints | Relational enterprise data, audit logs, metadata joins |
| **P99 Read Latency** | Sub-millisecond (< 1ms) | Single-digit millisecond (3-8ms) | 5-25ms depending on indexing & connection pool |
| **Durability** | Ephemeral / Snapshot (AOF/RDB) | Fully durable multi-AZ replication | ACID compliant, Write-Ahead Log (WAL) |
| **Query Flexibility** | Key-value, Hash, Sorted Sets, Vector search | Partition Key + Sort Key queries | Full relational SQL, JSONB querying, vector extension (pgvector) |
| **Cost Model** | Billed by provisioned memory (expensive at scale) | Pay-per-request (on-demand) or provisioned RCUs/WCUs | Provisioned compute + storage instance hours |
| **Best Practice Pattern** | Write hot active window to Redis; flush checkpoints to DynamoDB / Postgres on thread completion |

```python
# no-run
# Architecture comparison summary
def select_state_store(session_type: str, durability_needed: bool) -> str:
    if session_type == "active_turn_cache" and not durability_needed:
        return "Redis"
    elif session_type == "agent_checkpoint" and durability_needed:
        return "DynamoDB"
    elif session_type == "compliance_audit_ledger":
        return "PostgreSQL"
    return "DynamoDB"
```

## Likely follow-ups

- When should you use Redis persistence (AOF fsync=always) versus offloading to a managed NoSQL store?
- How does DynamoDB DAX (DynamoDB Accelerator) compare with an external Redis cache?

---

[← Q0823](../../batch_09_genai_services_fastapi/0823_mongodb_document_schema_design_for_hierarchical_agent_traces/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0825 →](../../batch_09_genai_services_fastapi/0825_implementing_an_async_key_value_checkpoint_saver_for_agent/README.md)
