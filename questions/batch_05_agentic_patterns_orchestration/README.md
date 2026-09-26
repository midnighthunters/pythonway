# Agentic Patterns & Orchestration

ReAct, plan-and-execute, reflection, routing, supervisor and multi-agent designs, tool-calling loops, memory, human approval, loop guards, parallel tool execution, DAG orchestration and sagas with compensation, all coded against fake LLMs so the logic is testable.

Maps to the job description: Agentic systems with modern agentic frameworks; agentic orchestrators; turn early patterns into production-ready capabilities.

Q0401–Q0500 · 100 questions · Easy 6 · Medium 83 · Hard 11

| # | Question | Topic | Difficulty |
|---|---|---|---|
| Q0401 | [What makes a system agentic](0401_what_makes_a_system_agentic/README.md) | Agent foundations | Easy |
| Q0402 | [Workflows versus agents](0402_workflows_versus_agents/README.md) | Agent design | Medium |
| Q0403 | [Anatomy of an agent loop](0403_anatomy_of_an_agent_loop/README.md) | Agent foundations | Easy |
| Q0404 | [Minimal ReAct loop with a fake model](0404_minimal_react_loop_with_a_fake_model/README.md) | Agent loops | Medium |
| Q0405 | [Tool registry with schemas and permissions](0405_tool_registry_with_schemas_and_permissions/README.md) | Tooling | Medium |
| Q0406 | [Format tool results for the model](0406_format_tool_results_for_the_model/README.md) | Tooling | Medium |
| Q0407 | [Loop guards: steps, tokens and repetition](0407_loop_guards_steps_tokens_and_repetition/README.md) | Agent safety | Medium |
| Q0408 | [Detect cyclic tool-call patterns](0408_detect_cyclic_tool_call_patterns/README.md) | Agent safety | Medium |
| Q0409 | [Plan-and-execute agent](0409_plan_and_execute_agent/README.md) | Planning patterns | Medium |
| Q0410 | [Re-planning after a failed step](0410_re_planning_after_a_failed_step/README.md) | Planning patterns | Medium |
| Q0411 | [Reflection and self-correction for agents](0411_reflection_and_self_correction_for_agents/README.md) | Agent patterns | Medium |
| Q0412 | [Router pattern](0412_router_pattern/README.md) | Agent patterns | Easy |
| Q0413 | [Supervisor multi-agent pattern](0413_supervisor_multi_agent_pattern/README.md) | Multi-agent | Medium |
| Q0414 | [Hierarchical agents](0414_hierarchical_agents/README.md) | Multi-agent | Medium |
| Q0415 | [Handoffs versus agents-as-tools](0415_handoffs_versus_agents_as_tools/README.md) | Multi-agent | Medium |
| Q0416 | [Handoff loop with ping-pong protection](0416_handoff_loop_with_ping_pong_protection/README.md) | Multi-agent | Medium |
| Q0417 | [Parallel tool execution with timeouts](0417_parallel_tool_execution_with_timeouts/README.md) | Concurrency | Medium |
| Q0418 | [Fan-out and fan-in with bounded concurrency](0418_fan_out_and_fan_in_with_bounded_concurrency/README.md) | Concurrency | Medium |
| Q0419 | [Topological sort of a task graph](0419_topological_sort_of_a_task_graph/README.md) | Orchestration | Medium |
| Q0420 | [Execute a task graph with maximum parallelism](0420_execute_a_task_graph_with_maximum_parallelism/README.md) | Orchestration | Hard |
| Q0421 | [Critical path of an agent workflow](0421_critical_path_of_an_agent_workflow/README.md) | Orchestration | Medium |
| Q0422 | [Saga pattern for multi-step bookings](0422_saga_pattern_for_multi_step_bookings/README.md) | Transactions | Hard |
| Q0423 | [Idempotency keys for tool calls](0423_idempotency_keys_for_tool_calls/README.md) | Reliability | Medium |
| Q0424 | [Retry with exponential backoff and jitter](0424_retry_with_exponential_backoff_and_jitter/README.md) | Reliability | Medium |
| Q0425 | [Circuit breaker for flaky tools](0425_circuit_breaker_for_flaky_tools/README.md) | Reliability | Medium |
| Q0426 | [Timeouts and cancellation in agent runs](0426_timeouts_and_cancellation_in_agent_runs/README.md) | Concurrency | Medium |
| Q0427 | [Deadline propagation across nested calls](0427_deadline_propagation_across_nested_calls/README.md) | Concurrency | Medium |
| Q0428 | [Human approval gate for side effects](0428_human_approval_gate_for_side_effects/README.md) | Human-in-the-loop | Medium |
| Q0429 | [Approve, edit or reject a tool call](0429_approve_edit_or_reject_a_tool_call/README.md) | Human-in-the-loop | Medium |
| Q0430 | [Risk-tiered autonomy](0430_risk_tiered_autonomy/README.md) | Human-in-the-loop | Medium |
| Q0431 | [Designing agent state](0431_designing_agent_state/README.md) | State management | Medium |
| Q0432 | [Checkpoint and resume agent runs](0432_checkpoint_and_resume_agent_runs/README.md) | Durability | Medium |
| Q0433 | [Durable execution for long-running agents](0433_durable_execution_for_long_running_agents/README.md) | Durability | Medium |
| Q0434 | [Event-sourced agent state](0434_event_sourced_agent_state/README.md) | State management | Medium |
| Q0435 | [Short-term versus long-term agent memory](0435_short_term_versus_long_term_agent_memory/README.md) | Memory | Easy |
| Q0436 | [Episodic memory retrieval for agents](0436_episodic_memory_retrieval_for_agents/README.md) | Memory | Medium |
| Q0437 | [Scratchpads and working notes](0437_scratchpads_and_working_notes/README.md) | Context engineering | Medium |
| Q0438 | [Summarise tool outputs between steps](0438_summarise_tool_outputs_between_steps/README.md) | Context engineering | Medium |
| Q0439 | [Sub-agents to isolate context](0439_sub_agents_to_isolate_context/README.md) | Context engineering | Medium |
| Q0440 | [Token and cost budget manager](0440_token_and_cost_budget_manager/README.md) | Cost control | Medium |
| Q0441 | [Choose a model per step](0441_choose_a_model_per_step/README.md) | Cost control | Medium |
| Q0442 | [Final answer schema for agents](0442_final_answer_schema_for_agents/README.md) | Structured output | Medium |
| Q0443 | [Stop conditions for agents](0443_stop_conditions_for_agents/README.md) | Agent control | Easy |
| Q0444 | [Agent failure modes and recovery](0444_agent_failure_modes_and_recovery/README.md) | Reliability | Medium |
| Q0445 | [Return tool errors the model can act on](0445_return_tool_errors_the_model_can_act_on/README.md) | Tooling | Medium |
| Q0446 | [Business-rule validation for tool arguments](0446_business_rule_validation_for_tool_arguments/README.md) | Tooling | Medium |
| Q0447 | [Authorisation checks inside tools](0447_authorisation_checks_inside_tools/README.md) | Security | Hard |
| Q0448 | [Scope tools to the task with capability tokens](0448_scope_tools_to_the_task_with_capability_tokens/README.md) | Security | Medium |
| Q0449 | [Sandboxed code execution tool](0449_sandboxed_code_execution_tool/README.md) | Tooling | Hard |
| Q0450 | [Computer-use and browser agents](0450_computer_use_and_browser_agents/README.md) | Agent types | Medium |
| Q0451 | [Perceive, act, verify loop](0451_perceive_act_verify_loop/README.md) | Agent types | Medium |
| Q0452 | [Queue-triggered agents](0452_queue_triggered_agents/README.md) | Event-driven agents | Medium |
| Q0453 | [Scheduled and background agents](0453_scheduled_and_background_agents/README.md) | Event-driven agents | Medium |
| Q0454 | [Locks when agents share resources](0454_locks_when_agents_share_resources/README.md) | Concurrency | Medium |
| Q0455 | [Optimistic concurrency for agent writes](0455_optimistic_concurrency_for_agent_writes/README.md) | Concurrency | Medium |
| Q0456 | [Transactional outbox for agent side effects](0456_transactional_outbox_for_agent_side_effects/README.md) | Reliability | Hard |
| Q0457 | [Escalate to a human with context](0457_escalate_to_a_human_with_context/README.md) | Human-in-the-loop | Medium |
| Q0458 | [Proposer and critic agents](0458_proposer_and_critic_agents/README.md) | Multi-agent | Medium |
| Q0459 | [Verify agent outputs before returning](0459_verify_agent_outputs_before_returning/README.md) | Verification | Medium |
| Q0460 | [Weighted voting across agents](0460_weighted_voting_across_agents/README.md) | Multi-agent | Medium |
| Q0461 | [Blackboard architecture](0461_blackboard_architecture/README.md) | Multi-agent | Medium |
| Q0462 | [Agent communication options](0462_agent_communication_options/README.md) | Protocols | Medium |
| Q0463 | [Choosing an agent framework](0463_choosing_an_agent_framework/README.md) | Frameworks | Medium |
| Q0464 | [Stateless versus stateful agent services](0464_stateless_versus_stateful_agent_services/README.md) | Architecture | Medium |
| Q0465 | [Stream agent progress events](0465_stream_agent_progress_events/README.md) | UX engineering | Medium |
| Q0466 | [Pause and resume an agent with generators](0466_pause_and_resume_an_agent_with_generators/README.md) | Human-in-the-loop | Medium |
| Q0467 | [Observability requirements for agents](0467_observability_requirements_for_agents/README.md) | Observability | Medium |
| Q0468 | [Cost of multi-agent systems](0468_cost_of_multi_agent_systems/README.md) | Cost control | Medium |
| Q0469 | [When multi-agent is overkill](0469_when_multi_agent_is_overkill/README.md) | Agent design | Medium |
| Q0470 | [Orchestrating a personal AI assistant](0470_orchestrating_a_personal_ai_assistant/README.md) | Personal assistants | Medium |
| Q0471 | [Design a flight-disruption rebooking agent](0471_design_a_flight_disruption_rebooking_agent/README.md) | Agent design | Hard |
| Q0472 | [Rank rebooking options under constraints](0472_rank_rebooking_options_under_constraints/README.md) | Agent tools | Medium |
| Q0473 | [Trade-break remediation agent](0473_trade_break_remediation_agent/README.md) | Agent design | Hard |
| Q0474 | [Route exceptions to remediation playbooks](0474_route_exceptions_to_remediation_playbooks/README.md) | Agent tools | Medium |
| Q0475 | [Agentic code-fix loop design](0475_agentic_code_fix_loop_design/README.md) | Agent design | Medium |
| Q0476 | [Code-fix loop with test feedback](0476_code_fix_loop_with_test_feedback/README.md) | Agent loops | Medium |
| Q0477 | [Fraud investigation agent design](0477_fraud_investigation_agent_design/README.md) | Agent design | Hard |
| Q0478 | [Explainable risk score aggregation](0478_explainable_risk_score_aggregation/README.md) | Agent tools | Medium |
| Q0479 | [Guardrails on agent actions](0479_guardrails_on_agent_actions/README.md) | Agent safety | Medium |
| Q0480 | [Policy engine for tool calls](0480_policy_engine_for_tool_calls/README.md) | Agent safety | Medium |
| Q0481 | [Per-user rate limits on agent tools](0481_per_user_rate_limits_on_agent_tools/README.md) | Agent safety | Medium |
| Q0482 | [Detect goal drift during a run](0482_detect_goal_drift_during_a_run/README.md) | Agent safety | Medium |
| Q0483 | [Judging the quality of a task decomposition](0483_judging_the_quality_of_a_task_decomposition/README.md) | Planning | Medium |
| Q0484 | [Tool selection at scale](0484_tool_selection_at_scale/README.md) | Tooling | Medium |
| Q0485 | [Load tools on demand](0485_load_tools_on_demand/README.md) | Tooling | Medium |
| Q0486 | [Testing strategy for agents](0486_testing_strategy_for_agents/README.md) | Testing | Medium |
| Q0487 | [Simulated backends for agent tests](0487_simulated_backends_for_agent_tests/README.md) | Testing | Medium |
| Q0488 | [Fault injection for agents](0488_fault_injection_for_agents/README.md) | Testing | Medium |
| Q0489 | [Replay an agent run for debugging](0489_replay_an_agent_run_for_debugging/README.md) | Debugging | Medium |
| Q0490 | [Versioning agents and workflows](0490_versioning_agents_and_workflows/README.md) | Operations | Medium |
| Q0491 | [Migrating in-flight runs across versions](0491_migrating_in_flight_runs_across_versions/README.md) | Operations | Medium |
| Q0492 | [Multi-tenant agent platform concerns](0492_multi_tenant_agent_platform_concerns/README.md) | Platform architecture | Medium |
| Q0493 | [SLOs for agents](0493_slos_for_agents/README.md) | Operations | Medium |
| Q0494 | [Fair scheduling of agent jobs across tenants](0494_fair_scheduling_of_agent_jobs_across_tenants/README.md) | Platform architecture | Hard |
| Q0495 | [Backpressure in agent pipelines](0495_backpressure_in_agent_pipelines/README.md) | Concurrency | Medium |
| Q0496 | [Cross-user isolation in shared agents](0496_cross_user_isolation_in_shared_agents/README.md) | Security | Medium |
| Q0497 | [Explain what the agent did](0497_explain_what_the_agent_did/README.md) | UX | Easy |
| Q0498 | [Tamper-evident audit trail for agent actions](0498_tamper_evident_audit_trail_for_agent_actions/README.md) | Governance | Medium |
| Q0499 | [Design an agentic orchestration platform for LLM Suite](0499_design_an_agentic_orchestration_platform_for_llm_suite/README.md) | System design | Hard |
| Q0500 | [Whiteboard: disruption recovery with cooperating agents](0500_whiteboard_disruption_recovery_with_cooperating_agents/README.md) | System design | Hard |

[← All sections](../README.md)
