"""
Verification Test Suite for Project 018: Contextual Compression & Cross-Encoder Re-ranking
"""

import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from main import (
    rerank_chunks,
    compress_context,
    RETRIEVED_CANDIDATE_CHUNKS,
)


def test_reranker_accuracy():
    print("Testing Cross-Encoder / Precision Re-ranking...")
    query = "How often do we descale the espresso machine, and what cleaning solution is approved?"

    top_chunks = rerank_chunks(query, RETRIEVED_CANDIDATE_CHUNKS, top_k=2, score_threshold=6.0)

    assert len(top_chunks) >= 1, "Re-ranker returned empty results"
    top_hit = top_chunks[0]
    assert "Descaling" in top_hit["title"], f"Expected descaling document ranked #1, got: {top_hit['title']}"
    assert top_hit["rerank_score"] >= 8.0, f"Expected high score for exact match, got {top_hit['rerank_score']}"
    print(f"  [PASSED] Re-ranker correctly placed [{top_hit['title']}] at Rank #1 with score {top_hit['rerank_score']}/10.")


def test_contextual_compression():
    print("\nTesting Contextual Compression (Trimming)...")
    query = "What is the approved descaling solution?"
    original_text = RETRIEVED_CANDIDATE_CHUNKS[2]["text"]

    compressed = compress_context(query, original_text)

    assert len(compressed) < len(original_text), "Compressed text was not shorter than original text"
    assert "EcoScale" in compressed or "Citric Acid" in compressed, "Critical answer fact was dropped during compression"
    print(f"  [PASSED] Context compressed from {len(original_text)} to {len(compressed)} characters while retaining critical entity.")


if __name__ == "__main__":
    print("=" * 60)
    print("RUNNING VERIFICATION SUITE: PROJECT 018")
    print("=" * 60)
    test_reranker_accuracy()
    test_contextual_compression()
    print("\n[ALL TESTS PASSED] Project 018 verified successfully!")
