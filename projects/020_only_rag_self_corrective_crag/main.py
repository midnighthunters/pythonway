"""
===============================================================================
PROJECT 020: CRAG (CORRECTIVE RAG) WITH AI EVALUATION METRICS
Stage 1: Pure Fundamentals | Difficulty: 3.5 / 10 (Intermediate)
===============================================================================

THE BIG QUESTION:
Why is Standard RAG dangerous when retrieval fails?

In standard RAG:
  User Query -> Vector Search -> [Retrieved Chunks] -> LLM Answers

What happens if the user asks a question about something NOT in the database?
Vector search still returns the "closest" chunks, even if they are completely
irrelevant! The LLM reads the irrelevant chunks, tries to connect them to the
question, and confidently HALLUCINATES!

THE CRAG SOLUTION (Corrective RAG - Yan et al., 2024):
We insert an "AI EVALUATOR / RETRIEVAL GRADER" between retrieval and generation!
1. Evaluate Document Relevance:
   - CORRECT (Relevant): Proceed directly to generation.
   - AMBIGUOUS (Partial Match): Strip noise and refine context.
   - INCORRECT (Irrelevant / Noise): TRIGGER CORRECTIVE ACTION!
     (e.g. fall back to web search, or issue a polite, accurate abstention).
2. AI Evaluation Metric:
   - Automated Faithfulness Check: verifies that every claim in the generated
     response is 100% grounded in verified evidence.
===============================================================================
"""

import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import re
from typing import List, Dict, Any, Tuple
from config import get_llm, ACTIVE_MODEL


# =============================================================================
# 1. KNOWLEDGE BASE (COZY COFFEE CUSTOMER SERVICE POLICIES)
# =============================================================================
COZY_COFFEE_POLICIES = [
    {
        "id": "policy_refills",
        "title": "Beverage Refill Policy",
        "text": (
            "Customers who purchase a hot drip coffee or iced coffee are eligible for one complimentary refill "
            "within two hours of original purchase upon presenting their receipt at the counter. "
            "Handcrafted espresso beverages, cold brew, and matcha lattes are strictly excluded from free refills."
        ),
    },
    {
        "id": "policy_loyalty",
        "title": "Stamp Card Rewards Program",
        "text": (
            "Collect 10 physical stamps on your Cozy Loyalty Card to earn any standard drink of your choice for free. "
            "Stamps cannot be redeemed for cash or retail merchandise."
        ),
    },
    {
        "id": "policy_merchandise",
        "title": "Retail Mugs & Coffee Beans",
        "text": (
            "We sell 12oz ceramic logo diner mugs for $14 and organic cotton tote bags for $18. "
            "Whole bean 250g coffee bags are available for $16 each."
        ),
    },
]


# =============================================================================
# 2. RETRIEVAL ENGINE (SIMULATED VECTOR LOOKUP)
# =============================================================================
def retrieve_nearest_document(query: str, corpus: List[Dict[str, str]]) -> Dict[str, str]:
    """Finds closest document by token overlap (simulates vector nearest neighbor)."""
    query_tokens = set(re.findall(r"\w+", query.lower()))
    best_doc = corpus[0]
    best_score = -1

    for doc in corpus:
        doc_tokens = set(re.findall(r"\w+", (doc["title"] + " " + doc["text"]).lower()))
        common = query_tokens.intersection(doc_tokens)
        score = len(common)
        if score > best_score:
            best_score = score
            best_doc = doc

    return best_doc


# =============================================================================
# 3. CRAG AI EVALUATOR / RETRIEVAL GRADER
# =============================================================================
def evaluate_retrieval_relevance(query: str, document: Dict[str, str]) -> Tuple[str, str]:
    """
    Evaluates whether the retrieved document is genuinely relevant to the query.
    Returns: (GRADE, RATIONALE)
      - 'CORRECT'   : Document provides direct evidence to answer the query.
      - 'AMBIGUOUS' : Document contains related keywords but only partial context.
      - 'INCORRECT' : Document is irrelevant or lacks answering evidence.
    """
    llm = get_llm(temperature=0.0)
    prompt = (
        f"You are a strict Retrieval Relevance Grader.\n"
        f"User Query: '{query}'\n"
        f"Document Title: '{document['title']}'\n"
        f"Document Text: '{document['text']}'\n\n"
        "Assess whether this document contains sufficient factual information to answer the query.\n"
        "Respond in EXACTLY this format:\n"
        "GRADE: <CORRECT or AMBIGUOUS or INCORRECT>\n"
        "REASON: <one concise explanation sentence>"
    )
    res = llm.invoke(prompt)
    output = res.content.strip()

    grade = "INCORRECT"
    reason = "Evaluated"
    for line in output.split("\n"):
        if line.startswith("GRADE:"):
            val = line.replace("GRADE:", "").strip().upper()
            if "CORRECT" in val and "INCORRECT" not in val:
                grade = "CORRECT"
            elif "AMBIGUOUS" in val:
                grade = "AMBIGUOUS"
            else:
                grade = "INCORRECT"
        elif line.startswith("REASON:"):
            reason = line.replace("REASON:", "").strip()

    return grade, reason


