"""
Test verification suite for Project 041: VectorDB + RAG Parent Document Retriever
"""

import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from main import ParentDocumentRetriever, CAFE_OPERATING_MANUAL, run_rag_answer


def test_parent_child_indexing():
    retriever = ParentDocumentRetriever()
    doc = CAFE_OPERATING_MANUAL[0]
    retriever.add_document(doc["parent_id"], doc["title"], doc["full_text"], doc["category"])

    assert len(retriever.parent_store) == 1
    assert doc["parent_id"] in retriever.parent_store
    assert len(retriever.child_index) >= 3

    # All children have parent pointer
    for child in retriever.child_index:
        assert child.parent_id == doc["parent_id"]
        assert len(child.vector) == 128


def test_small_to_big_retrieval_and_deduplication():
    retriever = ParentDocumentRetriever()
    for doc in CAFE_OPERATING_MANUAL:
        retriever.add_document(doc["parent_id"], doc["title"], doc["full_text"], doc["category"])

    query = "error code E-04 boiler temperature"
    results = retriever.retrieve(query, top_k_children=5)

    assert len(results) > 0
    top = results[0]
    assert top["parent_id"] == "sop_001_boiler"
    assert "Emergency Reset Valve" in top["parent_full_text"]
    assert len(top["matched_child_snippet"]) > 0

    # Test deduplication: each parent appears at most once in results
    parent_ids = [r["parent_id"] for r in results]
    assert len(parent_ids) == len(set(parent_ids))


def test_parent_rag_llm_synthesis():
    retriever = ParentDocumentRetriever()
    for doc in CAFE_OPERATING_MANUAL:
        retriever.add_document(doc["parent_id"], doc["title"], doc["full_text"], doc["category"])

    query = "What color pitcher is used for almond milk and what is the allergen rule?"
    answer = run_rag_answer(query, retriever, use_parent_expansion=True)
    assert isinstance(answer, str)
    assert len(answer) > 20
    # Should mention almond/green pitcher or dishwasher
    assert ("green" in answer.lower() or "almond" in answer.lower() or "pitcher" in answer.lower())


if __name__ == "__main__":
    test_parent_child_indexing()
    test_small_to_big_retrieval_and_deduplication()
    test_parent_rag_llm_synthesis()
    print("Project 041: All verification tests PASSED successfully!")
