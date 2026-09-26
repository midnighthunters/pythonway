"""
===============================================================================
PROJECT 041: VECTORDB + RAG: PARENT DOCUMENT RETRIEVER FOR DEEP CONTEXT
Stage 2: Pairwise Combos | Difficulty: 4.5 / 10
===============================================================================

THE BIG QUESTION:
Why do production RAG systems suffer from the 'Chunk Size Dilemma'?
- If chunks are TOO LARGE (500+ words): Vector embeddings become vague and
  diluted, causing retrieval to miss specific, targeted facts.
- If chunks are TOO SMALL (20 words): Vectors have razor-sharp retrieval accuracy,
  BUT the retrieved snippet lacks surrounding context, causing the LLM to hallucinate
  or omit vital instructions.

THE SMALL-TO-BIG SOLUTION (Parent Document Retriever):
1. Index small child chunks (1-2 sentences) in the vector database for high-precision
   semantic similarity search.
2. Maintain a parent document store linking each child back to its parent paragraph.
3. At query time, match against small child vectors, but fetch and feed the entire
   parent document into the LLM context!
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
import json
from typing import List, Dict, Any, Optional, Set
from pydantic import BaseModel, Field

from config import get_llm, ACTIVE_MODEL


# =============================================================================
# 1. VECTOR EMBEDDING ENGINE
# =============================================================================
VECTOR_DIM = 128


def embed_text(text: str, dim: int = VECTOR_DIM) -> List[float]:
    """Generates L2-normalized dense frequency vector for monotonic semantic similarity."""
    cleaned = re.sub(r"[^\w\s]", " ", text.lower()).strip()
    words = cleaned.split()
    vec = [0.0] * dim

    for w in words:
        if len(w) <= 1:
            continue
        h = int(hashlib.md5(w.encode("utf-8")).hexdigest(), 16)
        idx = h % dim
        vec[idx] += 1.0

    for i in range(len(cleaned) - 2):
        trigram = cleaned[i:i + 3]
        if "  " in trigram:
            continue
        h = int(hashlib.md5(trigram.encode("utf-8")).hexdigest(), 16)
        idx = h % dim
        vec[idx] += 0.25

    norm = math.sqrt(sum(x * x for x in vec))
    if norm > 0.0:
        vec = [x / norm for x in vec]
    return vec


def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    return sum(a * b for a, b in zip(v1, v2))


# =============================================================================
# 2. PARENT DOCUMENT RETRIEVER ENGINE
# =============================================================================
class ParentDocument:

    def __init__(self, parent_id: str, title: str, full_text: str, category: str):
        self.parent_id = parent_id
        self.title = title
        self.full_text = full_text
        self.category = category


class ChildChunk:

    def __init__(self, child_id: str, parent_id: str, text: str, vector: List[float]):
        self.child_id = child_id
        self.parent_id = parent_id
        self.text = text
        self.vector = vector


class ParentDocumentRetriever:
    """
    Implements Small-to-Big Retrieval:
    Child chunks are embedded for vector search; Parent documents are retrieved for generation.
    """

    def __init__(self):
        self.parent_store: Dict[str, ParentDocument] = {}
        self.child_index: List[ChildChunk] = []

    def split_into_sentences(self, text: str) -> List[str]:
        # Split on sentence boundaries
        sentences = re.split(r"(?<=[.!?])\s+", text.strip())
        return [s.strip() for s in sentences if len(s.strip()) > 5]

    def add_document(self, parent_id: str, title: str, full_text: str, category: str):
        """Indexes parent document and splits into small 1-2 sentence child chunks."""
        parent_doc = ParentDocument(parent_id, title, full_text, category)
        self.parent_store[parent_id] = parent_doc

        sentences = self.split_into_sentences(full_text)

        # Create child chunks: individual sentences and overlapping sentence pairs
        for idx, sentence in enumerate(sentences):
            child_id = f"{parent_id}_c{idx:02d}"
            vec = embed_text(sentence)
            child = ChildChunk(child_id, parent_id, sentence, vec)
            self.child_index.append(child)

    def retrieve(self, query: str, top_k_children: int = 4) -> List[Dict[str, Any]]:
        """
        1. Searches child vector index for top matching sentences.
        2. Resolves each child to its parent document.
        3. Deduplicates parents, returning full parent context + matched triggers.
        """
        query_vec = embed_text(query)
        scored_children = []

        for child in self.child_index:
            score = cosine_similarity(query_vec, child.vector)
            scored_children.append((score, child))

        scored_children.sort(key=lambda x: x[0], reverse=True)
        top_candidates = scored_children[:top_k_children]

        # Deduplicate parent documents while maintaining best matching score
        seen_parents: Set[str] = set()
        retrieved_parents = []

        for score, child in top_candidates:
            if child.parent_id not in seen_parents:
                seen_parents.add(child.parent_id)
                parent_doc = self.parent_store[child.parent_id]
                retrieved_parents.append({
                    "parent_id": parent_doc.parent_id,
                    "title": parent_doc.title,
                    "category": parent_doc.category,
                    "matched_child_snippet": child.text,
                    "match_score": round(score, 4),
                    "parent_full_text": parent_doc.full_text,
                })

        return retrieved_parents


# =============================================================================
# 3. CORPUS INGESTION & DEMONSTRATION
# =============================================================================
CAFE_OPERATING_MANUAL = [
    {
        "parent_id": "sop_001_boiler",
        "title": "Dual-Boiler Espresso Machine Emergency Temperature Calibration",
        "category": "Maintenance",
        "full_text": (
            "During peak morning volume, the brew boiler temperature may drift beyond the target 200°F (93.3°C). "
            "If the digital display indicates an error code E-04 (Thermal Excursion Over 205°F), the barista must "
            "NOT attempt to bleed steam from the steam wand, as this could cause hydraulic back-pressure rupture. "
            "Instead, immediately locate the Emergency Reset Valve (Red Toggle Switch #2) situated underneath the "
            "drip tray. Depress this switch firmly for 3 seconds while powering off the secondary heating element. "
            "Allow 8 minutes for passive convection cooling, then verify with the manual analog needle gauge. "
            "Resuming brewing prematurely will burn the coffee grounds and void the commercial warranty."
        ),
    },
    {
        "parent_id": "sop_002_milk_allergens",
        "title": "Cross-Contamination & Alternative Milk Allergen Protocol",
        "category": "Food Safety",
        "full_text": (
            "Cozy Cafe serves whole dairy, oat, almond, and soy milks. Under FDA allergen compliance regulations, "
            "each milk alternative is strictly designated to its color-coded stainless steel steaming pitcher: "
            "Blue for Dairy, Yellow for Oat Milk, Green for Almond (Tree Nut), and Orange for Soy. "
            "Steam wands must be purged for a full 2 seconds and wiped with a sanitizer-soaked dedicated towel "
            "immediately after every pitcher. Never use the green almond towel on the blue dairy wand. "
            "In case of suspected tree-nut contact on a dairy pitcher, the pitcher must be quarantined and sent "
            "to the Hobart high-temperature dishwasher at 180°F before reuse."
        ),
    },
    {
        "parent_id": "sop_003_cold_brew_fermentation",
        "title": "Cold Brew Immersion & Microbial Control Standards",
        "category": "Brewing Operations",
        "full_text": (
            "Our cold brew is extracted via continuous 20-hour immersion at an ambient walk-in cooler temperature "
            "of 38°F (3.3°C). Under no circumstances should brewing occur at room temperature, as ambient room "
            "temperatures exceed the threshold for lactic acid bacterial souring and mold spore proliferation. "
            "At hour 20, the stainless Toddy vessel drain valve is opened and the concentrate is double-filtered "
            "through unbleached hemp paper filters. The resulting concentrate must be diluted at a 1:1 ratio with "
            "triple-filtered reverse osmosis water and stored in purged corny kegs under 8 PSI nitrogen pressure."
        ),
    },
]


def run_rag_answer(query: str, retriever: ParentDocumentRetriever, use_parent_expansion: bool = True) -> str:
    """Demonstrates difference between Naive child-snippet RAG vs Parent Document RAG."""
    retrieved = retriever.retrieve(query, top_k_children=3)
    if not retrieved:
        return "No relevant documentation found."

    top_match = retrieved[0]
    llm = get_llm(temperature=0.2)

    if use_parent_expansion:
        context = f"PARENT DOCUMENT: {top_match['title']}\n{top_match['parent_full_text']}"
    else:
        # Naive approach: giving only the 1 isolated child sentence
        context = f"ISOLATED SNIPPET: {top_match['matched_child_snippet']}"

    prompt = (
        f"You are the Lead Equipment Technician at Cozy Cafe. Answer the user query using ONLY the provided context.\n\n"
        f"CONTEXT:\n{context}\n\n"
        f"USER QUESTION: {query}\n"
        f"Provide a direct, accurate 2-sentence response detailing the exact steps or precautions."
    )
    res = llm.invoke(prompt)
    return res.content.strip()


# =============================================================================
# 4. MAIN DEMONSTRATION RUNNER
# =============================================================================
def main():
    print("=" * 75)
    print("PROJECT 041: VECTORDB + RAG: PARENT DOCUMENT RETRIEVER")
    print(f"Active Groq Model: {ACTIVE_MODEL}")
    print("=" * 75)

    retriever = ParentDocumentRetriever()

    # 1. Ingest Documents & Split into Child Chunks
    print("\n" + "-" * 75)
    print("1. INGESTING S.O.P. MANUAL INTO SMALL-TO-BIG INDEX")
    print("-" * 75)
    for doc in CAFE_OPERATING_MANUAL:
        retriever.add_document(doc["parent_id"], doc["title"], doc["full_text"], doc["category"])

    print(f"Total Parent Documents in Store: {len(retriever.parent_store)}")
    print(f"Total Child Vectors in Index:    {len(retriever.child_index)}")

    # 2. Targeted Query (Testing precision match on specific error code)
    query = "What should I do if the espresso machine shows error code E-04 for boiler overheating?"
    print("\n" + "-" * 75)
    print(f"2. QUERY: '{query}'")
    print("-" * 75)

    retrieval_results = retriever.retrieve(query, top_k_children=3)
    for r in retrieval_results:
        print(f"-> Parent ID: {r['parent_id']} ({r['title']})")
        print(f"   Match Score: {r['match_score']}")
        print(f"   Matched Child Trigger: \"{r['matched_child_snippet']}\"")
        print(f"   Expanded Context Length: {len(r['parent_full_text'])} characters")

    # 3. Naive RAG (Child snippet only) vs Parent Document RAG
    print("\n" + "-" * 75)
    print("3. CONTRAST: NAIVE CHILD-ONLY RAG vs. PARENT DOCUMENT EXPANDED RAG")
    print("-" * 75)

    print("\n[A] NAIVE RAG (Fed only the 1 matched sentence):")
    naive_ans = run_rag_answer(query, retriever, use_parent_expansion=False)
    print(f"AI Answer: {naive_ans}")

    print("\n[B] PARENT DOCUMENT RAG (Fed complete parent paragraph context):")
    parent_ans = run_rag_answer(query, retriever, use_parent_expansion=True)
    print(f"AI Answer: {parent_ans}")

    print("\n" + "=" * 75)
    print("[SUCCESS] Project 041 demonstration completed cleanly!")


if __name__ == "__main__":
    main()
