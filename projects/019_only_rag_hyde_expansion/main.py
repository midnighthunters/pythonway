"""
===============================================================================
PROJECT 019: HyDE (HYPOTHETICAL DOCUMENT EMBEDDINGS) FOR DEEP SEARCH
Stage 1: Pure Fundamentals | Difficulty: 3.0 / 10 (Intermediate)
===============================================================================

THE BIG QUESTION:
Why do search engines struggle when users ask informal or colloquial questions?

THE QUERY-TO-DOCUMENT ASYMMETRY PROBLEM:
- A user query is typically short, vague, or informal:
    "Why does my espresso shot taste super sour like lemon juice?"
- A high-quality technical document is dense, formal, and explanatory:
    "Under-extracted coffee is characterized by prominent citric acidity.
     It is caused by coarse grind particle distribution or channeling..."

Because the query and the target document look nothing alike, traditional
vector embeddings place them far apart in semantic space.

THE HyDE REVOLUTION (Hypothetical Document Embeddings):
1. Instead of searching with the short query, ask an LLM to generate a
   "HYPOTHETICAL ANSWER" (even if the LLM's answer has minor hallucinations!).
2. Why? Because a hypothetical answer has the structure, vocabulary, and length
   of a real document!
3. Search the database using the HYPOTHETICAL DOCUMENT.
4. Document-to-Document search bridges the vocabulary gap and yields dramatic
   gains in retrieval accuracy!
===============================================================================
"""

import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import re
from typing import List, Dict, Any
from config import get_llm, ACTIVE_MODEL


# =============================================================================
# 1. KNOWLEDGE BASE (TECHNICAL BARISTA MANUAL)
# =============================================================================
BARISTA_TROUBLESHOOTING_CORPUS = [
    {
        "id": "doc_milk_microfoam",
        "title": "Milk Steaming & Microfoam Texturing",
        "text": (
            "To achieve glossy latte art microfoam, purge the steam wand before submerging. "
            "Introduce air during the first 3 seconds until the pitcher reaches 100 degrees Fahrenheit, "
            "then tilt the pitcher to create a vigorous vortex until reaching 140-150 degrees Fahrenheit."
        ),
    },
    {
        "id": "doc_extraction_calibration",
        "title": "Espresso Extraction Dialing-In & Grind Calibration",
        "text": (
            "Under-extracted espresso is characterized by excessive citric acidity, thin crema, and an unpleasantly "
            "sharp, sour sensory profile. This occurs when water flows too rapidly through a coarse coffee bed or "
            "when brew temperature is below 198F. Corrective protocol: Step the Mazzer grinder collar finer by 2 notches, "
            "maintain a 1:2 brew ratio (18g dry dose yielding 36g liquid espresso), and target a 28-30 second extraction time."
        ),
    },
    {
        "id": "doc_water_filtration",
        "title": "Reverse Osmosis Water TDS Standards",
        "text": (
            "Water hardness directly governs coffee extraction chemistry. Our reverse osmosis system blends minerals "
            "to maintain an optimal Total Dissolved Solids (TDS) target between 120 and 150 ppm with zero chlorine."
        ),
    },
    {
        "id": "doc_cold_brew_toddy",
        "title": "Cold Brew Concentrate Steeping Protocol",
        "text": (
            "Coarse ground Colombian beans must steep in room temperature water for 18 to 20 hours using Toddy paper filters. "
            "Dilute the finished concentrate 1:1 with filtered water before serving over ice."
        ),
    },
]


# =============================================================================
# 2. HyDE HYPOTHETICAL DOCUMENT GENERATOR
# =============================================================================
def generate_hypothetical_document(query: str) -> str:
    """
    Generates a speculative, technical paragraph that answers the user's question.
    This paragraph acts as a synthetic document bridge.
    """
    llm = get_llm(temperature=0.3)
    prompt = (
        "You are an expert master barista and food scientist. Write a short, highly technical "
        "manual excerpt (3-4 sentences) that thoroughly answers this barista's question:\n"
        f"'{query}'\n\n"
        "Include technical concepts like extraction yield, grind size, brew ratio, and acidity. "
        "Do NOT write conversational greetings; write ONLY the formal manual paragraph."
    )
    res = llm.invoke(prompt)
    return res.content.strip()


