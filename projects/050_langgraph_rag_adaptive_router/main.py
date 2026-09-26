"""
===============================================================================
PROJECT 050: LANGGRAPH + RAG: ADAPTIVE QUERY ROUTING STATE MACHINE
Stage 2: Pairwise Combos | Difficulty: 5.0 / 10
===============================================================================

THE BIG QUESTION:
Why is a one-size-fits-all retrieval strategy disastrous in production?
- If a user asks for tabular sales revenue: Vector search will hallucinate numbers
  because embeddings cannot perform SQL aggregates (SUM, COUNT, GROUP BY).
- If a user asks for qualitative barista technique: SQL databases have no relevant
  rows; vector search over unstructured manuals is required.
- If a user asks for creative brainstorming or general conversation: Querying any
  database wastes latency and compute; direct LLM reasoning is best.

THE ADAPTIVE ROUTER PATTERN:
1. Classifier Node: Analyzes semantic intent and routes query dynamically.
2. Specialized Knowledge Handlers:
   - SQL RAG Node: Generates and executes analytical queries on relational databases.
   - Vector RAG Node: Conducts semantic search over unstructured S.O.P. documentation.
   - Direct LLM Node: Employs pure model reasoning with zero retrieval latency.
3. Graph Convergence: All execution paths unify into clear, grounded answers.
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
import sqlite3
import json
from typing import TypedDict, List, Dict, Any, Optional

from langgraph.graph import StateGraph, START, END
from pydantic import BaseModel, Field

from config import get_llm, ACTIVE_MODEL


# =============================================================================
# 1. SPECIALIZED KNOWLEDGE ENGINES: SQL & VECTOR
# =============================================================================
# A. Tabular SQL Database
def init_in_memory_db() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE daily_sales (
            id INTEGER PRIMARY KEY,
            item_name TEXT,
            category TEXT,
            units_sold INTEGER,
            unit_price REAL,
            total_revenue REAL
        );
    """)
    sample_data = [
        (1, "Cold Brew", "beverage", 60, 5.50, 330.00),
        (2, "Cortado", "beverage", 45, 4.25, 191.25),
        (3, "Almond Croissant", "pastry", 30, 4.50, 135.00),
        (4, "Matcha Latte", "beverage", 25, 5.75, 143.75),
        (5, "Blueberry Muffin", "pastry", 40, 4.00, 160.00),
    ]
    cursor.executemany("INSERT INTO daily_sales VALUES (?, ?, ?, ?, ?, ?)", sample_data)
    conn.commit()
    return conn


DB_CONN = init_in_memory_db()


# B. Unstructured Vector S.O.P. Knowledge Base
VECTOR_DIM = 128


def embed_text(text: str, dim: int = VECTOR_DIM) -> List[float]:
    cleaned = re.sub(r"[^\w\s]", " ", text.lower()).strip()
    words = cleaned.split()
    vec = [0.0] * dim

    for w in words:
        if len(w) <= 1:
            continue
        h = int(hashlib.md5(w.encode("utf-8")).hexdigest(), 16)
        idx = h % dim
        vec[idx] += 3.0

    for i in range(len(cleaned) - 2):
        trigram = cleaned[i:i + 3]
        if "  " in trigram:
            continue
        h = int(hashlib.md5(trigram.encode("utf-8")).hexdigest(), 16)
        idx = h % dim
        vec[idx] += 0.2

    norm = math.sqrt(sum(x * x for x in vec))
    if norm > 0.0:
        vec = [x / norm for x in vec]
    return vec


def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    return sum(a * b for a, b in zip(v1, v2))


SOP_ARTICLES = [
    {
        "id": "sop_oat_milk",
        "title": "Minor Figures Oat Milk Steaming Protocol",
        "text": (
            "Steam oat milk to a maximum temperature of 145°F (63°C). Never heat beyond 155°F, as high heat denatures "
            "the delicate plant oat starches, causing watery liquid separation and burnt bitterness. Position the steam wand "
            "tip just under the surface for the first 3 seconds to introduce silky microfoam."
        ),
    },
    {
        "id": "sop_cold_brew_filtration",
        "title": "Cold Brew Concentrate Dilution & Filtration",
        "text": (
            "Cold brew steep time is strictly 20 hours at 38°F. Concentrate must be double-filtered through hemp paper "
            "and diluted at a 1:1 ratio with filtered water before charging kegs to 8 PSI nitrogen pressure."
        ),
    },
]


