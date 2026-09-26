"""
Verification Test Suite for Project 017: Query Transformation, Multi-Query & Sub-Questions
"""

import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from main import (
    generate_multi_queries,
    decompose_complex_query,
    retrieve_relevant_chunk,
    synthesize_final_answer,
    COFFEE_SHOP_KNOWLEDGE_BASE,
)


def test_multi_query_expansion():
    print("Testing Multi-Query Expansion...")
    q = "What are the laptop rules?"
    queries = generate_multi_queries(q, num_queries=3)

    assert isinstance(queries, list), "Output should be a list"
    assert len(queries) >= 2, f"Expected at least 2 queries, got {len(queries)}"
    print(f"  [PASSED] Generated {len(queries)} alternate query variations.")


def test_sub_question_decomposition():
    print("\nTesting Sub-Question Decomposition...")
    complex_q = "What time do you open on weekends and do you allow dogs inside?"
    sub_qs = decompose_complex_query(complex_q)

    assert isinstance(sub_qs, list), "Expected list of sub-questions"
    assert len(sub_qs) >= 2, f"Expected at least 2 sub-questions, got {len(sub_qs)}"
    print(f"  [PASSED] Successfully decomposed compound inquiry into {len(sub_qs)} sub-questions.")


def test_retrieval_and_synthesis():
    print("\nTesting targeted retrieval and final answer synthesis...")
    sub_q1 = "What time do you open on Saturday?"
    sub_q2 = "Are dogs allowed?"

    doc1 = retrieve_relevant_chunk(sub_q1, COFFEE_SHOP_KNOWLEDGE_BASE)
    doc2 = retrieve_relevant_chunk(sub_q2, COFFEE_SHOP_KNOWLEDGE_BASE)

    assert "Hours" in doc1["title"], f"Expected Hours doc, got {doc1['title']}"
    assert "Pet" in doc2["title"], f"Expected Pet doc, got {doc2['title']}"
    print("  [PASSED] Sub-questions correctly routed to targeted knowledge chunks.")

    pairs = [
        {"sub_query": sub_q1, "doc": doc1},
        {"sub_query": sub_q2, "doc": doc2},
    ]
    ans = synthesize_final_answer("Weekend hours and dog policy?", pairs)
    assert len(ans) > 50, "Synthesized answer was unexpectedly brief"
    assert "Saturday" in ans or "8:00" in ans or "patio" in ans.lower() or "dog" in ans.lower(), "Answer lacked grounded facts"
    print("  [PASSED] Final answer successfully synthesized all sub-query evidence.")


if __name__ == "__main__":
    print("=" * 60)
    print("RUNNING VERIFICATION SUITE: PROJECT 017")
    print("=" * 60)
    test_multi_query_expansion()
    test_sub_question_decomposition()
    test_retrieval_and_synthesis()
    print("\n[ALL TESTS PASSED] Project 017 verified successfully!")
