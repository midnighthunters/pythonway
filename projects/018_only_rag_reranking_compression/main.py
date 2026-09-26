"""
===============================================================================
PROJECT 018: CONTEXTUAL COMPRESSION & CROSS-ENCODER RE-RANKING
Stage 1: Pure Fundamentals | Difficulty: 3.0 / 10 (Intermediate)
===============================================================================

THE BIG QUESTION:
Why is retrieving 10 or 20 chunks dangerous in production RAG?

1. THE "LOST IN THE MIDDLE" PHENOMENON:
   When you dump 10 long chunks into an LLM context, the LLM pays heavy attention
   to the very beginning and very end, but ignores facts buried in the middle!
2. TOKEN INFLATION & LATENCY:
   Sending irrelevant paragraphs wastes tokens, slows down API responses, and costs money.
3. THE BI-ENCODER RETRIEVAL BLIND SPOT:
   Vector embedding models are fast, but they compress text into a single vector,
   often returning documents that match words but miss the exact nuance.

THE TWO-STAGE SOLUTION:
Stage 1: Fast Broad Retrieval (fetch top 5-10 candidates).
Stage 2: Re-ranking (Cross-Encoder / LLM evaluates exact relevance of each candidate).
Stage 3: Contextual Compression (extract ONLY the relevant sentences, trimming out filler).
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
# 1. CANDIDATE CHUNKS RETURNED BY BROAD RETRIEVAL (CONTAINS NOISE)
# =============================================================================
RETRIEVED_CANDIDATE_CHUNKS = [
    {
        "id": "chunk_01",
        "title": "Coffee Bean Storage & Freshness",
        "text": (
            "Whole bean coffee must be kept in airtight vacuum canisters away from direct sunlight. "
            "Never store whole beans in the walk-in refrigerator as condensation ruins delicate oils. "
            "Roasted batches older than 21 days should be repurposed for cold brew."
        ),
    },
    {
        "id": "chunk_02",
        "title": "Daily Espresso Grouphead Maintenance",
        "text": (
            "At closing each evening, the barista must backflush each espresso grouphead using a blind filter "
            "basket and 1 scoop of espresso detergent powder. Run five 10-second cycles, then rinse with fresh "
            "water. Wipe the shower screens with a clean microfiber cloth."
        ),
    },
    {
        "id": "chunk_03",
        "title": "Espresso Machine Monthly Descaling Protocol",
        "text": (
            "The espresso boiler and internal heat exchange copper pipes must undergo thorough descaling "
            "on the first Monday of every month. Staff must ONLY use 'EcoScale Organic Citric Acid Solution' "
            "(Green Bottle #4). NEVER use vinegar or industrial bleach, as they corrode internal brass fittings. "
            "Flush the boiler with 5 gallons of pure filtered water after descaling before pulling any shots."
        ),
    },
    {
        "id": "chunk_04",
        "title": "Commercial Dishwasher Sanitization",
        "text": (
            "The under-counter Hobart dishwasher operates at a minimum rinse temperature of 180 degrees Fahrenheit. "
            "Always inspect the spray arms for mineral build-up and empty the scrap trap after the morning lunch rush."
        ),
    },
    {
        "id": "chunk_05",
        "title": "Ice Maker Quarterly Cleaning",
        "text": (
            "Every three months, the front-of-house ice maker must be emptied completely and scrubbed with "
            "food-safe sanitizer solution. Replace the inline water filtration cartridge every six months."
        ),
    },
]


# =============================================================================
# 2. STAGE 2: RE-RANKER (CROSS-ENCODER / PRECISION SCORING)
# =============================================================================
def rerank_chunks(
    query: str,
    candidates: List[Dict[str, str]],
    top_k: int = 2,
    score_threshold: float = 7.0,
    return_all: bool = False,
) -> Any:
    """
    Evaluates each candidate chunk against the specific query.
    Assigns a precision score from 0.0 to 10.0 and sorts candidates in descending order.
    Marks each chunk as KEPT or DISCARDED based on score threshold and top_k.
    """
    print(f"\n[STAGE 2: RE-RANKER] Scoring {len(candidates)} candidates against query...")
    llm = get_llm(temperature=0.0)

    reranked = []
    for cand in candidates:
        prompt = (
            f"You are a precision search relevance evaluator.\n"
            f"Query: '{query}'\n"
            f"Document Title: '{cand['title']}'\n"
            f"Document Text: '{cand['text']}'\n\n"
            "On a scale from 0.0 to 10.0, how directly does this document answer the query?\n"
            "Respond in EXACTLY this format:\n"
            "SCORE: <float between 0.0 and 10.0>\n"
            "REASON: <one short sentence>"
        )
        res = llm.invoke(prompt)
        text_out = res.content.strip()

        score = 0.0
        reason = "Evaluated"
        for line in text_out.split("\n"):
            if line.startswith("SCORE:"):
                try:
                    score = float(line.replace("SCORE:", "").strip())
                except ValueError:
                    score = 0.0
            elif line.startswith("REASON:"):
                reason = line.replace("REASON:", "").strip()

        cand_copy = cand.copy()
        cand_copy["rerank_score"] = score
        cand_copy["rerank_reason"] = reason
        reranked.append(cand_copy)

    # Sort descending by score
    reranked.sort(key=lambda x: x["rerank_score"], reverse=True)

    # Tag each candidate with KEPT or DISCARDED
    for i, c in enumerate(reranked):
        if c["rerank_score"] < score_threshold:
            c["rerank_status"] = f"DISCARDED (Score {c['rerank_score']:.1f} < threshold {score_threshold:.1f})"
        elif i >= top_k:
            c["rerank_status"] = f"DISCARDED (Rank #{i+1} exceeds top_k={top_k})"
        else:
            c["rerank_status"] = "KEPT (Qualified Context)"

    # Filter by threshold and top_k
    filtered = [c for c in reranked if c["rerank_score"] >= score_threshold][:top_k]

    if return_all:
        return reranked, filtered
    return filtered


# =============================================================================
# 3. STAGE 3: CONTEXTUAL COMPRESSION (TRIMMING THE FAT)
# =============================================================================
def compress_context(query: str, chunk_text: str) -> str:
    """
    Contextual Compressor:
    Extracts only the sentences that directly contribute to answering the query,
    stripping out unrelated procedures or background fluff.
    """
    llm = get_llm(temperature=0.0)
    prompt = (
        f"You are a context compression engine. Given this query:\n'{query}'\n\n"
        f"Extract ONLY the precise sentences from this document that answer the query:\n"
        f"'{chunk_text}'\n\n"
        "Do not invent new information. Return only the extracted factual sentences."
    )
    res = llm.invoke(prompt)
    return res.content.strip()


# =============================================================================
# 4. MAIN DEMONSTRATION
# =============================================================================
def main():
    print("=" * 75)
    print("PROJECT 018: CONTEXTUAL COMPRESSION & CROSS-ENCODER RE-RANKING")
    print(f"Active Groq Model: {ACTIVE_MODEL}")
    print("=" * 75)

    user_query = "How often do we descale the espresso machine, and what cleaning solution is approved?"
    print(f"\nUser Query:\n  '{user_query}'")

    print(f"\n[STAGE 1]: Initial vector search returned {len(RETRIEVED_CANDIDATE_CHUNKS)} candidate chunks.")
    print("Notice: Some are about dishwashers, ice machines, or bean storage (noisy distractors!).")

    # Run Re-ranking
    all_chunks, top_chunks = rerank_chunks(
        user_query,
        RETRIEVED_CANDIDATE_CHUNKS,
        top_k=2,
        score_threshold=6.5,
        return_all=True,
    )

    print("\n" + "-" * 75)
    print("ALL CANDIDATE CHUNKS EVALUATED BY RE-RANKER:")
    print("-" * 75)
    for i, chunk in enumerate(all_chunks, 1):
        status_label = "✅ KEPT" if "KEPT" in chunk["rerank_status"] else "❌ DISCARDED"
        print(f"Rank #{i} | Score: {chunk['rerank_score']:>4.1f}/10.0 | {status_label}")
        print(f"        Document: [{chunk['title']}]")
        print(f"        Status  : {chunk['rerank_status']}")
        print(f"        Reason  : {chunk['rerank_reason']}\n")

    # Select best chunk
    best_chunk = top_chunks[0]
    original_text = best_chunk["text"]

    # Run Contextual Compression
    print("-" * 75)
    print("[STAGE 3: CONTEXTUAL COMPRESSION] Trimming non-essential filler...")
    print("-" * 75)

    compressed_text = compress_context(user_query, original_text)

    orig_chars = len(original_text)
    comp_chars = len(compressed_text)
    savings = (1 - (comp_chars / orig_chars)) * 100

    print(f"\nOriginal Chunk Text ({orig_chars} chars):\n\"{original_text}\"")
    print(f"\nCompressed Context ({comp_chars} chars):\n\"{compressed_text}\"")
    print(f"\n>>> Context Size Reduced by: {savings:.1f}% without losing key facts!")

    # Final Generation
    print("\n" + "=" * 75)
    print("FINAL ANSWER GENERATION (Using Clean, Compressed Context)")
    print("=" * 75)

    llm = get_llm(temperature=0.0)
    prompt = (
        f"Answer the query using ONLY this verified compressed context:\n'{compressed_text}'\n\n"
        f"Query: {user_query}"
    )
    answer = llm.invoke(prompt)
    print(answer.content.strip())

    print("\n" + "=" * 75)
    print("[SUCCESS] Project 018 demonstration completed cleanly!")


if __name__ == "__main__":
    main()
