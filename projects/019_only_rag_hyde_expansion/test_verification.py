"""
Verification Test Suite for Project 019: HyDE (Hypothetical Document Embeddings)
"""

import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from main import (
    generate_hypothetical_document,
    score_relevance,
    search_corpus,
    BARISTA_TROUBLESHOOTING_CORPUS,
)


def test_hypothetical_document_generation():
    print("Testing HyDE synthetic document generation...")
    q = "Why is my shot sour?"
    hypo = generate_hypothetical_document(q)

    assert len(hypo) > 50, "Hypothetical document was unexpectedly short"
    lower_hypo = hypo.lower()
    has_technical_terms = any(t in lower_hypo for t in ["extract", "grind", "ratio", "acid", "dose", "temperature"])
    assert has_technical_terms, f"Hypothetical document lacked technical domain terms: {hypo}"
    print(f"  [PASSED] Generated rich synthetic document ({len(hypo)} chars) with technical domain terminology.")


def test_hyde_retrieval_accuracy():
    print("\nTesting HyDE retrieval accuracy on technical corpus...")
    hypo_text = (
        "Under-extraction causes severe sour taste and thin crema when the grind is too coarse "
        "and water flows too rapidly. Increase the extraction time and grind finer."
    )
    result = search_corpus(hypo_text, BARISTA_TROUBLESHOOTING_CORPUS)

    assert "Calibration" in result["doc"]["title"] or "Extraction" in result["doc"]["title"], (
        f"Failed to match extraction document: {result['doc']['title']}"
    )
    assert result["score"] > 0.1, f"Score was unexpectedly low: {result['score']}"
    print(f"  [PASSED] HyDE document matched target [{result['doc']['title']}] with score {result['score']:.4f}.")


if __name__ == "__main__":
    print("=" * 60)
    print("RUNNING VERIFICATION SUITE: PROJECT 019")
    print("=" * 60)
    test_hypothetical_document_generation()
    test_hyde_retrieval_accuracy()
    print("\n[ALL TESTS PASSED] Project 019 verified successfully!")
