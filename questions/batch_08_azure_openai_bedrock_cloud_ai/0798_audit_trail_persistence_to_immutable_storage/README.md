# Q0798 · Audit trail persistence to immutable storage

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | Cloud AI Compliance | Hard |

## Question

How do enterprise banks persist AI prompt and completion audit trails to Write-Once-Read-Many (WORM) storage to satisfy SEC Rule 17a-4 and PRA guidelines?

## Answer

Compliance Requirements for AI Audit Trails:
- All interactions leading to financial advice, trade execution, or loan approvals must be stored in immutable records that cannot be modified, overwritten, or deleted by any user (including cloud administrators) for 3 to 7 years.

Cloud WORM Storage Architecture:
1. S3 Object Lock (AWS) & Azure Immutable Blob Storage:
   - Buckets are configured with Object Lock in Compliance Mode.
   - Even the AWS root account or Azure Subscription Owner cannot bypass retention locks or delete records before the retention period expires.
2. Streaming Ingestion:
   - Gateways stream audit records asynchronously to Amazon Kinesis Data Firehose or Azure Event Hubs.
   - Firehose aggregates records into encrypted Parquet batches, signs each batch with an HMAC SHA-256 hash, and writes them to the locked WORM bucket.
3. Content Cryptographic Proof:
   - Each audit record includes: `timestamp`, `session_id`, `user_id`, `model_version`, `prompt_hash`, `completion_hash`, `guardrail_evaluation`.

## Likely follow-ups

- What is the difference between S3 Governance Mode and Compliance Mode in Object Lock?
- How do legal hold mechanisms suspend deletion when a regulatory investigation begins?

---

[← Q0797](../../batch_08_azure_openai_bedrock_cloud_ai/0797_concurrency_limited_request_dispatcher_with_queue_reject_in/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0799 →](../../batch_08_azure_openai_bedrock_cloud_ai/0799_cryptographic_audit_batch_signer_in_python/README.md)
