# Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure

Azure OpenAI (deployments, quotas, PTUs, content filtering, Entra ID auth, API Management as an AI gateway), Amazon Bedrock (Converse API, Guardrails, Knowledge Bases, AgentCore, cross-Region inference), multi-provider routing, rate-limit handling, streaming, elastic compute and GPU serving.

Maps to the job description: Implement GenAI services leveraging Azure OpenAI models and AWS Bedrock; public cloud architecture; elastic compute.

Q0701–Q0800 · 100 questions · Easy 2 · Medium 77 · Hard 21

| # | Question | Topic | Difficulty |
|---|---|---|---|
| Q0701 | [Azure OpenAI service overview and enterprise benefits](0701_azure_openai_service_overview_and_enterprise_benefits/README.md) | Azure OpenAI | Easy |
| Q0702 | [Azure OpenAI deployment types: Standard, Global Standard, and Provisioned](0702_azure_openai_deployment_types_standard_global_standard_and/README.md) | Azure OpenAI | Medium |
| Q0703 | [Azure Entra ID and Managed Identity authentication](0703_azure_entra_id_and_managed_identity_authentication/README.md) | Azure OpenAI | Medium |
| Q0704 | [Azure OpenAI content safety filters and custom blocklists](0704_azure_openai_content_safety_filters_and_custom_blocklists/README.md) | Azure OpenAI | Medium |
| Q0705 | [Private Endpoints and network isolation in Azure OpenAI](0705_private_endpoints_and_network_isolation_in_azure_openai/README.md) | Azure OpenAI | Medium |
| Q0706 | [Azure API Management as an AI Gateway](0706_azure_api_management_as_an_ai_gateway/README.md) | Azure OpenAI | Hard |
| Q0707 | [Amazon Bedrock service overview and multi-model strategy](0707_amazon_bedrock_service_overview_and_multi_model_strategy/README.md) | AWS Bedrock | Easy |
| Q0708 | [Amazon Bedrock Converse API unified abstraction](0708_amazon_bedrock_converse_api_unified_abstraction/README.md) | AWS Bedrock | Medium |
| Q0709 | [Tool calling in the Amazon Bedrock Converse API](0709_tool_calling_in_the_amazon_bedrock_converse_api/README.md) | AWS Bedrock | Medium |
| Q0710 | [Amazon Bedrock Cross-Region Inference](0710_amazon_bedrock_cross_region_inference/README.md) | AWS Bedrock | Medium |
| Q0711 | [Amazon Bedrock Guardrails and PII masking](0711_amazon_bedrock_guardrails_and_pii_masking/README.md) | AWS Bedrock | Medium |
| Q0712 | [Amazon Bedrock Knowledge Bases and vector indexing](0712_amazon_bedrock_knowledge_bases_and_vector_indexing/README.md) | AWS Bedrock | Medium |
| Q0713 | [Amazon Bedrock Agents and AgentCore](0713_amazon_bedrock_agents_and_agentcore/README.md) | AWS Bedrock | Medium |
| Q0714 | [Handling HTTP 429 Too Many Requests with exponential backoff and jitter](0714_handling_http_429_too_many_requests_with_exponential/README.md) | Cloud AI Gateways | Medium |
| Q0715 | [Multi-provider fallback router: Azure OpenAI to AWS Bedrock](0715_multi_provider_fallback_router_azure_openai_to_aws_bedrock/README.md) | Cloud AI Gateways | Hard |
| Q0716 | [Token counting and cost metering per tenant](0716_token_counting_and_cost_metering_per_tenant/README.md) | Cloud AI Gateways | Medium |
| Q0717 | [Semantic caching at the AI gateway layer](0717_semantic_caching_at_the_ai_gateway_layer/README.md) | Cloud AI Gateways | Medium |
| Q0718 | [Weighted round-robin load balancing across cloud LLM regions](0718_weighted_round_robin_load_balancing_across_cloud_llm_regions/README.md) | Cloud AI Gateways | Medium |
| Q0719 | [Streaming responses: Time To First Token vs Throughput](0719_streaming_responses_time_to_first_token_vs_throughput/README.md) | Cloud AI Gateways | Medium |
| Q0720 | [Zero Data Retention agreements in regulated cloud AI](0720_zero_data_retention_agreements_in_regulated_cloud_ai/README.md) | Cloud AI Compliance | Hard |
| Q0721 | [Customer-Managed Keys with Azure Key Vault and AWS KMS](0721_customer_managed_keys_with_azure_key_vault_and_aws_kms/README.md) | Cloud AI Compliance | Hard |
| Q0722 | [Data residency and sovereignty in the UK and EU](0722_data_residency_and_sovereignty_in_the_uk_and_eu/README.md) | Cloud AI Compliance | Medium |
| Q0723 | [Disaster Recovery: Active-Active versus Active-Passive multi-region cloud AI](0723_disaster_recovery_active_active_versus_active_passive_multi/README.md) | Cloud AI Architecture | Hard |
| Q0724 | [Cloud egress cost optimization and dedicated network peering](0724_cloud_egress_cost_optimization_and_dedicated_network_peering/README.md) | Cloud AI Architecture | Medium |
| Q0725 | [Continuous batching vs static batching in LLM inference engines](0725_continuous_batching_vs_static_batching_in_llm_inference/README.md) | GPU Serving | Medium |
| Q0726 | [PagedAttention and KV cache memory allocation](0726_pagedattention_and_kv_cache_memory_allocation/README.md) | GPU Serving | Hard |
| Q0727 | [Simulating PagedAttention block table allocation in Python](0727_simulating_pagedattention_block_table_allocation_in_python/README.md) | GPU Serving | Hard |
| Q0728 | [GPU quantization: FP8, AWQ, GPTQ, INT4 for enterprise inference](0728_gpu_quantization_fp8_awq_gptq_int4_for_enterprise_inference/README.md) | GPU Serving | Medium |
| Q0729 | [vLLM architecture and deployment on Kubernetes](0729_vllm_architecture_and_deployment_on_kubernetes/README.md) | GPU Serving | Medium |
| Q0730 | [TensorRT-LLM optimization for NVIDIA GPUs](0730_tensorrt_llm_optimization_for_nvidia_gpus/README.md) | GPU Serving | Medium |
| Q0731 | [Autoscaling inference pods with KEDA based on queue depth](0731_autoscaling_inference_pods_with_keda_based_on_queue_depth/README.md) | Elastic Compute | Hard |
| Q0732 | [Implementing a queue-depth autoscaling simulator in Python](0732_implementing_a_queue_depth_autoscaling_simulator_in_python/README.md) | Elastic Compute | Hard |
| Q0733 | [Spot instances for batch offline LLM inference](0733_spot_instances_for_batch_offline_llm_inference/README.md) | Elastic Compute | Medium |
| Q0734 | [Checkpoint resumption for long-running batch inference](0734_checkpoint_resumption_for_long_running_batch_inference/README.md) | Elastic Compute | Medium |
| Q0735 | [Multi-LoRA adapter serving on a single base model](0735_multi_lora_adapter_serving_on_a_single_base_model/README.md) | Elastic Compute | Hard |
| Q0736 | [Implementing a Multi-LoRA adapter router in Python](0736_implementing_a_multi_lora_adapter_router_in_python/README.md) | Elastic Compute | Hard |
| Q0737 | [Speculative decoding: draft model plus target model acceleration](0737_speculative_decoding_draft_model_plus_target_model/README.md) | GPU Serving | Hard |
| Q0738 | [Simulating speculative decoding acceptance logic in Python](0738_simulating_speculative_decoding_acceptance_logic_in_python/README.md) | GPU Serving | Hard |
| Q0739 | [Prefix caching and prompt caching across multi-turn sessions](0739_prefix_caching_and_prompt_caching_across_multi_turn_sessions/README.md) | GPU Serving | Medium |
| Q0740 | [Implementing prompt prefix cache matching in Python](0740_implementing_prompt_prefix_cache_matching_in_python/README.md) | GPU Serving | Medium |
| Q0741 | [Triton Inference Server for multi-model serving](0741_triton_inference_server_for_multi_model_serving/README.md) | GPU Serving | Medium |
| Q0742 | [Model deprecation and graceful version migration pipelines](0742_model_deprecation_and_graceful_version_migration_pipelines/README.md) | Cloud AI Gateways | Medium |
| Q0743 | [Circuit breaker pattern for failing cloud AI endpoints](0743_circuit_breaker_pattern_for_failing_cloud_ai_endpoints/README.md) | Cloud AI Gateways | Medium |
| Q0744 | [Implementing a stateful Circuit Breaker in Python](0744_implementing_a_stateful_circuit_breaker_in_python/README.md) | Cloud AI Gateways | Medium |
| Q0745 | [Per-tenant rate limiting with sliding window in Python](0745_per_tenant_rate_limiting_with_sliding_window_in_python/README.md) | Cloud AI Gateways | Medium |
| Q0746 | [Request deduplication for identical in-flight prompts](0746_request_deduplication_for_identical_in_flight_prompts/README.md) | Cloud AI Gateways | Medium |
| Q0747 | [Implementing an in-flight single-flight request coalescer](0747_implementing_an_in_flight_single_flight_request_coalescer/README.md) | Cloud AI Gateways | Hard |
| Q0748 | [Health checks and canary deployments for LLM services](0748_health_checks_and_canary_deployments_for_llm_services/README.md) | Cloud AI Gateways | Medium |
| Q0749 | [Distributed tracing with OpenTelemetry GenAI semantic conventions](0749_distributed_tracing_with_opentelemetry_genai_semantic/README.md) | Cloud AI Gateways | Medium |
| Q0750 | [Building an OpenTelemetry span formatter for LLM invocations](0750_building_an_opentelemetry_span_formatter_for_llm_invocations/README.md) | Cloud AI Gateways | Medium |
| Q0751 | [Azure OpenAI Assistants API with Code Interpreter in banking](0751_azure_openai_assistants_api_with_code_interpreter_in_banking/README.md) | Azure OpenAI | Medium |
| Q0752 | [Asynchronous file batch analysis pipeline with Azure OpenAI](0752_asynchronous_file_batch_analysis_pipeline_with_azure_openai/README.md) | Azure OpenAI | Medium |
| Q0753 | [Fine-tuning models on Azure OpenAI with custom enterprise datasets](0753_fine_tuning_models_on_azure_openai_with_custom_enterprise/README.md) | Azure OpenAI | Medium |
| Q0754 | [Preparing JSONL training data for Azure OpenAI fine-tuning](0754_preparing_jsonl_training_data_for_azure_openai_fine_tuning/README.md) | Azure OpenAI | Medium |
| Q0755 | [Multi-tenant quota management across business units](0755_multi_tenant_quota_management_across_business_units/README.md) | Azure OpenAI | Medium |
| Q0756 | [Simulating a dynamic TPM quota allocator in Python](0756_simulating_a_dynamic_tpm_quota_allocator_in_python/README.md) | Azure OpenAI | Medium |
| Q0757 | [Azure Monitor and Application Insights for LLM latency alerting](0757_azure_monitor_and_application_insights_for_llm_latency/README.md) | Azure OpenAI | Medium |
| Q0758 | [Custom log analytics query parser for Azure OpenAI](0758_custom_log_analytics_query_parser_for_azure_openai/README.md) | Azure OpenAI | Medium |
| Q0759 | [Azure OpenAI on Foundry Models and model catalog integration](0759_azure_openai_on_foundry_models_and_model_catalog_integration/README.md) | Azure OpenAI | Medium |
| Q0760 | [Data Zone Standard: architecture and legal boundary verification](0760_data_zone_standard_architecture_and_legal_boundary/README.md) | Azure OpenAI | Medium |
| Q0761 | [Network routing: ExpressRoute versus public internet latency](0761_network_routing_expressroute_versus_public_internet_latency/README.md) | Cloud AI Architecture | Medium |
| Q0762 | [Azure Policy enforcement: preventing public IP creation on AI endpoints](0762_azure_policy_enforcement_preventing_public_ip_creation_on/README.md) | Cloud AI Architecture | Medium |
| Q0763 | [Azure OpenAI token-bucket rate limiter with burst multiplier](0763_azure_openai_token_bucket_rate_limiter_with_burst_multiplier/README.md) | Azure OpenAI | Medium |
| Q0764 | [Content filtering bypass review process in regulated banks](0764_content_filtering_bypass_review_process_in_regulated_banks/README.md) | Azure OpenAI | Medium |
| Q0765 | [Disaster Recovery runbook: automated regional failover for Azure OpenAI](0765_disaster_recovery_runbook_automated_regional_failover_for/README.md) | Cloud AI Architecture | Hard |
| Q0766 | [Amazon Bedrock Provisioned Throughput: Model Units and capacity reservation](0766_amazon_bedrock_provisioned_throughput_model_units_and/README.md) | AWS Bedrock | Medium |
| Q0767 | [Provisioned Throughput cost vs On-Demand breakeven calculator](0767_provisioned_throughput_cost_vs_on_demand_breakeven/README.md) | AWS Bedrock | Medium |
| Q0768 | [Custom Model Import in Amazon Bedrock](0768_custom_model_import_in_amazon_bedrock/README.md) | AWS Bedrock | Medium |
| Q0769 | [Bedrock Guardrails contextual grounding evaluation](0769_bedrock_guardrails_contextual_grounding_evaluation/README.md) | AWS Bedrock | Medium |
| Q0770 | [Evaluating hallucination scores against ground-truth context in Python](0770_evaluating_hallucination_scores_against_ground_truth/README.md) | AWS Bedrock | Medium |
| Q0771 | [Knowledge Bases hybrid search: BM25 plus OpenSearch vector similarity](0771_knowledge_bases_hybrid_search_bm25_plus_opensearch_vector/README.md) | AWS Bedrock | Medium |
| Q0772 | [Reciprocal Rank Fusion for Bedrock Knowledge Bases](0772_reciprocal_rank_fusion_for_bedrock_knowledge_bases/README.md) | AWS Bedrock | Medium |
| Q0773 | [Bedrock Agents action group Lambda implementation](0773_bedrock_agents_action_group_lambda_implementation/README.md) | AWS Bedrock | Medium |
| Q0774 | [Formatting Bedrock Agent Lambda response payloads in Python](0774_formatting_bedrock_agent_lambda_response_payloads_in_python/README.md) | AWS Bedrock | Medium |
| Q0775 | [IAM policies for least-privilege Bedrock model access](0775_iam_policies_for_least_privilege_bedrock_model_access/README.md) | AWS Bedrock | Medium |
| Q0776 | [Validating Bedrock IAM policy statements in Python](0776_validating_bedrock_iam_policy_statements_in_python/README.md) | AWS Bedrock | Medium |
| Q0777 | [Bedrock CloudTrail event logging for compliance audits](0777_bedrock_cloudtrail_event_logging_for_compliance_audits/README.md) | AWS Bedrock | Medium |
| Q0778 | [Parsing CloudTrail Bedrock event logs in Python](0778_parsing_cloudtrail_bedrock_event_logs_in_python/README.md) | AWS Bedrock | Medium |
| Q0779 | [Cross-Region Inference profile latency monitoring](0779_cross_region_inference_profile_latency_monitoring/README.md) | AWS Bedrock | Medium |
| Q0780 | [Measuring CRI latency variance and jitter in Python](0780_measuring_cri_latency_variance_and_jitter_in_python/README.md) | AWS Bedrock | Medium |
| Q0781 | [Dual-cloud AI gateway architecture: Azure plus AWS Active-Active](0781_dual_cloud_ai_gateway_architecture_azure_plus_aws_active/README.md) | Multi-Cloud AI Gateways | Hard |
| Q0782 | [High-availability multi-provider client with retry and fallback](0782_high_availability_multi_provider_client_with_retry_and/README.md) | Multi-Cloud AI Gateways | Hard |
| Q0783 | [Cost arbitrage: routing non-critical tasks to lowest-cost provider](0783_cost_arbitrage_routing_non_critical_tasks_to_lowest_cost/README.md) | Multi-Cloud AI Gateways | Medium |
| Q0784 | [Cost vs quality routing engine in Python](0784_cost_vs_quality_routing_engine_in_python/README.md) | Multi-Cloud AI Gateways | Medium |
| Q0785 | [Streaming SSE proxy with backpressure handling](0785_streaming_sse_proxy_with_backpressure_handling/README.md) | Multi-Cloud AI Gateways | Hard |
| Q0786 | [Client-side timeout strategies for streaming vs non-streaming calls](0786_client_side_timeout_strategies_for_streaming_vs_non/README.md) | Multi-Cloud AI Gateways | Medium |
| Q0787 | [Adaptive timeout manager based on expected token count](0787_adaptive_timeout_manager_based_on_expected_token_count/README.md) | Multi-Cloud AI Gateways | Medium |
| Q0788 | [Token estimation using model tokenizers before cloud API dispatch](0788_token_estimation_using_model_tokenizers_before_cloud_api/README.md) | Multi-Cloud AI Gateways | Medium |
| Q0789 | [Fast token counter and budget validator in Python](0789_fast_token_counter_and_budget_validator_in_python/README.md) | Multi-Cloud AI Gateways | Medium |
| Q0790 | [Key rotation and credential reloading without service restart](0790_key_rotation_and_credential_reloading_without_service/README.md) | Multi-Cloud AI Gateways | Medium |
| Q0791 | [In-memory rotating secret provider in Python](0791_in_memory_rotating_secret_provider_in_python/README.md) | Multi-Cloud AI Gateways | Medium |
| Q0792 | [Canary traffic splitter for model A/B testing in Python](0792_canary_traffic_splitter_for_model_a_b_testing_in_python/README.md) | Multi-Cloud AI Gateways | Medium |
| Q0793 | [Error classification: transient vs terminal cloud AI errors](0793_error_classification_transient_vs_terminal_cloud_ai_errors/README.md) | Multi-Cloud AI Gateways | Medium |
| Q0794 | [Automated error categorizer for cloud HTTP responses in Python](0794_automated_error_categorizer_for_cloud_http_responses_in/README.md) | Multi-Cloud AI Gateways | Medium |
| Q0795 | [Rate limit header parser: Retry-After, X-RateLimit-Reset](0795_rate_limit_header_parser_retry_after_x_ratelimit_reset/README.md) | Multi-Cloud AI Gateways | Medium |
| Q0796 | [Load shedding under extreme cloud AI gateway concurrency](0796_load_shedding_under_extreme_cloud_ai_gateway_concurrency/README.md) | Multi-Cloud AI Gateways | Medium |
| Q0797 | [Concurrency-limited request dispatcher with queue reject in Python](0797_concurrency_limited_request_dispatcher_with_queue_reject_in/README.md) | Multi-Cloud AI Gateways | Hard |
| Q0798 | [Audit trail persistence to immutable storage](0798_audit_trail_persistence_to_immutable_storage/README.md) | Cloud AI Compliance | Hard |
| Q0799 | [Cryptographic audit batch signer in Python](0799_cryptographic_audit_batch_signer_in_python/README.md) | Cloud AI Compliance | Medium |
| Q0800 | [Comprehensive end-to-end integration test of a multi-cloud AI gateway](0800_comprehensive_end_to_end_integration_test_of_a_multi_cloud/README.md) | Multi-Cloud AI Gateways | Hard |

[← All sections](../README.md)
