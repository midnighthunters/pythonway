# AI Security, Guardrails & Responsible AI in a Bank

Prompt injection (direct and indirect), OWASP Top 10 for LLM and agentic applications, tool permissioning and least privilege, PII redaction, output handling, data leakage and entitlements, red teaming, model risk management and regulation, audit logging, with guardrail code you can run.

Maps to the job description: Write secure, high-quality production code; secure, reliable AI capabilities; technology controls agenda.

Q0901–Q1000 · 100 questions · Easy 21 · Medium 43 · Hard 36

| # | Question | Topic | Difficulty |
|---|---|---|---|
| Q0901 | [Direct prompt injection and instruction override mechanics](0901_direct_prompt_injection_and_instruction_override_mechanics/README.md) | Prompt injection defense | Easy |
| Q0902 | [Indirect prompt injection via untrusted external retrieval documents](0902_indirect_prompt_injection_via_untrusted_external_retrieval/README.md) | Prompt injection defense | Hard |
| Q0903 | [Delimiter hijacking and instruction boundary isolation](0903_delimiter_hijacking_and_instruction_boundary_isolation/README.md) | Prompt injection defense | Medium |
| Q0904 | [ASCII smuggling and Unicode zero-width character evasion detection](0904_ascii_smuggling_and_unicode_zero_width_character_evasion/README.md) | Prompt injection defense | Hard |
| Q0905 | [Base64 and hex encoding evasion in user prompts](0905_base64_and_hex_encoding_evasion_in_user_prompts/README.md) | Prompt injection defense | Easy |
| Q0906 | [Multilingual prompt injection and cross-language translation evasion](0906_multilingual_prompt_injection_and_cross_language/README.md) | Prompt injection defense | Medium |
| Q0907 | [Recursive prompt injection in multi-agent tool communication](0907_recursive_prompt_injection_in_multi_agent_tool_communication/README.md) | Prompt injection defense | Hard |
| Q0908 | [Markdown injection and image exfiltration tags](0908_markdown_injection_and_image_exfiltration_tags/README.md) | Prompt injection defense | Medium |
| Q0909 | [Dual-LLM architecture: Privileged Executor vs Quarantined Analyzer](0909_dual_llm_architecture_privileged_executor_vs_quarantined/README.md) | Prompt injection defense | Hard |
| Q0910 | [Defense-in-depth prompt defense pipeline](0910_defense_in_depth_prompt_defense_pipeline/README.md) | Prompt injection defense | Medium |
| Q0911 | [Canary tokens in system prompts for leak detection and alerting](0911_canary_tokens_in_system_prompts_for_leak_detection_and/README.md) | Prompt injection defense | Easy |
| Q0912 | [Classifier-based prompt injection detection](0912_classifier_based_prompt_injection_detection/README.md) | Prompt injection defense | Medium |
| Q0913 | [Perplexity-based adversarial prompt detection](0913_perplexity_based_adversarial_prompt_detection/README.md) | Prompt injection defense | Hard |
| Q0914 | [Few-shot defensive priming against adversarial jailbreaks](0914_few_shot_defensive_priming_against_adversarial_jailbreaks/README.md) | Prompt injection defense | Easy |
| Q0915 | [XML tag escaping and AST parsing for prompt inputs](0915_xml_tag_escaping_and_ast_parsing_for_prompt_inputs/README.md) | Prompt injection defense | Medium |
| Q0916 | [Universal adversarial triggers and suffix attacks (GCG)](0916_universal_adversarial_triggers_and_suffix_attacks_gcg/README.md) | Prompt injection defense | Hard |
| Q0917 | [Context window stuffing and denial of service via prompt explosion](0917_context_window_stuffing_and_denial_of_service_via_prompt/README.md) | Prompt injection defense | Medium |
| Q0918 | [Tree of Attacks with Pruning and automated red teaming defense](0918_tree_of_attacks_with_pruning_and_automated_red_teaming/README.md) | Prompt injection defense | Hard |
| Q0919 | [Virtual persona and roleplay jailbreak defenses](0919_virtual_persona_and_roleplay_jailbreak_defenses/README.md) | Prompt injection defense | Medium |
| Q0920 | [Multi-turn conversational drift and gradual jailbreak escalation](0920_multi_turn_conversational_drift_and_gradual_jailbreak/README.md) | Prompt injection defense | Hard |
| Q0921 | [Multimodal prompt injection in images and visual typography](0921_multimodal_prompt_injection_in_images_and_visual_typography/README.md) | Prompt injection defense | Medium |
| Q0922 | [Audio prompt injection and ultrasonic command evasion](0922_audio_prompt_injection_and_ultrasonic_command_evasion/README.md) | Prompt injection defense | Easy |
| Q0923 | [Model hallucination vs adversarial manipulation differentiation](0923_model_hallucination_vs_adversarial_manipulation/README.md) | Prompt injection defense | Medium |
| Q0924 | [Benchmarking prompt injection resistance using automated eval suites](0924_benchmarking_prompt_injection_resistance_using_automated/README.md) | Prompt injection defense | Hard |
| Q0925 | [Real-time adversarial prompt blocking middleware in FastAPI](0925_real_time_adversarial_prompt_blocking_middleware_in_fastapi/README.md) | Prompt injection defense | Easy |
| Q0926 | [OWASP LLM01: Prompt Injection comprehensive taxonomy and defense checklist](0926_owasp_llm01_prompt_injection_comprehensive_taxonomy_and/README.md) | OWASP LLM Top 10 | Hard |
| Q0927 | [OWASP LLM02: Sensitive Information Disclosure and model weight inversion](0927_owasp_llm02_sensitive_information_disclosure_and_model/README.md) | OWASP LLM Top 10 | Medium |
| Q0928 | [OWASP LLM03: Supply Chain Vulnerabilities in model hubs and LoRA adapters](0928_owasp_llm03_supply_chain_vulnerabilities_in_model_hubs_and/README.md) | OWASP LLM Top 10 | Medium |
| Q0929 | [OWASP LLM04: Data and Model Poisoning in fine-tuning and pre-training](0929_owasp_llm04_data_and_model_poisoning_in_fine_tuning_and_pre/README.md) | OWASP LLM Top 10 | Hard |
| Q0930 | [OWASP LLM05: Improper Output Handling (stored XSS, SSRF, and SQL injection)](0930_owasp_llm05_improper_output_handling_stored_xss_ssrf_and/README.md) | OWASP LLM Top 10 | Medium |
| Q0931 | [OWASP LLM06: Excessive Agency and autonomous destructive tool execution](0931_owasp_llm06_excessive_agency_and_autonomous_destructive/README.md) | OWASP LLM Top 10 | Hard |
| Q0932 | [OWASP LLM07: System Prompt Leakage and intellectual property extraction](0932_owasp_llm07_system_prompt_leakage_and_intellectual_property/README.md) | OWASP LLM Top 10 | Easy |
| Q0933 | [OWASP LLM08: Vector and Embedding Weaknesses](0933_owasp_llm08_vector_and_embedding_weaknesses/README.md) | OWASP LLM Top 10 | Hard |
| Q0934 | [OWASP LLM09: Misinformation and Hallucination mitigation in financial advice](0934_owasp_llm09_misinformation_and_hallucination_mitigation_in/README.md) | OWASP LLM Top 10 | Medium |
| Q0935 | [OWASP LLM10: Unbounded Consumption and Denial of Wallet](0935_owasp_llm10_unbounded_consumption_and_denial_of_wallet/README.md) | OWASP LLM Top 10 | Easy |
| Q0936 | [Tool permission scopes and least privilege in agent tools](0936_tool_permission_scopes_and_least_privilege_in_agent_tools/README.md) | Agent security | Medium |
| Q0937 | [Human-in-the-loop approval gates for sensitive bank actions](0937_human_in_the_loop_approval_gates_for_sensitive_bank_actions/README.md) | Agent security | Medium |
| Q0938 | [Step-up authentication and TOTP verification in agent workflows](0938_step_up_authentication_and_totp_verification_in_agent/README.md) | Agent security | Easy |
| Q0939 | [Agent impersonation and synthetic identity spoofing](0939_agent_impersonation_and_synthetic_identity_spoofing/README.md) | Agent security | Medium |
| Q0940 | [Server-Side Request Forgery prevention in agent web browsing tools](0940_server_side_request_forgery_prevention_in_agent_web/README.md) | Agent security | Hard |
| Q0941 | [Sandboxed execution environments for LLM-generated code](0941_sandboxed_execution_environments_for_llm_generated_code/README.md) | Agent security | Hard |
| Q0942 | [Limiting file system access in agent tools](0942_limiting_file_system_access_in_agent_tools/README.md) | Agent security | Medium |
| Q0943 | [Agent credential management: avoiding long-lived API tokens in agent memory](0943_agent_credential_management_avoiding_long_lived_api_tokens/README.md) | Agent security | Easy |
| Q0944 | [Guarding against unauthorized database mutations: enforcing read-only SQL](0944_guarding_against_unauthorized_database_mutations_enforcing/README.md) | Agent security | Medium |
| Q0945 | [SQL query AST validation and blocking DDL/DML in text-to-SQL agents](0945_sql_query_ast_validation_and_blocking_ddl_dml_in_text_to/README.md) | Agent security | Hard |
| Q0946 | [Blast radius containment: rate-limiting agent tool invocations](0946_blast_radius_containment_rate_limiting_agent_tool/README.md) | Agent security | Easy |
| Q0947 | [Dual-custody and 4-eyes principle enforcement for financial actions](0947_dual_custody_and_4_eyes_principle_enforcement_for_financial/README.md) | Agent security | Medium |
| Q0948 | [Preventing recursive agent loop runaway and infinite loop detection](0948_preventing_recursive_agent_loop_runaway_and_infinite_loop/README.md) | Agent security | Medium |
| Q0949 | [Agent tool call parameter schema validation with Pydantic v2](0949_agent_tool_call_parameter_schema_validation_with_pydantic_v2/README.md) | Agent security | Easy |
| Q0950 | [Auditing agent action intents before tool execution](0950_auditing_agent_action_intents_before_tool_execution/README.md) | Agent security | Medium |
| Q0951 | [Microsoft Presidio architecture: Analyzers, Recognizers, and Anonymizers](0951_microsoft_presidio_architecture_analyzers_recognizers_and/README.md) | PII and DLP | Medium |
| Q0952 | [Custom banking PII recognizers: IBAN, SSN, Credit Card, CUSIP, Swift BIC](0952_custom_banking_pii_recognizers_iban_ssn_credit_card_cusip/README.md) | PII and DLP | Hard |
| Q0953 | [Reversible PII tokenization (pseudonymization) with secure lookup mapping](0953_reversible_pii_tokenization_pseudonymization_with_secure/README.md) | PII and DLP | Medium |
| Q0954 | [Irreversible PII masking, redaction, and synthetic data replacement](0954_irreversible_pii_masking_redaction_and_synthetic_data/README.md) | PII and DLP | Easy |
| Q0955 | [Handling PII in unstructured multi-turn chat dialogues](0955_handling_pii_in_unstructured_multi_turn_chat_dialogues/README.md) | PII and DLP | Medium |
| Q0956 | [NER-based PII detection using Transformer models](0956_ner_based_pii_detection_using_transformer_models/README.md) | PII and DLP | Medium |
| Q0957 | [Enterprise Data Loss Prevention integration in API Gateways](0957_enterprise_data_loss_prevention_integration_in_api_gateways/README.md) | PII and DLP | Hard |
| Q0958 | [Entitlement-aware RAG: document metadata ACL filtering at retrieval time](0958_entitlement_aware_rag_document_metadata_acl_filtering_at/README.md) | PII and DLP | Hard |
| Q0959 | [Attribute-Based Access Control in semantic search](0959_attribute_based_access_control_in_semantic_search/README.md) | PII and DLP | Medium |
| Q0960 | [Preventing cross-tenant data bleed in shared vector databases](0960_preventing_cross_tenant_data_bleed_in_shared_vector/README.md) | PII and DLP | Hard |
| Q0961 | [Customer banking secrecy regulations (GLBA, GDPR Art. 9, NYDFS 23 NYCRR 500)](0961_customer_banking_secrecy_regulations_glba_gdpr_art_9_nydfs/README.md) | PII and DLP | Medium |
| Q0962 | [Redacting PII before public cloud LLM calls (Zero-Data Retention)](0962_redacting_pii_before_public_cloud_llm_calls_zero_data/README.md) | PII and DLP | Easy |
| Q0963 | [Differential Privacy in fine-tuning and synthetic dataset generation](0963_differential_privacy_in_fine_tuning_and_synthetic_dataset/README.md) | PII and DLP | Hard |
| Q0964 | [Membership Inference Attacks: detecting private records in model weights](0964_membership_inference_attacks_detecting_private_records_in/README.md) | PII and DLP | Hard |
| Q0965 | [Model inversion attacks: reconstructing private inputs from output probabilities](0965_model_inversion_attacks_reconstructing_private_inputs_from/README.md) | PII and DLP | Medium |
| Q0966 | [Right to be Forgotten (GDPR Art. 17): deleting customer data from vector stores](0966_right_to_be_forgotten_gdpr_art_17_deleting_customer_data/README.md) | PII and DLP | Medium |
| Q0967 | [Detecting internal financial insider information (MNPI) in prompts](0967_detecting_internal_financial_insider_information_mnpi_in/README.md) | PII and DLP | Hard |
| Q0968 | [Watermarking LLM outputs for forensic provenance and copyright tracking](0968_watermarking_llm_outputs_for_forensic_provenance_and/README.md) | PII and DLP | Hard |
| Q0969 | [Synthetic data generation for testing RAG without exposing customer PII](0969_synthetic_data_generation_for_testing_rag_without_exposing/README.md) | PII and DLP | Medium |
| Q0970 | [Redacting sensitive connection strings and secrets from agent traceback outputs](0970_redacting_sensitive_connection_strings_and_secrets_from/README.md) | PII and DLP | Easy |
| Q0971 | [Optical Character Recognition PII scrubbing from uploaded document scans](0971_optical_character_recognition_pii_scrubbing_from_uploaded/README.md) | PII and DLP | Medium |
| Q0972 | [Audio transcript PII masking in call center voice agents](0972_audio_transcript_pii_masking_in_call_center_voice_agents/README.md) | PII and DLP | Easy |
| Q0973 | [Evaluating PII redaction precision, recall, and false-positive impact](0973_evaluating_pii_redaction_precision_recall_and_false/README.md) | PII and DLP | Hard |
| Q0974 | [Fast streaming PII redaction on token chunks without buffering entire responses](0974_fast_streaming_pii_redaction_on_token_chunks_without/README.md) | PII and DLP | Hard |
| Q0975 | [End-to-end PII anonymization and de-anonymization gateway](0975_end_to_end_pii_anonymization_and_de_anonymization_gateway/README.md) | PII and DLP | Hard |
| Q0976 | [Federal Reserve SR 11-7 and OCC 2011-12 Model Risk Management framework](0976_federal_reserve_sr_11_7_and_occ_2011_12_model_risk/README.md) | Model risk management | Hard |
| Q0977 | [UK PRA SS1/23 Model Risk Management principles for banks: Principle 3](0977_uk_pra_ss1_23_model_risk_management_principles_for_banks/README.md) | Model risk management | Hard |
| Q0978 | [UK PRA SS1/23 Principle 4: Independent Model Validation and Challenger Models](0978_uk_pra_ss1_23_principle_4_independent_model_validation_and/README.md) | Model risk management | Hard |
| Q0979 | [EU AI Act high-risk classification and compliance for financial services](0979_eu_ai_act_high_risk_classification_and_compliance_for/README.md) | Model risk management | Medium |
| Q0980 | [NIST AI Risk Management Framework (AI RMF 1.0): Govern, Map, Measure, Manage](0980_nist_ai_risk_management_framework_ai_rmf_1_0_govern_map/README.md) | Model risk management | Easy |
| Q0981 | [ISO/IEC 42001 Artificial Intelligence Management System standard](0981_iso_iec_42001_artificial_intelligence_management_system/README.md) | Model risk management | Medium |
| Q0982 | [Technology Controls Agenda and internal audit controls in JPMorganChase](0982_technology_controls_agenda_and_internal_audit_controls_in/README.md) | Model risk management | Medium |
| Q0983 | [Model inventory management, tiered risk rating, and model cards](0983_model_inventory_management_tiered_risk_rating_and_model/README.md) | Model risk management | Easy |
| Q0984 | [Immutable WORM audit trails for prompts, completions, and tool calls](0984_immutable_worm_audit_trails_for_prompts_completions_and/README.md) | Model risk management | Hard |
| Q0985 | [Cryptographic signing of LLM audit logs for non-repudiation](0985_cryptographic_signing_of_llm_audit_logs_for_non_repudiation/README.md) | Model risk management | Hard |
| Q0986 | [Automated red teaming pipelines for continuous vulnerability assessment](0986_automated_red_teaming_pipelines_for_continuous/README.md) | Model risk management | Medium |
| Q0987 | [Automated jailbreak eval suites in CI/CD deployment pipelines](0987_automated_jailbreak_eval_suites_in_ci_cd_deployment/README.md) | Model risk management | Easy |
| Q0988 | [Evaluating hallucination and factual consistency using RAG Triad](0988_evaluating_hallucination_and_factual_consistency_using_rag/README.md) | Model risk management | Hard |
| Q0989 | [Bias and fairness testing in credit scoring and loan recommendation LLM assistants](0989_bias_and_fairness_testing_in_credit_scoring_and_loan/README.md) | Model risk management | Medium |
| Q0990 | [Toxicity, hate speech, and brand reputation filtering using guardrail models](0990_toxicity_hate_speech_and_brand_reputation_filtering_using/README.md) | Model risk management | Easy |
| Q0991 | [NeMo Guardrails: Colang programmable dialog rails](0991_nemo_guardrails_colang_programmable_dialog_rails/README.md) | Model risk management | Medium |
| Q0992 | [LLM as a Judge: Designing reliable evaluation rubrics and inter-annotator agreement](0992_llm_as_a_judge_designing_reliable_evaluation_rubrics_and/README.md) | Model risk management | Hard |
| Q0993 | [Semantic drift detection and output distribution shifts in production](0993_semantic_drift_detection_and_output_distribution_shifts_in/README.md) | Model risk management | Medium |
| Q0994 | [Shadow deployments and champion-challenger routing in live banking traffic](0994_shadow_deployments_and_champion_challenger_routing_in_live/README.md) | Model risk management | Medium |
| Q0995 | [Incident response playbook for GenAI security breach](0995_incident_response_playbook_for_genai_security_breach/README.md) | Model risk management | Medium |
| Q0996 | [Explainability and Explainable AI (XAI) requirements in automated lending](0996_explainability_and_explainable_ai_xai_requirements_in/README.md) | Model risk management | Hard |
| Q0997 | [Disaster recovery and emergency kill switches for autonomous agent systems](0997_disaster_recovery_and_emergency_kill_switches_for/README.md) | Model risk management | Medium |
| Q0998 | [Third-party foundation model risk assessment and vendor dependency governance](0998_third_party_foundation_model_risk_assessment_and_vendor/README.md) | Model risk management | Easy |
| Q0999 | [Continuous compliance monitoring and automated regulatory reporting](0999_continuous_compliance_monitoring_and_automated_regulatory/README.md) | Model risk management | Medium |
| Q1000 | [Complete enterprise AI security and responsible governance architecture review](1000_complete_enterprise_ai_security_and_responsible_governance/README.md) | Model risk management | Hard |

[← All sections](../README.md)
