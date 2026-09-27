"""
===============================================================================
PROJECT 014: METADATA PAYLOADS, NAMESPACES & BOOLEAN FILTERING
Stage 1: Pure Fundamentals | Difficulty: 3.0 / 10 (Intermediate)
===============================================================================

THE BIG QUESTION:
In multi-tenant SaaS applications, how do you prevent catastrophic data leakage
between tenants sharing the same Vector Database, and why does naive "post-filtering"
cause catastrophic "Recall Collapse"?

THE HAZARD OF POST-FILTERING:
Suppose Tenant A asks: "What are our Q3 financial projections?"
If the database retrieves the global top-5 nearest vectors first:
- All top 5 matches might belong to Tenant B (who published large public earnings reports).
- The post-filter discards all 5 Tenant B documents because tenant_id != 'Tenant_A'.
- Result: The user receives ZERO RESULTS, even though Tenant A has 50 valid financial
  documents in the index! This fatal failure mode is called "Recall Collapse".

THE SOLUTION: PRE-FILTERING WITH TENANT GUARDRAILS
1. Boolean Expression Engine: Evaluates rich predicates ($eq, $in, $gt, $and, $or)
   directly against JSON metadata payloads.
2. Pre-Filtering Candidate Masking: Evaluates boolean predicates BEFORE vector ranking,
   guaranteeing 100% of top-K results satisfy security and tenant boundaries.
3. Tenant Namespace Guardrail: Automatically injects non-bypassable tenant isolation
   clauses to eliminate cross-tenant data contamination.
===============================================================================
"""

import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import re
import math
import hashlib
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple, Union
import numpy as np

from config import get_llm, ACTIVE_MODEL


# =============================================================================
# 1. DENSE VECTOR EMBEDDER
# =============================================================================
VECTOR_DIM = 128


def embed_text(text: str, dim: int = VECTOR_DIM) -> np.ndarray:
    """Computes a deterministic, L2-normalized dense embedding vector."""
    cleaned = re.sub(r"[^\w\s]", " ", text.lower()).strip()
    words = cleaned.split()
    vec = np.zeros(dim, dtype=np.float32)

    for w in words:
        if len(w) <= 1:
            continue
        h = int(hashlib.md5(w.encode("utf-8")).hexdigest(), 16)
        vec[h % dim] += 1.0

    for i in range(len(cleaned) - 2):
        trigram = cleaned[i:i + 3]
        if "  " in trigram:
            continue
        h = int(hashlib.md5(trigram.encode("utf-8")).hexdigest(), 16)
        vec[h % dim] += 0.35

    norm = float(np.linalg.norm(vec))
    if norm > 1e-12:
        vec = vec / norm
    return vec


# =============================================================================
# 2. RICH BOOLEAN FILTER EXPRESSION ENGINE
# =============================================================================

def evaluate_predicate(val: Any, op: str, target: Any) -> bool:
    """Evaluates an atomic operator against a metadata payload field."""
    if op == "$eq":
        return val == target
    elif op == "$ne":
        return val != target
    elif op == "$gt":
        return val is not None and val > target
    elif op == "$gte":
        return val is not None and val >= target
    elif op == "$lt":
        return val is not None and val < target
    elif op == "$lte":
        return val is not None and val <= target
    elif op == "$in":
        return isinstance(target, (list, tuple, set)) and val in target
    elif op == "$nin":
        return isinstance(target, (list, tuple, set)) and val not in target
    elif op == "$contains":
        return isinstance(val, (list, tuple, set, str)) and target in val
    else:
        raise ValueError(f"Unsupported filter operator: {op}")


def evaluate_filter(payload: Dict[str, Any], filter_expr: Optional[Dict[str, Any]]) -> bool:
    """
    Recursively evaluates a MongoDB-style boolean filter expression AST against a payload.
    Supports: $and, $or, $not, and nested field operators ($eq, $in, $gt, etc.).
    """
    if not filter_expr:
        return True

    for key, condition in filter_expr.items():
        if key == "$and":
            if not isinstance(condition, list):
                raise ValueError("$and condition must be a list of sub-expressions.")
            if not all(evaluate_filter(payload, sub) for sub in condition):
                return False
        elif key == "$or":
            if not isinstance(condition, list):
                raise ValueError("$or condition must be a list of sub-expressions.")
            if not any(evaluate_filter(payload, sub) for sub in condition):
                return False
        elif key == "$not":
            if not isinstance(condition, dict):
                raise ValueError("$not condition must be a dictionary sub-expression.")
            if evaluate_filter(payload, condition):
                return False
        else:
            # Field-level condition
            field_val = payload.get(key)
            if isinstance(condition, dict):
                # E.g. {"price": {"$lte": 5.0, "$gt": 2.0}}
                for op, target in condition.items():
                    if not evaluate_predicate(field_val, op, target):
                        return False
            else:
                # Direct equality shorthand: {"department": "kitchen"}
                if field_val != condition:
                    return False

    return True


