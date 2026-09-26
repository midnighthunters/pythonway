"""
===============================================================================
PROJECT 017: QUERY TRANSFORMATION, MULTI-QUERY & SUB-QUESTIONS
Stage 1: Pure Fundamentals | Difficulty: 2.5 / 10 (Beginner Friendly)
===============================================================================

THE BIG QUESTION:
Why do RAG systems fail when users ask complex questions?

Real users rarely ask clean, single-fact questions. Instead, they ask:
  "Can I bring my laptop to work on Sunday morning, and do you have decaf oat lattes and vegan bakery treats?"

If you feed that giant sentence directly into a vector database:
1. It tries to find one single paragraph that talks about Sundays, laptops, decaf, oat milk, AND vegan pastries all at once.
2. In reality, that information is scattered across 3 separate documents:
   - Document A: Hours & Laptop Policy
   - Document B: Beverage Customization
   - Document C: Bakery & Dietary Options
3. Result: Retrieval failure or partial hallucination!

THE SOLUTION: QUERY TRANSFORMATION
1. Multi-Query Expansion: Generating alternative rephrasings to avoid vocabulary mismatch.
2. Sub-Question Decomposition: Breaking a compound question into atomic sub-questions,
   retrieving targeted context for each, and synthesizing a comprehensive final answer!
===============================================================================
"""

import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import json
import re
from typing import List, Dict, Any
from config import get_llm, ACTIVE_MODEL


# =============================================================================
# 1. KNOWLEDGE BASE (3 DISCRETE DOCUMENTS)
# =============================================================================
COFFEE_SHOP_KNOWLEDGE_BASE = [
    {
        "id": "doc_hours_wifi",
        "title": "Hours, Seating & Laptop Policy",
        "content": (
            "Cozy Coffee is open Monday-Friday 6:30 AM - 8:00 PM, and Saturday-Sunday 8:00 AM - 6:00 PM. "
            "Free high-speed customer Wi-Fi ('CozyGuest_Free') is provided. Laptops and remote workers are "
            "warmly welcome anytime in the quiet back lounge, which offers power outlets at every seat."
        ),
    },
    {
        "id": "doc_beverages",
        "title": "Beverage Menu & Milk Alternatives",
        "content": (
            "We serve classic espresso, cold brews, and ceremonial grade matcha. All espresso drinks can be "
            "made decaffeinated using our chemical-free Swiss Water Process. Plant-based milk options include "
            "organic oat milk and unsweetened almond milk for an additional $0.75."
        ),
    },
    {
        "id": "doc_bakery",
        "title": "Bakery, Gluten-Free & Vegan Treats",
        "content": (
            "All bakery items are made from scratch each morning. Our daily selection includes butter croissants, "
            "sourdough bagels, and certified 100% vegan, gluten-free cinnamon swirl buns. Vegan items are marked "
            "with a green flag in the display case."
        ),
    },
    {
        "id": "doc_pets",
        "title": "Pet & Animal Policy",
        "content": (
            "Service animals are permitted inside at all times. Friendly, leashed pet dogs are welcome on our "
            "heated outdoor garden patio, but cannot enter the indoor counter area due to health regulations."
        ),
    },
]