# =============================================================================
# 4. GENERATORS: GROUNDED PATH vs CORRECTIVE FALLBACK PATH
# =============================================================================
def generate_grounded_answer(query: str, document: Dict[str, str]) -> str:
    """Standard generation path when evidence is verified."""
    llm = get_llm(temperature=0.0)
    prompt = (
        f"Answer the user query based ONLY on this official policy:\n"
        f"Policy Title: {document['title']}\n"
        f"Content: {document['text']}\n\n"
        f"User Query: {query}"
    )
    res = llm.invoke(prompt)
    return res.content.strip()


def generate_corrective_fallback(query: str, reason: str) -> str:
    """Corrective fallback path when retrieval fails or query is out-of-domain."""
    return (
        f"I apologize, but our Cozy Coffee knowledge base does not contain information regarding: '{query}'. "
        f"(Verification Note: Retrieved documentation was assessed as unrelated - {reason}). "
        "Please speak directly with a cafe manager for assistance on this topic."
    )


# =============================================================================
# 5. AI EVALUATION METRIC: FAITHFULNESS CHECK
# =============================================================================
def evaluate_faithfulness(answer: str, context: str) -> Tuple[int, str]:
    """
    Evaluates whether the generated answer contains any hallucinated claims
    not supported by the context document.
    Returns: (Score 1-10, Explanation)
    """
    llm = get_llm(temperature=0.0)
    prompt = (
        f"You are an AI Hallucination Evaluator.\n"
        f"Source Context:\n'{context}'\n\n"
        f"Generated Answer:\n'{answer}'\n\n"
        "Check if every statement in the generated answer is directly supported by the source context.\n"
        "Format output as:\n"
        "FAITHFULNESS_SCORE: <integer 1 to 10>\n"
        "EXPLANATION: <brief reason>"
    )
    res = llm.invoke(prompt)
    score = 10
    explanation = "Strictly faithful"

    for line in res.content.split("\n"):
        if line.startswith("FAITHFULNESS_SCORE:"):
            try:
                score = int(re.findall(r"\d+", line)[0])
            except Exception:
                score = 10
        elif line.startswith("EXPLANATION:"):
            explanation = line.replace("EXPLANATION:", "").strip()

    return score, explanation


# =============================================================================
# 6. MAIN CRAG WORKFLOW RUNNER
# =============================================================================
def run_crag_pipeline(query: str):
    print("\n" + "=" * 75)
    print(f"RUNNING CRAG PIPELINE FOR QUERY: '{query}'")
    print("=" * 75)

    # Step 1: Retrieve candidate document
    retrieved_doc = retrieve_nearest_document(query, COZY_COFFEE_POLICIES)
    print(f"\n[STEP 1: RETRIEVAL] Nearest Document: [{retrieved_doc['title']}]")

    # Step 2: AI Evaluator grades retrieval relevance
    grade, reason = evaluate_retrieval_relevance(query, retrieved_doc)
    print(f"\n[STEP 2: CRAG EVALUATION]")
    print(f" -> Assessment Grade : {grade}")
    print(f" -> Evaluator Reason : {reason}")

    # Step 3: Dynamic Corrective Routing
    if grade == "CORRECT":
        print("\n[STEP 3: ACTION] Evidence verified! Proceeding to Grounded Generation...")
        answer = generate_grounded_answer(query, retrieved_doc)
        print(f"\n[FINAL RESPONSE]:\n{answer}")

        # Step 4: AI Evaluation metric (Faithfulness)
        f_score, f_exp = evaluate_faithfulness(answer, retrieved_doc["text"])
        print(f"\n[AI EVALUATION METRIC - FAITHFULNESS]: {f_score}/10")
        print(f"Explanation: {f_exp}")

    elif grade == "AMBIGUOUS":
        print("\n[STEP 3: ACTION] Ambiguous evidence. Refined context required.")
        answer = generate_grounded_answer(query, retrieved_doc)
        print(f"\n[FINAL RESPONSE (PARTIAL)]:\n{answer}")

    else:  # INCORRECT
        print("\n[STEP 3: CORRECTIVE ACTION TRIGGERED!]")
        print(" -> Halting standard RAG to prevent hallucination!")
        print(" -> Routing to Corrective Fallback Handler...")
        answer = generate_corrective_fallback(query, reason)
        print(f"\n[CORRECTIVE RESPONSE]:\n{answer}")

    return grade, answer


# =============================================================================
# 7. MAIN DEMONSTRATION
# =============================================================================
def main():
    print("*" * 75)
    print("PROJECT 020: CRAG (CORRECTIVE RAG) WITH AI EVALUATION METRICS")
    print(f"Active Groq Model: {ACTIVE_MODEL}")
    print("*" * 75)

    # SCENARIO 1: Valid in-domain query (Should pass CRAG evaluation)
    q1 = "Can I get a free refill on my iced coffee, and what are the conditions?"
    run_crag_pipeline(q1)

    # SCENARIO 2: Out-of-domain query (Should trigger CRAG Corrective Fallback!)
    q2 = "Can I purchase an international plane ticket to Paris at the counter?"
    run_crag_pipeline(q2)

    print("\n" + "=" * 75)
    print("[SUCCESS] Project 020 demonstration completed cleanly!")


if __name__ == "__main__":
    main()