# =============================================================================
# 3. SECURE MULTI-TENANT FILTERED VECTOR STORE
# =============================================================================

@dataclass
class DocumentPayload:
    """Structured vector document with metadata payload."""
    doc_id: str
    text: str
    metadata: Dict[str, Any]
    vector: Optional[np.ndarray] = None


class FilteredVectorStore:
    """
    Vector store with native metadata indexing and dual Pre/Post filtering engines.
    """

    def __init__(self, dim: int = VECTOR_DIM):
        self.dim = dim
        self.documents: Dict[str, DocumentPayload] = {}
        self.ids: List[str] = []
        self.vectors: np.ndarray = np.empty((0, dim), dtype=np.float32)

    def insert(self, doc: DocumentPayload) -> None:
        """Inserts or upserts a document with metadata."""
        if doc.doc_id in self.documents:
            self.delete(doc.doc_id)

        vec = doc.vector if doc.vector is not None else embed_text(doc.text, dim=self.dim)
        doc.vector = vec

        self.ids.append(doc.doc_id)
        self.documents[doc.doc_id] = doc
        self.vectors = np.vstack([self.vectors, vec.reshape(1, self.dim)])

    def delete(self, doc_id: str) -> bool:
        if doc_id not in self.documents:
            return False
        idx = self.ids.index(doc_id)
        self.ids.pop(idx)
        del self.documents[doc_id]
        self.vectors = np.delete(self.vectors, idx, axis=0)
        return True

    def search_pre_filter(
        self,
        query_vector: np.ndarray,
        filter_expr: Optional[Dict[str, Any]] = None,
        k: int = 5,
    ) -> List[Tuple[DocumentPayload, float]]:
        """
        PRE-FILTERING: Evaluates boolean predicates FIRST to build candidate mask,
        then evaluates vector distance ONLY on eligible documents.
        Guarantees full top-k results and 100% namespace compliance.
        """
        if len(self.ids) == 0:
            return []

        # 1. Filter candidates
        matching_indices = [
            i for i, doc_id in enumerate(self.ids)
            if evaluate_filter(self.documents[doc_id].metadata, filter_expr)
        ]

        if not matching_indices:
            return []

        # 2. Vector distance evaluation only on matching subset
        cand_vecs = self.vectors[matching_indices]
        scores = np.dot(cand_vecs, query_vector)

        # 3. Top-k sorting within candidates
        sorted_pos = np.argsort(-scores)[:k]
        results = []
        for pos in sorted_pos:
            actual_idx = matching_indices[pos]
            doc_id = self.ids[actual_idx]
            results.append((self.documents[doc_id], float(scores[pos])))
        return results

    def search_post_filter(
        self,
        query_vector: np.ndarray,
        filter_expr: Optional[Dict[str, Any]] = None,
        k: int = 5,
        global_k: Optional[int] = None,
    ) -> List[Tuple[DocumentPayload, float]]:
        """
        POST-FILTERING: Searches global top-K nearest vectors across the ENTIRE dataset,
        then drops any that fail the filter.
        Prone to RECALL COLLAPSE when matching items are pushed down by irrelevant clusters!
        """
        if len(self.ids) == 0:
            return []

        global_k = global_k or k
        global_k = min(global_k, len(self.ids))

        # 1. Global vector search
        scores = np.dot(self.vectors, query_vector)
        top_indices = np.argsort(-scores)[:global_k]

        # 2. Filter post-hoc
        results = []
        for idx in top_indices:
            doc_id = self.ids[idx]
            doc = self.documents[doc_id]
            if evaluate_filter(doc.metadata, filter_expr):
                results.append((doc, float(scores[idx])))
            if len(results) >= k:
                break
        return results


# =============================================================================
# 4. TENANT NAMESPACE GUARDRAIL
# =============================================================================

