# MCP, A2A, Agent Skills & Personal AI Assistants

Model Context Protocol (tools, resources, prompts, transports, authorization and the stateless 2026-07-28 revision), the A2A protocol v1.0 (Agent Cards, tasks, parts, streaming, push notifications), Agent Skills, and personal-assistant design, with JSON-RPC and protocol handlers you can run.

Maps to the job description: Knowledge of A2A, MCP, AI skills development, personal AI assistants and agentic orchestrators.

Q0601–Q0700 · 100 questions · Easy 11 · Medium 68 · Hard 21

| # | Question | Topic | Difficulty |
|---|---|---|---|
| Q0601 | [What the Model Context Protocol is and why it exists](0601_what_the_model_context_protocol_is_and_why_it_exists/README.md) | MCP foundations | Easy |
| Q0602 | [MCP architecture: hosts, clients and servers](0602_mcp_architecture_hosts_clients_and_servers/README.md) | MCP foundations | Easy |
| Q0603 | [JSON-RPC 2.0 framing in MCP](0603_json_rpc_2_0_framing_in_mcp/README.md) | MCP foundations | Easy |
| Q0604 | [MCP transports: Stdio versus SSE versus Streamable HTTP](0604_mcp_transports_stdio_versus_sse_versus_streamable_http/README.md) | MCP foundations | Medium |
| Q0605 | [MCP 2026-07-28 stateless revision](0605_mcp_2026_07_28_stateless_revision/README.md) | MCP foundations | Medium |
| Q0606 | [MCP initialize lifecycle and handshake](0606_mcp_initialize_lifecycle_and_handshake/README.md) | MCP foundations | Medium |
| Q0607 | [Capability negotiation in MCP](0607_capability_negotiation_in_mcp/README.md) | MCP foundations | Medium |
| Q0608 | [MCP ping and liveness detection](0608_mcp_ping_and_liveness_detection/README.md) | MCP foundations | Easy |
| Q0609 | [MCP standard and custom error codes](0609_mcp_standard_and_custom_error_codes/README.md) | MCP foundations | Medium |
| Q0610 | [Building a minimal JSON-RPC 2.0 message parser and builder](0610_building_a_minimal_json_rpc_2_0_message_parser_and_builder/README.md) | MCP foundations | Medium |
| Q0611 | [Parsing stdio stream into JSON-RPC messages](0611_parsing_stdio_stream_into_json_rpc_messages/README.md) | MCP foundations | Medium |
| Q0612 | [Notification versus Request in MCP](0612_notification_versus_request_in_mcp/README.md) | MCP foundations | Easy |
| Q0613 | [Handling client and server cancellations in MCP](0613_handling_client_and_server_cancellations_in_mcp/README.md) | MCP foundations | Medium |
| Q0614 | [What are MCP Tools](0614_what_are_mcp_tools/README.md) | MCP tools | Easy |
| Q0615 | [Designing a tool schema with JSON Schema](0615_designing_a_tool_schema_with_json_schema/README.md) | MCP tools | Medium |
| Q0616 | [Listing tools with tools/list and pagination](0616_listing_tools_with_tools_list_and_pagination/README.md) | MCP tools | Medium |
| Q0617 | [Handling tools/call requests](0617_handling_tools_call_requests/README.md) | MCP tools | Medium |
| Q0618 | [Tool response structure: text, image and resource contents](0618_tool_response_structure_text_image_and_resource_contents/README.md) | MCP tools | Medium |
| Q0619 | [Reporting tool errors: isError flag versus JSON-RPC error](0619_reporting_tool_errors_iserror_flag_versus_json_rpc_error/README.md) | MCP tools | Medium |
| Q0620 | [Validating tool arguments against Pydantic models](0620_validating_tool_arguments_against_pydantic_models/README.md) | MCP tools | Medium |
| Q0621 | [Implementing a tool execution timeout](0621_implementing_a_tool_execution_timeout/README.md) | MCP tools | Medium |
| Q0622 | [Building an in-memory MCP tool registry and dispatcher](0622_building_an_in_memory_mcp_tool_registry_and_dispatcher/README.md) | MCP tools | Medium |
| Q0623 | [Implementing tool output truncation and token budgeting](0623_implementing_tool_output_truncation_and_token_budgeting/README.md) | MCP tools | Medium |
| Q0624 | [Dynamic tool registration and tools/list_changed notification](0624_dynamic_tool_registration_and_tools_list_changed/README.md) | MCP tools | Medium |
| Q0625 | [Securing filesystem access in an MCP file server](0625_securing_filesystem_access_in_an_mcp_file_server/README.md) | MCP tools | Hard |
| Q0626 | [Sandboxing database query execution in an SQL MCP server](0626_sandboxing_database_query_execution_in_an_sql_mcp_server/README.md) | MCP tools | Hard |
| Q0627 | [Handling parallel tool calls across multiple MCP servers](0627_handling_parallel_tool_calls_across_multiple_mcp_servers/README.md) | MCP tools | Hard |
| Q0628 | [Rate limiting MCP tool calls with token bucket](0628_rate_limiting_mcp_tool_calls_with_token_bucket/README.md) | MCP tools | Medium |
| Q0629 | [Caching idempotent MCP tool call responses](0629_caching_idempotent_mcp_tool_call_responses/README.md) | MCP tools | Medium |
| Q0630 | [Converting LangChain tools to MCP tool definitions](0630_converting_langchain_tools_to_mcp_tool_definitions/README.md) | MCP tools | Medium |
| Q0631 | [What are MCP Resources and how do they differ from Tools](0631_what_are_mcp_resources_and_how_do_they_differ_from_tools/README.md) | MCP resources | Easy |
| Q0632 | [MCP resource URI schemes and structure](0632_mcp_resource_uri_schemes_and_structure/README.md) | MCP resources | Medium |
| Q0633 | [Listing resources with resources/list and pagination](0633_listing_resources_with_resources_list_and_pagination/README.md) | MCP resources | Medium |
| Q0634 | [Reading resource content with resources/read](0634_reading_resource_content_with_resources_read/README.md) | MCP resources | Medium |
| Q0635 | [Implementing text versus binary resources](0635_implementing_text_versus_binary_resources/README.md) | MCP resources | Medium |
| Q0636 | [Resource templates with RFC 6570 URI templates](0636_resource_templates_with_rfc_6570_uri_templates/README.md) | MCP resources | Medium |
| Q0637 | [Subscribing to resource updates with resources/subscribe](0637_subscribing_to_resource_updates_with_resources_subscribe/README.md) | MCP resources | Medium |
| Q0638 | [Emitting notifications/resources/updated on resource mutation](0638_emitting_notifications_resources_updated_on_resource/README.md) | MCP resources | Medium |
| Q0639 | [Implementing an in-memory resource store with MIME types](0639_implementing_an_in_memory_resource_store_with_mime_types/README.md) | MCP resources | Medium |
| Q0640 | [Access control on sensitive resources by URI pattern](0640_access_control_on_sensitive_resources_by_uri_pattern/README.md) | MCP resources | Hard |
| Q0641 | [What are MCP Prompts and use cases](0641_what_are_mcp_prompts_and_use_cases/README.md) | MCP prompts | Easy |
| Q0642 | [Listing prompt templates with prompts/list](0642_listing_prompt_templates_with_prompts_list/README.md) | MCP prompts | Medium |
| Q0643 | [Getting prompt messages with prompts/get and arguments](0643_getting_prompt_messages_with_prompts_get_and_arguments/README.md) | MCP prompts | Medium |
| Q0644 | [Mapping prompt messages to LLM roles](0644_mapping_prompt_messages_to_llm_roles/README.md) | MCP prompts | Medium |
| Q0645 | [Embedding resource content into MCP prompt messages](0645_embedding_resource_content_into_mcp_prompt_messages/README.md) | MCP prompts | Medium |
| Q0646 | [Dynamic prompt template evaluation with parameter validation](0646_dynamic_prompt_template_evaluation_with_parameter_validation/README.md) | MCP prompts | Medium |
| Q0647 | [Building an in-memory MCP prompt catalog](0647_building_an_in_memory_mcp_prompt_catalog/README.md) | MCP prompts | Medium |
| Q0648 | [Notifying clients with notifications/prompts/list_changed](0648_notifying_clients_with_notifications_prompts_list_changed/README.md) | MCP prompts | Easy |
| Q0649 | [Multi-server tool aggregation in an MCP client](0649_multi_server_tool_aggregation_in_an_mcp_client/README.md) | MCP architecture | Hard |
| Q0650 | [Namespacing tools across multiple MCP servers](0650_namespacing_tools_across_multiple_mcp_servers/README.md) | MCP architecture | Medium |
| Q0651 | [What the A2A protocol is and why it exists](0651_what_the_a2a_protocol_is_and_why_it_exists/README.md) | A2A foundations | Easy |
| Q0652 | [MCP versus A2A: comparative architectural analysis](0652_mcp_versus_a2a_comparative_architectural_analysis/README.md) | A2A foundations | Medium |
| Q0653 | [A2A Agent Card specification and discovery](0653_a2a_agent_card_specification_and_discovery/README.md) | A2A protocol | Medium |
| Q0654 | [Validating an A2A Agent Card against JSON schema](0654_validating_an_a2a_agent_card_against_json_schema/README.md) | A2A protocol | Medium |
| Q0655 | [A2A Task state machine and lifecycle](0655_a2a_task_state_machine_and_lifecycle/README.md) | A2A protocol | Medium |
| Q0656 | [A2A Task creation and submission](0656_a2a_task_creation_and_submission/README.md) | A2A protocol | Medium |
| Q0657 | [A2A Parts: TextPart, FilePart, DataPart](0657_a2a_parts_textpart_filepart_datapart/README.md) | A2A protocol | Medium |
| Q0658 | [Handling the needs_input state in A2A tasks](0658_handling_the_needs_input_state_in_a2a_tasks/README.md) | A2A protocol | Medium |
| Q0659 | [A2A Server-Sent Events (SSE) streaming of task progress](0659_a2a_server_sent_events_sse_streaming_of_task_progress/README.md) | A2A protocol | Medium |
| Q0660 | [Parsing A2A streaming event frames in Python](0660_parsing_a2a_streaming_event_frames_in_python/README.md) | A2A protocol | Medium |
| Q0661 | [A2A push notifications and webhook delivery](0661_a2a_push_notifications_and_webhook_delivery/README.md) | A2A protocol | Medium |
| Q0662 | [A2A task cancellation and compensation](0662_a2a_task_cancellation_and_compensation/README.md) | A2A protocol | Medium |
| Q0663 | [A2A thread and context propagation](0663_a2a_thread_and_context_propagation/README.md) | A2A protocol | Medium |
| Q0664 | [A2A task idempotency with client tokens](0664_a2a_task_idempotency_with_client_tokens/README.md) | A2A protocol | Medium |
| Q0665 | [Building an in-memory A2A task engine](0665_building_an_in_memory_a2a_task_engine/README.md) | A2A protocol | Hard |
| Q0666 | [Supervisor-Worker topology using A2A protocol](0666_supervisor_worker_topology_using_a2a_protocol/README.md) | A2A orchestration | Hard |
| Q0667 | [Implementing an A2A Peer-to-Peer messaging bus](0667_implementing_an_a2a_peer_to_peer_messaging_bus/README.md) | A2A orchestration | Hard |
| Q0668 | [Contract Net Protocol in A2A multi-agent systems](0668_contract_net_protocol_in_a2a_multi_agent_systems/README.md) | A2A orchestration | Hard |
| Q0669 | [Implementing A2A Call for Proposal and Bidding](0669_implementing_a2a_call_for_proposal_and_bidding/README.md) | A2A orchestration | Hard |
| Q0670 | [Multi-Agent debate and consensus protocol](0670_multi_agent_debate_and_consensus_protocol/README.md) | A2A orchestration | Hard |
| Q0671 | [A2A deadlocks and cycle detection in agent delegation](0671_a2a_deadlocks_and_cycle_detection_in_agent_delegation/README.md) | A2A orchestration | Hard |
| Q0672 | [Shared blackboard architecture for A2A collaboration](0672_shared_blackboard_architecture_for_a2a_collaboration/README.md) | A2A orchestration | Hard |
| Q0673 | [Error handling and failover in A2A worker pools](0673_error_handling_and_failover_in_a2a_worker_pools/README.md) | A2A orchestration | Medium |
| Q0674 | [Tracing multi-agent A2A message chains with correlation IDs](0674_tracing_multi_agent_a2a_message_chains_with_correlation_ids/README.md) | A2A orchestration | Medium |
| Q0675 | [Evaluating performance and communication cost in A2A swarms](0675_evaluating_performance_and_communication_cost_in_a2a_swarms/README.md) | A2A orchestration | Medium |
| Q0676 | [What is an Agent Skill and how does it differ from a Tool](0676_what_is_an_agent_skill_and_how_does_it_differ_from_a_tool/README.md) | Agent skills | Easy |
| Q0677 | [Anatomical structure of an enterprise Agent Skill](0677_anatomical_structure_of_an_enterprise_agent_skill/README.md) | Agent skills | Medium |
| Q0678 | [Progressive disclosure pattern for agent skills](0678_progressive_disclosure_pattern_for_agent_skills/README.md) | Agent skills | Medium |
| Q0679 | [Loading skills on demand based on user intent](0679_loading_skills_on_demand_based_on_user_intent/README.md) | Agent skills | Medium |
| Q0680 | [Validating skill configuration and metadata with Pydantic](0680_validating_skill_configuration_and_metadata_with_pydantic/README.md) | Agent skills | Medium |
| Q0681 | [Sandboxing skill execution in isolated runtimes](0681_sandboxing_skill_execution_in_isolated_runtimes/README.md) | Agent skills | Hard |
| Q0682 | [Skill composition: combining multiple skills for compound tasks](0682_skill_composition_combining_multiple_skills_for_compound/README.md) | Agent skills | Medium |
| Q0683 | [Skill versioning, deprecation and rollback in production](0683_skill_versioning_deprecation_and_rollback_in_production/README.md) | Agent skills | Medium |
| Q0684 | [Auditing skill inputs and generated artifacts](0684_auditing_skill_inputs_and_generated_artifacts/README.md) | Agent skills | Medium |
| Q0685 | [Implementing a dynamic Skill Registry and loader](0685_implementing_a_dynamic_skill_registry_and_loader/README.md) | Agent skills | Medium |
| Q0686 | [Architecture of an enterprise Personal AI Assistant](0686_architecture_of_an_enterprise_personal_ai_assistant/README.md) | Personal AI assistants | Medium |
| Q0687 | [Layered memory in personal assistants: working, episodic, semantic](0687_layered_memory_in_personal_assistants_working_episodic/README.md) | Personal AI assistants | Hard |
| Q0688 | [Semantic profile store for user preferences and entity memory](0688_semantic_profile_store_for_user_preferences_and_entity/README.md) | Personal AI assistants | Medium |
| Q0689 | [Intent routing between local tools and specialized A2A agents](0689_intent_routing_between_local_tools_and_specialized_a2a/README.md) | Personal AI assistants | Hard |
| Q0690 | [Calendar and meeting management via personal assistant](0690_calendar_and_meeting_management_via_personal_assistant/README.md) | Personal AI assistants | Medium |
| Q0691 | [Proactive vs reactive assistant behavior: triggers and schedules](0691_proactive_vs_reactive_assistant_behavior_triggers_and/README.md) | Personal AI assistants | Medium |
| Q0692 | [Human-in-the-loop confirmation UX for personal assistant actions](0692_human_in_the_loop_confirmation_ux_for_personal_assistant/README.md) | Personal AI assistants | Medium |
| Q0693 | [Handling multi-turn conversational context drift](0693_handling_multi_turn_conversational_context_drift/README.md) | Personal AI assistants | Medium |
| Q0694 | [Cross-channel personal assistant: Teams, Slack, Email, Web](0694_cross_channel_personal_assistant_teams_slack_email_web/README.md) | Personal AI assistants | Medium |
| Q0695 | [Privacy boundaries and sensitive personal data isolation](0695_privacy_boundaries_and_sensitive_personal_data_isolation/README.md) | Personal AI assistants | Medium |
| Q0696 | [Zero-trust architecture for enterprise MCP and A2A networks](0696_zero_trust_architecture_for_enterprise_mcp_and_a2a_networks/README.md) | MCP and A2A security | Hard |
| Q0697 | [Preventing Prompt Injection across A2A agent boundaries](0697_preventing_prompt_injection_across_a2a_agent_boundaries/README.md) | MCP and A2A security | Hard |
| Q0698 | [PII scrubbing and data loss prevention at tool gateways](0698_pii_scrubbing_and_data_loss_prevention_at_tool_gateways/README.md) | MCP and A2A security | Hard |
| Q0699 | [Audit logging for regulatory compliance](0699_audit_logging_for_regulatory_compliance/README.md) | MCP and A2A security | Hard |
| Q0700 | [End-to-end integration test of an MCP tool within an A2A agent](0700_end_to_end_integration_test_of_an_mcp_tool_within_an_a2a/README.md) | MCP and A2A security | Hard |

[← All sections](../README.md)
