# Prompting, Context Engineering & Structured Output

Prompt design, system prompts, few-shot and reasoning models, context engineering and token budgets, structured output with JSON Schema and Pydantic, function-calling formats, prompt versioning, and coding tasks such as template rendering, context trimming and JSON repair with validation.

Maps to the job description: Proficiency working with LLMs; write secure, high-quality production code.

Q0101–Q0200 · 100 questions · Easy 21 · Medium 74 · Hard 5

| # | Question | Topic | Difficulty |
|---|---|---|---|
| Q0101 | [Anatomy of a good system prompt](0101_anatomy_of_a_good_system_prompt/README.md) | Prompt design | Easy |
| Q0102 | [Zero-shot, few-shot and instruction prompts](0102_zero_shot_few_shot_and_instruction_prompts/README.md) | Prompt design | Easy |
| Q0103 | [Render versioned prompt templates safely](0103_render_versioned_prompt_templates_safely/README.md) | Prompt management | Medium |
| Q0104 | [Prompt registry with versions and rollback](0104_prompt_registry_with_versions_and_rollback/README.md) | Prompt management | Medium |
| Q0105 | [Delimit untrusted content in prompts](0105_delimit_untrusted_content_in_prompts/README.md) | Prompt safety | Medium |
| Q0106 | [Select few-shot examples by similarity with diversity](0106_select_few_shot_examples_by_similarity_with_diversity/README.md) | Few-shot | Medium |
| Q0107 | [Balance few-shot examples across labels](0107_balance_few_shot_examples_across_labels/README.md) | Few-shot | Easy |
| Q0108 | [Few-shot order and recency effects](0108_few_shot_order_and_recency_effects/README.md) | Few-shot | Medium |
| Q0109 | [Role prompting and personas](0109_role_prompting_and_personas/README.md) | Prompt design | Easy |
| Q0110 | [Prompting reasoning models versus chat models](0110_prompting_reasoning_models_versus_chat_models/README.md) | Prompt design | Medium |
| Q0111 | [Prompt chaining with validation between steps](0111_prompt_chaining_with_validation_between_steps/README.md) | Decomposition | Medium |
| Q0112 | [Teach the model to say I don't know](0112_teach_the_model_to_say_i_don_t_know/README.md) | Reliability | Medium |
| Q0113 | [Controlling output length](0113_controlling_output_length/README.md) | Prompt design | Easy |
| Q0114 | [Negative instructions and their pitfalls](0114_negative_instructions_and_their_pitfalls/README.md) | Prompt design | Easy |
| Q0115 | [Measure prompt robustness to paraphrase](0115_measure_prompt_robustness_to_paraphrase/README.md) | Prompt testing | Medium |
| Q0116 | [What context engineering means](0116_what_context_engineering_means/README.md) | Context engineering | Medium |
| Q0117 | [Allocate a token budget across context sections](0117_allocate_a_token_budget_across_context_sections/README.md) | Context engineering | Medium |
| Q0118 | [Trim conversation history without breaking tool pairs](0118_trim_conversation_history_without_breaking_tool_pairs/README.md) | Context engineering | Hard |
| Q0119 | [Rolling summary memory](0119_rolling_summary_memory/README.md) | Context engineering | Medium |
| Q0120 | [Compact large tool outputs](0120_compact_large_tool_outputs/README.md) | Context engineering | Medium |
| Q0121 | [Where to place documents and the question](0121_where_to_place_documents_and_the_question/README.md) | Context engineering | Medium |
| Q0122 | [Parse and validate citations in answers](0122_parse_and_validate_citations_in_answers/README.md) | Grounding | Medium |
| Q0123 | [JSON mode, structured outputs and function calling](0123_json_mode_structured_outputs_and_function_calling/README.md) | Structured output | Medium |
| Q0124 | [Extract data into a validated Pydantic model](0124_extract_data_into_a_validated_pydantic_model/README.md) | Structured output | Medium |
| Q0125 | [Generate a JSON Schema from a Pydantic model](0125_generate_a_json_schema_from_a_pydantic_model/README.md) | Structured output | Easy |
| Q0126 | [Make a schema strict for providers](0126_make_a_schema_strict_for_providers/README.md) | Structured output | Medium |
| Q0127 | [Validate and retry with error feedback](0127_validate_and_retry_with_error_feedback/README.md) | Structured output | Medium |
| Q0128 | [Extract JSON from a chatty model response](0128_extract_json_from_a_chatty_model_response/README.md) | Output parsing | Medium |
| Q0129 | [Repair common JSON errors conservatively](0129_repair_common_json_errors_conservatively/README.md) | Output parsing | Medium |
| Q0130 | [Constrain classification labels with Literal](0130_constrain_classification_labels_with_literal/README.md) | Structured output | Easy |
| Q0131 | [Nullable versus missing fields](0131_nullable_versus_missing_fields/README.md) | Structured output | Medium |
| Q0132 | [Money and dates in structured output](0132_money_and_dates_in_structured_output/README.md) | Structured output | Medium |
| Q0133 | [Parse partial JSON while streaming](0133_parse_partial_json_while_streaming/README.md) | Streaming structured output | Hard |
| Q0134 | [Discriminated unions for agent actions](0134_discriminated_unions_for_agent_actions/README.md) | Structured output | Medium |
| Q0135 | [Cross-field validation of extracted invoices](0135_cross_field_validation_of_extracted_invoices/README.md) | Structured output | Medium |
| Q0136 | [Classification prompt with label definitions](0136_classification_prompt_with_label_definitions/README.md) | Classification | Easy |
| Q0137 | [Multi-label classification output](0137_multi_label_classification_output/README.md) | Classification | Medium |
| Q0138 | [Self-reported confidence pitfalls](0138_self_reported_confidence_pitfalls/README.md) | Reliability | Medium |
| Q0139 | [Verify extracted entities against the source](0139_verify_extracted_entities_against_the_source/README.md) | Grounding | Medium |
| Q0140 | [Summarisation prompt design](0140_summarisation_prompt_design/README.md) | Summarisation | Easy |
| Q0141 | [Map-reduce summarisation](0141_map_reduce_summarisation/README.md) | Summarisation | Medium |
| Q0142 | [Refine summarisation](0142_refine_summarisation/README.md) | Summarisation | Medium |
| Q0143 | [Faithful summaries of financial documents](0143_faithful_summaries_of_financial_documents/README.md) | Summarisation | Medium |
| Q0144 | [Read-only guardrails for text-to-SQL](0144_read_only_guardrails_for_text_to_sql/README.md) | Text-to-SQL | Hard |
| Q0145 | [Schema context for text-to-SQL](0145_schema_context_for_text_to_sql/README.md) | Text-to-SQL | Medium |
| Q0146 | [The sandwich defence and its limits](0146_the_sandwich_defence_and_its_limits/README.md) | Prompt safety | Medium |
| Q0147 | [Automatic prompt optimisation with an eval loop](0147_automatic_prompt_optimisation_with_an_eval_loop/README.md) | Prompt optimisation | Medium |
| Q0148 | [Unit tests for prompts](0148_unit_tests_for_prompts/README.md) | Prompt testing | Medium |
| Q0149 | [Snapshot testing rendered prompts](0149_snapshot_testing_rendered_prompts/README.md) | Prompt testing | Medium |
| Q0150 | [Sanitise model markdown before rendering](0150_sanitise_model_markdown_before_rendering/README.md) | Output handling | Hard |
| Q0151 | [Coerce and validate tool arguments](0151_coerce_and_validate_tool_arguments/README.md) | Tool use | Medium |
| Q0152 | [Minimal JSON Schema validator](0152_minimal_json_schema_validator/README.md) | Structured output | Medium |
| Q0153 | [Writing good tool descriptions](0153_writing_good_tool_descriptions/README.md) | Tool use | Medium |
| Q0154 | [Select relevant tools for the context](0154_select_relevant_tools_for_the_context/README.md) | Tool use | Medium |
| Q0155 | [Assemble the system prompt per user role](0155_assemble_the_system_prompt_per_user_role/README.md) | Context engineering | Medium |
| Q0156 | [Context distraction and poisoning](0156_context_distraction_and_poisoning/README.md) | Context engineering | Medium |
| Q0157 | [Instruction drift in long conversations](0157_instruction_drift_in_long_conversations/README.md) | Context engineering | Medium |
| Q0158 | [What to store in long-term memory](0158_what_to_store_in_long_term_memory/README.md) | Memory | Medium |
| Q0159 | [Extract user preferences into structured memory](0159_extract_user_preferences_into_structured_memory/README.md) | Memory | Medium |
| Q0160 | [Deduplicate memory facts](0160_deduplicate_memory_facts/README.md) | Memory | Medium |
| Q0161 | [Account for every token in a request](0161_account_for_every_token_in_a_request/README.md) | Context engineering | Medium |
| Q0162 | [System prompt confidentiality](0162_system_prompt_confidentiality/README.md) | Prompt safety | Medium |
| Q0163 | [Rubrics and checklists inside prompts](0163_rubrics_and_checklists_inside_prompts/README.md) | Prompt design | Easy |
| Q0164 | [Generate, critique and revise loop](0164_generate_critique_and_revise_loop/README.md) | Self-refinement | Medium |
| Q0165 | [Check required sections in generated reports](0165_check_required_sections_in_generated_reports/README.md) | Output validation | Easy |
| Q0166 | [Avoid str.format injection in templates](0166_avoid_str_format_injection_in_templates/README.md) | Prompt safety | Medium |
| Q0167 | [Log prompt metadata for traceability](0167_log_prompt_metadata_for_traceability/README.md) | Observability | Medium |
| Q0168 | [Compare two prompts on a dev set](0168_compare_two_prompts_on_a_dev_set/README.md) | Prompt evaluation | Medium |
| Q0169 | [Combined citation and abstention template](0169_combined_citation_and_abstention_template/README.md) | Grounding | Medium |
| Q0170 | [Extract the final answer from tagged output](0170_extract_the_final_answer_from_tagged_output/README.md) | Output parsing | Easy |
| Q0171 | [Strip scratchpad content before display](0171_strip_scratchpad_content_before_display/README.md) | Output handling | Medium |
| Q0172 | [Structured plans with dependency validation](0172_structured_plans_with_dependency_validation/README.md) | Planning | Medium |
| Q0173 | [Handle refusals in structured output](0173_handle_refusals_in_structured_output/README.md) | Structured output | Medium |
| Q0174 | [When to ask a clarifying question](0174_when_to_ask_a_clarifying_question/README.md) | Conversation design | Medium |
| Q0175 | [Slot filling for a booking assistant](0175_slot_filling_for_a_booking_assistant/README.md) | Conversation design | Medium |
| Q0176 | [Style guide compliance](0176_style_guide_compliance/README.md) | Output validation | Easy |
| Q0177 | [Prompt compression](0177_prompt_compression/README.md) | Cost optimisation | Medium |
| Q0178 | [Token-efficient data formats in prompts](0178_token_efficient_data_formats_in_prompts/README.md) | Cost optimisation | Easy |
| Q0179 | [Render tables for prompts with row caps](0179_render_tables_for_prompts_with_row_caps/README.md) | Context engineering | Easy |
| Q0180 | [Inject the current date and time zone](0180_inject_the_current_date_and_time_zone/README.md) | Context engineering | Easy |
| Q0181 | [Source metadata for grounding](0181_source_metadata_for_grounding/README.md) | Grounding | Medium |
| Q0182 | [Resolve conflicting policy versions](0182_resolve_conflicting_policy_versions/README.md) | Grounding | Medium |
| Q0183 | [Require exact quotes and verify them](0183_require_exact_quotes_and_verify_them/README.md) | Grounding | Medium |
| Q0184 | [Extract action items from emails](0184_extract_action_items_from_emails/README.md) | Personal assistants | Medium |
| Q0185 | [Chunked extraction over long documents](0185_chunked_extraction_over_long_documents/README.md) | Extraction | Medium |
| Q0186 | [Schema evolution for structured outputs](0186_schema_evolution_for_structured_outputs/README.md) | Structured output | Medium |
| Q0187 | [Tolerant parsing of older payloads](0187_tolerant_parsing_of_older_payloads/README.md) | Structured output | Medium |
| Q0188 | [Structured outputs versus regex post-processing](0188_structured_outputs_versus_regex_post_processing/README.md) | Structured output | Easy |
| Q0189 | [Validate parallel tool calls independently](0189_validate_parallel_tool_calls_independently/README.md) | Tool use | Medium |
| Q0190 | [Handoff payload between agents](0190_handoff_payload_between_agents/README.md) | Multi-agent | Medium |
| Q0191 | [Tell the model about tool side effects](0191_tell_the_model_about_tool_side_effects/README.md) | Tool use | Medium |
| Q0192 | [Design outputs for evaluation](0192_design_outputs_for_evaluation/README.md) | Evaluation-friendly design | Medium |
| Q0193 | [Prompt anti-patterns](0193_prompt_anti_patterns/README.md) | Prompt design | Easy |
| Q0194 | [Review this prompt](0194_review_this_prompt/README.md) | Prompt review | Medium |
| Q0195 | [Language control in multilingual replies](0195_language_control_in_multilingual_replies/README.md) | Global users | Easy |
| Q0196 | [Few-shot examples from production data](0196_few_shot_examples_from_production_data/README.md) | Privacy | Medium |
| Q0197 | [Choosing generation settings per task](0197_choosing_generation_settings_per_task/README.md) | Generation settings | Easy |
| Q0198 | [Prompt debugging workflow](0198_prompt_debugging_workflow/README.md) | Prompt engineering process | Medium |
| Q0199 | [Per-model prompt variants with fallback](0199_per_model_prompt_variants_with_fallback/README.md) | Model-agnostic design | Medium |
| Q0200 | [Design the prompt stack for an LLM Suite assistant](0200_design_the_prompt_stack_for_an_llm_suite_assistant/README.md) | Context engineering design | Hard |

[← All sections](../README.md)
