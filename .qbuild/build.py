#!/usr/bin/env python3
"""Build the JPMorganChase LLM Suite Engineering (Round 1 coding) question bank.

Sources live in .qbuild/*.txt. Each question block:

    @@ Short title | Easy|Medium|Hard | Topic
    Q: Full question text (may continue on following lines, may contain code fences)
    A:
    Markdown answer (approach, ```python solution with asserts```, complexity) ...
    F:
    - follow-up question

Output tree (all under questions/):

    behavioural_questions/NNNN_<slug>/README.md      B0001-B0100 (source: behavioural.txt)
    batch_XX_<slug>/NNNN_<slug>/README.md            Q0001-Q1000 (source: batch_XX.txt)
    resume_questions/NNNN_<slug>/README.md           R0001-R0100 (source: resume.txt)

Usage (run with the project venv so FastAPI/LangGraph snippets can execute):
    python .qbuild/build.py --check                 # validate sources, print counts
    python .qbuild/build.py --build [--only KEY]    # write complete sections + root index
    python .qbuild/build.py --test  [--only KEY]    # execute every ```python block in answers
    python .qbuild/build.py --verify                # check the generated tree and links

KEY is a section key: behavioural, resume, or 01..10 for coding batches.
A python block whose first line contains "# no-run" is compiled but not executed.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = ROOT / "questions"
PER_SECTION = 100
JOB_URL = "https://jpmc.fa.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1002/job/210746921"

HEADER_RE = re.compile(r"^@@ (?P<title>.+?) \| (?P<difficulty>Easy|Medium|Hard) \| (?P<topic>.+?)\s*$")
QDIR_RE = re.compile(r"^(\d{4})_")
LINK_RE = re.compile(r"\]\(([^)\s]+)\)")
FORBIDDEN_TITLE_CHARS = set("|[]")


@dataclass(frozen=True)
class Section:
    key: str
    dirname: str
    title: str
    summary: str
    jd: str
    source_name: str
    prefix: str  # Q (coding), B (behavioural), R (resume)
    offset: int  # number of the first question minus one
    group: str  # prev/next navigation runs within a group

    @property
    def source(self) -> Path:
        return HERE / self.source_name


def coding(n: int, slug: str, title: str, summary: str, jd: str) -> Section:
    return Section(f"{n:02d}", f"batch_{n:02d}_{slug}", title, summary, jd, f"batch_{n:02d}.txt", "Q",
                   (n - 1) * PER_SECTION, "coding")


SECTIONS: list[Section] = [
    coding(1, "llm_fundamentals", "LLM Fundamentals & Inference",
           "How large language models work and how they are served: transformers and attention, tokenization, "
           "embeddings, decoding and sampling, context windows, KV cache, latency and throughput, fine-tuning "
           "versus RAG, with NumPy/Python coding tasks that implement the core pieces.",
           "Proficiency working with large language models; build AI/ML solutions."),
    coding(2, "prompting_context_structured_output", "Prompting, Context Engineering & Structured Output",
           "Prompt design, system prompts, few-shot and reasoning models, context engineering and token budgets, "
           "structured output with JSON Schema and Pydantic, function-calling formats, prompt versioning, and "
           "coding tasks such as template rendering, context trimming and JSON repair with validation.",
           "Proficiency working with LLMs; write secure, high-quality production code."),
    coding(3, "rag_retrieval", "Retrieval-Augmented Generation (RAG)",
           "End-to-end RAG: ingestion and chunking, embeddings, vector indexes, hybrid search (BM25 + vectors), "
           "reciprocal rank fusion, reranking, query rewriting, entitlement-aware retrieval, citations and "
           "grounding, with runnable implementations of each building block.",
           "Build AI/ML solutions for the LLM Suite platform; algorithms that integrate with existing systems."),
    coding(4, "llm_evaluation_observability", "LLM Evaluation, Testing & Observability",
           "Golden datasets, retrieval and generation metrics, LLM-as-judge and calibration, agent trajectory "
           "evaluation, CI evaluation gates, tracing (LangSmith, OpenTelemetry GenAI conventions), cost and latency "
           "monitoring, online experiments, with metric implementations you can run.",
           "Testing and operational stability; strong understanding of the SDLC."),
    coding(5, "agentic_patterns_orchestration", "Agentic Patterns & Orchestration",
           "ReAct, plan-and-execute, reflection, routing, supervisor and multi-agent designs, tool-calling loops, "
           "memory, human approval, loop guards, parallel tool execution, DAG orchestration and sagas with "
           "compensation, all coded against fake LLMs so the logic is testable.",
           "Agentic systems with modern agentic frameworks; agentic orchestrators; turn early patterns into "
           "production-ready capabilities."),
    coding(6, "langgraph_langchain", "LangGraph & LangChain in Practice",
           "LangGraph 1.x hands-on: StateGraph and reducers, conditional edges, Send and Command, subgraphs, "
           "checkpointers and threads, interrupts for human-in-the-loop, streaming modes, the Store for long-term "
           "memory, time travel, and LangChain 1.x agents and middleware. Snippets run against the installed "
           "langgraph package.",
           "Proficiency building agents with LangGraph."),
    coding(7, "mcp_a2a_skills_assistants", "MCP, A2A, Agent Skills & Personal AI Assistants",
           "Model Context Protocol (tools, resources, prompts, transports, authorization and the stateless "
           "2026-07-28 revision), the A2A protocol v1.0 (Agent Cards, tasks, parts, streaming, push notifications), "
           "Agent Skills, and personal-assistant design, with JSON-RPC and protocol handlers you can run.",
           "Knowledge of A2A, MCP, AI skills development, personal AI assistants and agentic orchestrators."),
    coding(8, "azure_openai_bedrock_cloud_ai", "Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure",
           "Azure OpenAI (deployments, quotas, PTUs, content filtering, Entra ID auth, API Management as an AI "
           "gateway), Amazon Bedrock (Converse API, Guardrails, Knowledge Bases, AgentCore, cross-Region "
           "inference), multi-provider routing, rate-limit handling, streaming, elastic compute and GPU serving.",
           "Implement GenAI services leveraging Azure OpenAI models and AWS Bedrock; public cloud architecture; "
           "elastic compute."),
    coding(9, "genai_services_fastapi", "Building GenAI Services: FastAPI, Streaming, Queues & NoSQL",
           "Production GenAI microservices: FastAPI endpoints for chat and agents, SSE token streaming, async "
           "concurrency and backpressure, long-running agent jobs on queues, conversation state in NoSQL, "
           "semantic caching, per-tenant quotas and cost metering, containers and autoscaling. Endpoints are "
           "tested with FastAPI's TestClient.",
           "Python (FastAPI); microservices and APIs; elastic compute, NoSQL databases and messaging queues; "
           "containerization."),
    coding(10, "ai_security_responsible_ai", "AI Security, Guardrails & Responsible AI in a Bank",
           "Prompt injection (direct and indirect), OWASP Top 10 for LLM and agentic applications, tool "
           "permissioning and least privilege, PII redaction, output handling, data leakage and entitlements, "
           "red teaming, model risk management and regulation, audit logging, with guardrail code you can run.",
           "Write secure, high-quality production code; secure, reliable AI capabilities; technology controls "
           "agenda."),
    Section("behavioural", "behavioural_questions", "Behavioural, Role & JPMorganChase",
            "Recruiter-screen, hiring-manager and HireVue-style questions: motivation, JPMorganChase and LLM Suite, "
            "the Business Principles, and STAR stories on collaboration, feedback, ownership and integrity.",
            "Team player who seeks and applies feedback; collaborate with senior engineers in design discussions.",
            "behavioural.txt", "B", 0, "behavioural"),
    Section("resume", "resume_questions", "Resume Deep-Dive (Nikhil Goyal)",
            "Questions an interviewer is likely to ask from the resume: American Express (Trip Rescue, Smart Spend, "
            "MCP code-fix, AskAmex RAG), Morgan Stanley (LLM risk assistant, trade breaks, Kafka to Cassandra), "
            "Nagarro payments, and the Madagascar, FraudShield, Aurelia and QLoRA projects. Many include code.",
            "Every JD line mapped to a claim on the resume that the interviewer can probe.",
            "resume.txt", "R", 0, "resume"),
]
BY_KEY = {s.key: s for s in SECTIONS}


@dataclass
class Question:
    section: Section
    index: int
    title: str
    difficulty: str
    topic: str
    question: str
    answer: str
    followups: str
    line: int

    @property
    def number(self) -> int:
        return self.section.offset + self.index

    @property
    def qid(self) -> str:
        return f"{self.section.prefix}{self.number:04d}"

    @property
    def dirname(self) -> str:
        return f"{self.number:04d}_{slugify(self.title)}"

    @property
    def relpath(self) -> str:
        return f"{self.section.dirname}/{self.dirname}/README.md"


def slugify(text: str, max_len: int = 60) -> str:
    slug = text.lower().replace("&", " and ")
    slug = re.sub(r"[^a-z0-9]+", "_", slug).strip("_")
    if len(slug) > max_len:
        cut = slug[:max_len]
        slug = cut.rsplit("_", 1)[0] if "_" in cut else cut
    return slug.strip("_") or "question"


def _clean(lines: list[str]) -> str:
    lines = list(lines)
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    return "\n".join(lines)


def parse_section(section: Section) -> tuple[list[Question], list[str]]:
    errors: list[str] = []
    if not section.source.exists():
        return [], errors
    name = section.source.name
    questions: list[Question] = []
    current: dict | None = None
    part = ""
    in_code = False

    def close() -> None:
        nonlocal current
        if current is None:
            return
        where = f"{name}:{current['line']} ({current['title']})"
        if in_code:
            errors.append(f"{where}: unclosed code fence")
        if part != "f":
            errors.append(f"{where}: missing 'A:' or 'F:' marker")
        q, a, f = (_clean(current[key]) for key in ("q", "a", "f"))
        for label, value in (("question", q), ("answer", a), ("follow-ups", f)):
            if not value:
                errors.append(f"{where}: empty {label}")
        if FORBIDDEN_TITLE_CHARS & set(current["title"]):
            errors.append(f"{where}: title must not contain | [ ]")
        questions.append(Question(section, len(questions) + 1, current["title"].strip(), current["difficulty"],
                                  current["topic"].strip(), q, a, f, current["line"]))
        current = None

    for lineno, raw in enumerate(section.source.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.rstrip()
        stripped = line.strip()
        if not in_code:
            match = HEADER_RE.match(line)
            if match:
                close()
                in_code = False
                current = {"line": lineno, "q": [], "a": [], "f": [], **match.groupdict()}
                part = "q"
                continue
        if current is None:
            if stripped:
                errors.append(f"{name}:{lineno}: text before the first '@@' header")
            continue
        if stripped.startswith("```"):
            in_code = not in_code
        elif not in_code:
            if part == "q" and stripped == "A:":
                part = "a"
                continue
            if part == "a" and stripped == "F:":
                part = "f"
                continue
        if part == "q" and line.startswith("Q: "):
            line = line[3:]
        current[part].append(line)
    close()
    return questions, errors


def python_blocks(markdown: str) -> list[str]:
    blocks, buf, inside = [], [], False
    for line in markdown.splitlines():
        s = line.strip()
        if not inside and s.startswith("```python"):
            inside, buf = True, []
        elif inside and s.startswith("```"):
            inside = False
            blocks.append("\n".join(buf))
        elif inside:
            buf.append(line)
    return blocks


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)


def nav_line(q: Question, prev: Question | None, nxt: Question | None) -> str:
    parts = []
    if prev:
        parts.append(f"[← {prev.qid}](../../{prev.relpath})")
    parts.append(f"[{q.section.title} index](../README.md)")
    parts.append("[All sections](../../README.md)")
    if nxt:
        parts.append(f"[{nxt.qid} →](../../{nxt.relpath})")
    return " · ".join(parts)


def render_question(q: Question, prev: Question | None, nxt: Question | None) -> str:
    return "\n".join([
        f"# {q.qid} · {q.title}", "",
        "| Section | Topic | Difficulty |", "|---|---|---|",
        f"| {q.section.title} | {q.topic} | {q.difficulty} |", "",
        "## Question", "", q.question, "",
        "## Answer", "", q.answer, "",
        "## Likely follow-ups", "", q.followups, "",
        "---", "", nav_line(q, prev, nxt), "",
    ])


def render_section(section: Section, qs: list[Question]) -> str:
    counts = Counter(q.difficulty for q in qs)
    lines = [
        f"# {section.title}", "", section.summary, "",
        f"Maps to the job description: {section.jd}", "",
        f"{qs[0].qid}–{qs[-1].qid} · {len(qs)} questions · Easy {counts['Easy']} · "
        f"Medium {counts['Medium']} · Hard {counts['Hard']}", "",
        "| # | Question | Topic | Difficulty |", "|---|---|---|---|",
    ]
    lines += [f"| {q.qid} | [{q.title}]({q.dirname}/README.md) | {q.topic} | {q.difficulty} |" for q in qs]
    lines += ["", "[← All sections](../README.md)", ""]
    return "\n".join(lines)


ROOT_README = """
# JPMorganChase · Software Engineer III – LLM Suite Engineering · AI Interview Question Bank