def search_sop_manual(query: str) -> Dict[str, Any]:
    q_vec = embed_text(query)
    scored = []
    for art in SOP_ARTICLES:
        sim = cosine_similarity(q_vec, embed_text(f"{art['title']} {art['text']}"))
        scored.append((sim, art))
    scored.sort(key=lambda x: x[0], reverse=True)
    return scored[0][1]


# =============================================================================
# 2. LANGGRAPH STATE SCHEMA & NODES
# =============================================================================
class AdaptiveRouterState(TypedDict):
    query: str
    route: str  # "sql_rag", "vector_rag", "direct_llm"
    classification_reason: str
    retrieved_context: Optional[str]
    sql_query: Optional[str]
    sql_result: Optional[List[Dict[str, Any]]]
    final_answer: Optional[str]


def query_classifier_node(state: AdaptiveRouterState) -> Dict[str, Any]:
    """Classifies user query into 'sql_rag', 'vector_rag', or 'direct_llm'."""
    llm = get_llm(temperature=0.0)
    query = state["query"]

    classifier_prompt = (
        f"You are an expert Query Routing Classifier for a cafe operations system.\n"
        f"Analyze the following user query: '{query}'\n\n"
        f"Classify into exactly one of three routing strategies:\n"
        f"1. 'sql_rag': Questions about sales figures, revenue, numbers, quantities, prices, or tabular data.\n"
        f"2. 'vector_rag': Questions about barista procedures, recipes, techniques, S.O.P. manuals, or how-to guides.\n"
        f"3. 'direct_llm': Creative brainstorming, greetings, casual jokes, rhymes, or general knowledge.\n\n"
        f"Output ONLY valid JSON with keys:\n"
        f'- "route": "sql_rag" | "vector_rag" | "direct_llm"\n'
        f'- "reason": one sentence explanation\n'
    )

    response = llm.invoke(classifier_prompt)
    content = response.content.strip()

    try:
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
        data = json.loads(content)
        route = data.get("route", "direct_llm")
        reason = data.get("reason", "Classifier evaluated intent.")
    except Exception:
        # Fallback heuristic
        if any(w in query.lower() for w in ["sales", "revenue", "sold", "units", "total", "price"]):
            route = "sql_rag"
            reason = "Keyword matched sales analytics."
        elif any(w in query.lower() for w in ["temperature", "steam", "milk", "sop", "how to", "protocol"]):
            route = "vector_rag"
            reason = "Keyword matched operational procedure."
        else:
            route = "direct_llm"
            reason = "Defaulted to direct reasoning."

    return {
        "route": route,
        "classification_reason": reason,
    }


def sql_rag_node(state: AdaptiveRouterState) -> Dict[str, Any]:
    """Generates and executes SQL query against relational database."""
    llm = get_llm(temperature=0.0)
    query = state["query"]

    sql_gen_prompt = (
        f"You are a PostgreSQL/SQLite expert. The table schema is:\n"
        f"daily_sales(id INT, item_name TEXT, category TEXT, units_sold INT, unit_price REAL, total_revenue REAL)\n\n"
        f"User question: {query}\n"
        f"Write a single valid read-only SQLite SELECT query to answer this question. "
        f"Output ONLY the SQL query without markdown or explanations."
    )
    res = llm.invoke(sql_gen_prompt)
    raw_sql = res.content.strip().replace("```sql", "").replace("```", "").strip()

    # Safety guardrail: enforce SELECT only
    if not raw_sql.lower().startswith("select"):
        raw_sql = "SELECT item_name, units_sold, total_revenue FROM daily_sales"

    cursor = DB_CONN.cursor()
    cursor.execute(raw_sql)
    rows = cursor.fetchall()
    cols = [d[0] for d in cursor.description] if cursor.description else []
    structured_data = [dict(zip(cols, row)) for row in rows]

    # Synthesize natural language answer from SQL results
    synthesis_prompt = (
        f"User Question: {query}\n"
        f"SQL Query Executed: {raw_sql}\n"
        f"Database Result: {json.dumps(structured_data)}\n\n"
        f"Provide a clear, accurate 2-sentence response directly answering the question with the numbers."
    )
    final_ans = llm.invoke(synthesis_prompt).content.strip()

    return {
        "sql_query": raw_sql,
        "sql_result": structured_data,
        "final_answer": final_ans,
    }


