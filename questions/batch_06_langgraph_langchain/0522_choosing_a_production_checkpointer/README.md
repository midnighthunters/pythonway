# Q0522 · Choosing a production checkpointer

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | Persistence | Medium |

## Question

Which checkpointer would you use in production for LangGraph agents, and what operational concerns come with it?

## Answer

Options:
- Postgres (`langgraph-checkpoint-postgres`): the common production choice. It is durable, transactional, queryable, and fits existing database operations (backups, high availability, encryption).
- SQLite: good for local development and single-node tools, not for multi-replica services.
- Redis-based or other community and cloud checkpointers: fast, but check durability settings and semantics.
- Managed: LangGraph Platform or Server provides persistence as part of its deployment.

Operational concerns:
- Size and retention: checkpoints accumulate per step, and messages grow. Set a TTL or retention policy, prune old checkpoints, and keep large blobs out of the state (store references).
- Sensitive data: checkpoints contain prompts, tool results and personal data, so encrypt them, control access, and include them in deletion workflows.
- Performance: write latency per step (durability modes trade safety for speed), connection pooling, and indexes on thread id.
- Schema evolution: state schema changes versus old checkpoints (migrations or tolerant readers).
- Multi-region: where the data resides, and failover behaviour.

## Likely follow-ups

- How would you delete all checkpoints for a user who leaves the firm?

---

[← Q0521](../../batch_06_langgraph_langchain/0521_checkpointers_and_threads/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0523 →](../../batch_06_langgraph_langchain/0523_approval_with_interrupt/README.md)
