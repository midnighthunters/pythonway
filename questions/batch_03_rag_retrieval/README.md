# Retrieval-Augmented Generation (RAG)

End-to-end RAG: ingestion and chunking, embeddings, vector indexes, hybrid search (BM25 + vectors), reciprocal rank fusion, reranking, query rewriting, entitlement-aware retrieval, citations and grounding, with runnable implementations of each building block.

Maps to the job description: Build AI/ML solutions for the LLM Suite platform; algorithms that integrate with existing systems.

Q0201–Q0300 · 100 questions · Easy 8 · Medium 83 · Hard 9

| # | Question | Topic | Difficulty |
|---|---|---|---|
| Q0201 | [RAG end to end](0201_rag_end_to_end/README.md) | RAG architecture | Easy |
| Q0202 | [When not to use RAG](0202_when_not_to_use_rag/README.md) | RAG architecture | Medium |
| Q0203 | [Fixed-size chunking with overlap](0203_fixed_size_chunking_with_overlap/README.md) | Chunking | Easy |
| Q0204 | [Recursive text splitting](0204_recursive_text_splitting/README.md) | Chunking | Medium |
| Q0205 | [Structure-aware chunking of markdown](0205_structure_aware_chunking_of_markdown/README.md) | Chunking | Medium |
| Q0206 | [Choosing a chunk size](0206_choosing_a_chunk_size/README.md) | Chunking | Medium |
| Q0207 | [Parent-child retrieval](0207_parent_child_retrieval/README.md) | Retrieval patterns | Medium |
| Q0208 | [Sentence-window retrieval](0208_sentence_window_retrieval/README.md) | Retrieval patterns | Medium |
| Q0209 | [Contextual chunk headers](0209_contextual_chunk_headers/README.md) | Chunking | Medium |
| Q0210 | [Document parsing challenges](0210_document_parsing_challenges/README.md) | Ingestion | Medium |
| Q0211 | [Remove repeated headers and footers](0211_remove_repeated_headers_and_footers/README.md) | Ingestion | Medium |
| Q0212 | [Tables in RAG](0212_tables_in_rag/README.md) | Ingestion | Medium |
| Q0213 | [Deduplicate near-duplicate chunks with MinHash](0213_deduplicate_near_duplicate_chunks_with_minhash/README.md) | Ingestion | Hard |
| Q0214 | [Deterministic chunk ids for idempotent ingestion](0214_deterministic_chunk_ids_for_idempotent_ingestion/README.md) | Ingestion | Medium |
| Q0215 | [Incremental re-indexing on document change](0215_incremental_re_indexing_on_document_change/README.md) | Ingestion | Medium |
| Q0216 | [Metadata schema for chunks](0216_metadata_schema_for_chunks/README.md) | Ingestion | Medium |
| Q0217 | [Build an inverted index](0217_build_an_inverted_index/README.md) | Keyword search | Medium |
| Q0218 | [BM25 scoring from scratch](0218_bm25_scoring_from_scratch/README.md) | Keyword search | Medium |
| Q0219 | [Why BM25 still matters](0219_why_bm25_still_matters/README.md) | Hybrid search | Easy |
| Q0220 | [Vector search with metadata filters](0220_vector_search_with_metadata_filters/README.md) | Vector search | Medium |
| Q0221 | [Pre-filtering versus post-filtering](0221_pre_filtering_versus_post_filtering/README.md) | Vector search | Medium |
| Q0222 | [HNSW explained](0222_hnsw_explained/README.md) | Vector search | Medium |
| Q0223 | [IVF and product quantisation](0223_ivf_and_product_quantisation/README.md) | Vector search | Medium |
| Q0224 | [Measure ANN recall against exact search](0224_measure_ann_recall_against_exact_search/README.md) | Vector search | Medium |
| Q0225 | [Reciprocal rank fusion](0225_reciprocal_rank_fusion/README.md) | Hybrid search | Easy |
| Q0226 | [Weighted score fusion with normalisation](0226_weighted_score_fusion_with_normalisation/README.md) | Hybrid search | Medium |
| Q0227 | [Rerank candidates with a fallback](0227_rerank_candidates_with_a_fallback/README.md) | Reranking | Medium |
| Q0228 | [Condense follow-up questions](0228_condense_follow_up_questions/README.md) | Query understanding | Medium |
| Q0229 | [Multi-query retrieval](0229_multi_query_retrieval/README.md) | Query understanding | Medium |
| Q0230 | [Hypothetical document embeddings](0230_hypothetical_document_embeddings/README.md) | Query understanding | Medium |
| Q0231 | [Query decomposition for multi-hop questions](0231_query_decomposition_for_multi_hop_questions/README.md) | Query understanding | Medium |
| Q0232 | [Extract metadata filters from queries](0232_extract_metadata_filters_from_queries/README.md) | Query understanding | Medium |
| Q0233 | [Entitlement-aware retrieval](0233_entitlement_aware_retrieval/README.md) | Security | Hard |
| Q0234 | [Why entitlements must filter before generation](0234_why_entitlements_must_filter_before_generation/README.md) | Security | Medium |
| Q0235 | [Information barriers in RAG](0235_information_barriers_in_rag/README.md) | Security | Hard |
| Q0236 | [Document-level versus chunk-level security](0236_document_level_versus_chunk_level_security/README.md) | Security | Medium |
| Q0237 | [Tenant isolation in vector stores](0237_tenant_isolation_in_vector_stores/README.md) | Security | Medium |
| Q0238 | [Build numbered context with a citation map](0238_build_numbered_context_with_a_citation_map/README.md) | Citations | Medium |
| Q0239 | [Pack context under a token budget](0239_pack_context_under_a_token_budget/README.md) | Context assembly | Medium |
| Q0240 | [Reorder context against lost in the middle](0240_reorder_context_against_lost_in_the_middle/README.md) | Context assembly | Easy |
| Q0241 | [RAG answer prompt builder](0241_rag_answer_prompt_builder/README.md) | Generation | Medium |
| Q0242 | [Lexical groundedness check](0242_lexical_groundedness_check/README.md) | Grounding | Medium |
| Q0243 | [Hit rate and MRR for a retriever](0243_hit_rate_and_mrr_for_a_retriever/README.md) | Retrieval evaluation | Easy |
| Q0244 | [nDCG for graded relevance](0244_ndcg_for_graded_relevance/README.md) | Retrieval evaluation | Medium |
| Q0245 | [Build a retrieval golden set](0245_build_a_retrieval_golden_set/README.md) | Retrieval evaluation | Medium |
| Q0246 | [Synthetic questions for retrieval evaluation](0246_synthetic_questions_for_retrieval_evaluation/README.md) | Retrieval evaluation | Medium |
| Q0247 | [Diagnose a bad RAG answer](0247_diagnose_a_bad_rag_answer/README.md) | Debugging | Medium |
| Q0248 | [Recency boosting with time decay](0248_recency_boosting_with_time_decay/README.md) | Ranking | Medium |
| Q0249 | [Authority boosting with source priors](0249_authority_boosting_with_source_priors/README.md) | Ranking | Medium |
| Q0250 | [Semantic cache keys with entitlements](0250_semantic_cache_keys_with_entitlements/README.md) | Caching | Hard |
| Q0251 | [Conversational RAG memory](0251_conversational_rag_memory/README.md) | Conversation | Medium |
| Q0252 | [Agentic RAG](0252_agentic_rag/README.md) | Agentic retrieval | Medium |
| Q0253 | [Iterative retrieval tool loop](0253_iterative_retrieval_tool_loop/README.md) | Agentic retrieval | Medium |
| Q0254 | [GraphRAG and knowledge graphs](0254_graphrag_and_knowledge_graphs/README.md) | Advanced retrieval | Medium |
| Q0255 | [Entity co-occurrence graph expansion](0255_entity_co_occurrence_graph_expansion/README.md) | Advanced retrieval | Medium |
| Q0256 | [Route between RAG and SQL](0256_route_between_rag_and_sql/README.md) | Routing | Medium |
| Q0257 | [Choose long context or retrieval per request](0257_choose_long_context_or_retrieval_per_request/README.md) | Routing | Medium |
| Q0258 | [Cache embeddings by content and model](0258_cache_embeddings_by_content_and_model/README.md) | Ingestion | Medium |
| Q0259 | [Migrate to a new embedding model](0259_migrate_to_a_new_embedding_model/README.md) | Operations | Medium |
| Q0260 | [Choosing a vector store](0260_choosing_a_vector_store/README.md) | Infrastructure | Medium |
| Q0261 | [Azure AI Search for RAG](0261_azure_ai_search_for_rag/README.md) | Cloud AI services | Medium |
| Q0262 | [Amazon Bedrock Knowledge Bases](0262_amazon_bedrock_knowledge_bases/README.md) | Cloud AI services | Medium |
| Q0263 | [OpenSearch hybrid retrieval](0263_opensearch_hybrid_retrieval/README.md) | Cloud AI services | Medium |
| Q0264 | [pgvector for RAG](0264_pgvector_for_rag/README.md) | Infrastructure | Medium |
| Q0265 | [Scaling vector search to 100M chunks](0265_scaling_vector_search_to_100m_chunks/README.md) | Infrastructure | Hard |
| Q0266 | [Sharding and replicas for search](0266_sharding_and_replicas_for_search/README.md) | Infrastructure | Medium |
| Q0267 | [RAG latency budget](0267_rag_latency_budget/README.md) | Latency engineering | Medium |
| Q0268 | [Is a reranker worth it](0268_is_a_reranker_worth_it/README.md) | Reranking | Medium |
| Q0269 | [Late interaction MaxSim scoring](0269_late_interaction_maxsim_scoring/README.md) | Advanced retrieval | Medium |
| Q0270 | [Learned sparse retrieval](0270_learned_sparse_retrieval/README.md) | Advanced retrieval | Medium |
| Q0271 | [Synonym expansion for enterprise queries](0271_synonym_expansion_for_enterprise_queries/README.md) | Query understanding | Easy |
| Q0272 | [Acronym expansion](0272_acronym_expansion/README.md) | Query understanding | Easy |
| Q0273 | [Typo-tolerant term matching](0273_typo_tolerant_term_matching/README.md) | Query understanding | Medium |
| Q0274 | [Multilingual RAG](0274_multilingual_rag/README.md) | Global users | Medium |
| Q0275 | [Exact-match routing for identifiers](0275_exact_match_routing_for_identifiers/README.md) | Query understanding | Medium |
| Q0276 | [Chunk boundary problems](0276_chunk_boundary_problems/README.md) | Chunking | Medium |
| Q0277 | [Compare chunking strategies with an evaluation](0277_compare_chunking_strategies_with_an_evaluation/README.md) | Chunking | Medium |
| Q0278 | [Abstain when retrieval is weak](0278_abstain_when_retrieval_is_weak/README.md) | Reliability | Medium |
| Q0279 | [Calibrate a retrieval score threshold](0279_calibrate_a_retrieval_score_threshold/README.md) | Reliability | Medium |
| Q0280 | [Collapse near-identical hits across documents](0280_collapse_near_identical_hits_across_documents/README.md) | Context assembly | Medium |
| Q0281 | [Document versioning in the index](0281_document_versioning_in_the_index/README.md) | Ingestion | Medium |
| Q0282 | [Deletion and erasure in vector stores](0282_deletion_and_erasure_in_vector_stores/README.md) | Data governance | Hard |
| Q0283 | [PII in indexed content](0283_pii_in_indexed_content/README.md) | Data governance | Medium |
| Q0284 | [Prompt injection through retrieved documents](0284_prompt_injection_through_retrieved_documents/README.md) | Security | Medium |
| Q0285 | [Scan documents for injection patterns at ingestion](0285_scan_documents_for_injection_patterns_at_ingestion/README.md) | Security | Medium |
| Q0286 | [Hierarchical summaries as retrieval units](0286_hierarchical_summaries_as_retrieval_units/README.md) | Advanced retrieval | Medium |
| Q0287 | [Index generated question-answer pairs](0287_index_generated_question_answer_pairs/README.md) | Advanced retrieval | Medium |
| Q0288 | [Multi-vector document scoring](0288_multi_vector_document_scoring/README.md) | Advanced retrieval | Medium |
| Q0289 | [RAG over code repositories](0289_rag_over_code_repositories/README.md) | Domain RAG | Medium |
| Q0290 | [RAG over email and chat](0290_rag_over_email_and_chat/README.md) | Domain RAG | Medium |
| Q0291 | [Learn from user feedback](0291_learn_from_user_feedback/README.md) | Continuous improvement | Medium |
| Q0292 | [Monitoring RAG in production](0292_monitoring_rag_in_production/README.md) | Operations | Medium |
| Q0293 | [Interleaving tests for retrievers](0293_interleaving_tests_for_retrievers/README.md) | Experimentation | Hard |
| Q0294 | [RAG over scanned and image-heavy documents](0294_rag_over_scanned_and_image_heavy_documents/README.md) | Multimodal RAG | Medium |
| Q0295 | [Invalidate cached answers on document change](0295_invalidate_cached_answers_on_document_change/README.md) | Caching | Medium |
| Q0296 | [Streaming RAG answers with citations](0296_streaming_rag_answers_with_citations/README.md) | UX engineering | Medium |
| Q0297 | [End-to-end mini RAG pipeline](0297_end_to_end_mini_rag_pipeline/README.md) | RAG implementation | Hard |
| Q0298 | [RAG failure-mode checklist](0298_rag_failure_mode_checklist/README.md) | Debugging | Medium |
| Q0299 | [Cost model for a RAG service](0299_cost_model_for_a_rag_service/README.md) | Cost engineering | Medium |
| Q0300 | [Design entitlement-aware enterprise RAG for LLM Suite](0300_design_entitlement_aware_enterprise_rag_for_llm_suite/README.md) | System design | Hard |

[← All sections](../README.md)
