# LangGraph & LangChain in Practice

LangGraph 1.x hands-on: StateGraph and reducers, conditional edges, Send and Command, subgraphs, checkpointers and threads, interrupts for human-in-the-loop, streaming modes, the Store for long-term memory, time travel, and LangChain 1.x agents and middleware. Snippets run against the installed langgraph package.

Maps to the job description: Proficiency building agents with LangGraph.

Q0501–Q0600 · 100 questions · Easy 16 · Medium 75 · Hard 9

| # | Question | Topic | Difficulty |
|---|---|---|---|
| Q0501 | [What LangGraph is and why use it](0501_what_langgraph_is_and_why_use_it/README.md) | LangGraph foundations | Easy |
| Q0502 | [LangGraph versus LangChain](0502_langgraph_versus_langchain/README.md) | LangGraph foundations | Easy |
| Q0503 | [State, nodes and edges](0503_state_nodes_and_edges/README.md) | LangGraph foundations | Easy |
| Q0504 | [Your first StateGraph](0504_your_first_stategraph/README.md) | Graph API | Easy |
| Q0505 | [Reducers and state channels](0505_reducers_and_state_channels/README.md) | Graph API | Medium |
| Q0506 | [Custom reducer for merging dictionaries](0506_custom_reducer_for_merging_dictionaries/README.md) | Graph API | Medium |
| Q0507 | [MessagesState and add_messages semantics](0507_messagesstate_and_add_messages_semantics/README.md) | Messages | Medium |
| Q0508 | [Remove messages with RemoveMessage](0508_remove_messages_with_removemessage/README.md) | Messages | Medium |
| Q0509 | [Conditional edges for routing](0509_conditional_edges_for_routing/README.md) | Graph API | Easy |
| Q0510 | [Loops and the recursion limit](0510_loops_and_the_recursion_limit/README.md) | Graph API | Medium |
| Q0511 | [Update and route with Command](0511_update_and_route_with_command/README.md) | Graph API | Medium |
| Q0512 | [Map-reduce fan-out with Send](0512_map_reduce_fan_out_with_send/README.md) | Graph API | Medium |
| Q0513 | [Parallel branches and supersteps](0513_parallel_branches_and_supersteps/README.md) | Graph API | Medium |
| Q0514 | [Input and output schemas](0514_input_and_output_schemas/README.md) | Graph API | Medium |
| Q0515 | [Pydantic state validation](0515_pydantic_state_validation/README.md) | Graph API | Medium |
| Q0516 | [A ReAct agent graph with ToolNode](0516_a_react_agent_graph_with_toolnode/README.md) | Agents | Medium |
| Q0517 | [Custom routing after the model](0517_custom_routing_after_the_model/README.md) | Agents | Hard |
| Q0518 | [create_agent in LangChain 1.x](0518_create_agent_in_langchain_1_x/README.md) | LangChain agents | Medium |
| Q0519 | [Agent middleware in LangChain 1.x](0519_agent_middleware_in_langchain_1_x/README.md) | LangChain agents | Medium |
| Q0520 | [Human-in-the-loop middleware](0520_human_in_the_loop_middleware/README.md) | LangChain agents | Medium |
| Q0521 | [Checkpointers and threads](0521_checkpointers_and_threads/README.md) | Persistence | Medium |
| Q0522 | [Choosing a production checkpointer](0522_choosing_a_production_checkpointer/README.md) | Persistence | Medium |
| Q0523 | [Approval with interrupt()](0523_approval_with_interrupt/README.md) | Human-in-the-loop | Medium |
| Q0524 | [Nodes re-run from the start on resume](0524_nodes_re_run_from_the_start_on_resume/README.md) | Human-in-the-loop | Hard |
| Q0525 | [Validate human input in an interrupt loop](0525_validate_human_input_in_an_interrupt_loop/README.md) | Human-in-the-loop | Medium |
| Q0526 | [Static breakpoints with interrupt_before](0526_static_breakpoints_with_interrupt_before/README.md) | Human-in-the-loop | Medium |
| Q0527 | [Inspect state snapshots](0527_inspect_state_snapshots/README.md) | Persistence | Medium |
| Q0528 | [Time travel: replay and fork](0528_time_travel_replay_and_fork/README.md) | Persistence | Hard |
| Q0529 | [Correct an agent with update_state](0529_correct_an_agent_with_update_state/README.md) | Human-in-the-loop | Medium |
| Q0530 | [Streaming modes overview](0530_streaming_modes_overview/README.md) | Streaming | Easy |
| Q0531 | [Stream node updates to a client](0531_stream_node_updates_to_a_client/README.md) | Streaming | Easy |
| Q0532 | [Stream LLM tokens with messages mode](0532_stream_llm_tokens_with_messages_mode/README.md) | Streaming | Medium |
| Q0533 | [Custom progress events with get_stream_writer](0533_custom_progress_events_with_get_stream_writer/README.md) | Streaming | Medium |
| Q0534 | [Subgraphs as nodes](0534_subgraphs_as_nodes/README.md) | Composition | Medium |
| Q0535 | [Subgraph with its own state schema](0535_subgraph_with_its_own_state_schema/README.md) | Composition | Medium |
| Q0536 | [Runtime context with context_schema](0536_runtime_context_with_context_schema/README.md) | Configuration | Medium |
| Q0537 | [Long-term memory with the Store](0537_long_term_memory_with_the_store/README.md) | Memory | Medium |
| Q0538 | [Semantic search in the Store](0538_semantic_search_in_the_store/README.md) | Memory | Medium |
| Q0539 | [Use the store inside nodes](0539_use_the_store_inside_nodes/README.md) | Memory | Medium |
| Q0540 | [Retry policies on nodes](0540_retry_policies_on_nodes/README.md) | Reliability | Medium |
| Q0541 | [Cache expensive nodes with CachePolicy](0541_cache_expensive_nodes_with_cachepolicy/README.md) | Performance | Medium |
| Q0542 | [Durability modes](0542_durability_modes/README.md) | Persistence | Medium |
| Q0543 | [Functional API with entrypoint and task](0543_functional_api_with_entrypoint_and_task/README.md) | Functional API | Medium |
| Q0544 | [Functional API versus Graph API](0544_functional_api_versus_graph_api/README.md) | Functional API | Easy |
| Q0545 | [Remaining steps for graceful stops](0545_remaining_steps_for_graceful_stops/README.md) | Reliability | Medium |
| Q0546 | [Supervisor pattern in LangGraph](0546_supervisor_pattern_in_langgraph/README.md) | Multi-agent | Medium |
| Q0547 | [Handoffs between agents with Command](0547_handoffs_between_agents_with_command/README.md) | Multi-agent | Medium |
| Q0548 | [Plan-and-execute in LangGraph](0548_plan_and_execute_in_langgraph/README.md) | Planning | Medium |
| Q0549 | [Reflection loop in LangGraph](0549_reflection_loop_in_langgraph/README.md) | Self-refinement | Medium |
| Q0550 | [Guardrail nodes around an agent](0550_guardrail_nodes_around_an_agent/README.md) | Safety | Medium |
| Q0551 | [Tool errors with handle_tool_errors](0551_tool_errors_with_handle_tool_errors/README.md) | Agents | Medium |
| Q0552 | [Structured output node with validation and retry](0552_structured_output_node_with_validation_and_retry/README.md) | Structured output | Medium |
| Q0553 | [Trim history before the model call](0553_trim_history_before_the_model_call/README.md) | Context management | Medium |
| Q0554 | [Summarise long conversations in a graph](0554_summarise_long_conversations_in_a_graph/README.md) | Context management | Medium |
| Q0555 | [Visualise a graph as Mermaid](0555_visualise_a_graph_as_mermaid/README.md) | Tooling | Easy |
| Q0556 | [Unit-test nodes and graphs](0556_unit_test_nodes_and_graphs/README.md) | Testing | Medium |
| Q0557 | [Assert trajectories from streamed updates](0557_assert_trajectories_from_streamed_updates/README.md) | Testing | Medium |
| Q0558 | [Compile-time validation errors](0558_compile_time_validation_errors/README.md) | Graph API | Easy |
| Q0559 | [TypedDict, dataclass or Pydantic state](0559_typeddict_dataclass_or_pydantic_state/README.md) | State design | Easy |
| Q0560 | [What gets serialised in checkpoints](0560_what_gets_serialised_in_checkpoints/README.md) | Persistence | Medium |
| Q0561 | [Thread ids and multi-user safety](0561_thread_ids_and_multi_user_safety/README.md) | Security | Medium |
| Q0562 | [Deploying LangGraph applications](0562_deploying_langgraph_applications/README.md) | Deployment | Medium |
| Q0563 | [Assistants, threads and runs](0563_assistants_threads_and_runs/README.md) | LangGraph Server | Medium |
| Q0564 | [Double-texting strategies](0564_double_texting_strategies/README.md) | LangGraph Server | Medium |
| Q0565 | [Background runs and webhooks](0565_background_runs_and_webhooks/README.md) | LangGraph Server | Medium |
| Q0566 | [Cron jobs for agents](0566_cron_jobs_for_agents/README.md) | LangGraph Server | Easy |
| Q0567 | [Streaming agents to a web front end](0567_streaming_agents_to_a_web_front_end/README.md) | UX engineering | Medium |
| Q0568 | [Observability for LangGraph with LangSmith](0568_observability_for_langgraph_with_langsmith/README.md) | Observability | Medium |
| Q0569 | [Async nodes and ainvoke](0569_async_nodes_and_ainvoke/README.md) | Concurrency | Medium |
| Q0570 | [Limit parallelism with max_concurrency](0570_limit_parallelism_with_max_concurrency/README.md) | Concurrency | Medium |
| Q0571 | [Timeouts inside nodes](0571_timeouts_inside_nodes/README.md) | Reliability | Medium |
| Q0572 | [Error handling strategy in LangGraph](0572_error_handling_strategy_in_langgraph/README.md) | Reliability | Medium |
| Q0573 | [Model fallbacks with with_fallbacks](0573_model_fallbacks_with_with_fallbacks/README.md) | LangChain | Medium |
| Q0574 | [LCEL basics: composing runnables](0574_lcel_basics_composing_runnables/README.md) | LangChain | Easy |
| Q0575 | [RunnableParallel and RunnablePassthrough](0575_runnableparallel_and_runnablepassthrough/README.md) | LangChain | Medium |
| Q0576 | [ChatPromptTemplate and MessagesPlaceholder](0576_chatprompttemplate_and_messagesplaceholder/README.md) | LangChain | Medium |
| Q0577 | [Output parsers](0577_output_parsers/README.md) | LangChain | Easy |
| Q0578 | [Define tools with the @tool decorator](0578_define_tools_with_the_tool_decorator/README.md) | LangChain tools | Easy |
| Q0579 | [StructuredTool with a Pydantic args schema](0579_structuredtool_with_a_pydantic_args_schema/README.md) | LangChain tools | Medium |
| Q0580 | [The tool-calling message protocol](0580_the_tool_calling_message_protocol/README.md) | LangChain tools | Medium |
| Q0581 | [Message types and content blocks](0581_message_types_and_content_blocks/README.md) | LangChain | Medium |
| Q0582 | [Fake chat models for testing](0582_fake_chat_models_for_testing/README.md) | Testing | Easy |
| Q0583 | [Callbacks for logging and metrics](0583_callbacks_for_logging_and_metrics/README.md) | Observability | Medium |
| Q0584 | [Read configurable values inside nodes](0584_read_configurable_values_inside_nodes/README.md) | Configuration | Medium |
| Q0585 | [Provider-agnostic model initialisation](0585_provider_agnostic_model_initialisation/README.md) | Model-agnostic design | Medium |
| Q0586 | [Using MCP tools in LangGraph](0586_using_mcp_tools_in_langgraph/README.md) | MCP integration | Medium |
| Q0587 | [Exposing a LangGraph agent over A2A](0587_exposing_a_langgraph_agent_over_a2a/README.md) | A2A integration | Medium |
| Q0588 | [Migrating from create_react_agent to create_agent](0588_migrating_from_create_react_agent_to_create_agent/README.md) | Migration | Medium |
| Q0589 | [Migrating from LangChain 0.x to 1.x](0589_migrating_from_langchain_0_x_to_1_x/README.md) | Migration | Medium |
| Q0590 | [State design anti-patterns](0590_state_design_anti_patterns/README.md) | State design | Medium |
| Q0591 | [Performance tuning for LangGraph apps](0591_performance_tuning_for_langgraph_apps/README.md) | Performance | Medium |
| Q0592 | [Securing a LangGraph deployment](0592_securing_a_langgraph_deployment/README.md) | Security | Hard |
| Q0593 | [Debugging a stuck or looping graph](0593_debugging_a_stuck_or_looping_graph/README.md) | Debugging | Medium |
| Q0594 | [Side effects and replays in LangGraph](0594_side_effects_and_replays_in_langgraph/README.md) | Reliability | Hard |
| Q0595 | [Human-in-the-loop UX with LangGraph](0595_human_in_the_loop_ux_with_langgraph/README.md) | UX | Medium |
| Q0596 | [Evaluate a LangGraph agent](0596_evaluate_a_langgraph_agent/README.md) | Evaluation | Medium |
| Q0597 | [Design a LangGraph trade-break agent](0597_design_a_langgraph_trade_break_agent/README.md) | System design | Hard |
| Q0598 | [Design a LangGraph personal assistant](0598_design_a_langgraph_personal_assistant/README.md) | System design | Hard |
| Q0599 | [Rebooking workflow as a LangGraph graph](0599_rebooking_workflow_as_a_langgraph_graph/README.md) | LangGraph implementation | Hard |
| Q0600 | [Build a small agent end to end in an interview](0600_build_a_small_agent_end_to_end_in_an_interview/README.md) | LangGraph implementation | Hard |

[← All sections](../README.md)
