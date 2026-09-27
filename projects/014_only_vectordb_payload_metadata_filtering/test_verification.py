"""
Automated Verification Suite for Project 014: Metadata Payloads, Namespaces & Boolean Filtering.
Validates boolean filter AST evaluation, pre-filtering vs post-filtering recall collapse,
and multi-tenant security guardrails.
"""

import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import numpy as np
from main import (
    evaluate_predicate,
    evaluate_filter,
    DocumentPayload,
    FilteredVectorStore,
    TenantGuardrail,
    embed_text,
)


def test_boolean_filter_operators():
    print("Testing Boolean Filter Operators...")
    doc = {
        "tenant_id": "org_alpha",
        "role": "barista",
        "hourly_wage": 18.50,
        "certified": True,
        "skills": ["latte_art", "cupping", "pos"],
    }

    # Equality & Negation
    assert evaluate_filter(doc, {"tenant_id": {"$eq": "org_alpha"}}) is True
    assert evaluate_filter(doc, {"tenant_id": {"$ne": "org_beta"}}) is True
    assert evaluate_filter(doc, {"tenant_id": {"$eq": "org_beta"}}) is False

    # Numeric comparisons
    assert evaluate_filter(doc, {"hourly_wage": {"$gt": 15.0}}) is True
    assert evaluate_filter(doc, {"hourly_wage": {"$lte": 18.50}}) is True
    assert evaluate_filter(doc, {"hourly_wage": {"$lt": 18.0}}) is False

    # In / Nin
    assert evaluate_filter(doc, {"role": {"$in": ["barista", "manager"]}}) is True
    assert evaluate_filter(doc, {"role": {"$nin": ["chef", "dishwasher"]}}) is True

    # Contains
    assert evaluate_filter(doc, {"skills": {"$contains": "latte_art"}}) is True
    assert evaluate_filter(doc, {"skills": {"$contains": "roasting"}}) is False

    # Complex Logical AST ($and, $or, $not)
    complex_ast = {
        "$and": [
            {"hourly_wage": {"$gte": 18.0}},
            {"$or": [
                {"role": {"$eq": "manager"}},
                {"skills": {"$contains": "latte_art"}},
            ]},
            {"$not": {"role": {"$eq": "executive"}}},
        ]
    }
    assert evaluate_filter(doc, complex_ast) is True
    print("  [PASSED] Boolean filter AST operations verified.")


def test_pre_filtering_namespace_isolation():
    print("Testing Pre-filtering Strict Namespace Isolation...")
    store = FilteredVectorStore()

    store.insert(DocumentPayload("t1_doc", "Brewing dark roast espresso", {"tenant_id": "tenant_1"}))
    store.insert(DocumentPayload("t2_doc", "Brewing dark roast espresso", {"tenant_id": "tenant_2"}))

    q = embed_text("Brewing dark roast espresso")
    filter_t1 = {"tenant_id": {"$eq": "tenant_1"}}

    hits = store.search_pre_filter(q, filter_expr=filter_t1, k=5)
    assert len(hits) == 1
    assert hits[0][0].doc_id == "t1_doc"
    assert hits[0][0].metadata["tenant_id"] == "tenant_1"
    print("  [PASSED] Pre-filtering namespace isolation verified.")


def test_recall_collapse_phenomenon():
    print("Testing Recall Collapse Reproduction...")
    store = FilteredVectorStore()

    # Insert 5 documents with identical high-relevance text for Tenant Competitor
    for i in range(5):
        store.insert(DocumentPayload(
            f"comp_{i}",
            "Secret cold brew recipe nitrogen infusion technique",
            {"tenant_id": "competitor"}
        ))

    # Insert 1 document for Tenant Client
    store.insert(DocumentPayload(
        "client_0",
        "Cold brew steeping time and temperature",
        {"tenant_id": "client"}
    ))

    q = embed_text("Secret cold brew recipe nitrogen infusion technique")
    client_filter = {"tenant_id": {"$eq": "client"}}

    # Post-filter with k=3 across global top 3:
    # All 3 belong to competitor, client gets 0 results!
    post_hits = store.search_post_filter(q, filter_expr=client_filter, k=1, global_k=3)
    assert len(post_hits) == 0, f"Expected Recall Collapse (0 results), but got {len(post_hits)}"

    # Pre-filter evaluates candidate mask first and finds client_0:
    pre_hits = store.search_pre_filter(q, filter_expr=client_filter, k=1)
    assert len(pre_hits) == 1, f"Expected 1 hit via pre-filter, got {len(pre_hits)}"
    assert pre_hits[0][0].doc_id == "client_0"
    print("  [PASSED] Recall collapse and pre-filter mitigation verified.")


def test_tenant_guardrail_security():
    print("Testing Tenant Guardrail Injection and Defense...")
    guard = TenantGuardrail(tenant_id="acme_tenant", department="kitchen", clearance=2)
    injected_filter = guard.apply_guardrail({"item_type": {"$eq": "blender"}})

    # Verify mandatory tenant_id is injected
    assert injected_filter["$and"][0]["tenant_id"]["$eq"] == "acme_tenant"
    assert injected_filter["$and"][1]["clearance_level"]["$lte"] == 2

    # Verify spoofing prevention
    try:
        guard.apply_guardrail({"tenant_id": {"$eq": "hacked_tenant"}})
        assert False, "Should have raised PermissionError on tenant_id tampering!"
    except PermissionError:
        pass
    print("  [PASSED] Tenant guardrail security enforcement verified.")


if __name__ == "__main__":
    print("=" * 60)
    print("RUNNING VERIFICATION SUITE: PROJECT 014")
    print("=" * 60)
    test_boolean_filter_operators()
    test_pre_filtering_namespace_isolation()
    test_recall_collapse_phenomenon()
    test_tenant_guardrail_security()
    print("\n[ALL TESTS PASSED] Project 014 verified successfully!")
