"""
===============================================================================
PROJECT 010: SUBGRAPHS & HIERARCHICAL MULTI-AGENT SYSTEMS
Stage 1: Pure Fundamentals | Difficulty: 4.0 / 10 (Intermediate - Advanced)
===============================================================================

Core Concepts Demonstrated:
1. Subgraphs (Hierarchical Graphs): Embedding independent StateGraphs as nodes within a parent graph.
2. State Schema Encapsulation: Each subgraph maintains its own isolated, domain-specific state.
3. Inter-Graph State Mapping: Transforming parent state into child state and re-integrating child results.
4. Modular Multi-Agent System (MAS): Separating research and editorial workflows into autonomous sub-teams.
5. Independent Testability: Subgraphs can be compiled and verified in complete isolation before being composed.
===============================================================================
"""

import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import json
import re
from typing import TypedDict, Annotated, List
import operator
from langgraph.graph import StateGraph, START, END
from config import get_llm, ACTIVE_MODEL


# =============================================================================
# 1. SUBGRAPH A: RESEARCH TEAM (Isolated Schema & Nodes)
# =============================================================================
class ResearchState(TypedDict):
    topic: str
    raw_notes: str
    key_takeaways: List[str]


def research_gatherer_node(state: ResearchState) -> dict:
    """Gathers technical raw points on the given topic."""
    print("   [RESEARCH SUBGRAPH: Gatherer] Collecting technical concepts...")
    llm = get_llm(temperature=0.1)

    prompt = (
        f"You are a Senior Systems Analyst. Research this topic: '{state['topic']}'.\n"
        "Provide 3 key architectural facts or technical specifications.\n"
        "Be concise, technical, and concrete."
    )
    res = llm.invoke(prompt)
    return {"raw_notes": res.content.strip()}