# =============================================================================
# 3. RETRIEVAL SCORER: DOCUMENT-TO-DOCUMENT SIMILARITY
# =============================================================================
def score_relevance(source_text: str, target_doc_text: str) -> float:
    """
    Computes a semantic term-overlap score between source text and a candidate document.
    """
    source_words = set(re.findall(r"\b[a-zA-Z]{4,}\b", source_text.lower()))
    doc_words = set(re.findall(r"\b[a-zA-Z]{4,}\b", target_doc_text.lower()))

    if not source_words:
        return 0.0

    overlap = source_words.intersection(doc_words)
    return len(overlap) / len(source_words)


def search_corpus(query_or_doc: str, corpus: List[Dict[str, str]]) -> Dict[str, Any]:
    """Searches corpus using either raw query or hypothetical document."""
    scored = []
    for doc in corpus:
        score = score_relevance(query_or_doc, doc["title"] + " " + doc["text"])
        scored.append({"doc": doc, "score": score})

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[0]


# =============================================================================
# 4. MAIN DEMONSTRATION
# =============================================================================
def main():
    print("=" * 75)
    print("PROJECT 019: HyDE (HYPOTHETICAL DOCUMENT EMBEDDINGS) FOR DEEP SEARCH")
    print(f"Active Groq Model: {ACTIVE_MODEL}")
    print("=" * 75)

    user_query = "Why does my espresso shot taste super sour like lemon juice?"
    print(f"\nUser Query (Informal / Colloquial):\n  '{user_query}'")

    # -------------------------------------------------------------------------
    # PART 1: BASELINE NAIVE SEARCH (WITHOUT HyDE)
    # -------------------------------------------------------------------------
    print("\n" + "-" * 75)
    print("BASELINE SEARCH (Searching Directly with User's Short Query)")
    print("-" * 75)
    baseline_result = search_corpus(user_query, BARISTA_TROUBLESHOOTING_CORPUS)
    print(f"Matched Document : [{baseline_result['doc']['title']}]")
    print(f"Overlap Score    : {baseline_result['score']:.4f}")
    print(">>> Note: The user asked about 'sour' and 'lemon juice'. Because formal manuals")
    print("    use terms like 'citric acidity' and 'under-extraction', raw query search is weak.")

    # -------------------------------------------------------------------------
    # PART 2: HyDE GENERATION (CREATING THE SYNTHETIC DOCUMENT)
    # -------------------------------------------------------------------------
    print("\n" + "-" * 75)
    print("HyDE STEP: Generating Synthetic Hypothetical Document...")
    print("-" * 75)
    hypothetical_doc = generate_hypothetical_document(user_query)
    print(f"Generated Hypothetical Document:\n\"\"\"\n{hypothetical_doc}\n\"\"\"")

    print("\n>>> NOTICE THE MAGIC OF HyDE:")
    print("Look at the words the LLM generated: 'under-extraction', 'acidity', 'grind size'!")
    print("The LLM translated an informal complaint into the exact technical dialect of the manual!")

    # -------------------------------------------------------------------------
    # PART 3: HyDE SEARCH (DOCUMENT-TO-DOCUMENT MATCHING)
    # -------------------------------------------------------------------------
    print("\n" + "-" * 75)
    print("HyDE RETRIEVAL: Searching Corpus with Hypothetical Document")
    print("-" * 75)
    hyde_result = search_corpus(hypothetical_doc, BARISTA_TROUBLESHOOTING_CORPUS)
    print(f"Matched Document : [{hyde_result['doc']['title']}]")
    print(f"Overlap Score    : {hyde_result['score']:.4f}")
    print(f"Confidence Boost : {(hyde_result['score'] / max(baseline_result['score'], 0.0001)):.1f}x higher semantic match!")

    # -------------------------------------------------------------------------
    # PART 4: FINAL GROUNDED ANSWER
    # -------------------------------------------------------------------------
    print("\n" + "=" * 75)
    print("FINAL GROUNDED RESPONSE (Based on Verified Manual Excerpt)")
    print("=" * 75)

    llm = get_llm(temperature=0.0)
    prompt = (
        "You are the Head Barista Trainer. Answer the barista's question based strictly "
        f"on this official standard operating procedure:\n\n{hyde_result['doc']['text']}\n\n"
        f"Barista Question: {user_query}\n"
        "Provide a clear, 3-step action plan to fix the shot."
    )
    answer = llm.invoke(prompt)
    print(answer.content.strip())

    print("\n" + "=" * 75)
    print("[SUCCESS] Project 019 demonstration completed cleanly!")


if __name__ == "__main__":
    main()
