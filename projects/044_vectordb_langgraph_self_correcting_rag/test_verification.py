"""
Test verification suite for Project 044: VectorDB + LangGraph Self-Correcting RAG
"""

import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from main import crag_graph, grade_relevance_node, query_vectordb, SelfCorrectingRAGState


def test_direct_relevant_query():
    state: SelfCorrectingRAGState = {
        "original_query": "Swiss Water decaf process and chemical solvents",
        "current_query": "Swiss Water decaf process and chemical solvents",
        "documents": [],
        "overall_verdict": "PENDING",
        "relevance_score": 0.0,
        "grading_rationale": "",
        "rewrite_count": 0,
        "query_history": [],
        "final_generation": None,
    }
    result = crag_graph.invoke(state)
    assert result["overall_verdict"] == "RELEVANT"
    assert result["relevance_score"] >= 0.6
    assert result["documents"][0]["id"] == "doc_swiss_decaf"
    assert result["final_generation"] is not None
    assert len(result["final_generation"]) > 15


def test_relevance_grader_evaluator():
    # Test grading a relevant document
    docs = query_vectordb("Swiss Water decaf", top_k=1)
    state: SelfCorrectingRAGState = {
        "original_query": "What chemicals are used in decaf?",
        "current_query": "What chemicals are used in decaf?",
        "documents": docs,
        "overall_verdict": "PENDING",
        "relevance_score": 0.0,
        "grading_rationale": "",
        "rewrite_count": 0,
        "query_history": [],
        "final_generation": None,
    }
    graded = grade_relevance_node(state)
    assert graded["overall_verdict"] in ["RELEVANT", "IRRELEVANT"]
    assert "grading_rationale" in graded
    assert isinstance(graded["relevance_score"], float)


def test_self_correcting_cycle_completion():
    # Colloquial query
    state: SelfCorrectingRAGState = {
        "original_query": "how do they take the buzz out without chemicals?",
        "current_query": "how do they take the buzz out without chemicals?",
        "documents": [],
        "overall_verdict": "PENDING",
        "relevance_score": 0.0,
        "grading_rationale": "",
        "rewrite_count": 0,
        "query_history": [],
        "final_generation": None,
    }
    result = crag_graph.invoke(state)
    assert result["final_generation"] is not None
    assert len(result["query_history"]) >= 1
    # swiss water or decaf mentioned
    gen = result["final_generation"].lower()
    assert "decaf" in gen or "swiss water" in gen or "water" in gen


if __name__ == "__main__":
    test_direct_relevant_query()
    test_relevance_grader_evaluator()
    test_self_correcting_cycle_completion()
    print("Project 044: All verification tests PASSED successfully!")
