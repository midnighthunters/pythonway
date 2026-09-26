# JPMorganChase · Software Engineer III – LLM Suite Engineering · AI Interview Question Bank

1,000 AI-focused interview questions (10 batches of 100) for the
[Software Engineer III – LLM Suite Engineering – Senior Associate](https://jpmc.fa.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1002/job/210746921) role (requisition 210746921,
Corporate Technology, London). Every question is tied to an AI line of the job description: LLMs, RAG,
agents, LangGraph, MCP and A2A, Azure OpenAI and AWS Bedrock, GenAI services, evaluation and AI
security. Coding questions come with tested Python solutions; concept questions come with model
answers. Every question has its own folder with a `README.md`, plus likely follow-ups.

Two extra sections sit alongside the 1,000: `resume_questions` (AI deep-dive on the candidate's
resume) and `behavioural_questions` (the earlier behavioural bank, kept for reference).

## The AI parts of the job description, and where to practise them

| JD line | What the interviewer is likely to probe | Batch |
|---|---|---|
| Proficiency working with large language models | Tokens, attention, sampling, context windows, KV cache, latency and cost | 01 |
| Build AI/ML solutions … secure, reliable, production-ready | Prompt and context engineering, structured output, validation | 02 |
| Build AI/ML solutions for the LLM Suite platform; algorithms that integrate with existing systems | Chunking, embeddings, hybrid search, reranking, entitlement-aware RAG | 03 |
| Testing and operational stability; SDLC | Eval datasets, metrics, LLM-as-judge, CI gates, tracing | 04 |
| Agentic systems with modern agentic frameworks; agentic orchestration | ReAct, supervisor, planning, tool loops, sagas, DAG orchestration | 05 |
| Building agents with LangGraph | StateGraph, reducers, Send/Command, checkpointers, interrupts, streaming | 06 |
| A2A, MCP, AI skills development, personal AI assistants | MCP servers and clients, A2A tasks and Agent Cards, skills, assistants | 07 |
| Implement GenAI services on Azure OpenAI and AWS Bedrock; public cloud; elastic compute | Deployments, quotas, PTUs, Converse API, Guardrails, gateways, 429 handling | 08 |
| Python (FastAPI); microservices and APIs; NoSQL; messaging queues; containerization | Streaming endpoints, async jobs, conversation stores, caching, autoscaling | 09 |
| Write secure, high-quality code; technology controls agenda | Prompt injection, OWASP LLM Top 10, PII, tool permissions, model risk | 10 |

## What the rounds usually look like for AI roles at JPMorganChase

Candidate reports vary by team, so confirm the format with your recruiter.

- Online assessment (HackerRank): coding problems, increasingly with an applied flavour.
- Technical screen: a deep dive into past AI projects, then LLM/RAG/agent concepts, then live coding.
  For AI roles, reported coding tasks include implementing retrieval pieces, parsing model output,
  writing an agent loop, or building an API around a model.
- Final rounds: GenAI system design (for example an enterprise LLM gateway or entitlement-aware RAG),
  code review with a security lens, and behavioural questions.

## Sections

