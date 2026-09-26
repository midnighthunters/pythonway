"""
Verification Test Suite for Project 020: CRAG (Corrective RAG) & AI Evaluation
"""

import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from main import (
    evaluate_retrieval_relevance,
    evaluate_faithfulness,
    run_crag_pipeline,
    COZY_COFFEE_POLICIES,
)


def test_crag_retrieval_evaluator():
    print("Testing CRAG Retrieval Evaluator / AI Grader...")

    # Case 1: In-domain query against matching doc
    doc_refill = COZY_COFFEE_POLICIES[0]
    q_valid = "Can I get a refill on my iced coffee?"
    grade_valid, _ = evaluate_retrieval_relevance(q_valid, doc_refill)
    assert grade_valid == "CORRECT", f"Expected CORRECT grade, got {grade_valid}"
    print("  [PASSED] In-domain query correctly received 'CORRECT' grade.")

    # Case 2: Irrelevant query against refill doc
    q_irrelevant = "How do I renew my driver's license?"
    grade_bad, _ = evaluate_retrieval_relevance(q_irrelevant, doc_refill)
    assert grade_bad == "INCORRECT", f"Expected INCORRECT grade, got {grade_bad}"
    print("  [PASSED] Irrelevant query correctly received 'INCORRECT' grade.")


def test_faithfulness_metric():
    print("\nTesting AI Faithfulness Metric...")
    context = "We sell whole bean coffee for $16 per bag."
    faithful_ans = "A bag of whole bean coffee costs $16."

    score, _ = evaluate_faithfulness(faithful_ans, context)
    assert score >= 8, f"Expected faithfulness score >= 8, got {score}"
    print(f"  [PASSED] Faithfulness metric correctly awarded {score}/10 to grounded answer.")


def test_crag_pipeline_branches():
    print("\nTesting CRAG end-to-end routing branches...")
    grade1, ans1 = run_crag_pipeline("What is the iced coffee refill policy?")
    assert grade1 == "CORRECT", "Expected valid query to branch to CORRECT"
    assert "refill" in ans1.lower()

    grade2, ans2 = run_crag_pipeline("Can I book a commercial submarine tour?")
    assert grade2 == "INCORRECT", "Expected out-of-domain query to branch to INCORRECT"
    assert "apologize" in ans2.lower() or "not contain" in ans2.lower()
    print("  [PASSED] CRAG dynamic routing executed both Grounded and Corrective branches.")


if __name__ == "__main__":
    print("=" * 60)
    print("RUNNING VERIFICATION SUITE: PROJECT 020")
    print("=" * 60)
    test_crag_retrieval_evaluator()
    test_faithfulness_metric()
    test_crag_pipeline_branches()
    print("\n[ALL TESTS PASSED] Project 020 verified successfully!")
