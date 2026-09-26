"""
===============================================================================
PROJECT 043: VECTORDB + LANGCHAIN: DYNAMIC SEMANTIC FEW-SHOT SELECTOR
Stage 2: Pairwise Combos | Difficulty: 4.5 / 10
===============================================================================

THE BIG QUESTION:
Why do static few-shot prompts fail in complex enterprise applications?
1. Rigid Context Limits: Hardcoding 5 examples for every query wastes tokens on
   irrelevant demonstrations (e.g. showing a recipe when the user has an equipment error).
2. Out-of-Domain Confusion: Giving the LLM examples that do not match the input's
   semantic domain causes format drift and hallucinated responses.

THE DYNAMIC VECTOR SOLUTION:
1. Maintain an index of labeled task demonstrations across multiple subdomains
   (Custom Recipes, Technical Diagnostics, Cupping Profiles, Catering Math).
2. For each incoming query, perform vector similarity search over example inputs.
3. Dynamically inject ONLY the top-2 most semantically relevant few-shot examples
   into the LangChain prompt template, achieving high accuracy with minimal token overhead!
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
from typing import List, Dict, Any, Optional

from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate, ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from config import get_llm, ACTIVE_MODEL


# =============================================================================
# 1. VECTOR EMBEDDING ENGINE
# =============================================================================
VECTOR_DIM = 128


def embed_text(text: str, dim: int = VECTOR_DIM) -> List[float]:
    """Generates L2-normalized dense frequency vector for semantic similarity."""
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


# =============================================================================
# 2. DIVERSE TASK EXAMPLE REPOSITORY (MULTI-DOMAIN)
# =============================================================================
FEW_SHOT_EXAMPLES: List[Dict[str, str]] = [
    # Subdomain A: POS Custom Beverage Spec Formatting
    {
        "category": "pos_customization",
        "input": "Large iced latte with oat milk, 2 pumps vanilla, extra espresso shot",
        "output": "[POS-TICKET] Size: 24oz | Base: Iced Latte | Milk: Oat (Steam Wand Yellow) | Syrups: Vanilla (2 Pumps) | Modifiers: +1 Shot Espresso (Triple Total).",
    },
    {
        "category": "pos_customization",
        "input": "Small decaf cappuccino with almond milk, half sweet caramel, dusting of cinnamon",
        "output": "[POS-TICKET] Size: 12oz | Base: Hot Cappuccino (Heavy Foam) | Espresso: Decaf Blend | Milk: Almond (Pitcher Green) | Syrups: Caramel (1 Pump Half-Sweet) | Topping: Cinnamon Powder.",
    },
    {
        "category": "pos_customization",
        "input": "Medium mocha with skim milk, light whip cream, sugar free hazelnut",
        "output": "[POS-TICKET] Size: 16oz | Base: Hot Caffe Mocha | Milk: Non-Fat Skim | Syrups: Mocha Sauce (3 Pumps) + SF Hazelnut (2 Pumps) | Topping: Light Whipped Cream.",
    },
    {
        "category": "pos_customization",
        "input": "Medium cold brew with vanilla syrup and sweet foam",
        "output": "[POS-TICKET] Size: 16oz | Base: Nitro Cold Brew | Syrups: Vanilla (2 Pumps) | Topping: Sweet Cream Cold Foam.",
    },

    # Subdomain B: Technical Hardware Diagnostics
    {
        "category": "equipment_diagnostics",
        "input": "Grouphead 1 display is flashing error E-02 low water pressure",
        "output": "[DIAGNOSTIC] Subsystem: Water Line Pump | Urgency: High | Action: Check inline filter gauge #3, inspect municipal booster solenoid, purge grouphead for 10s.",
    },
    {
        "category": "equipment_diagnostics",
        "input": "Grinder #2 burrs are screeching and espresso grounds are coming out coarse like sea salt",
        "output": "[DIAGNOSTIC] Subsystem: Mahlkönig Flat Burrs | Urgency: Immediate | Action: Disengage power, inspect burr chamber for foreign stone, recalibrate zero-point collar to notch 1.4.",
    },
    {
        "category": "equipment_diagnostics",
        "input": "Hobart dishwasher drain is backed up with foamy water after morning rinse cycle",
        "output": "[DIAGNOSTIC] Subsystem: Commercial Sanitizer Drain | Urgency: Medium | Action: Power down, pull scrap basket tray, inspect impeller for debris, run chemical wash flush.",
    },

    # Subdomain C: Specialty Origin Cupping Notes
    {
        "category": "cupping_notes",
        "input": "Tell me about the natural processed Ethiopian Yirgacheffe harvest",
        "output": "[CUPPING PROFILE] Origin: Yirgacheffe, Ethiopia | Process: Natural Sun-Dried | Altitude: 2100m | Tasting Notes: Meyer Lemon, Bergamot, Blueberry Jam, Delicate Black Tea Finish.",
    },
    {
        "category": "cupping_notes",
        "input": "What is the sensory profile for the anaerobic Colombia Huila Geisha?",
        "output": "[CUPPING PROFILE] Origin: Huila, Colombia | Process: 72hr Anaerobic Maceration | Altitude: 1850m | Tasting Notes: Passionfruit, Jasmine Blossom, Papaya, Sparkling Wine Acidity.",
    },
    {
        "category": "cupping_notes",
        "input": "Describe the tasting profile of our Sumatra Mandheling dark roast",
        "output": "[CUPPING PROFILE] Origin: Aceh, Sumatra | Process: Wet-Hulled (Giling Basah) | Tasting Notes: Cedarwood, Dark Baker's Cocoa, Tobacco Leaf, Heavy Earthy Syrupy Body.",
    },
]


# =============================================================================
# 3. SEMANTIC SIMILARITY EXAMPLE SELECTOR
# =============================================================================
class VectorExampleSelector:
    """
    Vector-driven example selector that indexes human demonstrations and selects
    the top-k nearest examples matching the user's incoming query in embedding space.
    """

    def __init__(self, examples: List[Dict[str, str]]):
        self.examples = examples
        self.indexed_examples = []
        self._build_index()

    def _build_index(self):
        for ex in self.examples:
            vec = embed_text(ex["input"])
            self.indexed_examples.append({
                "example": ex,
                "vector": vec,
            })

    def select_examples(self, query: str, top_k: int = 2) -> List[Dict[str, Any]]:
        query_vec = embed_text(query)
        scored = []
        for item in self.indexed_examples:
            sim = cosine_similarity(query_vec, item["vector"])
            scored.append((sim, item["example"]))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [{"score": round(score, 4), "example": ex} for score, ex in scored[:top_k]]


# =============================================================================
# 4. DYNAMIC FEW-SHOT PROMPT PIPELINE
# =============================================================================
def build_dynamic_few_shot_chain(selector: VectorExampleSelector):
    llm = get_llm(temperature=0.1)

    def run_chain(user_input: str) -> Dict[str, Any]:
        top_matches = selector.select_examples(user_input, top_k=2)

        # Assemble prompt dynamically with selected examples
        examples_str = ""
        for idx, match in enumerate(top_matches, start=1):
            ex = match["example"]
            examples_str += f"\n--- Example {idx} (Category: {ex['category']}, Sim: {match['score']}) ---\n"
            examples_str += f"Input: {ex['input']}\n"
            examples_str += f"Output: {ex['output']}\n"

        prompt = (
            "You are Cozy Cafe's Intelligent Operations Copilot.\n"
            "Analyze the user's request and respond strictly in the precise formatting style "
            "demonstrated in the most relevant few-shot examples below.\n\n"
            f"RELEVANT DEMONSTRATIONS:{examples_str}\n"
            "--- User Request ---\n"
            f"Input: {user_input}\n"
            "Output:"
        )

        response = llm.invoke(prompt)
        return {
            "query": user_input,
            "selected_examples": top_matches,
            "llm_output": response.content.strip(),
        }

    return run_chain


# =============================================================================
# 5. MAIN DEMONSTRATION RUNNER
# =============================================================================
def main():
    print("=" * 75)
    print("PROJECT 043: VECTORDB + LANGCHAIN DYNAMIC FEW-SHOT SELECTOR")
    print(f"Active Groq Model: {ACTIVE_MODEL}")
    print("=" * 75)

    selector = VectorExampleSelector(FEW_SHOT_EXAMPLES)
    pipeline = build_dynamic_few_shot_chain(selector)

    test_queries = [
        # Query 1: Custom Beverage Order (Target: pos_customization)
        "Large hot flat white with oat milk, 1 pump vanilla, double shot extra hot",
        # Query 2: Hardware Malfunction (Target: equipment_diagnostics)
        "Grinder #1 motor is overheating and burr chamber is locked with a buzzing noise",
        # Query 3: Cupping & Origin Profile (Target: cupping_notes)
        "Can you describe the tasting notes and processing for washed Kenyan Peaberry?",
    ]

    for idx, query in enumerate(test_queries, start=1):
        print(f"\n{'='*75}")
        print(f"TEST QUERY #{idx}: '{query}'")
        print(f"{'='*75}")

        result = pipeline(query)

        print("\n[DYNAMICALLY RETRIEVED FEW-SHOT EXAMPLES]")
        for item in result["selected_examples"]:
            ex = item["example"]
            print(f"- Category: [{ex['category']}] | Cosine Similarity: {item['score']}")
            print(f"  Input:  {ex['input']}")
            print(f"  Format: {ex['output']}")

        print("\n[GROQ LLM GENERATED OUTPUT (Adhering to Retrieved Format)]")
        print(result["llm_output"])

    print("\n" + "=" * 75)
    print("[SUCCESS] Project 043 demonstration completed cleanly!")


if __name__ == "__main__":
    main()
