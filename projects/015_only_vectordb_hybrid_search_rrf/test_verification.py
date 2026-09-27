"""
Automated Verification Suite for Project 015: Hybrid Search: Dense Vectors + Sparse BM25 with RRF.
Validates BM25 lexical scoring, Dense cosine similarity, RRF rank fusion mathematics,
and end-to-end hybrid retrieval scenarios.
"""

import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from main import (
    Document,
    DenseVectorEngine,
    BM25Engine,
    ReciprocalRankFusion,
    HybridSearchPipeline,
    ScoredResult,
    SAMPLE_CORPUS,
)


def test_bm25_scoring():
    print("Testing BM25 Exact Keyword Scoring...")
    docs = [
        Document("d1", "Hardware Reset", "Error code ERR-RESET-999 requires pressing red switch."),
        Document("d2", "Espresso Cleaning", "Daily cleaning with detergent powder."),
    ]
    bm25 = BM25Engine()
    bm25.index_documents(docs)

    hits = bm25.search("ERR-RESET-999", top_k=2)
    assert len(hits) > 0, "BM25 should find exact token match"
    assert hits[0].doc_id == "d1", f"Expected top match d1, got {hits[0].doc_id}"
    assert hits[0].score > 0.0
    print("  [PASSED] BM25 exact keyword scoring verified.")


def test_dense_vector_scoring():
    print("Testing Dense Vector Semantic Scoring...")
    docs = [
        Document("d_drink", "Coffee Beverage", "Hot freshly poured espresso with foamy steamed milk."),
        Document("d_repair", "Plumbing Valve", "Replacing high pressure copper pipe fittings."),
    ]
    dense = DenseVectorEngine()
    dense.index_documents(docs)

    hits = dense.search("delicious warm morning coffee with froth", top_k=2)
    assert len(hits) == 2
    assert hits[0].doc_id == "d_drink", f"Expected top match d_drink, got {hits[0].doc_id}"
    assert hits[0].score > 0.3
    print("  [PASSED] Dense vector semantic scoring verified.")


def test_rrf_rank_fusion_math():
    print("Testing RRF Rank Fusion Mathematics...")
    rrf = ReciprocalRankFusion(k=60)

    # Document A is Rank 1 in Retriever 1 and Rank 2 in Retriever 2
    # Document B is Rank 2 in Retriever 1 and Rank 1 in Retriever 2
    # Document C is Rank 1 in Retriever 1 but unranked in Retriever 2
    list_1 = [
        ScoredResult("doc_A", 0.9, 1, "R1"),
        ScoredResult("doc_B", 0.8, 2, "R1"),
        ScoredResult("doc_C", 0.7, 3, "R1"),
    ]
    list_2 = [
        ScoredResult("doc_B", 10.5, 1, "R2"),
        ScoredResult("doc_A", 8.2, 2, "R2"),
    ]

    fused = rrf.fuse([list_1, list_2], top_k=3)

    # Score for doc_A: 1/(60+1) + 1/(60+2) = 1/61 + 1/62
    expected_score_a = (1.0 / 61.0) + (1.0 / 62.0)
    score_a = next(x["rrf_score"] for x in fused if x["doc_id"] == "doc_A")
    assert abs(score_a - expected_score_a) < 1e-9, f"Expected {expected_score_a}, got {score_a}"

    # doc_A and doc_B both have ranks 1 and 2, so their RRF scores must be identical
    score_b = next(x["rrf_score"] for x in fused if x["doc_id"] == "doc_B")
    assert abs(score_a - score_b) < 1e-9, "Symmetric rank distributions must yield equal RRF scores"
    print("  [PASSED] RRF rank fusion mathematics verified.")


def test_hybrid_pipeline_exact_code_scenario():
    print("Testing Hybrid Pipeline on Exact Code Query...")
    pipeline = HybridSearchPipeline(SAMPLE_CORPUS)
    res = pipeline.search("ERR-STEAM-8821 troubleshooting", top_k=2)

    top_hit = res["fused_results"][0]
    assert top_hit["doc_id"] == "manual_steam_valve", (
        f"Expected exact manual to be top rank, got {top_hit['doc_id']}"
    )
    print("  [PASSED] Exact code query handled successfully by Hybrid RRF.")


def test_hybrid_pipeline_conceptual_scenario():
    print("Testing Hybrid Pipeline on Conceptual Paraphrase Query...")
    pipeline = HybridSearchPipeline(SAMPLE_CORPUS)
    res = pipeline.search("frothy warm milk morning beverage", top_k=2)

    top_hit = res["fused_results"][0]
    assert top_hit["doc_id"] == "guide_latte_art", (
        f"Expected latte art guide to be top rank, got {top_hit['doc_id']}"
    )
    print("  [PASSED] Conceptual paraphrase query handled successfully by Hybrid RRF.")


if __name__ == "__main__":
    print("=" * 60)
    print("RUNNING VERIFICATION SUITE: PROJECT 015")
    print("=" * 60)
    test_bm25_scoring()
    test_dense_vector_scoring()
    test_rrf_rank_fusion_math()
    test_hybrid_pipeline_exact_code_scenario()
    test_hybrid_pipeline_conceptual_scenario()
    print("\n[ALL TESTS PASSED] Project 015 verified successfully!")