def vector_rag_node(state: AdaptiveRouterState) -> Dict[str, Any]:
    """Retrieves unstructured documentation and synthesizes answer."""
    llm = get_llm(temperature=0.2)
    query = state["query"]

    doc = search_sop_manual(query)
    context = f"S.O.P. DOCUMENT: {doc['title']}\n{doc['text']}"

    prompt = (
        f"You are the Operations Lead. Answer using the provided S.O.P. context.\n\n"
        f"CONTEXT:\n{context}\n\n"
        f"QUESTION: {query}\n"
        f"Provide a precise, practical 2-sentence instruction citing the operational guideline."
    )
    res = llm.invoke(prompt)

    return {
        "retrieved_context": doc["title"],
        "final_answer": res.content.strip(),
    }


def direct_llm_node(state: AdaptiveRouterState) -> Dict[str, Any]:
    """Handles general conversational or creative queries with zero retrieval overhead."""
    llm = get_llm(temperature=0.7)
    query = state["query"]

    prompt = f"You are a friendly, witty barista at Cozy Cafe.\nPrompt: {query}\nProvide a creative, concise answer."
    res = llm.invoke(prompt)

    return {
        "final_answer": res.content.strip(),
    }


# =============================================================================
# 3. COMPILE ADAPTIVE ROUTER GRAPH
# =============================================================================
def route_decision(state: AdaptiveRouterState) -> str:
    return state["route"]


workflow = StateGraph(AdaptiveRouterState)

workflow.add_node("classifier", query_classifier_node)
workflow.add_node("sql_rag", sql_rag_node)
workflow.add_node("vector_rag", vector_rag_node)
workflow.add_node("direct_llm", direct_llm_node)

workflow.add_edge(START, "classifier")
workflow.add_conditional_edges(
    "classifier",
    route_decision,
    {
        "sql_rag": "sql_rag",
        "vector_rag": "vector_rag",
        "direct_llm": "direct_llm",
    },
)

workflow.add_edge("sql_rag", END)
workflow.add_edge("vector_rag", END)
workflow.add_edge("direct_llm", END)

adaptive_graph = workflow.compile()


# =============================================================================
# 4. MAIN DEMONSTRATION RUNNER
# =============================================================================
def main():
    print("=" * 75)
    print("PROJECT 050: LANGGRAPH + RAG ADAPTIVE QUERY ROUTING STATE MACHINE")
    print(f"Active Groq Model: {ACTIVE_MODEL}")
    print("=" * 75)

    scenarios = [
        # Scenario 1: Tabular data requiring SQL aggregation
        {
            "name": "TABULAR ANALYTICS QUERY",
            "query": "What was our total revenue and units sold for Cold Brew?",
        },
        # Scenario 2: Unstructured procedure requiring Vector RAG
        {
            "name": "UNSTRUCTURED S.O.P. QUERY",
            "query": "What is the recommended maximum temperature for steaming oat milk and why?",
        },
        # Scenario 3: Creative request requiring Direct LLM
        {
            "name": "CREATIVE / DIRECT LLM QUERY",
            "query": "Write a playful 2-line rhyme about sipping espresso on a rainy morning.",
        },
    ]

    for idx, sc in enumerate(scenarios, start=1):
        print(f"\n{'='*75}")
        print(f"SCENARIO #{idx}: {sc['name']}")
        print(f"Query: \"{sc['query']}\"")
        print(f"{'='*75}")

        initial_state: AdaptiveRouterState = {
            "query": sc["query"],
            "route": "PENDING",
            "classification_reason": "",
            "retrieved_context": None,
            "sql_query": None,
            "sql_result": None,
            "final_answer": None,
        }

        output = adaptive_graph.invoke(initial_state)

        print(f"\n[ROUTING DECISION]: {output['route'].upper()}")
        print(f"Reason: {output['classification_reason']}")

        if output["route"] == "sql_rag":
            print(f"Generated SQL:  {output['sql_query']}")
            print(f"Database Rows:  {json.dumps(output['sql_result'])}")
        elif output["route"] == "vector_rag":
            print(f"Retrieved Doc:  {output['retrieved_context']}")

        print(f"\n[FINAL RESPONSE]:\n{output['final_answer']}")

    print("\n" + "=" * 75)
    print("[SUCCESS] Project 050 demonstration completed cleanly!")


if __name__ == "__main__":
    main()
