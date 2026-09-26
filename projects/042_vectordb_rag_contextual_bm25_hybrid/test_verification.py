"""
Test verification suite for Project 042: VectorDB + RAG Contextual BM25 Hybrid Search with RRF
"""

import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from main import HybridSearchEngine, BM25Index, CAFE_EQUIPMENT_KNOWLEDGE, run_hybrid_rag


def test_bm25_exact_token_matching():
    bm25 = BM25Index()
    bm25.add_document("d1", "Pressure relief valve VALVE-TR-200 in bin 4B")
    bm25.add_document("d2", "Steam wand nozzle maintenance PART-NOZZLE-89")
    bm25.add_document("d3", "Cold brew coffee concentrate beverage")

    results = bm25.search("VALVE-TR-200", top_k=2)
    assert len(results) > 0
    assert results[0][0] == "d1"
    assert results[0][1] > 0.0


def test_hybrid_search_rrf_scoring():
    engine = HybridSearchEngine(rrf_k=60)
    for item in CAFE_EQUIPMENT_KNOWLEDGE:
        engine.add_document(item["doc_id"], item["title"], item["text"])

    # Test exact code query
    res_code = engine.search("Where is component PART-NOZZLE-89?", top_k=3)
    fused_code = res_code["fused_results"]
    assert len(fused_code) > 0
    assert fused_code[0]["doc_id"] == "kb_02_nozzle"
    assert fused_code[0]["rrf_score"] > 0.0

    # Test conceptual query
    res_concept = engine.search("cold brew morning wake up drink", top_k=3)
    fused_concept = res_concept["fused_results"]
    assert len(fused_concept) > 0
    assert fused_concept[0]["doc_id"] == "kb_04_cold_brew"


def test_hybrid_rag_synthesis():
    engine = HybridSearchEngine(rrf_k=60)
    for item in CAFE_EQUIPMENT_KNOWLEDGE:
        engine.add_document(item["doc_id"], item["title"], item["text"])

    ans = run_hybrid_rag("Where is VALVE-TR-200 located?", engine)
    assert isinstance(ans, str)
    assert len(ans) > 10
    # Must mention Bin #4B or pressure relief valve
    assert "4b" in ans.lower() or "valve" in ans.lower()


if __name__ == "__main__":
    test_bm25_exact_token_matching()
    test_hybrid_search_rrf_scoring()
    test_hybrid_rag_synthesis()
    print("Project 042: All verification tests PASSED successfully!")