| Section | Focus | Questions | Maps to the job description |
|---|---|---|---|
| [batch_01_llm_fundamentals](batch_01_llm_fundamentals/README.md) | LLM Fundamentals & Inference | Q0001–Q0100 | Proficiency working with large language models; build AI/ML solutions. |
| [batch_02_prompting_context_structured_output](batch_02_prompting_context_structured_output/README.md) | Prompting, Context Engineering & Structured Output | Q0101–Q0200 | Proficiency working with LLMs; write secure, high-quality production code. |
| [batch_03_rag_retrieval](batch_03_rag_retrieval/README.md) | Retrieval-Augmented Generation (RAG) | Q0201–Q0300 | Build AI/ML solutions for the LLM Suite platform; algorithms that integrate with existing systems. |
| [batch_04_llm_evaluation_observability](batch_04_llm_evaluation_observability/README.md) | LLM Evaluation, Testing & Observability | Q0301–Q0400 | Testing and operational stability; strong understanding of the SDLC. |
| [batch_05_agentic_patterns_orchestration](batch_05_agentic_patterns_orchestration/README.md) | Agentic Patterns & Orchestration | Q0401–Q0500 | Agentic systems with modern agentic frameworks; agentic orchestrators; turn early patterns into production-ready capabilities. |
| [batch_06_langgraph_langchain](batch_06_langgraph_langchain/README.md) | LangGraph & LangChain in Practice | Q0501–Q0600 | Proficiency building agents with LangGraph. |
| [batch_07_mcp_a2a_skills_assistants](batch_07_mcp_a2a_skills_assistants/README.md) | MCP, A2A, Agent Skills & Personal AI Assistants | Q0601–Q0700 | Knowledge of A2A, MCP, AI skills development, personal AI assistants and agentic orchestrators. |
| [batch_08_azure_openai_bedrock_cloud_ai](batch_08_azure_openai_bedrock_cloud_ai/README.md) | Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | Q0701–Q0800 | Implement GenAI services leveraging Azure OpenAI models and AWS Bedrock; public cloud architecture; elastic compute. |
| batch_09_genai_services_fastapi | Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | pending | Python (FastAPI); microservices and APIs; elastic compute, NoSQL databases and messaging queues; containerization. |
| batch_10_ai_security_responsible_ai | AI Security, Guardrails & Responsible AI in a Bank | pending | Write secure, high-quality production code; secure, reliable AI capabilities; technology controls agenda. |
| [behavioural_questions](behavioural_questions/README.md) | Behavioural, Role & JPMorganChase | B0001–B0100 | Team player who seeks and applies feedback; collaborate with senior engineers in design discussions. |
| resume_questions | Resume Deep-Dive (Nikhil Goyal) | pending | Every JD line mapped to a claim on the resume that the interviewer can probe. |

## How to use this bank

- Work batch by batch. Answer each question out loud before reading the model answer; for coding
  questions, write the code first against the stated tests.
- Every Python solution includes assertions and runs offline with fake LLMs where a model would be
  called. `python .qbuild/build.py --test` executes all of them.
- Fast-moving facts (MCP 2026-07-28, A2A v1.0, LangGraph 1.x, cloud service features) were checked in
  September 2026. Re-check them before the interview.
- Use the follow-ups as the interviewer's next move.

## Sources

Content was researched from the sources below and rephrased for compliance with licensing
restrictions. Model answers are preparation material, not official JPMorganChase content.

- [Job posting 210746921 (JPMorganChase careers)](https://jpmc.fa.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1002/job/210746921)
- [Exponent: JP Morgan Chase AI engineer interview experience](https://www.tryexponent.com/experiences/jp-morgan-chase-ai-engineer-interview-3ef69d)
- [Glassdoor: JPMorganChase Applied AI/ML Associate interviews](https://www.glassdoor.com/Interview/JPMorganChase-Interview-Questions-E5224839.htm?filter.jobTitleExact=Applied%20AI/ML%20Associate)
- [Medium: interviewing at JPMorgan Chase for an ML engineer role](https://medium.com/@nagapavithralagisetty/i-interviewed-at-jpmorgan-chase-for-an-ml-engineer-role-and-got-rejected-here-is-what-i-learned-cf65f2b31cc0)
- [Dataford: JPMorganChase agentic AI engineer interview guide](https://dataford.io/interview-guides/jpmorganchase/agentic-ai-engineer)
- [TechPrep: JPMorgan interview process 2026](https://www.techprep.app/blog/jpmorgan-interview-process)
- [MCP specification 2026-07-28 changelog](https://modelcontextprotocol.io/specification/2026-07-28/changelog)
- [A2A protocol: what's new in v1.0](https://a2a-protocol.org/latest/whats-new-v1/)
- [A2A protocol specification](https://a2a-protocol.org/latest/specification/)
- [LangGraph documentation](https://docs.langchain.com/oss/python/langgraph/overview)
- [LangChain: human-in-the-loop middleware](https://docs.langchain.com/oss/python/langchain/human-in-the-loop)
- [OWASP Top 10 for LLM Applications](https://genai.owasp.org/llm-top-10/)
- [Microsoft Learn: Azure OpenAI in Foundry Models](https://learn.microsoft.com/en-us/azure/ai-foundry/openai/overview)
- [AWS: Amazon Bedrock Converse API](https://docs.aws.amazon.com/bedrock/latest/userguide/conversation-inference.html)
- [Bank of England: PRA SS1/23 model risk management principles](https://www.bankofengland.co.uk/prudential-regulation/publication/2023/may/model-risk-management-principles-for-banks-ss)
