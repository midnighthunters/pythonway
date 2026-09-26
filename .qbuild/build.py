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
    coding(1, "arrays_strings_hashing", "Arrays, Strings & Hashing",
           "The most reported JPMorganChase HackerRank territory: array manipulation, string processing, "
           "counting with hash maps and sets, matrix basics and number/string conversions.",
           "Write secure, high-quality production code and maintain algorithms that integrate with existing systems."),
    coding(2, "two_pointers_sliding_window_intervals", "Two Pointers, Sliding Window, Prefix Sums, Intervals & Sorting",
           "Linear-time patterns that turn O(n^2) brute force into O(n): two pointers, fixed and variable windows, "
           "prefix sums with hash maps, interval merging/scheduling and custom sorting.",
           "Design, develop and troubleshoot software using creative approaches to solve complex technical challenges."),
    coding(3, "stacks_queues_linked_lists", "Stacks, Queues, Linked Lists & Data-Structure Design",
           "Stacks (parsing, monotonic stacks), queues and deques, linked-list surgery, and classic "
           "design-a-structure problems such as LRU/LFU caches, min stack and hit counters.",
           "Maintain algorithms that integrate with existing systems; operational stability."),
    coding(4, "trees_heaps_tries", "Trees, BSTs, Heaps & Tries",
           "Binary-tree traversal and recursion, BST properties, serialization, lowest common ancestors, "
           "heaps for top-k/streaming/scheduling problems, and tries for prefix search.",
           "Write and maintain algorithms that integrate with existing systems."),
    coding(5, "graphs_grids", "Graphs & Grids",
           "BFS/DFS on grids and graphs, topological sort for dependency ordering (think agent/task DAGs), "
           "union-find, shortest paths (Dijkstra, 0-1 BFS, Bellman-Ford), MST and cycle detection.",
           "Agentic orchestration (DAG scheduling), system design fundamentals."),
    coding(6, "dp_greedy_backtracking_binary_search", "Dynamic Programming, Greedy, Backtracking, Binary Search & Bits",
           "1-D/2-D DP, knapsack and string DP, greedy proofs, backtracking with pruning, binary search on the "
           "answer, and bit manipulation.",
           "Creative approaches to complex technical challenges; algorithms that integrate with existing systems."),
    coding(7, "python_coding_internals_async", "Python Coding, Internals, Concurrency & asyncio",
           "Python-specific coding: output prediction, data model, decorators, generators, context managers, "
           "descriptors, dataclasses and typing, collections/itertools, threading/multiprocessing and asyncio.",
           "Proficiency in Python (FastAPI); secure, high-quality production code."),
    coding(8, "sql_nosql_data_wrangling", "SQL, NoSQL & Data Wrangling",
           "SQL coding on banking-style schemas (joins, aggregates, window functions, CTEs, gaps and islands), "
           "each verified with sqlite3, plus NoSQL access patterns and Python data processing (CSV, JSON, logs).",
           "Modern database querying languages; NoSQL databases; large corporate environment."),
    coding(9, "practical_lld_fastapi_code_review", "Practical Coding, Low-Level Design, FastAPI & Code Review",
           "Interview-style practical problems: rate limiters, ledgers, idempotency, retries and circuit breakers, "
           "queue consumers, FastAPI endpoints tested with TestClient, and 'find the bugs' code-review exercises.",
           "Python (FastAPI); microservices and APIs; messaging queues; testing and operational stability; SDLC."),
    coding(10, "genai_agentic_coding", "GenAI & Agentic Coding: RAG, LangGraph, MCP, A2A, LLM Clients",
           "Hands-on GenAI coding: tokenization and chunking, vector and hybrid retrieval, evaluation metrics, "
           "streaming parsers, tool-call dispatch, guardrails, LangGraph graphs, MCP and A2A message handling, "
           "and resilient Azure OpenAI / Bedrock client code.",
           "Azure OpenAI and AWS Bedrock; LLMs and LangGraph agents; A2A, MCP, AI skills, personal assistants, "
           "agentic orchestrators."),
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
# JPMorganChase · Software Engineer III – LLM Suite Engineering · Round 1 Coding Question Bank

1,000 Round 1 coding questions (10 batches of 100) with tested Python solutions, complexity notes and
likely follow-ups, built for the [Software Engineer III – LLM Suite Engineering – Senior Associate]({job})
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
{rows}

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

- [Job posting 210746921 (JPMorganChase careers)]({job})
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
