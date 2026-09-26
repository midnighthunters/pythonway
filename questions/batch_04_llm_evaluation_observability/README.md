# LLM Evaluation, Testing & Observability

Golden datasets, retrieval and generation metrics, LLM-as-judge and calibration, agent trajectory evaluation, CI evaluation gates, tracing (LangSmith, OpenTelemetry GenAI conventions), cost and latency monitoring, online experiments, with metric implementations you can run.

Maps to the job description: Testing and operational stability; strong understanding of the SDLC.

Q0301–Q0400 · 100 questions · Easy 15 · Medium 80 · Hard 5

| # | Question | Topic | Difficulty |
|---|---|---|---|
| Q0301 | [Why LLM evaluation is hard](0301_why_llm_evaluation_is_hard/README.md) | Evaluation foundations | Easy |
| Q0302 | [The evaluation pyramid for GenAI](0302_the_evaluation_pyramid_for_genai/README.md) | Evaluation strategy | Medium |
| Q0303 | [Define success criteria before building](0303_define_success_criteria_before_building/README.md) | Evaluation strategy | Easy |
| Q0304 | [Evaluation dataset schema](0304_evaluation_dataset_schema/README.md) | Datasets | Medium |
| Q0305 | [Exact and normalised match](0305_exact_and_normalised_match/README.md) | Metrics | Easy |
| Q0306 | [Token-level F1](0306_token_level_f1/README.md) | Metrics | Easy |
| Q0307 | [ROUGE-L with longest common subsequence](0307_rouge_l_with_longest_common_subsequence/README.md) | Metrics | Medium |
| Q0308 | [Why BLEU and ROUGE mislead for LLM outputs](0308_why_bleu_and_rouge_mislead_for_llm_outputs/README.md) | Metrics | Medium |
| Q0309 | [Semantic similarity scoring and its limits](0309_semantic_similarity_scoring_and_its_limits/README.md) | Metrics | Medium |
| Q0310 | [Precision, recall and F1 per label](0310_precision_recall_and_f1_per_label/README.md) | Classification metrics | Medium |
| Q0311 | [Confusion matrix for intent routing](0311_confusion_matrix_for_intent_routing/README.md) | Classification metrics | Easy |
| Q0312 | [Cohen's kappa for annotator agreement](0312_cohen_s_kappa_for_annotator_agreement/README.md) | Human evaluation | Medium |
| Q0313 | [Bootstrap confidence intervals for a metric](0313_bootstrap_confidence_intervals_for_a_metric/README.md) | Statistics | Medium |
| Q0314 | [Sample size for detecting an improvement](0314_sample_size_for_detecting_an_improvement/README.md) | Statistics | Medium |
| Q0315 | [Unbiased pass@k](0315_unbiased_pass_k/README.md) | Code and agent metrics | Medium |
| Q0316 | [pass^k reliability for agents](0316_pass_k_reliability_for_agents/README.md) | Agent metrics | Medium |
| Q0317 | [LLM-as-judge design](0317_llm_as_judge_design/README.md) | Model-graded evaluation | Medium |
| Q0318 | [Judge prompt with rubric and structured verdict](0318_judge_prompt_with_rubric_and_structured_verdict/README.md) | Model-graded evaluation | Medium |
| Q0319 | [Pairwise judging with position swap](0319_pairwise_judging_with_position_swap/README.md) | Model-graded evaluation | Medium |
| Q0320 | [Known biases of LLM judges](0320_known_biases_of_llm_judges/README.md) | Model-graded evaluation | Medium |
| Q0321 | [Calibrate a judge against human labels](0321_calibrate_a_judge_against_human_labels/README.md) | Model-graded evaluation | Medium |
| Q0322 | [Faithfulness by claim decomposition](0322_faithfulness_by_claim_decomposition/README.md) | RAG evaluation | Medium |
| Q0323 | [Answer relevance metric](0323_answer_relevance_metric/README.md) | RAG evaluation | Medium |
| Q0324 | [Context precision and context recall](0324_context_precision_and_context_recall/README.md) | RAG evaluation | Medium |
| Q0325 | [Citation accuracy metric](0325_citation_accuracy_metric/README.md) | RAG evaluation | Medium |
| Q0326 | [Abstention quality metrics](0326_abstention_quality_metrics/README.md) | Reliability evaluation | Medium |
| Q0327 | [Build a safety evaluation set](0327_build_a_safety_evaluation_set/README.md) | Safety evaluation | Medium |
| Q0328 | [Refusal and over-refusal rates](0328_refusal_and_over_refusal_rates/README.md) | Safety evaluation | Medium |
| Q0329 | [Jailbreak success-rate harness](0329_jailbreak_success_rate_harness/README.md) | Safety evaluation | Medium |
| Q0330 | [Field-level extraction evaluation](0330_field_level_extraction_evaluation/README.md) | Extraction evaluation | Medium |
| Q0331 | [Evaluating summarisation](0331_evaluating_summarisation/README.md) | Summarisation evaluation | Medium |
| Q0332 | [Key-point coverage metric](0332_key_point_coverage_metric/README.md) | Summarisation evaluation | Easy |
| Q0333 | [Evaluating tool-calling accuracy](0333_evaluating_tool_calling_accuracy/README.md) | Agent evaluation | Medium |
| Q0334 | [Agent trajectory evaluation](0334_agent_trajectory_evaluation/README.md) | Agent evaluation | Medium |
| Q0335 | [Final-state evaluation for agents](0335_final_state_evaluation_for_agents/README.md) | Agent evaluation | Medium |
| Q0336 | [Report cost and latency percentiles](0336_report_cost_and_latency_percentiles/README.md) | Evaluation reporting | Easy |
| Q0337 | [Select a model on the quality-cost frontier](0337_select_a_model_on_the_quality_cost_frontier/README.md) | Model selection | Medium |
| Q0338 | [Detect per-case regressions between versions](0338_detect_per_case_regressions_between_versions/README.md) | Regression testing | Medium |
| Q0339 | [CI evaluation gate](0339_ci_evaluation_gate/README.md) | Regression testing | Medium |
| Q0340 | [Concurrent evaluation runner with retries](0340_concurrent_evaluation_runner_with_retries/README.md) | Evaluation infrastructure | Hard |
| Q0341 | [Cache evaluation results by configuration](0341_cache_evaluation_results_by_configuration/README.md) | Evaluation infrastructure | Medium |
| Q0342 | [Scripted fake LLM for tests](0342_scripted_fake_llm_for_tests/README.md) | Testing | Easy |
| Q0343 | [Record and replay LLM calls](0343_record_and_replay_llm_calls/README.md) | Testing | Medium |
| Q0344 | [Property-based fuzzing of output parsers](0344_property_based_fuzzing_of_output_parsers/README.md) | Testing | Medium |
| Q0345 | [Pytest fixtures for LLM applications](0345_pytest_fixtures_for_llm_applications/README.md) | Testing | Medium |
| Q0346 | [Contract tests for provider adapters](0346_contract_tests_for_provider_adapters/README.md) | Testing | Medium |
| Q0347 | [Test streaming handlers against arbitrary chunking](0347_test_streaming_handlers_against_arbitrary_chunking/README.md) | Testing | Medium |
| Q0348 | [Metamorphic testing for LLM systems](0348_metamorphic_testing_for_llm_systems/README.md) | Testing | Medium |
| Q0349 | [Perturbation robustness tests](0349_perturbation_robustness_tests/README.md) | Testing | Medium |
| Q0350 | [Slice evaluation results by segment](0350_slice_evaluation_results_by_segment/README.md) | Evaluation analysis | Medium |
| Q0351 | [Designing a human evaluation](0351_designing_a_human_evaluation/README.md) | Human evaluation | Medium |
| Q0352 | [Annotation guidelines and quality control](0352_annotation_guidelines_and_quality_control/README.md) | Human evaluation | Medium |
| Q0353 | [Offline versus online evaluation](0353_offline_versus_online_evaluation/README.md) | Evaluation strategy | Easy |
| Q0354 | [A/B test an assistant change](0354_a_b_test_an_assistant_change/README.md) | Online evaluation | Medium |
| Q0355 | [Guardrail metrics in production](0355_guardrail_metrics_in_production/README.md) | Online evaluation | Medium |
| Q0356 | [Implicit feedback signals](0356_implicit_feedback_signals/README.md) | Online evaluation | Medium |
| Q0357 | [Detect query drift with PSI](0357_detect_query_drift_with_psi/README.md) | Monitoring | Medium |
| Q0358 | [Detect embedding drift](0358_detect_embedding_drift/README.md) | Monitoring | Medium |
| Q0359 | [Traces, spans and attributes for LLM apps](0359_traces_spans_and_attributes_for_llm_apps/README.md) | Observability | Easy |
| Q0360 | [OpenTelemetry GenAI semantic conventions](0360_opentelemetry_genai_semantic_conventions/README.md) | Observability | Medium |
| Q0361 | [Tracing decorator with nested spans](0361_tracing_decorator_with_nested_spans/README.md) | Observability | Medium |
| Q0362 | [Meter tokens and cost per tenant](0362_meter_tokens_and_cost_per_tenant/README.md) | Cost observability | Medium |
| Q0363 | [Structured JSON logs for LLM calls](0363_structured_json_logs_for_llm_calls/README.md) | Observability | Easy |
| Q0364 | [Redact PII before logging](0364_redact_pii_before_logging/README.md) | Privacy | Medium |
| Q0365 | [Sample traces for review](0365_sample_traces_for_review/README.md) | Observability | Medium |
| Q0366 | [LangSmith for tracing and evaluation](0366_langsmith_for_tracing_and_evaluation/README.md) | Tooling | Medium |
| Q0367 | [Dashboards and SLOs for GenAI services](0367_dashboards_and_slos_for_genai_services/README.md) | Operations | Medium |
| Q0368 | [SLO compliance and error budget for TTFT](0368_slo_compliance_and_error_budget_for_ttft/README.md) | Reliability engineering | Medium |
| Q0369 | [Multi-window burn-rate alerts](0369_multi_window_burn_rate_alerts/README.md) | Reliability engineering | Hard |
| Q0370 | [Alert on an online quality regression](0370_alert_on_an_online_quality_regression/README.md) | Monitoring | Medium |
| Q0371 | [Canary analysis for prompt or model rollouts](0371_canary_analysis_for_prompt_or_model_rollouts/README.md) | Release engineering | Medium |
| Q0372 | [Shadow testing a new model](0372_shadow_testing_a_new_model/README.md) | Release engineering | Medium |
| Q0373 | [Evaluating provider model upgrades](0373_evaluating_provider_model_upgrades/README.md) | Release engineering | Medium |
| Q0374 | [Maintaining the golden set](0374_maintaining_the_golden_set/README.md) | Datasets | Medium |
| Q0375 | [Check for evaluation leakage](0375_check_for_evaluation_leakage/README.md) | Evaluation integrity | Medium |
| Q0376 | [Deduplicate evaluation cases](0376_deduplicate_evaluation_cases/README.md) | Datasets | Easy |
| Q0377 | [Stratified sampling for evaluation sets](0377_stratified_sampling_for_evaluation_sets/README.md) | Datasets | Medium |
| Q0378 | [Evaluating multi-turn conversations](0378_evaluating_multi_turn_conversations/README.md) | Conversation evaluation | Medium |
| Q0379 | [User simulator for conversation evaluation](0379_user_simulator_for_conversation_evaluation/README.md) | Conversation evaluation | Hard |
| Q0380 | [Evaluating memory and personalisation](0380_evaluating_memory_and_personalisation/README.md) | Personal assistants | Medium |
| Q0381 | [End-to-end versus component RAG evaluation](0381_end_to_end_versus_component_rag_evaluation/README.md) | RAG evaluation | Medium |
| Q0382 | [Error taxonomy counts](0382_error_taxonomy_counts/README.md) | Error analysis | Easy |
| Q0383 | [Error analysis workflow](0383_error_analysis_workflow/README.md) | Error analysis | Medium |
| Q0384 | [Load test an LLM endpoint](0384_load_test_an_llm_endpoint/README.md) | Performance testing | Medium |
| Q0385 | [Rate-limit evaluation traffic with a token bucket](0385_rate_limit_evaluation_traffic_with_a_token_bucket/README.md) | Evaluation infrastructure | Medium |
| Q0386 | [Reproducible evaluations](0386_reproducible_evaluations/README.md) | Evaluation integrity | Medium |
| Q0387 | [Evaluation run manifest](0387_evaluation_run_manifest/README.md) | Evaluation integrity | Easy |
| Q0388 | [Reporting evaluation results to stakeholders](0388_reporting_evaluation_results_to_stakeholders/README.md) | Communication | Easy |
| Q0389 | [Fairness evaluation across groups](0389_fairness_evaluation_across_groups/README.md) | Responsible AI | Medium |
| Q0390 | [Counterfactual name-swap test](0390_counterfactual_name_swap_test/README.md) | Responsible AI | Medium |
| Q0391 | [Choose a moderation classifier threshold](0391_choose_a_moderation_classifier_threshold/README.md) | Safety evaluation | Medium |
| Q0392 | [Guardrail false positives](0392_guardrail_false_positives/README.md) | Safety evaluation | Medium |
| Q0393 | [Turn red-team findings into regression tests](0393_turn_red_team_findings_into_regression_tests/README.md) | Safety evaluation | Medium |
| Q0394 | [Ongoing monitoring for model risk management](0394_ongoing_monitoring_for_model_risk_management/README.md) | Governance | Medium |
| Q0395 | [Total cost including human rework](0395_total_cost_including_human_rework/README.md) | Cost evaluation | Medium |
| Q0396 | [Evaluating code-fix agents](0396_evaluating_code_fix_agents/README.md) | Agent evaluation | Medium |
| Q0397 | [Evaluating an MCP tool server](0397_evaluating_an_mcp_tool_server/README.md) | Agent evaluation | Medium |
| Q0398 | [Evaluating across languages](0398_evaluating_across_languages/README.md) | Evaluation coverage | Medium |
| Q0399 | [Design an evaluation platform for LLM Suite](0399_design_an_evaluation_platform_for_llm_suite/README.md) | System design | Hard |
| Q0400 | [Pre-launch evaluation plan for a new assistant](0400_pre_launch_evaluation_plan_for_a_new_assistant/README.md) | Evaluation strategy | Hard |

[← All sections](../README.md)