# =============================================================================
# 2. TECHNIQUE 1: MULTI-QUERY EXPANSION
# =============================================================================
def generate_multi_queries(original_query: str, num_queries: int = 3) -> List[str]:
    """
    Rephrases a single question into multiple perspectives to increase search recall.
    Prevents missing documents due to synonym mismatches (e.g. 'wifi' vs 'internet').
    """
    llm = get_llm(temperature=0.3)
    prompt = (
        f"You are an AI search query optimizer. Given this user question:\n"
        f"'{original_query}'\n\n"
        f"Generate {num_queries} different ways to search for this same information.\n"
        "Use different synonyms or phrasing. Respond ONLY with a valid JSON array of strings.\n"
        "Example: [\"query 1\", \"query 2\", \"query 3\"]"
    )
    res = llm.invoke(prompt)
    raw = res.content.strip()
    raw = re.sub(r"^```json\s*", "", raw)
    raw = re.sub(r"^```\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw).strip()

    try:
        queries = json.loads(raw)
        if isinstance(queries, list):
            return [q.strip() for q in queries if q.strip()]
    except Exception:
        pass
    return [original_query]


# =============================================================================
# 3. TECHNIQUE 2: SUB-QUESTION DECOMPOSITION
# =============================================================================
def decompose_complex_query(complex_query: str) -> List[str]:
    """
    Breaks a multi-part query into atomic, independent sub-questions.
    Each sub-question addresses exactly one specific fact needed to answer the whole.
    """
    llm = get_llm(temperature=0.0)
    prompt = (
        f"You are a query decomposition engine for a retrieval system.\n"
        f"Deconstruct this compound user inquiry into 2 to 4 independent, single-topic sub-questions:\n"
        f"'{complex_query}'\n\n"
        "Format output ONLY as a valid JSON list of strings, for example:\n"
        "[\"Sub-question 1\", \"Sub-question 2\", \"Sub-question 3\"]"
    )
    res = llm.invoke(prompt)
    raw = res.content.strip()
    raw = re.sub(r"^```json\s*", "", raw)
    raw = re.sub(r"^```\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw).strip()

    try:
        sub_questions = json.loads(raw)
        if isinstance(sub_questions, list) and len(sub_questions) > 0:
            return [sq.strip() for sq in sub_questions if sq.strip()]
    except Exception:
        pass
    return [complex_query]


# =============================================================================
# 4. SIMULATED RETRIEVER: MATCH BEST DOCUMENT CHUNK
# =============================================================================
def retrieve_relevant_chunk(query: str, corpus: List[Dict[str, str]]) -> Dict[str, str]:
    """
    Finds the most relevant document chunk using keyword overlap scoring.
    """
    query_tokens = set(re.findall(r"\w+", query.lower()))
    best_doc = corpus[0]
    best_score = -1

    for doc in corpus:
        doc_tokens = set(re.findall(r"\w+", (doc["title"] + " " + doc["content"]).lower()))
        common = query_tokens.intersection(doc_tokens)
        score = len(common)
        if score > best_score:
            best_score = score
            best_doc = doc

    return best_doc


# =============================================================================
# 5. SYNTHESIS ENGINE: ASSEMBLE SUB-ANSWERS INTO UNIFIED RESPONSE
# =============================================================================
def synthesize_final_answer(
    original_query: str,
    sub_qa_pairs: List[Dict[str, Any]],
) -> str:
    """
    Takes all retrieved sub-contexts and synthesizes a clear, direct answer to the user.
    """
    llm = get_llm(temperature=0.0)

    context_blocks = []
    for i, pair in enumerate(sub_qa_pairs, 1):
        context_blocks.append(
            f"[Source {i}: {pair['doc']['title']}]\n"
            f"Sub-Query: {pair['sub_query']}\n"
            f"Evidence: {pair['doc']['content']}"
        )

    all_context = "\n\n".join(context_blocks)
    prompt = (
        "You are a friendly customer concierge at Cozy Coffee. Answer the customer's question "
        "thoroughly using ONLY the provided evidence from our knowledge base.\n\n"
        f"Customer Question: '{original_query}'\n\n"
        f"Retrieved Evidence:\n{all_context}\n\n"
        "Provide a well-structured, warm response addressing every aspect of the question."
    )
    res = llm.invoke(prompt)
    return res.content.strip()


# =============================================================================
# 6. MAIN DEMONSTRATION
# =============================================================================
def main():
    print("=" * 75)
    print("PROJECT 017: QUERY TRANSFORMATION, MULTI-QUERY & SUB-QUESTIONS")
    print(f"Active Groq Model: {ACTIVE_MODEL}")
    print("=" * 75)

    # -------------------------------------------------------------------------
    # PART 1: DEMONSTRATE MULTI-QUERY EXPANSION
    # -------------------------------------------------------------------------
    print("\n" + "-" * 75)
    print("PART 1: MULTI-QUERY EXPANSION (SOLVING VOCABULARY MISMATCH)")
    print("-" * 75)
    simple_q = "How is the internet connection in the cafe?"
    print(f"Original User Question: '{simple_q}'")

    expanded_queries = generate_multi_queries(simple_q, num_queries=3)
    print("\nGenerated Alternative Search Queries:")
    for i, eq in enumerate(expanded_queries, 1):
        print(f"  {i}. {eq}")
    print("\n>>> Benefit: If the document says 'Wi-Fi' but the user searched 'internet',")
    print("    multi-query expansion guarantees a match without missing results!")

    # -------------------------------------------------------------------------
    # PART 2: DEMONSTRATE SUB-QUESTION DECOMPOSITION ON A COMPLEX QUERY
    # -------------------------------------------------------------------------
    print("\n" + "-" * 75)
    print("PART 2: SUB-QUESTION DECOMPOSITION (SOLVING COMPOUND INQUIRIES)")
    print("-" * 75)
    compound_q = (
        "Can I bring my laptop to work on Sunday morning, and do you offer decaf oat lattes "
        "and any vegan bakery treats?"
    )
    print(f"Complex User Query:\n  \"{compound_q}\"\n")

    print("[Decomposing into atomic sub-questions...]")
    sub_questions = decompose_complex_query(compound_q)

    for i, sq in enumerate(sub_questions, 1):
        print(f"  Sub-Question {i}: {sq}")

    # -------------------------------------------------------------------------
    # PART 3: DISPATCH AND INDIVIDUAL RETRIEVAL
    # -------------------------------------------------------------------------
    print("\n" + "-" * 75)
    print("PART 3: RETRIEVING TARGETED CONTEXT PER SUB-QUESTION")
    print("-" * 75)

    sub_qa_pairs = []
    for sq in sub_questions:
        matched_doc = retrieve_relevant_chunk(sq, COFFEE_SHOP_KNOWLEDGE_BASE)
        sub_qa_pairs.append({"sub_query": sq, "doc": matched_doc})
        print(f"• Query: '{sq}'")
        print(f"  -> Matched Document: [{matched_doc['title']}]")

    # -------------------------------------------------------------------------
    # PART 4: FINAL SYNTHESIS
    # -------------------------------------------------------------------------
    print("\n" + "=" * 75)
    print("PART 4: SYNTHESIZED FINAL ANSWER (ALL FACTS COMBINED)")
    print("=" * 75)

    final_answer = synthesize_final_answer(compound_q, sub_qa_pairs)
    print(final_answer)

    print("\n" + "=" * 75)
    print("[SUCCESS] Project 017 demonstration finished cleanly!")


if __name__ == "__main__":
    main()
