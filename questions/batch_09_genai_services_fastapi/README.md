# Building GenAI Services: FastAPI, Streaming, Queues & NoSQL

Production GenAI microservices: FastAPI endpoints for chat and agents, SSE token streaming, async concurrency and backpressure, long-running agent jobs on queues, conversation state in NoSQL, semantic caching, per-tenant quotas and cost metering, containers and autoscaling. Endpoints are tested with FastAPI's TestClient.

Maps to the job description: Python (FastAPI); microservices and APIs; elastic compute, NoSQL databases and messaging queues; containerization.

Q0801–Q0900 · 100 questions · Easy 22 · Medium 55 · Hard 23

| # | Question | Topic | Difficulty |
|---|---|---|---|
| Q0801 | [FastAPI lifespan context manager for GenAI models](0801_fastapi_lifespan_context_manager_for_genai_models/README.md) | FastAPI foundations | Easy |
| Q0802 | [Pydantic v2 request and response validation for chat endpoints](0802_pydantic_v2_request_and_response_validation_for_chat/README.md) | FastAPI foundations | Easy |
| Q0803 | [FastAPI dependency injection for tenant identification and auth](0803_fastapi_dependency_injection_for_tenant_identification_and/README.md) | FastAPI foundations | Medium |
| Q0804 | [Preventing event loop blocking in async FastAPI routes](0804_preventing_event_loop_blocking_in_async_fastapi_routes/README.md) | FastAPI foundations | Medium |
| Q0805 | [Global exception handler for model provider errors](0805_global_exception_handler_for_model_provider_errors/README.md) | FastAPI foundations | Medium |
| Q0806 | [Testing GenAI endpoints with FastAPI TestClient and mocking](0806_testing_genai_endpoints_with_fastapi_testclient_and_mocking/README.md) | FastAPI foundations | Medium |
| Q0807 | [Server-Sent Events streaming with StreamingResponse](0807_server_sent_events_streaming_with_streamingresponse/README.md) | FastAPI streaming | Medium |
| Q0808 | [Streaming LangChain chat model events over FastAPI](0808_streaming_langchain_chat_model_events_over_fastapi/README.md) | FastAPI streaming | Medium |
| Q0809 | [Client disconnect detection during streaming generation](0809_client_disconnect_detection_during_streaming_generation/README.md) | FastAPI streaming | Hard |
| Q0810 | [Bidirectional WebSockets for interactive agent steering](0810_bidirectional_websockets_for_interactive_agent_steering/README.md) | FastAPI WebSockets | Medium |
| Q0811 | [Managing WebSocket connection pools and heartbeats](0811_managing_websocket_connection_pools_and_heartbeats/README.md) | FastAPI WebSockets | Medium |
| Q0812 | [Asynchronous job submission pattern: 202 Accepted and polling](0812_asynchronous_job_submission_pattern_202_accepted_and_polling/README.md) | Asynchronous Queues | Medium |
| Q0813 | [Background task processing with FastAPI BackgroundTasks](0813_background_task_processing_with_fastapi_backgroundtasks/README.md) | Asynchronous Queues | Easy |
| Q0814 | [Distributed message queues: Celery, ARQ, and Redis Queue for agents](0814_distributed_message_queues_celery_arq_and_redis_queue_for/README.md) | Asynchronous Queues | Medium |
| Q0815 | [Idempotency keys in message queue consumers](0815_idempotency_keys_in_message_queue_consumers/README.md) | Asynchronous Queues | Medium |
| Q0816 | [Dead Letter Queues and exponential backoff retry policies](0816_dead_letter_queues_and_exponential_backoff_retry_policies/README.md) | Asynchronous Queues | Medium |
| Q0817 | [Worker concurrency and graceful shutdown on SIGTERM](0817_worker_concurrency_and_graceful_shutdown_on_sigterm/README.md) | Asynchronous Queues | Hard |
| Q0818 | [Storing conversation history in NoSQL: DynamoDB and Cosmos DB](0818_storing_conversation_history_in_nosql_dynamodb_and_cosmos_db/README.md) | NoSQL state stores | Medium |
| Q0819 | [DynamoDB thread history repository implementation in Python](0819_dynamodb_thread_history_repository_implementation_in_python/README.md) | NoSQL state stores | Medium |
| Q0820 | [Optimistic concurrency control for parallel agent state updates](0820_optimistic_concurrency_control_for_parallel_agent_state/README.md) | NoSQL state stores | Hard |
| Q0821 | [Redis TTL session store with sliding window expiration](0821_redis_ttl_session_store_with_sliding_window_expiration/README.md) | NoSQL state stores | Easy |
| Q0822 | [Cosmos DB partition key strategies for enterprise chat apps](0822_cosmos_db_partition_key_strategies_for_enterprise_chat_apps/README.md) | NoSQL state stores | Medium |
| Q0823 | [MongoDB document schema design for hierarchical agent traces](0823_mongodb_document_schema_design_for_hierarchical_agent_traces/README.md) | NoSQL state stores | Medium |
| Q0824 | [Redis vs DynamoDB vs PostgreSQL for conversation state](0824_redis_vs_dynamodb_vs_postgresql_for_conversation_state/README.md) | NoSQL state stores | Medium |
| Q0825 | [Implementing an async key-value checkpoint saver for agent graphs](0825_implementing_an_async_key_value_checkpoint_saver_for_agent/README.md) | NoSQL state stores | Hard |
| Q0826 | [Conversation history pruning and summarization triggers](0826_conversation_history_pruning_and_summarization_triggers/README.md) | NoSQL state stores | Medium |
| Q0827 | [Multi-region active-active replication for conversation state](0827_multi_region_active_active_replication_for_conversation/README.md) | NoSQL state stores | Hard |
| Q0828 | [PII encryption at rest in NoSQL state stores with envelope encryption](0828_pii_encryption_at_rest_in_nosql_state_stores_with_envelope/README.md) | NoSQL state stores | Hard |
| Q0829 | [Bulk export and retention policies for compliance chat histories](0829_bulk_export_and_retention_policies_for_compliance_chat/README.md) | NoSQL state stores | Medium |
| Q0830 | [Read consistency models in NoSQL state stores for GenAI apps](0830_read_consistency_models_in_nosql_state_stores_for_genai_apps/README.md) | NoSQL state stores | Medium |
| Q0831 | [Redis vector similarity search for semantic prompt response caching](0831_redis_vector_similarity_search_for_semantic_prompt_response/README.md) | Semantic caching | Medium |
| Q0832 | [Semantic cache invalidation strategies and cache-hit threshold tuning](0832_semantic_cache_invalidation_strategies_and_cache_hit/README.md) | Semantic caching | Hard |
| Q0833 | [Exact SHA-256 caching versus semantic vector caching trade-offs](0833_exact_sha_256_caching_versus_semantic_vector_caching_trade/README.md) | Semantic caching | Easy |
| Q0834 | [Multi-tier caching architecture: L1 in-memory LRU and L2 distributed Redis](0834_multi_tier_caching_architecture_l1_in_memory_lru_and_l2/README.md) | Semantic caching | Medium |
| Q0835 | [Handling temperature and non-determinism in semantic cache keys](0835_handling_temperature_and_non_determinism_in_semantic_cache/README.md) | Semantic caching | Medium |
| Q0836 | [Cache stampede prevention with distributed locks (Redlock)](0836_cache_stampede_prevention_with_distributed_locks_redlock/README.md) | Semantic caching | Hard |
| Q0837 | [Negative caching and error response caching mitigation](0837_negative_caching_and_error_response_caching_mitigation/README.md) | Semantic caching | Medium |
| Q0838 | [Estimating and tracking prompt token savings and cache ROI in production](0838_estimating_and_tracking_prompt_token_savings_and_cache_roi/README.md) | Semantic caching | Easy |
| Q0839 | [Streaming responses from a semantic cache with synthetic chunk delays](0839_streaming_responses_from_a_semantic_cache_with_synthetic/README.md) | Semantic caching | Medium |
| Q0840 | [Sensitive data leakage prevention in shared enterprise semantic caches](0840_sensitive_data_leakage_prevention_in_shared_enterprise/README.md) | Semantic caching | Hard |
| Q0841 | [Sliding-window rate limiting middleware using Redis Lua scripts](0841_sliding_window_rate_limiting_middleware_using_redis_lua/README.md) | Rate limiting and quotas | Hard |
| Q0842 | [Token bucket algorithm for managing LLM token rate limits (TPM)](0842_token_bucket_algorithm_for_managing_llm_token_rate_limits/README.md) | Rate limiting and quotas | Medium |
| Q0843 | [Tenant-based quota enforcement and tiered subscription rate limits](0843_tenant_based_quota_enforcement_and_tiered_subscription_rate/README.md) | Rate limiting and quotas | Medium |
| Q0844 | [Per-request token budgeting and hard cutoff limits in FastAPI](0844_per_request_token_budgeting_and_hard_cutoff_limits_in/README.md) | Rate limiting and quotas | Easy |
| Q0845 | [FinOps cost metering: Calculating USD cost per request by model](0845_finops_cost_metering_calculating_usd_cost_per_request_by/README.md) | Rate limiting and quotas | Easy |
| Q0846 | [Asynchronous usage event publishing to Kafka for enterprise billing](0846_asynchronous_usage_event_publishing_to_kafka_for_enterprise/README.md) | Rate limiting and quotas | Medium |
| Q0847 | [HTTP 429 Retry-After headers and client cooperative backoff](0847_http_429_retry_after_headers_and_client_cooperative_backoff/README.md) | Rate limiting and quotas | Easy |
| Q0848 | [Concurrency limiting with asyncio Semaphore to prevent gateway saturation](0848_concurrency_limiting_with_asyncio_semaphore_to_prevent/README.md) | Rate limiting and quotas | Medium |
| Q0849 | [Priority queues for Tier-1 bank workloads versus batch background jobs](0849_priority_queues_for_tier_1_bank_workloads_versus_batch/README.md) | Rate limiting and quotas | Hard |
| Q0850 | [Circuit breaker pattern for downstream LLM provider outages](0850_circuit_breaker_pattern_for_downstream_llm_provider_outages/README.md) | Rate limiting and quotas | Hard |
| Q0851 | [Adaptive rate limiting based on upstream error rates and response latency](0851_adaptive_rate_limiting_based_on_upstream_error_rates_and/README.md) | Rate limiting and quotas | Hard |
| Q0852 | [Graceful degradation and fallback to smaller models under heavy load](0852_graceful_degradation_and_fallback_to_smaller_models_under/README.md) | Rate limiting and quotas | Medium |
| Q0853 | [Request deduplication middleware for idempotent chat completions](0853_request_deduplication_middleware_for_idempotent_chat/README.md) | Rate limiting and quotas | Medium |
| Q0854 | [Streaming backpressure handling when slow clients cannot consume tokens](0854_streaming_backpressure_handling_when_slow_clients_cannot/README.md) | FastAPI streaming | Hard |
| Q0855 | [Measuring Time to First Token and Inter-Token Latency in middleware](0855_measuring_time_to_first_token_and_inter_token_latency_in/README.md) | FastAPI streaming | Medium |
| Q0856 | [Structured JSON logging middleware with correlation IDs](0856_structured_json_logging_middleware_with_correlation_ids/README.md) | FastAPI foundations | Medium |
| Q0857 | [OpenTelemetry instrumentation for FastAPI routes and downstream model calls](0857_opentelemetry_instrumentation_for_fastapi_routes_and/README.md) | FastAPI foundations | Hard |
| Q0858 | [Prometheus metrics endpoint for request counts, latencies, and token counters](0858_prometheus_metrics_endpoint_for_request_counts_latencies/README.md) | FastAPI foundations | Medium |
| Q0859 | [Health checks: Deep versus shallow liveness and readiness probes](0859_health_checks_deep_versus_shallow_liveness_and_readiness/README.md) | FastAPI foundations | Easy |
| Q0860 | [Request body streaming and large file upload for document RAG endpoints](0860_request_body_streaming_and_large_file_upload_for_document/README.md) | FastAPI foundations | Medium |
| Q0861 | [File streaming and download for generated PDF and Excel reports](0861_file_streaming_and_download_for_generated_pdf_and_excel/README.md) | FastAPI foundations | Easy |
| Q0862 | [Custom Pydantic v2 validators for prompt injection patterns and toxic keywords](0862_custom_pydantic_v2_validators_for_prompt_injection_patterns/README.md) | FastAPI foundations | Easy |
| Q0863 | [Multipart form data with file parsing and simultaneous JSON metadata](0863_multipart_form_data_with_file_parsing_and_simultaneous_json/README.md) | FastAPI foundations | Medium |
| Q0864 | [Content negotiation supporting both JSON completion and SSE streaming](0864_content_negotiation_supporting_both_json_completion_and_sse/README.md) | FastAPI foundations | Medium |
| Q0865 | [Asynchronous generator cancellation and memory cleanup on disconnect](0865_asynchronous_generator_cancellation_and_memory_cleanup_on/README.md) | FastAPI streaming | Hard |
| Q0866 | [FastAPI dependency overrides for integration testing without live cloud services](0866_fastapi_dependency_overrides_for_integration_testing/README.md) | FastAPI foundations | Easy |
| Q0867 | [Sub-applications and API versioning with APIRouter](0867_sub_applications_and_api_versioning_with_apirouter/README.md) | FastAPI foundations | Easy |
| Q0868 | [Mutual TLS client certificate authentication in FastAPI](0868_mutual_tls_client_certificate_authentication_in_fastapi/README.md) | FastAPI foundations | Medium |
| Q0869 | [OAuth2 JWT bearer token validation with role-based access control](0869_oauth2_jwt_bearer_token_validation_with_role_based_access/README.md) | FastAPI foundations | Medium |
| Q0870 | [CORS, CSRF, and security headers middleware for GenAI frontends](0870_cors_csrf_and_security_headers_middleware_for_genai/README.md) | FastAPI foundations | Easy |
| Q0871 | [ARQ async Redis job queue implementation for long-running document indexing](0871_arq_async_redis_job_queue_implementation_for_long_running/README.md) | Asynchronous Queues | Hard |
| Q0872 | [Celery worker configuration for CPU-bound text splitting and embedding](0872_celery_worker_configuration_for_cpu_bound_text_splitting/README.md) | Asynchronous Queues | Medium |
| Q0873 | [SQS message visibility timeout management for multi-minute agent runs](0873_sqs_message_visibility_timeout_management_for_multi_minute/README.md) | Asynchronous Queues | Hard |
| Q0874 | [Job status tracking state machine: PENDING, RUNNING, SUCCESS, FAILED](0874_job_status_tracking_state_machine_pending_running_success/README.md) | Asynchronous Queues | Medium |
| Q0875 | [Real-time progress updates via Redis PubSub during batch jobs](0875_real_time_progress_updates_via_redis_pubsub_during_batch/README.md) | Asynchronous Queues | Medium |
| Q0876 | [Cancelling in-flight async queue jobs on user request](0876_cancelling_in_flight_async_queue_jobs_on_user_request/README.md) | Asynchronous Queues | Medium |
| Q0877 | [Distributed task workflows: Chains, Chords, and Groups for parallel map-reduce](0877_distributed_task_workflows_chains_chords_and_groups_for/README.md) | Asynchronous Queues | Hard |
| Q0878 | [Worker memory leak mitigation: recycling worker processes after N tasks](0878_worker_memory_leak_mitigation_recycling_worker_processes/README.md) | Asynchronous Queues | Easy |
| Q0879 | [Handling unhandled worker exceptions and capturing crash stack traces in DLQs](0879_handling_unhandled_worker_exceptions_and_capturing_crash/README.md) | Asynchronous Queues | Medium |
| Q0880 | [Scheduling recurring batch embedding updates with Celery Beat](0880_scheduling_recurring_batch_embedding_updates_with_celery/README.md) | Asynchronous Queues | Easy |
| Q0881 | [Dedicated worker pools: separating fast inference from slow scraping tasks](0881_dedicated_worker_pools_separating_fast_inference_from_slow/README.md) | Asynchronous Queues | Medium |
| Q0882 | [S3 large payload offloading pattern for message queues (Claim-Check pattern)](0882_s3_large_payload_offloading_pattern_for_message_queues/README.md) | Asynchronous Queues | Medium |
| Q0883 | [Exactly-once processing versus at-least-once processing in agent task queues](0883_exactly_once_processing_versus_at_least_once_processing_in/README.md) | Asynchronous Queues | Hard |
| Q0884 | [Throttling worker consumption to match downstream cloud API limits](0884_throttling_worker_consumption_to_match_downstream_cloud_api/README.md) | Asynchronous Queues | Medium |
| Q0885 | [Testing async workers in isolation with mocks and test runners](0885_testing_async_workers_in_isolation_with_mocks_and_test/README.md) | Asynchronous Queues | Easy |
| Q0886 | [Multi-stage Dockerfile for FastAPI GenAI microservices with non-root security](0886_multi_stage_dockerfile_for_fastapi_genai_microservices_with/README.md) | Containers and deployment | Medium |
| Q0887 | [Uvicorn vs Gunicorn architecture and worker count calculation](0887_uvicorn_vs_gunicorn_architecture_and_worker_count/README.md) | Containers and deployment | Medium |
| Q0888 | [Uvicorn loop optimization with uvloop and httptools in Linux containers](0888_uvicorn_loop_optimization_with_uvloop_and_httptools_in/README.md) | Containers and deployment | Easy |
| Q0889 | [Kubernetes Deployment, Service, and ConfigMap for GenAI microservice](0889_kubernetes_deployment_service_and_configmap_for_genai/README.md) | Containers and deployment | Medium |
| Q0890 | [Horizontal Pod Autoscaler using custom Prometheus metrics](0890_horizontal_pod_autoscaler_using_custom_prometheus_metrics/README.md) | Containers and deployment | Hard |
| Q0891 | [KEDA scaled object based on Redis queue depth](0891_keda_scaled_object_based_on_redis_queue_depth/README.md) | Containers and deployment | Medium |
| Q0892 | [Graceful termination lifecycle in Kubernetes: preStop hook and SIGTERM](0892_graceful_termination_lifecycle_in_kubernetes_prestop_hook/README.md) | Containers and deployment | Hard |
| Q0893 | [Rolling zero-downtime deployments and blue green canary rollouts](0893_rolling_zero_downtime_deployments_and_blue_green_canary/README.md) | Containers and deployment | Medium |
| Q0894 | [Managing secrets securely with Vault and AWS Secrets Manager in containers](0894_managing_secrets_securely_with_vault_and_aws_secrets/README.md) | Containers and deployment | Easy |
| Q0895 | [Ephemeral volume mounts and RAM disks for temporary file processing](0895_ephemeral_volume_mounts_and_ram_disks_for_temporary_file/README.md) | Containers and deployment | Easy |
| Q0896 | [Container security scanning and minimal base images](0896_container_security_scanning_and_minimal_base_images/README.md) | Containers and deployment | Medium |
| Q0897 | [Optimizing container startup time for serverless containers](0897_optimizing_container_startup_time_for_serverless_containers/README.md) | Containers and deployment | Easy |
| Q0898 | [Network policies and private egress via corporate forward proxies](0898_network_policies_and_private_egress_via_corporate_forward/README.md) | Containers and deployment | Medium |
| Q0899 | [Disaster recovery: multi-region active-passive failover and DNS routing](0899_disaster_recovery_multi_region_active_passive_failover_and/README.md) | Containers and deployment | Medium |
| Q0900 | [Complete production architecture review: end-to-end design of an enterprise GenAI service](0900_complete_production_architecture_review_end_to_end_design/README.md) | Containers and deployment | Hard |

[← All sections](../README.md)