def research_synthesizer_node(state: ResearchState) -> dict:
    """Condenses gathered research notes into structured bullet takeaways."""
    print("   [RESEARCH SUBGRAPH: Synthesizer] Extracting structured takeaways...")
    llm = get_llm(temperature=0.0)

    prompt = (
        f"Extract exactly 3 concise bullet points from these research notes:\n\n{state['raw_notes']}\n\n"
        "Format output as a valid JSON list of strings, e.g.: [\"Point 1\", \"Point 2\", \"Point 3\"]."
    )
    res = llm.invoke(prompt)
    raw = res.content.strip()

    # Clean markdown fences
    raw = re.sub(r"^```json\s*", "", raw)
    raw = re.sub(r"^```\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw).strip()

    try:
        points = json.loads(raw)
        if not isinstance(points, list):
            points = [p.strip() for p in raw.split("\n") if p.strip()]
    except Exception:
        points = [line.strip("- *") for line in raw.split("\n") if line.strip()][:3]

    return {"key_takeaways": points}


def build_research_subgraph():
    """Builds and compiles the standalone Research Subgraph."""
    builder = StateGraph(ResearchState)
    builder.add_node("gatherer", research_gatherer_node)
    builder.add_node("synthesizer", research_synthesizer_node)

    builder.add_edge(START, "gatherer")
    builder.add_edge("gatherer", "synthesizer")
    builder.add_edge("synthesizer", END)

    return builder.compile()


# =============================================================================
# 2. SUBGRAPH B: EDITORIAL TEAM (Isolated Schema & Nodes)
# =============================================================================
class EditorialState(TypedDict):
    topic: str
    facts: List[str]
    draft: str
    final_brief: str
    editor_approved: bool


def editorial_writer_node(state: EditorialState) -> dict:
    """Drafts an executive summary based on the research findings."""
    print("   [EDITORIAL SUBGRAPH: Writer] Composing executive brief...")
    llm = get_llm(temperature=0.2)

    facts_text = "\n".join(f"- {f}" for f in state["facts"])
    prompt = (
        f"You are a Lead Technology Journalist. Write a 2-paragraph executive brief on '{state['topic']}'\n"
        f"incorporating these technical facts:\n{facts_text}\n\n"
        "Make it engaging, authoritative, and clear."
    )
    res = llm.invoke(prompt)
    return {"draft": res.content.strip()}


def editorial_reviewer_node(state: EditorialState) -> dict:
    """Performs editorial review, adds an executive sign-off, and formats the final brief."""
    print("   [EDITORIAL SUBGRAPH: Reviewer] Conducting editorial check...")
    final = (
        f"# EXECUTIVE TECHNICAL BRIEF: {state['topic'].upper()}\n\n"
        f"{state['draft']}\n\n"
        f"---\n"
        f"Verified Facts Incorporated: {len(state['facts'])}\n"
        f"Editorial Sign-off: APPROVED FOR EXECUTIVE DISTRIBUTION\n"
    )
    return {"final_brief": final, "editor_approved": True}


def build_editorial_subgraph():
    """Builds and compiles the standalone Editorial Subgraph."""
    builder = StateGraph(EditorialState)
    builder.add_node("writer", editorial_writer_node)
    builder.add_node("reviewer", editorial_reviewer_node)

    builder.add_edge(START, "writer")
    builder.add_edge("writer", "reviewer")
    builder.add_edge("reviewer", END)

    return builder.compile()


# =============================================================================
# 3. PARENT GRAPH: ORCHESTRATOR PIPELINE
# =============================================================================
class ParentOrchestratorState(TypedDict):
    topic: str
    research_takeaways: List[str]
    final_published_document: str
    pipeline_audit: Annotated[List[str], operator.add]


# Instantiate compiled subgraphs
compiled_research_subgraph = build_research_subgraph()
compiled_editorial_subgraph = build_editorial_subgraph()


def call_research_team_node(state: ParentOrchestratorState) -> dict:
    """Adapter node: maps parent state to research subgraph, executes it, and maps results back."""
    print("\n>>> [PARENT ORCHESTRATOR] Delegating task to RESEARCH SUBGRAPH...")
    subgraph_input: ResearchState = {
        "topic": state["topic"],
        "raw_notes": "",
        "key_takeaways": [],
    }

    subgraph_output = compiled_research_subgraph.invoke(subgraph_input)
    takeaways = subgraph_output.get("key_takeaways", [])

    print(f">>> [PARENT ORCHESTRATOR] Research Subgraph returned {len(takeaways)} key findings.")
    return {
        "research_takeaways": takeaways,
        "pipeline_audit": [f"Research team finalized {len(takeaways)} takeaways."],
    }


def call_editorial_team_node(state: ParentOrchestratorState) -> dict:
    """Adapter node: maps research results to editorial subgraph, executes it, and maps results back."""
    print("\n>>> [PARENT ORCHESTRATOR] Delegating findings to EDITORIAL SUBGRAPH...")
    subgraph_input: EditorialState = {
        "topic": state["topic"],
        "facts": state["research_takeaways"],
        "draft": "",
        "final_brief": "",
        "editor_approved": False,
    }

    subgraph_output = compiled_editorial_subgraph.invoke(subgraph_input)
    document = subgraph_output.get("final_brief", "")

    print(">>> [PARENT ORCHESTRATOR] Editorial Subgraph returned approved document.")
    return {
        "final_published_document": document,
        "pipeline_audit": ["Editorial team published approved brief."],
    }


def build_hierarchical_orchestrator():
    """Builds and compiles the master hierarchical graph."""
    builder = StateGraph(ParentOrchestratorState)

    builder.add_node("research_team", call_research_team_node)
    builder.add_node("editorial_team", call_editorial_team_node)

    builder.add_edge(START, "research_team")
    builder.add_edge("research_team", "editorial_team")
    builder.add_edge("editorial_team", END)

    return builder.compile()


# =============================================================================
# 4. RUN DEMONSTRATION
# =============================================================================
def main():
    print("*" * 70)
    print("PROJECT 010: SUBGRAPHS & HIERARCHICAL MULTI-AGENT SYSTEMS")
    print(f"Active Groq Model: {ACTIVE_MODEL}")
    print("*" * 70)

    pipeline = build_hierarchical_orchestrator()

    topic = "The Role of Agentic Checkpointing in Long-Running Autonomous Workflows"
    initial_state = {
        "topic": topic,
        "research_takeaways": [],
        "final_published_document": "",
        "pipeline_audit": [f"Pipeline initialized for topic: '{topic}'"],
    }

    print(f"\nParent Pipeline Topic: '{topic}'")
    result = pipeline.invoke(initial_state)

    print("\n" + "=" * 70)
    print("FINAL PUBLISHED OUTPUT FROM HIERARCHICAL PIPELINE")
    print("=" * 70)
    print(result["final_published_document"])

    print("\n" + "=" * 70)
    print("MASTER PIPELINE AUDIT TRAIL")
    print("=" * 70)
    for log in result["pipeline_audit"]:
        print(f" • {log}")

    print("\n[SUCCESS] Project 010 executed cleanly end-to-end!")


if __name__ == "__main__":
    main()
