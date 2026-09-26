# JPMorganChase · Software Engineer III – LLM Suite Engineering · Round 1 Coding Question Bank

1,000 Round 1 coding questions (10 batches of 100) with tested Python solutions, complexity notes and
likely follow-ups, built for the [Software Engineer III – LLM Suite Engineering – Senior Associate](https://jpmc.fa.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1002/job/210746921)
role (requisition 210746921, Corporate Technology, London). Two extra sections sit alongside the
1,000: `behavioural_questions` (the earlier behavioural bank) and `resume_questions` (a deep dive on
the candidate's resume). Every question has its own folder with a `README.md`.

## What the job description says, and what it means for Round 1

| JD line | What Round 1 is likely to test | Where to practise |
|---|---|---|
| Write secure, high-quality production code and maintain algorithms that integrate with existing systems | Easy/medium DSA in HackerRank style, clean and readable code, edge cases | Batches 01–06 |
| Design, develop and troubleshoot software using creative approaches | Problem decomposition, debugging, spotting bugs in someone else's code | Batches 02, 06, 09 |
| Proficiency in Python (FastAPI); microservices and APIs | Python internals, asyncio, FastAPI endpoints with validation and tests | Batches 07, 09 |
| Elastic compute, NoSQL databases and messaging queues; database querying languages; containerization | SQL (joins, windows, CTEs), NoSQL access patterns, idempotent queue consumers | Batches 08, 09 |
| Build AI/ML and agentic systems on Azure and AWS; GenAI on Azure OpenAI and AWS Bedrock | Retry/fallback LLM clients, streaming, token budgets, structured output | Batch 10 |
| LLMs and building agents with LangGraph | StateGraph, reducers, conditional edges, tool loops, checkpointing | Batch 10 |
| A2A, MCP, AI skills, personal AI assistants, agentic orchestrators | JSON-RPC handlers, tool registries, agent cards, DAG orchestration | Batches 05, 10 |
| System design, testing, operational stability, SDLC | Testable code, rate limiters, circuit breakers, assertions and pytest | Batch 09 |
| Corporate Technology: Finance, Treasury, Risk, Compliance; technology controls | Banking-flavoured problems: ledgers, reconciliation, suspicious accounts, audit | Batches 08, 09 |

## What Round 1 usually looks like

Candidate reports vary by team, so confirm the format with your recruiter.

- HackerRank online assessment: usually two easy-to-medium problems in 60–90 minutes, sometimes with
  multiple-choice or aptitude questions. Arrays, strings, hash maps, sorting, greedy and heaps come
  up most.
- Live technical screen: one or two LeetCode-medium problems in about 45 minutes, often after
  10–20 minutes on past projects, followed by complexity and follow-up questions.
- For this team, expect Python-specific and GenAI-flavoured coding (LangGraph, MCP, RAG, FastAPI) on
  top of standard DSA, and a code-review mindset (security, naming, tests, concurrency).

## Sections

| Section | Focus | Questions | Maps to the job description |
|---|---|---|---|
| [batch_01_arrays_strings_hashing](batch_01_arrays_strings_hashing/README.md) | Arrays, Strings & Hashing | Q0001–Q0100 | Write secure, high-quality production code and maintain algorithms that integrate with existing systems. |
| [batch_02_two_pointers_sliding_window_intervals](batch_02_two_pointers_sliding_window_intervals/README.md) | Two Pointers, Sliding Window, Prefix Sums, Intervals & Sorting | Q0101–Q0200 | Design, develop and troubleshoot software using creative approaches to solve complex technical challenges. |
| batch_03_stacks_queues_linked_lists | Stacks, Queues, Linked Lists & Data-Structure Design | pending | Maintain algorithms that integrate with existing systems; operational stability. |
| batch_04_trees_heaps_tries | Trees, BSTs, Heaps & Tries | pending | Write and maintain algorithms that integrate with existing systems. |
| batch_05_graphs_grids | Graphs & Grids | pending | Agentic orchestration (DAG scheduling), system design fundamentals. |
| batch_06_dp_greedy_backtracking_binary_search | Dynamic Programming, Greedy, Backtracking, Binary Search & Bits | pending | Creative approaches to complex technical challenges; algorithms that integrate with existing systems. |
| batch_07_python_coding_internals_async | Python Coding, Internals, Concurrency & asyncio | pending | Proficiency in Python (FastAPI); secure, high-quality production code. |
| batch_08_sql_nosql_data_wrangling | SQL, NoSQL & Data Wrangling | pending | Modern database querying languages; NoSQL databases; large corporate environment. |
| batch_09_practical_lld_fastapi_code_review | Practical Coding, Low-Level Design, FastAPI & Code Review | pending | Python (FastAPI); microservices and APIs; messaging queues; testing and operational stability; SDLC. |
| batch_10_genai_agentic_coding | GenAI & Agentic Coding: RAG, LangGraph, MCP, A2A, LLM Clients | pending | Azure OpenAI and AWS Bedrock; LLMs and LangGraph agents; A2A, MCP, AI skills, personal assistants, agentic orchestrators. |
| [behavioural_questions](behavioural_questions/README.md) | Behavioural, Role & JPMorganChase | B0001–B0100 | Team player who seeks and applies feedback; collaborate with senior engineers in design discussions. |
| resume_questions | Resume Deep-Dive (Nikhil Goyal) | pending | Every JD line mapped to a claim on the resume that the interviewer can probe. |

## How to use this bank

- Do the batches in order. 01–06 are the core DSA for the online assessment and live coding.
  07–10 cover the Python, data, practical and GenAI depth this team adds.
- Solve each problem out loud against a timer (about 20 minutes for Medium) before reading the
  answer. State the brute force, then optimise, then test edge cases.
- Every Python solution includes assertions. `python .qbuild/build.py --test` runs all of them.
- Use the follow-ups as the interviewer's next move.

## Sources

Problem selection draws on public reports of JPMorganChase interviews. Content was rephrased for
compliance with licensing restrictions, and all solutions were written independently.

- [Job posting 210746921 (JPMorganChase careers)](https://jpmc.fa.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1002/job/210746921)
- [TechPrep: JPMorgan interview process 2026](https://www.techprep.app/blog/jpmorgan-interview-process)
- [Interview Query: JPMorgan Chase software engineer guide](https://www.interviewquery.com/guides/jp-morgan-chase-software-engineer)
- [JPMorgan-tagged LeetCode problems (snehasishroy/leetcode-companywise-interview-questions)](https://github.com/snehasishroy/leetcode-companywise-interview-questions/tree/master/jpmorgan)
- [JPMorgan-tagged LeetCode problems (krishnadey30/LeetCode-Questions-CompanyWise)](https://github.com/krishnadey30/LeetCode-Questions-CompanyWise/blob/master/jpmorgan_alltime.csv)
- [GeeksforGeeks: JPMorgan Chase on-campus interview experience](https://www.geeksforgeeks.org/interview-experiences/jpmorgan-chase-co-interview-experience-on-campus-2/)
- [Soumendra Sahoo: JPMC Python developer interview questions](https://www.soumendrak.com/blog/jpmc-interview-experience/)
- [Exponent: JP Morgan Chase AI engineer interview experience](https://www.tryexponent.com/experiences/jp-morgan-chase-ai-engineer-interview-3ef69d)
- [1Point3Acres: JPMorgan Chase interview questions](https://www.1point3acres.com/interview/problems/company/jpmorgan)
- [MCP specification](https://modelcontextprotocol.io/specification/2026-07-28/changelog)
- [A2A protocol specification](https://a2a-protocol.org/latest/specification/)
- [LangGraph documentation](https://docs.langchain.com/oss/python/langgraph/overview)
