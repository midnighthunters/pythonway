# LLM Fundamentals & Inference

How large language models work and how they are served: transformers and attention, tokenization, embeddings, decoding and sampling, context windows, KV cache, latency and throughput, fine-tuning versus RAG, with NumPy/Python coding tasks that implement the core pieces.

Maps to the job description: Proficiency working with large language models; build AI/ML solutions.

Q0001–Q0100 · 100 questions · Easy 20 · Medium 73 · Hard 7

| # | Question | Topic | Difficulty |
|---|---|---|---|
| Q0001 | [What an LLM actually computes](0001_what_an_llm_actually_computes/README.md) | Foundations | Easy |
| Q0002 | [Why subword tokenization](0002_why_subword_tokenization/README.md) | Tokenization | Easy |
| Q0003 | [Train a toy BPE tokenizer](0003_train_a_toy_bpe_tokenizer/README.md) | Tokenization | Medium |
| Q0004 | [Encode text with learned BPE merges](0004_encode_text_with_learned_bpe_merges/README.md) | Tokenization | Medium |
| Q0005 | [Estimate request cost from token usage](0005_estimate_request_cost_from_token_usage/README.md) | Cost | Easy |
| Q0006 | [What embeddings are](0006_what_embeddings_are/README.md) | Embeddings | Easy |
| Q0007 | [Cosine similarity and top-k with NumPy](0007_cosine_similarity_and_top_k_with_numpy/README.md) | Embeddings | Easy |
| Q0008 | [Numerically stable softmax](0008_numerically_stable_softmax/README.md) | Math | Easy |
| Q0009 | [Implement scaled dot-product attention](0009_implement_scaled_dot_product_attention/README.md) | Transformers | Medium |
| Q0010 | [Why attention scales by the square root of d_k](0010_why_attention_scales_by_the_square_root_of_d_k/README.md) | Transformers | Medium |
| Q0011 | [Build a causal attention mask](0011_build_a_causal_attention_mask/README.md) | Transformers | Easy |
| Q0012 | [Multi-head attention shapes](0012_multi_head_attention_shapes/README.md) | Transformers | Medium |
| Q0013 | [Sinusoidal positional encoding](0013_sinusoidal_positional_encoding/README.md) | Transformers | Easy |
| Q0014 | [Rotary position embeddings](0014_rotary_position_embeddings/README.md) | Transformers | Hard |
| Q0015 | [LayerNorm versus RMSNorm](0015_layernorm_versus_rmsnorm/README.md) | Transformers | Medium |
| Q0016 | [Anatomy of a decoder block](0016_anatomy_of_a_decoder_block/README.md) | Transformers | Medium |
| Q0017 | [Encoder, decoder and encoder-decoder models](0017_encoder_decoder_and_encoder_decoder_models/README.md) | Architectures | Easy |
| Q0018 | [Greedy decoding loop](0018_greedy_decoding_loop/README.md) | Decoding | Easy |
| Q0019 | [Temperature scaling](0019_temperature_scaling/README.md) | Decoding | Easy |
| Q0020 | [Top-k sampling](0020_top_k_sampling/README.md) | Decoding | Easy |
| Q0021 | [Top-p nucleus sampling](0021_top_p_nucleus_sampling/README.md) | Decoding | Medium |
| Q0022 | [Frequency and presence penalties](0022_frequency_and_presence_penalties/README.md) | Decoding | Medium |
| Q0023 | [Beam search](0023_beam_search/README.md) | Decoding | Medium |
| Q0024 | [Log probabilities as confidence signals](0024_log_probabilities_as_confidence_signals/README.md) | Decoding | Medium |
| Q0025 | [Sequence log-probability and perplexity](0025_sequence_log_probability_and_perplexity/README.md) | Evaluation math | Medium |
| Q0026 | [Next-token cross-entropy loss](0026_next_token_cross_entropy_loss/README.md) | Training | Medium |
| Q0027 | [Why LLMs hallucinate](0027_why_llms_hallucinate/README.md) | Reliability | Medium |
| Q0028 | [Context window limits and lost in the middle](0028_context_window_limits_and_lost_in_the_middle/README.md) | Context | Medium |
| Q0029 | [KV cache incremental decoding](0029_kv_cache_incremental_decoding/README.md) | Inference | Hard |
| Q0030 | [Size the KV cache](0030_size_the_kv_cache/README.md) | Inference capacity | Medium |
| Q0031 | [MQA and GQA](0031_mqa_and_gqa/README.md) | Architectures | Medium |
| Q0032 | [Prefill versus decode latency](0032_prefill_versus_decode_latency/README.md) | Inference performance | Medium |
| Q0033 | [Continuous batching and throughput](0033_continuous_batching_and_throughput/README.md) | Inference serving | Medium |
| Q0034 | [Model weight memory by precision](0034_model_weight_memory_by_precision/README.md) | Inference capacity | Easy |
| Q0035 | [Symmetric int8 quantization](0035_symmetric_int8_quantization/README.md) | Quantization | Medium |
| Q0036 | [Speculative decoding](0036_speculative_decoding/README.md) | Inference performance | Hard |
| Q0037 | [FlashAttention in one answer](0037_flashattention_in_one_answer/README.md) | Inference performance | Medium |
| Q0038 | [Online softmax recurrence](0038_online_softmax_recurrence/README.md) | Inference performance | Hard |
| Q0039 | [PagedAttention and vLLM](0039_pagedattention_and_vllm/README.md) | Inference serving | Medium |
| Q0040 | [Structure prompts for provider prompt caching](0040_structure_prompts_for_provider_prompt_caching/README.md) | Cost optimisation | Medium |
| Q0041 | [Mixture of experts routing](0041_mixture_of_experts_routing/README.md) | Architectures | Medium |
| Q0042 | [Reasoning models and test-time compute](0042_reasoning_models_and_test_time_compute/README.md) | Model capabilities | Medium |
| Q0043 | [Estimate training compute with 6ND](0043_estimate_training_compute_with_6nd/README.md) | Scaling | Medium |
| Q0044 | [Pre-training, SFT and preference tuning](0044_pre_training_sft_and_preference_tuning/README.md) | Training pipeline | Medium |
| Q0045 | [Implement the DPO loss](0045_implement_the_dpo_loss/README.md) | Preference optimisation | Hard |
| Q0046 | [LoRA forward pass and parameter savings](0046_lora_forward_pass_and_parameter_savings/README.md) | Fine-tuning | Medium |
| Q0047 | [QLoRA and NF4 quantisation](0047_qlora_and_nf4_quantisation/README.md) | Fine-tuning | Medium |
| Q0048 | [Fine-tune, RAG or prompt](0048_fine_tune_rag_or_prompt/README.md) | Solution design | Medium |
| Q0049 | [Catastrophic forgetting](0049_catastrophic_forgetting/README.md) | Fine-tuning | Medium |
| Q0050 | [Knowledge distillation](0050_knowledge_distillation/README.md) | Model optimisation | Medium |
| Q0051 | [Bi-encoders versus cross-encoders](0051_bi_encoders_versus_cross_encoders/README.md) | Embeddings | Medium |
| Q0052 | [Matryoshka embedding truncation](0052_matryoshka_embedding_truncation/README.md) | Embeddings | Medium |
| Q0053 | [Tokenization cost surprises](0053_tokenization_cost_surprises/README.md) | Tokenization | Easy |
| Q0054 | [Truncate text to a token budget](0054_truncate_text_to_a_token_budget/README.md) | Context management | Medium |
| Q0055 | [Padding side for batched generation](0055_padding_side_for_batched_generation/README.md) | Inference | Medium |
| Q0056 | [Render a chat template safely](0056_render_a_chat_template_safely/README.md) | Chat formats | Medium |
| Q0057 | [Stop sequences across streamed chunks](0057_stop_sequences_across_streamed_chunks/README.md) | Streaming | Medium |
| Q0058 | [Sources of non-determinism in LLM APIs](0058_sources_of_non_determinism_in_llm_apis/README.md) | Reliability | Medium |
| Q0059 | [Grammar-constrained decoding with token masks](0059_grammar_constrained_decoding_with_token_masks/README.md) | Structured decoding | Hard |
| Q0060 | [Budget max_tokens against the context window](0060_budget_max_tokens_against_the_context_window/README.md) | Context management | Easy |
| Q0061 | [Choosing an embedding model](0061_choosing_an_embedding_model/README.md) | Embeddings | Medium |
| Q0062 | [How vision-language models see images](0062_how_vision_language_models_see_images/README.md) | Multimodal | Medium |
| Q0063 | [Estimate image token cost](0063_estimate_image_token_cost/README.md) | Multimodal | Medium |
| Q0064 | [Model cascade by confidence](0064_model_cascade_by_confidence/README.md) | Model routing | Medium |
| Q0065 | [Choosing a model for a use case](0065_choosing_a_model_for_a_use_case/README.md) | Model selection | Medium |
| Q0066 | [Open-weight versus hosted models in a bank](0066_open_weight_versus_hosted_models_in_a_bank/README.md) | Model strategy | Medium |
| Q0067 | [Model version pinning and deprecation](0067_model_version_pinning_and_deprecation/README.md) | Operations | Medium |
| Q0068 | [Sustainable request rate from token quotas](0068_sustainable_request_rate_from_token_quotas/README.md) | Capacity planning | Medium |
| Q0069 | [Concurrency planning with Little's law](0069_concurrency_planning_with_little_s_law/README.md) | Capacity planning | Easy |
| Q0070 | [Data, tensor and pipeline parallelism](0070_data_tensor_and_pipeline_parallelism/README.md) | Distributed inference | Medium |
| Q0071 | [Self-consistency majority voting](0071_self_consistency_majority_voting/README.md) | Reasoning techniques | Medium |
| Q0072 | [Why chain-of-thought helps](0072_why_chain_of_thought_helps/README.md) | Reasoning techniques | Medium |
| Q0073 | [In-context learning](0073_in_context_learning/README.md) | Prompting fundamentals | Easy |
| Q0074 | [Scaling laws in practice](0074_scaling_laws_in_practice/README.md) | Foundations | Medium |
| Q0075 | [Instruction hierarchy and roles](0075_instruction_hierarchy_and_roles/README.md) | Prompting fundamentals | Medium |
| Q0076 | [Why LLMs struggle with character-level tasks](0076_why_llms_struggle_with_character_level_tasks/README.md) | Tokenization | Easy |
| Q0077 | [Sliding-window attention mask](0077_sliding_window_attention_mask/README.md) | Long context | Medium |
| Q0078 | [Alternatives to quadratic attention](0078_alternatives_to_quadratic_attention/README.md) | Architectures | Medium |
| Q0079 | [Bigram language model with smoothing](0079_bigram_language_model_with_smoothing/README.md) | Language modelling | Medium |
| Q0080 | [UTF-8 bytes and safe truncation](0080_utf_8_bytes_and_safe_truncation/README.md) | Text handling | Medium |
| Q0081 | [Unicode normalisation before model input](0081_unicode_normalisation_before_model_input/README.md) | Input hygiene | Medium |
| Q0082 | [Expected calibration error](0082_expected_calibration_error/README.md) | Model confidence | Medium |
| Q0083 | [Logit bias to ban or force tokens](0083_logit_bias_to_ban_or_force_tokens/README.md) | Decoding controls | Easy |
| Q0084 | [FP16 versus BF16 overflow](0084_fp16_versus_bf16_overflow/README.md) | Numerics | Medium |
| Q0085 | [Agent latency budget with parallel stages](0085_agent_latency_budget_with_parallel_stages/README.md) | Latency engineering | Medium |
| Q0086 | [Pack texts into embedding batches](0086_pack_texts_into_embedding_batches/README.md) | Embedding pipelines | Medium |
| Q0087 | [Batch inference APIs for offline workloads](0087_batch_inference_apis_for_offline_workloads/README.md) | Cost optimisation | Medium |
| Q0088 | [Handling a stream that breaks mid-response](0088_handling_a_stream_that_breaks_mid_response/README.md) | Streaming reliability | Medium |
| Q0089 | [Explaining LLM limitations to business stakeholders](0089_explaining_llm_limitations_to_business_stakeholders/README.md) | Communication | Easy |
| Q0090 | [Model documentation for model risk management](0090_model_documentation_for_model_risk_management/README.md) | Governance | Medium |
| Q0091 | [Benchmark contamination](0091_benchmark_contamination/README.md) | Evaluation integrity | Medium |
| Q0092 | [Vocabulary size trade-offs](0092_vocabulary_size_trade_offs/README.md) | Tokenization | Medium |
| Q0093 | [Memory needed to fine-tune](0093_memory_needed_to_fine_tune/README.md) | Fine-tuning | Medium |
| Q0094 | [Why cosine similarity thresholds don't transfer](0094_why_cosine_similarity_thresholds_don_t_transfer/README.md) | Embeddings | Medium |
| Q0095 | [How tool calling works under the hood](0095_how_tool_calling_works_under_the_hood/README.md) | Tool use | Medium |
| Q0096 | [Parse tool calls from raw model text](0096_parse_tool_calls_from_raw_model_text/README.md) | Tool use | Medium |
| Q0097 | [Multilingual performance considerations](0097_multilingual_performance_considerations/README.md) | Global users | Medium |
| Q0098 | [Small language models for platform tasks](0098_small_language_models_for_platform_tasks/README.md) | Model selection | Medium |
| Q0099 | [Continue generation past the output limit](0099_continue_generation_past_the_output_limit/README.md) | Long outputs | Medium |
| Q0100 | [An LLM request end to end on an enterprise platform](0100_an_llm_request_end_to_end_on_an_enterprise_platform/README.md) | Platform architecture | Hard |

[← All sections](../README.md)