class TenantGuardrail:
    """
    Security guardrail that enforces strict tenant isolation and department authorization.
    Injects non-bypassable predicates into user query filters to prevent data leakage.
    """

    def __init__(self, tenant_id: str, department: Optional[str] = None, clearance: int = 1):
        self.tenant_id = tenant_id
        self.department = department
        self.clearance = clearance

    def apply_guardrail(self, user_filter: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Wraps incoming user filters with mandatory tenant and clearance boundaries.
        Rejects any attempt to spoof or override the tenant_id.
        """
        mandatory_clauses: List[Dict[str, Any]] = [
            {"tenant_id": {"$eq": self.tenant_id}},
            {"clearance_level": {"$lte": self.clearance}},
        ]

        if self.department:
            mandatory_clauses.append({
                "$or": [
                    {"department": {"$eq": self.department}},
                    {"department": {"$eq": "general"}},
                ]
            })

        if user_filter:
            # Check for illegal tenant spoofing attempt
            if "tenant_id" in user_filter:
                raise PermissionError("Access Denied: Manual modification of 'tenant_id' filter is prohibited.")
            mandatory_clauses.append(user_filter)

        return {"$and": mandatory_clauses}


# =============================================================================
# 5. PEDAGOGICAL DEMONSTRATIONS
# =============================================================================

def demo_boolean_filtering():
    """Step 1: Demonstrates rich boolean operator evaluation."""
    print("=" * 80)
    print("STEP 1: RICH BOOLEAN FILTER EXPRESSIONS ($eq, $in, $gt, $and, $or)")
    print("=" * 80)

    sample_doc = {
        "tenant_id": "tenant_acme",
        "department": "kitchen",
        "item_type": "espresso_machine",
        "price_usd": 4200.0,
        "clearance_level": 2,
        "tags": ["commercial", "italian", "dual_boiler"],
    }

    f1 = {"tenant_id": {"$eq": "tenant_acme"}}
    f2 = {"price_usd": {"$gte": 5000.0}}
    f3 = {
        "$and": [
            {"department": {"$in": ["kitchen", "bakery"]}},
            {"clearance_level": {"$lte": 3}},
            {"tags": {"$contains": "dual_boiler"}},
        ]
    }
    f4 = {
        "$or": [
            {"item_type": {"$eq": "blender"}},
            {"price_usd": {"$gt": 4000.0}},
        ]
    }

    print(f"Sample Payload: {sample_doc}\n")
    print(f"Filter 1 (tenant_id == 'tenant_acme'):       {evaluate_filter(sample_doc, f1)} (Expected: True)")
    print(f"Filter 2 (price_usd >= 5000.0):             {evaluate_filter(sample_doc, f2)} (Expected: False)")
    print(f"Filter 3 ($and: department in [...] & tags): {evaluate_filter(sample_doc, f3)} (Expected: True)")
    print(f"Filter 4 ($or: blender OR price > 4000):     {evaluate_filter(sample_doc, f4)} (Expected: True)")
    print("-" * 80)


def demo_recall_collapse_comparison():
    """Step 2: Proves how post-filtering causes Recall Collapse while pre-filtering succeeds."""
    print("\n" + "=" * 80)
    print("STEP 2: PRE-FILTERING VS POST-FILTERING (RECALL COLLAPSE BENCHMARK)")
    print("=" * 80)

    store = FilteredVectorStore()

    # Populate 10 documents belonging to Tenant B (Competitor) that are heavily coffee-related
    for i in range(10):
        store.insert(DocumentPayload(
            doc_id=f"tenant_b_doc_{i}",
            text=f"Espresso extraction brew guidelines batch {i} for high volume cafes.",
            metadata={"tenant_id": "tenant_b", "clearance_level": 1, "department": "general"}
        ))

    # Populate 3 documents belonging to Tenant A (Our Tenant) that are slightly less lexical matches
    tenant_a_docs = [
        "Confidential Acme Cafe seasonal lavender syrup formulation.",
        "Acme Cafe espresso machine scheduled weekly descaling steps.",
        "Acme Cafe barista shift swap guidelines and holiday bonus schedule.",
    ]
    for i, t in enumerate(tenant_a_docs):
        store.insert(DocumentPayload(
            doc_id=f"tenant_a_doc_{i}",
            text=t,
            metadata={"tenant_id": "tenant_acme", "clearance_level": 1, "department": "kitchen"}
        ))

    print(f"Indexed total {len(store.ids)} documents: 10 belonging to Tenant B, 3 to Tenant Acme.\n")

    query = "espresso machine maintenance and extraction"
    q_vec = embed_text(query)
    tenant_acme_filter = {"tenant_id": {"$eq": "tenant_acme"}}

    print(f"Query: '{query}'")
    print("Security Goal: Retrieve Top 3 documents strictly belonging to 'tenant_acme'.\n")

    # 1. Post-Filtering with global_k = 5
    post_results = store.search_post_filter(q_vec, filter_expr=tenant_acme_filter, k=3, global_k=5)
    print(f"[POST-FILTERING] (Global k=5 evaluated, then filtered):")
    print(f"  Results Returned: {len(post_results)} documents.")
    if not post_results:
        print("  ⚠️ RECALL COLLAPSE OCCURRED! All top-5 nearest vectors belonged to Tenant B,")
        print("     so Tenant Acme received ZERO results despite having valid documents in index!")

    # 2. Pre-Filtering
    pre_results = store.search_pre_filter(q_vec, filter_expr=tenant_acme_filter, k=3)
    print(f"\n[PRE-FILTERING] (Filter evaluated first, then Top-3 ranked):")
    print(f"  Results Returned: {len(pre_results)} documents.")
    for rank, (doc, score) in enumerate(pre_results, 1):
        print(f"  #{rank} [{doc.doc_id} | Score: {score:.4f}] {doc.text}")

    print("\nConclusion: Pre-filtering is mandatory in multi-tenant architectures to guarantee recall.")
    print("-" * 80)


def demo_multi_tenant_guardrail_rag():
    """Step 3: Demonstrates TenantGuardrail preventing data leakage during Groq LLM synthesis."""
    print("\n" + "=" * 80)
    print("STEP 3: MULTI-TENANT GUARDRAIL + GROQ LLM SYNTHESIS")
    print("=" * 80)

    store = FilteredVectorStore()

    # Enterprise documents with sensitive metadata
    docs = [
        DocumentPayload(
            "acme_exec_salaries",
            "Acme Cafe Executive Director salary is $185,000 with a 15% annual bonus.",
            {"tenant_id": "tenant_acme", "department": "exec", "clearance_level": 5}
        ),
        DocumentPayload(
            "acme_barista_tips",
            "Acme Cafe barista tip pooling distributed evenly every Friday afternoon.",
            {"tenant_id": "tenant_acme", "department": "kitchen", "clearance_level": 1}
        ),
        DocumentPayload(
            "competitor_trade_secret",
            "BeanCo Secret Roast Formula: 60% Ethiopian Yirgacheffe, 40% Colombian Supremo roasted to Full City.",
            {"tenant_id": "tenant_beanco", "department": "roastery", "clearance_level": 5}
        ),
    ]
    for d in docs:
        store.insert(d)

    # Simulate an authenticated barista user from Acme Cafe (clearance 1)
    barista_guardrail = TenantGuardrail(tenant_id="tenant_acme", department="kitchen", clearance=1)

    user_query = "What is the secret roast formula and executive bonus structure?"
    print(f"Authenticated User: Tenant='tenant_acme', Department='kitchen', Clearance=1")
    print(f"User Query: '{user_query}'\n")

    # Guardrail enforces tenant and clearance boundary
    secure_filter = barista_guardrail.apply_guardrail()
    print(f"Injected Secure Filter AST:\n{secure_filter}\n")

    q_vec = embed_text(user_query)
    hits = store.search_pre_filter(q_vec, filter_expr=secure_filter, k=3)

    print(f"Authorized Documents Retrieved: {len(hits)}")
    for doc, score in hits:
        print(f"  - [{doc.doc_id}] {doc.text}")

    # Pass authorized context into Groq LLM
    context_str = "\n".join([f"- {d.text}" for d, _ in hits]) if hits else "NO AUTHORIZED RECORDS FOUND."

    llm = get_llm(temperature=0.0)
    prompt = (
        f"You are the Enterprise Cafe Compliance Assistant.\n"
        f"User Query: '{user_query}'\n\n"
        f"Authorized Knowledge Retrieved:\n{context_str}\n\n"
        "Instructions: Answer using ONLY the authorized knowledge. If the user asked about "
        "data not present in the authorized knowledge (e.g. competitor trade secrets or executive compensation), "
        "explicitly state that the information is either unavailable or restricted by security clearance."
    )
    answer = llm.invoke(prompt)

    print(f"\nModel Response ({ACTIVE_MODEL}):")
    print(answer.content)
    print("=" * 80)


def main():
    print("*" * 80)
    print("PROJECT 014: METADATA PAYLOADS & BOOLEAN FILTERING GUARDRAILS")
    print(f"Active Model: {ACTIVE_MODEL}")
    print("*" * 80)

    demo_boolean_filtering()
    demo_recall_collapse_comparison()
    demo_multi_tenant_guardrail_rag()
    print("\n[SUCCESS] Project 014 executed cleanly end-to-end!")


if __name__ == "__main__":
    main()
