"""
Test verification suite for Project 050: LangGraph + RAG Adaptive Query Routing State Machine
"""

import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from main import (
    adaptive_graph,
    query_classifier_node,
    sql_rag_node,
    vector_rag_node,
    direct_llm_node,
    AdaptiveRouterState,
)


def test_classifier_intent_detection():
    # 1. Tabular query
    s1: AdaptiveRouterState = {
        "query": "How much total revenue did we make selling Cold Brew?",
        "route": "PENDING",
        "classification_reason": "",
        "retrieved_context": None,
        "sql_query": None,
        "sql_result": None,
        "final_answer": None,
    }
    r1 = query_classifier_node(s1)
    assert r1["route"] == "sql_rag"

    # 2. Unstructured technique query
    s2: AdaptiveRouterState = {
        "query": "What is the proper temperature for steaming oat milk?",
        "route": "PENDING",
        "classification_reason": "",
        "retrieved_context": None,
        "sql_query": None,
        "sql_result": None,
        "final_answer": None,
    }
    r2 = query_classifier_node(s2)
    assert r2["route"] == "vector_rag"

    # 3. Creative query
    s3: AdaptiveRouterState = {
        "query": "Tell me a short coffee joke",
        "route": "PENDING",
        "classification_reason": "",
        "retrieved_context": None,
        "sql_query": None,
        "sql_result": None,
        "final_answer": None,
    }
    r3 = query_classifier_node(s3)
    assert r3["route"] == "direct_llm"


def test_adaptive_graph_end_to_end_routing():
    # Test SQL execution
    s_sql: AdaptiveRouterState = {
        "query": "What are the total units sold for Cortado?",
        "route": "PENDING",
        "classification_reason": "",
        "retrieved_context": None,
        "sql_query": None,
        "sql_result": None,
        "final_answer": None,
    }
    out_sql = adaptive_graph.invoke(s_sql)
    assert out_sql["route"] == "sql_rag"
    assert out_sql["sql_query"] is not None
    assert "45" in str(out_sql["sql_result"]) or "45" in out_sql["final_answer"]

    # Test Vector execution
    s_vec: AdaptiveRouterState = {
        "query": "How many hours do we steep cold brew concentrate?",
        "route": "PENDING",
        "classification_reason": "",
        "retrieved_context": None,
        "sql_query": None,
        "sql_result": None,
        "final_answer": None,
    }
    out_vec = adaptive_graph.invoke(s_vec)
    assert out_vec["route"] == "vector_rag"
    assert "20" in out_vec["final_answer"]


if __name__ == "__main__":
    test_classifier_intent_detection()
    test_adaptive_graph_end_to_end_routing()
    print("Project 050: All verification tests PASSED successfully!")
