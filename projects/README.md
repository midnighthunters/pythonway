# 🌐 The 100 AI Projects Master Index

A complete, progressive curriculum taking you from foundational primitives to full-scale autonomous ecosystems.

### 🏛️ The 7 Core Pillars (Primary Focus)
1. **LangGraph** | 2. **LangChain** | 3. **RAG** | 4. **VectorDB** | 5. **MCP** | 6. **A2A** | 7. **FastAPI**

### 🛡️ The 5 Production Disciplines (Auxiliary Focus)
1. **LangSmith** (Tracing, telemetry, dataset curation)
2. **AI Evaluation** (LLM-as-a-judge, RAG metrics, faithfulness scoring)
3. **Agent Memory** (Working buffer, episodic recall, semantic long-term memory)
4. **Multi-Agent Systems (MAS)** (Hierarchical delegation, debate, swarms)
5. **Guardrails** (PII redaction, prompt injection defense, approval gates)

---

| ID | Project Name | Stage | Primary Pillars | Auxiliary Disciplines | Difficulty |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **001** | [Hello LCEL: Chat Models, Messages & Unix Pipes](./001_only_langchain_hello_lcel/README.md) | Stage 1 | `LangChain` | LangSmith Tracing | 1.0 |
| **002** | [Dynamic Prompt Templates & Few-Shot In-Context Learning](./002_only_langchain_prompt_engineering/README.md) | Stage 1 | `LangChain` | — | 1.5 |
| **003** | [Structured Output & Strict Pydantic Schema Enforcement](./003_only_langchain_structured_output/README.md) | Stage 1 | `LangChain` | Guardrails | 2.0 |
| **004** | [Advanced LCEL: RunnableParallel, Passthrough & Lambdas](./004_only_langchain_runnable_primitives/README.md) | Stage 1 | `LangChain` | — | 2.5 |
| **005** | [Resilient Chains: Fallbacks, Retries & LangSmith Observability](./005_only_langchain_fallbacks_and_retries/README.md) | Stage 1 | `LangChain` | LangSmith | 3.0 |
| **006** | [StateGraph Fundamentals & Custom Reducers](./006_only_langgraph_state_and_reducers/README.md) | Stage 1 | `LangGraph` | — | 2.0 |
| **007** | [Conditional Edges, Dynamic Routing & Graph Cycles](./007_only_langgraph_conditional_routing/README.md) | Stage 1 | `LangGraph` | — | 2.5 |
| **008** | [MemorySaver, Thread Checkpoints & Agent Working Memory](./008_only_langgraph_checkpoints_persistence/README.md) | Stage 1 | `LangGraph` | Agent Memory | 3.0 |
| **009** | [Human-in-the-Loop: Breakpoints, State Rewind & Guardrail Approval](./009_only_langgraph_human_in_the_loop/README.md) | Stage 1 | `LangGraph` | Guardrails | 3.5 |
| **010** | [Hierarchical Multi-Graph Architecture & Subgraphs](./010_only_langgraph_subgraphs_hierarchies/README.md) | Stage 1 | `LangGraph` | Multi-Agent Systems | 3.5 |
| **011** | [Vector Mathematics from Scratch: Cosine, Dot & Euclidean](./011_only_vectordb_math_from_scratch/README.md) | Stage 1 | `VectorDB` | — | 2.0 |
| **012** | [In-Memory Flat Vector Store & k-NN Search Engine](./012_only_vectordb_flat_index_store/README.md) | Stage 1 | `VectorDB` | Agent Memory | 2.5 |
| **013** | [Approximate Nearest Neighbors (ANN): HNSW & IVF Graphs](./013_only_vectordb_approximate_nearest_neighbors/README.md) | Stage 1 | `VectorDB` | — | 3.0 |
| **014** | [Metadata Payloads, Namespaces & Boolean Filtering](./014_only_vectordb_payload_metadata_filtering/README.md) | Stage 1 | `VectorDB` | Guardrails | 3.0 |
| **015** | [Hybrid Search: Dense Vectors + Sparse BM25 with RRF](./015_only_vectordb_hybrid_search_rrf/README.md) | Stage 1 | `VectorDB` | — | 3.5 |
| **016** | [Document Ingestion & Chunking Strategy Benchmark](./016_only_rag_chunking_strategies/README.md) | Stage 1 | `RAG` | — | 2.0 |
| **017** | [Query Transformation, Multi-Query & Sub-Questions](./017_only_rag_query_decomposition/README.md) | Stage 1 | `RAG` | — | 2.5 |
| **018** | [Contextual Compression & Cross-Encoder Re-ranking](./018_only_rag_reranking_compression/README.md) | Stage 1 | `RAG` | — | 3.0 |
| **019** | [HyDE: Hypothetical Document Embeddings for Deep Search](./019_only_rag_hyde_expansion/README.md) | Stage 1 | `RAG` | — | 3.0 |
| **020** | [CRAG: Corrective RAG with AI Evaluation Metrics](./020_only_rag_self_corrective_crag/README.md) | Stage 1 | `RAG` | AI Evaluation | 3.5 |
| **021** | [MCP Architecture: JSON-RPC 2.0 & Handshake Protocol](./021_only_mcp_jsonrpc_protocol_basics/README.md) | Stage 1 | `MCP` | — | 2.5 |
| **022** | [Custom Local Filesystem MCP Server](./022_only_mcp_local_filesystem_server/README.md) | Stage 1 | `MCP` | — | 3.0 |
| **023** | [Relational Database & SQL Inspection MCP Server](./023_only_mcp_database_sql_server/README.md) | Stage 1 | `MCP` | Guardrails | 3.0 |
| **024** | [Dynamic Resources & Reusable Prompt Templates via MCP](./024_only_mcp_resource_prompt_provider/README.md) | Stage 1 | `MCP` | — | 3.5 |
| **025** | [MCP Tool Sandboxing, Authorization & Execution Guardrails](./025_only_mcp_security_sandboxing/README.md) | Stage 1 | `MCP` | Guardrails | 3.5 |
| **026** | [Peer-to-Peer Agent Messaging Protocol & Addressing](./026_only_a2a_peer_messaging_bus/README.md) | Stage 1 | `A2A` | Multi-Agent Systems | 2.5 |
| **027** | [Hierarchical Supervisor-Worker Delegation Protocol](./027_only_a2a_supervisor_worker_delegation/README.md) | Stage 1 | `A2A` | Multi-Agent Systems | 3.0 |
| **028** | [Multi-Agent Dialectical Debate & Consensus Protocol](./028_only_a2a_multi_agent_debate_consensus/README.md) | Stage 1 | `A2A` | Multi-Agent Systems, AI Evaluation | 3.0 |
| **029** | [Contract Net Protocol: Market-Based Task Allocation](./029_only_a2a_contract_net_protocol/README.md) | Stage 1 | `A2A` | Multi-Agent Systems | 3.5 |
| **030** | [Asynchronous Pub/Sub Agent Event Bus with Dead Letters](./030_only_a2a_distributed_event_bus/README.md) | Stage 1 | `A2A` | Multi-Agent Systems | 3.5 |
| **031** | [FastAPI Core: Pydantic v2 Models & OpenAPI Specs](./031_only_fastapi_fundamentals/README.md) | Stage 1 | `FastAPI` | — | 1.5 |
| **032** | [Async Handlers, Dependency Injection & BackgroundTasks](./032_only_fastapi_async_dependencies/README.md) | Stage 1 | `FastAPI` | — | 2.5 |
| **033** | [Real-Time Streaming: Server-Sent Events (SSE) & WebSockets](./033_only_fastapi_sse_websockets/README.md) | Stage 1 | `FastAPI` | — | 3.0 |
| **034** | [JWT Security, Rate-Limiting & Prompt Injection Guardrails](./034_only_fastapi_auth_middleware/README.md) | Stage 1 | `FastAPI` | Guardrails | 3.0 |
| **035** | [Production FastAPI: Lifespan Handlers, Logging & Docker](./035_only_fastapi_production_lifespan/README.md) | Stage 1 | `FastAPI` | — | 3.5 |
| **036** | [FastAPI + LangChain: Token Streaming API with LangSmith Tracing](./036_fastapi_langchain_streaming_api/README.md) | Stage 2 | `FastAPI + LangChain` | LangSmith | 4.0 |
| **037** | [FastAPI + LangGraph: Multi-Turn Stateful Chatbot with Working Memory](./037_fastapi_langgraph_stateful_chat/README.md) | Stage 2 | `FastAPI + LangGraph` | Agent Memory | 4.5 |
| **038** | [FastAPI + LangGraph: Async Human Guardrail Approval Webhook API](./038_fastapi_langgraph_hitl_webhooks/README.md) | Stage 2 | `FastAPI + LangGraph` | Guardrails | 5.0 |
| **039** | [FastAPI + VectorDB: Semantic Search & Embedding Microservice](./039_fastapi_vectordb_search_service/README.md) | Stage 2 | `FastAPI + VectorDB` | — | 4.0 |
| **040** | [FastAPI + MCP: Exposing REST Endpoints as an MCP Server](./040_fastapi_mcp_server_bridge/README.md) | Stage 2 | `FastAPI + MCP` | — | 4.5 |
| **041** | [VectorDB + RAG: Parent Document Retriever for Deep Context](./041_vectordb_rag_parent_document_retriever/README.md) | Stage 2 | `VectorDB + RAG` | — | 4.5 |
| **042** | [VectorDB + RAG: Contextual Hybrid Search with Rank Fusion](./042_vectordb_rag_contextual_bm25_hybrid/README.md) | Stage 2 | `VectorDB + RAG` | — | 5.0 |
| **043** | [VectorDB + LangChain: Dynamic Semantic Few-Shot Selector](./043_vectordb_langchain_dynamic_few_shot/README.md) | Stage 2 | `VectorDB + LangChain` | — | 4.5 |
| **044** | [VectorDB + LangGraph: Cyclic Self-Correcting RAG with Evaluation](./044_vectordb_langgraph_self_correcting_rag/README.md) | Stage 2 | `VectorDB + LangGraph` | AI Evaluation | 5.0 |
| **045** | [VectorDB + A2A: Collaborative Multi-Agent Blackboard Memory](./045_vectordb_a2a_shared_blackboard/README.md) | Stage 2 | `VectorDB + A2A` | Multi-Agent Systems, Agent Memory | 5.5 |
| **046** | [LangGraph + MCP: ReAct Agent Connected to External MCP](./046_langgraph_mcp_tool_integration/README.md) | Stage 2 | `LangGraph + MCP` | — | 5.0 |
| **047** | [LangGraph + A2A: Multi-Agent Coder-Reviewer Dual Loop](./047_langgraph_a2a_coder_reviewer_cycle/README.md) | Stage 2 | `LangGraph + A2A` | Multi-Agent Systems | 5.0 |
| **048** | [LangChain + MCP: Dynamically Piping MCP Tools into LCEL](./048_langchain_mcp_unified_tools/README.md) | Stage 2 | `LangChain + MCP` | — | 4.5 |
| **049** | [LangChain + A2A: Multi-Agent Sequential Role Handoff](./049_langchain_a2a_sequential_handoff/README.md) | Stage 2 | `LangChain + A2A` | Multi-Agent Systems | 4.5 |
| **050** | [LangGraph + RAG: Adaptive Query Routing State Machine](./050_langgraph_rag_adaptive_router/README.md) | Stage 2 | `LangGraph + RAG` | — | 5.0 |
| **051** | [A2A + MCP: Multi-Agent Network with Dedicated MCP Servers](./051_a2a_mcp_distributed_tool_workers/README.md) | Stage 2 | `A2A + MCP` | Multi-Agent Systems | 5.5 |
| **052** | [A2A + FastAPI: Asynchronous Multi-Agent Broker Service](./052_a2a_fastapi_agent_broker_api/README.md) | Stage 2 | `A2A + FastAPI` | Multi-Agent Systems | 5.0 |
| **053** | [FastAPI + RAG: Production Q&A API with AI Evaluation Benchmarks](./053_fastapi_rag_cited_qa_service/README.md) | Stage 2 | `FastAPI + RAG` | AI Evaluation | 5.0 |
| **054** | [LangGraph + VectorDB: Semantic Long-Term Episodic Memory](./054_langgraph_vectordb_long_term_memory/README.md) | Stage 2 | `LangGraph + VectorDB` | Agent Memory | 5.5 |
| **055** | [MCP + VectorDB: Vector Database Server for MCP Clients](./055_mcp_vectordb_server_wrapper/README.md) | Stage 2 | `MCP + VectorDB` | — | 5.0 |
| **056** | [MCP + RAG: Remote RAG Engine via Model Context Protocol](./056_mcp_rag_remote_knowledge_provider/README.md) | Stage 2 | `MCP + RAG` | — | 5.5 |
| **057** | [LangChain + VectorDB: Semantic Chat History Retrieval Window](./057_langchain_vectordb_memory_window/README.md) | Stage 2 | `LangChain + VectorDB` | Agent Memory | 4.5 |
| **058** | [FastAPI + LangChain: Asynchronous Batch Document Worker](./058_fastapi_langchain_batch_processor/README.md) | Stage 2 | `FastAPI + LangChain` | LangSmith | 5.0 |
| **059** | [LangGraph + FastAPI: Long-Running Workflow Engine API](./059_langgraph_fastapi_workflow_resumption/README.md) | Stage 2 | `LangGraph + FastAPI` | — | 5.5 |
| **060** | [A2A + VectorDB: Multi-Agent Consensus Knowledge Archive](./060_a2a_vectordb_consensus_archive/README.md) | Stage 2 | `A2A + VectorDB` | Multi-Agent Systems, Agent Memory | 5.5 |
| **061** | [FastAPI + LangChain + VectorDB: Enterprise Search API with Tracing](./061_fastapi_langchain_vectordb_semantic_api/README.md) | Stage 3 | `FastAPI + LangChain + VectorDB` | LangSmith | 6.5 |
| **062** | [FastAPI + LangGraph + VectorDB: Stateful Support with Working Memory](./062_fastapi_langgraph_vectordb_support_bot/README.md) | Stage 3 | `FastAPI + LangGraph + VectorDB` | Agent Memory | 7.0 |
| **063** | [LangGraph + VectorDB + RAG: Autonomous Agentic RAG with Self-Evaluation](./063_langgraph_vectordb_rag_agentic_rag/README.md) | Stage 3 | `LangGraph + VectorDB + RAG` | AI Evaluation, Guardrails | 7.5 |
| **064** | [LangGraph + MCP + A2A: Autonomous Multi-Agent Dev Team](./064_langgraph_mcp_a2a_dev_team/README.md) | Stage 3 | `LangGraph + MCP + A2A` | Multi-Agent Systems | 7.5 |
| **065** | [FastAPI + LangGraph + A2A: Multi-Agent Swarm WebSocket Feed](./065_fastapi_langgraph_a2a_swarm_dashboard/README.md) | Stage 3 | `FastAPI + LangGraph + A2A` | Multi-Agent Systems | 7.0 |
| **066** | [FastAPI + LangGraph + HITL: Audited Compliance & Safety Guardrails](./066_fastapi_langgraph_hitl_compliance/README.md) | Stage 3 | `FastAPI + LangGraph + VectorDB` | Guardrails | 7.0 |
| **067** | [LangChain + VectorDB + RAG: Multimodal Retrieval Pipeline](./067_langchain_vectordb_rag_multimodal_retrieval/README.md) | Stage 3 | `LangChain + VectorDB + RAG` | — | 7.0 |
| **068** | [LangGraph + RAG + MCP: Deep Research Agent with Live Tools](./068_langgraph_rag_mcp_live_researcher/README.md) | Stage 3 | `LangGraph + RAG + MCP` | AI Evaluation | 7.5 |
| **069** | [FastAPI + MCP + A2A: Enterprise Multi-Agent Tool Gateway](./069_fastapi_mcp_a2a_agent_gateway/README.md) | Stage 3 | `FastAPI + MCP + A2A` | Multi-Agent Systems, Guardrails | 7.5 |
| **070** | [FastAPI + LangGraph + VectorDB: Dynamic Agent Memory Profiling](./070_langgraph_vectordb_fastapi_profile_memory/README.md) | Stage 3 | `FastAPI + LangGraph + VectorDB` | Agent Memory | 7.0 |
| **071** | [FastAPI + LangChain + RAG: Real-Time Document Ingestion API](./071_langchain_rag_fastapi_doc_ingestor/README.md) | Stage 3 | `FastAPI + LangChain + RAG` | — | 6.5 |
| **072** | [LangGraph + A2A + RAG: Adversarial Fact-Checking with LLM Judge](./072_langgraph_a2a_rag_adversarial_factchecker/README.md) | Stage 3 | `LangGraph + A2A + RAG` | Multi-Agent Systems, AI Evaluation | 7.5 |
| **073** | [FastAPI + LangChain + MCP: Secure AI Tool Proxy & Guardrails](./073_fastapi_langchain_mcp_tool_proxy/README.md) | Stage 3 | `FastAPI + LangChain + MCP` | Guardrails | 7.0 |
| **074** | [LangGraph + MCP + VectorDB: Autonomous BI Data Analyst](./074_langgraph_mcp_vectordb_data_analyst/README.md) | Stage 3 | `LangGraph + MCP + VectorDB` | — | 7.5 |
| **075** | [A2A + VectorDB + RAG: Distributed Multi-Agent Knowledge Swarm](./075_a2a_vectordb_rag_distributed_knowledge/README.md) | Stage 3 | `A2A + VectorDB + RAG` | Multi-Agent Systems, Agent Memory | 8.0 |
| **076** | [FastAPI + LangGraph + MCP: Self-Healing DevOps Automator](./076_fastapi_langgraph_mcp_devops_automator/README.md) | Stage 3 | `FastAPI + LangGraph + MCP` | Guardrails | 7.5 |
| **077** | [LangGraph + RAG + A2A: Hierarchical Multi-Agent Research Swarm](./077_langgraph_rag_a2a_hierarchical_analyst/README.md) | Stage 3 | `LangGraph + RAG + A2A` | Multi-Agent Systems | 8.0 |
| **078** | [FastAPI + VectorDB + A2A: Swarm Intelligence Platform](./078_fastapi_vectordb_a2a_collective_blackboard/README.md) | Stage 3 | `FastAPI + VectorDB + A2A` | Multi-Agent Systems, Agent Memory | 7.5 |
| **079** | [LangChain + MCP + RAG: Context-Aware Dynamic Tool Selector](./079_langchain_mcp_rag_context_tool_selector/README.md) | Stage 3 | `LangChain + MCP + RAG` | — | 7.5 |
| **080** | [FastAPI + LangGraph + RAG: Adaptive Q&A API with LangSmith Tracing](./080_fastapi_langgraph_rag_dynamic_orchestrator/README.md) | Stage 3 | `FastAPI + LangGraph + RAG` | LangSmith | 8.0 |
| **081** | [Autonomous Enterprise Support Center with LangSmith Feedback](./081_fastapi_langgraph_vectordb_rag_support_center/README.md) | Stage 4 | `FastAPI + LangGraph + VectorDB + RAG` | LangSmith, Guardrails | 8.5 |
| **082** | [Autonomous Financial Analyst with SEC Filings & SQL Tools](./082_fastapi_langgraph_mcp_vectordb_financial_analyst/README.md) | Stage 4 | `FastAPI + LangGraph + MCP + VectorDB` | Guardrails | 8.5 |
| **083** | [Multi-Agent Support Triage Swarm with Shared Episodic Memory](./083_fastapi_langgraph_a2a_vectordb_triage_engine/README.md) | Stage 4 | `FastAPI + LangGraph + A2A + VectorDB` | Multi-Agent Systems, Agent Memory | 8.5 |
| **084** | [Autonomous Cybersecurity Incident Response Team (SOC)](./084_langgraph_a2a_mcp_rag_cybersecurity_incident_response/README.md) | Stage 4 | `LangGraph + A2A + MCP + RAG` | Multi-Agent Systems, Guardrails | 9.0 |
| **085** | [Automated Software Factory: Jira Ticket to Verified Code PR](./085_fastapi_langgraph_a2a_mcp_software_factory/README.md) | Stage 4 | `FastAPI + LangGraph + A2A + MCP` | Multi-Agent Systems, AI Evaluation | 9.0 |
| **086** | [Multi-Tenant Enterprise Knowledge Engine with Strict RBAC Guardrails](./086_fastapi_langchain_vectordb_rag_multi_tenant_kb/README.md) | Stage 4 | `FastAPI + LangChain + VectorDB + RAG` | Guardrails | 8.5 |
| **087** | [Evidence-Based Clinical Decision Support & Dosage Calculator](./087_langgraph_vectordb_rag_mcp_clinical_assistant/README.md) | Stage 4 | `LangGraph + VectorDB + RAG + MCP` | Guardrails | 9.0 |
| **088** | [Venture Capital Autonomous Due Diligence & Investment Memo](./088_fastapi_langgraph_vectordb_a2a_vc_due_diligence/README.md) | Stage 4 | `FastAPI + LangGraph + VectorDB + A2A` | Multi-Agent Systems, AI Evaluation | 9.0 |
| **089** | [Legal Contract Risk Analyzer & Human-Gated Redline Engine](./089_fastapi_langgraph_rag_hitl_legal_contract_editor/README.md) | Stage 4 | `FastAPI + LangGraph + RAG + VectorDB` | Guardrails | 8.5 |
| **090** | [Autonomous Site Reliability Engineer (SRE) Incident Resolver](./090_langgraph_a2a_mcp_vectordb_autonomous_sre/README.md) | Stage 4 | `LangGraph + A2A + MCP + VectorDB` | Multi-Agent Systems, Agent Memory | 9.0 |
| **091** | [Peer-Reviewed Academic Paper Generator & Reviewer Swarm](./091_fastapi_langgraph_rag_a2a_academic_paper_writer/README.md) | Stage 4 | `FastAPI + LangGraph + RAG + A2A` | Multi-Agent Systems, AI Evaluation | 9.0 |
| **092** | [Autonomous Enterprise ERP & Supply Chain Invoice Auditor](./092_fastapi_langgraph_mcp_rag_erp_workflow/README.md) | Stage 4 | `FastAPI + LangGraph + MCP + RAG` | Guardrails | 9.0 |
| **093** | [B2B Autonomous Procurement & Price Negotiator Swarm](./093_langgraph_vectordb_a2a_mcp_hitl_supply_chain_negotiator/README.md) | Stage 4 | `LangGraph + VectorDB + A2A + MCP` | Multi-Agent Systems, Agent Memory, Guardrails | 9.5 |
| **094** | [Autonomous 24/7 Competitive Intelligence & Market Radar](./094_fastapi_langgraph_vectordb_rag_a2a_competitive_radar/README.md) | Stage 4 | `FastAPI + LangGraph + VectorDB + A2A` | Multi-Agent Systems, Agent Memory | 9.0 |
| **095** | [Autonomous Cloud Architecture & Monolith-to-Microservice Refactorer](./095_fastapi_langgraph_mcp_a2a_vectordb_cloud_migration_planner/README.md) | Stage 4 | `FastAPI + LangGraph + MCP + VectorDB` | Multi-Agent Systems, LangSmith | 9.5 |
| **096** | [Project Nexus: Enterprise Autonomous AI Coworker Platform](./096_enterprise_autonomous_coworker_platform/README.md) | Stage 5 | `FastAPI + LangGraph + LangChain + VectorDB + RAG + MCP + A2A` | LangSmith, Agent Memory, Multi-Agent Systems, Guardrails | 10.0 |
| **097** | [Project Forge: Autonomous Software Product Studio](./097_autonomous_software_product_studio/README.md) | Stage 5 | `FastAPI + LangGraph + LangChain + VectorDB + RAG + MCP + A2A` | Multi-Agent Systems, AI Evaluation, Agent Memory | 10.0 |
| **098** | [Project Alpha: Autonomous Quant Hedge Fund & Risk Desk](./098_autonomous_hedge_fund_risk_desk/README.md) | Stage 5 | `FastAPI + LangGraph + LangChain + VectorDB + RAG + MCP + A2A` | Multi-Agent Systems, Guardrails, AI Evaluation | 10.0 |
| **099** | [Project Cure: Autonomous Clinical Trial & Drug Discovery Hub](./099_clinical_trial_drug_discovery_hub/README.md) | Stage 5 | `FastAPI + LangGraph + LangChain + VectorDB + RAG + MCP + A2A` | Multi-Agent Systems, Guardrails, AI Evaluation, Agent Memory | 10.0 |
| **100** | [Project Antigravity: Self-Refining Autonomous AI Operating System](./100_antigravity_autonomous_ai_os/README.md) | Stage 5 | `FastAPI + LangGraph + LangChain + VectorDB + RAG + MCP + A2A` | LangSmith, AI Evaluation, Agent Memory, Multi-Agent Systems, Guardrails | 10.0 |

---
Generated by Antigravity AI Engineering Suite.