1,000 AI-focused interview questions (10 batches of 100) for the
[Software Engineer III – LLM Suite Engineering – Senior Associate]({job}) role (requisition 210746921,
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
{rows}

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

- [Job posting 210746921 (JPMorganChase careers)]({job})
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
"""


def render_root(parsed: dict[str, list[Question]]) -> str:
    rows = []
    for s in SECTIONS:
        qs = parsed.get(s.key, [])
        if len(qs) == PER_SECTION:
            rows.append(f"| [{s.dirname}]({s.dirname}/README.md) | {s.title} | {qs[0].qid}–{qs[-1].qid} | {s.jd} |")
        else:
            rows.append(f"| {s.dirname} | {s.title} | pending | {s.jd} |")
    return ROOT_README.strip().format(job=JOB_URL, rows="\n".join(rows)) + "\n"


def build_section(section: Section, qs: list[Question], ordered: list[Question]) -> None:
    sdir = OUT / section.dirname
    expected = {q.dirname for q in qs}
    if sdir.exists():
        for child in sdir.iterdir():
            if child.is_dir() and QDIR_RE.match(child.name) and child.name not in expected:
                if {p.name for p in child.iterdir()} <= {"README.md"}:
                    shutil.rmtree(child)
                else:
                    print(f"WARNING: kept stale folder with extra files: {child}")
    pos = {q.qid: i for i, q in enumerate(ordered)}
    for q in qs:
        i = pos[q.qid]
        prev = ordered[i - 1] if i > 0 else None
        nxt = ordered[i + 1] if i + 1 < len(ordered) else None
        write(sdir / q.dirname / "README.md", render_question(q, prev, nxt))
    write(sdir / "README.md", render_section(section, qs))


def run_block(item: tuple[str, int, str]) -> str | None:
    qid, n, code = item
    label = f"{qid} block {n}"
    first = code.lstrip().splitlines()[0] if code.strip() else ""
    try:
        compile(code, label, "exec")
    except SyntaxError as exc:
        return f"{label}: SyntaxError {exc}"
    if "# no-run" in first:
        return None
    with tempfile.TemporaryDirectory() as tmp:
        try:
            proc = subprocess.run([sys.executable, "-c", code], cwd=tmp, capture_output=True, text=True,
                                  timeout=60, encoding="utf-8", errors="replace")
        except subprocess.TimeoutExpired:
            return f"{label}: timeout"
    if proc.returncode != 0:
        tail = "\n    ".join((proc.stderr or proc.stdout).strip().splitlines()[-6:])
        return f"{label}: exit {proc.returncode}\n    {tail}"
    return None


def test(parsed: dict[str, list[Question]], only: str | None) -> int:
    items = []
    for s in SECTIONS:
        if only not in (None, s.key):
            continue
        for q in parsed.get(s.key, []):
            for n, code in enumerate(python_blocks(q.answer), 1):
                items.append((q.qid, n, code))
    with ThreadPoolExecutor(max_workers=8) as pool:
        failures = [r for r in pool.map(run_block, items) if r]
    print(f"python blocks: {len(items)} | failures: {len(failures)}")
    for f in failures:
        print("FAIL:", f)
    return 1 if failures else 0


def verify() -> int:
    problems: list[str] = []
    if not OUT.exists():
        print("questions/ does not exist")
        return 1
    total = 0
    for s in SECTIONS:
        sdir = OUT / s.dirname
        if not sdir.exists():
            problems.append(f"missing section folder {s.dirname}")
            continue
        qdirs = sorted(p for p in sdir.iterdir() if p.is_dir())
        got = [int(QDIR_RE.match(p.name).group(1)) for p in qdirs if QDIR_RE.match(p.name)]
        want = list(range(s.offset + 1, s.offset + PER_SECTION + 1))
        if got != want:
            problems.append(f"{s.dirname}: {len(qdirs)} folders, numbering is not {want[0]}..{want[-1]}")
        for qdir in qdirs:
            readme = qdir / "README.md"
            if readme.is_file() and readme.stat().st_size > 0:
                total += 1
            else:
                problems.append(f"missing or empty README: {qdir.relative_to(OUT)}")
    extra = {p.name for p in OUT.iterdir() if p.is_dir()} - {s.dirname for s in SECTIONS}
    if extra:
        problems.append(f"unexpected folders in questions/: {sorted(extra)}")
    for md in OUT.rglob("README.md"):
        in_code = False
        for text_line in md.read_text(encoding="utf-8").splitlines():
            if text_line.strip().startswith("```"):
                in_code = not in_code
                continue
            if in_code:
                continue
            for target in LINK_RE.findall(text_line):
                if target.startswith(("http://", "https://", "#", "mailto:")):
                    continue
                if not (md.parent / target).resolve().exists():
                    problems.append(f"broken link in {md.relative_to(OUT)} -> {target}")
    print(f"question folders with README: {total}")
    for p in problems[:60]:
        print("PROBLEM:", p)
    if len(problems) > 60:
        print(f"... and {len(problems) - 60} more")
    return 1 if problems else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--build", action="store_true")
    mode.add_argument("--test", action="store_true")
    mode.add_argument("--verify", action="store_true")
    parser.add_argument("--only", help="section key: behavioural, resume, or 01..10")
    args = parser.parse_args(argv)
    if args.only and args.only not in BY_KEY:
        parser.error(f"unknown section {args.only!r}; choose from {sorted(BY_KEY)}")
    if args.verify:
        return verify()

    parsed: dict[str, list[Question]] = {}
    errors: list[str] = []
    for s in SECTIONS:
        qs, errs = parse_section(s)
        errors += errs
        if s.source.exists():
            parsed[s.key] = qs

    seen: dict[tuple[str, str], str] = {}
    for qs in parsed.values():
        for q in qs:
            key = (q.section.group, q.title.lower())
            if key in seen:
                errors.append(f"duplicate title '{q.title}' ({seen[key]} and {q.qid})")
            else:
                seen[key] = q.qid

    total = 0
    for s in SECTIONS:
        qs = parsed.get(s.key)
        if qs is None:
            print(f"{s.key:>11}: pending")
            continue
        c = Counter(q.difficulty for q in qs)
        status = "complete" if len(qs) == PER_SECTION else f"INCOMPLETE {len(qs)}/{PER_SECTION}"
        print(f"{s.key:>11}: {len(qs):3d} | Easy {c['Easy']:3d} Medium {c['Medium']:3d} Hard {c['Hard']:3d} | {status}")
        total += len(qs)
    print(f"total questions: {total}")
    for e in errors:
        print("ERROR:", e)

    if args.check:
        return 1 if errors else 0
    if args.test:
        return test(parsed, args.only)
    if errors:
        print("Refusing to build while there are errors.")
        return 1

    complete = [s for s in SECTIONS if len(parsed.get(s.key, [])) == PER_SECTION]
    targets = [s for s in complete if args.only in (None, s.key)]
    if args.only and not targets:
        print(f"Section {args.only} is not complete; nothing built.")
        return 1
    for s in targets:
        ordered = [q for c in complete if c.group == s.group for q in parsed[c.key]]
        build_section(s, parsed[s.key], ordered)
        print(f"built {s.dirname}")
    write(OUT / "README.md", render_root(parsed))
    print("wrote questions/README.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
