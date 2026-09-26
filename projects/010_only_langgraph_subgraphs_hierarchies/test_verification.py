"""
Verification Test Suite for Project 010: Subgraphs & Hierarchical Multi-Agent Systems
"""

import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from main import (
    build_research_subgraph,
    build_editorial_subgraph,
    build_hierarchical_orchestrator,
    ResearchState,
    EditorialState,
)


def test_research_subgraph_isolated():
    print("Testing Research Subgraph in complete isolation...")
    subgraph = build_research_subgraph()
    assert subgraph is not None, "Failed to compile research subgraph"

    input_state: ResearchState = {
        "topic": "Event-Driven Microservices",
        "raw_notes": "",
        "key_takeaways": [],
    }
    out = subgraph.invoke(input_state)

    assert "key_takeaways" in out, "Missing key_takeaways in research output"
    assert len(out["key_takeaways"]) >= 1, "Research subgraph produced empty takeaways"
    print(f"  [PASSED] Research subgraph isolated execution succeeded ({len(out['key_takeaways'])} takeaways produced).")


def test_editorial_subgraph_isolated():
    print("\nTesting Editorial Subgraph in complete isolation...")
    subgraph = build_editorial_subgraph()
    assert subgraph is not None, "Failed to compile editorial subgraph"

    input_state: EditorialState = {
        "topic": "Event-Driven Microservices",
        "facts": ["Decouples producers from consumers", "Enables asynchronous processing via message brokers"],
        "draft": "",
        "final_brief": "",
        "editor_approved": False,
    }
    out = subgraph.invoke(input_state)

    assert out["editor_approved"] is True, "Editorial approval flag was not set to True"
    assert "EXECUTIVE TECHNICAL BRIEF" in out["final_brief"], "Final brief missing expected header"
    print("  [PASSED] Editorial subgraph isolated execution succeeded.")


def test_hierarchical_orchestrator_end_to_end():
    print("\nTesting Parent Hierarchical Orchestrator end-to-end...")
    orchestrator = build_hierarchical_orchestrator()
    assert orchestrator is not None, "Failed to compile master orchestrator"

    state = {
        "topic": "Zero-Trust Architecture in Cloud Native AI",
        "research_takeaways": [],
        "final_published_document": "",
        "pipeline_audit": ["Test init"],
    }
    result = orchestrator.invoke(state)

    assert len(result["research_takeaways"]) >= 1, "Parent failed to capture research takeaways"
    assert len(result["final_published_document"]) > 0, "Parent failed to generate published document"
    assert len(result["pipeline_audit"]) >= 3, f"Expected at least 3 audit logs, got {len(result['pipeline_audit'])}"
    print(f"  [PASSED] Hierarchical Orchestrator completed successfully! Logs accumulated: {len(result['pipeline_audit'])}")


if __name__ == "__main__":
    print("=" * 60)
    print("RUNNING VERIFICATION SUITE: PROJECT 010")
    print("=" * 60)
    test_research_subgraph_isolated()
    test_editorial_subgraph_isolated()
    test_hierarchical_orchestrator_end_to_end()
    print("\n[ALL TESTS PASSED] Project 010 verified successfully!")
