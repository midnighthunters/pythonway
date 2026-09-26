"""
===============================================================================
PROJECT 045: VECTORDB + A2A: COLLABORATIVE MULTI-AGENT BLACKBOARD MEMORY
Stage 2: Pairwise Combos | Difficulty: 5.5 / 10
===============================================================================

THE BIG QUESTION:
How do autonomous agents in a decentralized swarm share discoveries, observations,
and domain knowledge asynchronously without tight point-to-point coupling or
direct RPC messaging?

THE SHARED SEMANTIC BLACKBOARD PATTERN:
1. The Blackboard: A shared vector memory space where agents write structured
   knowledge records tagged with their agent identity, timestamp, and confidence.
2. Producer Agents:
   - BaristaAgent: Posts observations regarding bean roast profiles & notes.
   - PastryChefAgent: Posts daily bakery batch status & flavor pairings.
   - InventoryAgent: Posts stock levels & rare ingredient arrivals.
3. Consumer / Synthesizer Agent:
   - CafeCuratorAgent: Queries the blackboard using semantic similarity to uncover
     cross-discipline synergies and synthesizes the Daily Featured Offering.
===============================================================================
"""

import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import time
import math
import hashlib
import json
import re
from typing import List, Dict, Any, Optional

from config import get_llm, ACTIVE_MODEL


# =============================================================================
# 1. VECTOR EMBEDDING ENGINE
# =============================================================================
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


# =============================================================================
# 2. SHARED SEMANTIC BLACKBOARD
# =============================================================================
class BlackboardEntry:

    def __init__(
        self,
        entry_id: str,
        author_agent: str,
        topic: str,
        content: str,
        vector: List[float],
        confidence: float,
        tags: List[str],
        timestamp: float,
    ):
        self.entry_id = entry_id
        self.author_agent = author_agent
        self.topic = topic
        self.content = content
        self.vector = vector
        self.confidence = confidence
        self.tags = tags
        self.timestamp = timestamp

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entry_id": self.entry_id,
            "author_agent": self.author_agent,
            "topic": self.topic,
            "content": self.content,
            "confidence": self.confidence,
            "tags": self.tags,
            "timestamp": round(self.timestamp, 2),
        }


class SharedSemanticBlackboard:
    """
    Decentralized semantic coordination medium.
    Agents asynchronously write facts and query peers using vector similarity.
    """

    def __init__(self):
        self.entries: List[BlackboardEntry] = []

    def post(
        self,
        author_agent: str,
        topic: str,
        content: str,
        confidence: float = 1.0,
        tags: Optional[List[str]] = None,
    ) -> BlackboardEntry:
        entry_id = f"bb_fact_{len(self.entries) + 1:03d}"
        vector = embed_text(f"{topic}: {content}")
        entry = BlackboardEntry(
            entry_id=entry_id,
            author_agent=author_agent,
            topic=topic,
            content=content,
            vector=vector,
            confidence=confidence,
            tags=tags or [],
            timestamp=time.time(),
        )
        self.entries.append(entry)
        return entry

    def query(
        self,
        search_query: str,
        top_k: int = 3,
        exclude_author: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        query_vec = embed_text(search_query)
        scored = []

        for entry in self.entries:
            if exclude_author and entry.author_agent == exclude_author:
                continue
            sim = cosine_similarity(query_vec, entry.vector)
            scored.append((sim, entry))

        scored.sort(key=lambda x: x[0], reverse=True)
        results = []
        for sim, e in scored[:top_k]:
            data = e.to_dict()
            data["similarity_score"] = round(sim, 4)
            results.append(data)
        return results

    def get_all_entries(self) -> List[Dict[str, Any]]:
        return [e.to_dict() for e in self.entries]


# =============================================================================
# 3. PEER AGENTS INTERACTING WITH BLACKBOARD
# =============================================================================
class BaristaAgent:

    def __init__(self, blackboard: SharedSemanticBlackboard):
        self.blackboard = blackboard
        self.name = "BaristaSpecialist"

    def record_morning_calibration(self):
        content = (
            "Dialed in today's featured single-origin: Washed Yirgacheffe Ethiopia. "
            "Cupping notes exhibit bright bergamot citrus, jasmine florals, and Meyer lemon acidity. "
            "Brew recipe: 1:2 ratio pulled in 29 seconds."
        )
        return self.blackboard.post(
            author_agent=self.name,
            topic="Coffee Roast Sensory Calibration",
            content=content,
            confidence=0.98,
            tags=["beverage", "ethiopia", "citrus", "floral"],
        )


class PastryChefAgent:

    def __init__(self, blackboard: SharedSemanticBlackboard):
        self.blackboard = blackboard
        self.name = "PastryChefSpecialist"

    def record_morning_bake(self):
        content = (
            "Fresh morning bake batch ready: Orange Blossom and Cardamom Scones with lemon glaze. "
            "Buttery, crumbly texture with subtle herbal warm spice and lingering sweet citrus zest."
        )
        return self.blackboard.post(
            author_agent=self.name,
            topic="Daily Artisan Bakery Batch",
            content=content,
            confidence=0.95,
            tags=["pastry", "scone", "citrus", "cardamom"],
        )


class InventoryAgent:

    def __init__(self, blackboard: SharedSemanticBlackboard):
        self.blackboard = blackboard
        self.name = "InventorySpecialist"

    def record_deliveries(self):
        content = (
            "Received express chilled crate from local farm: Wild Orange Blossom Honey and organic blood oranges. "
            "Stock verified in walk-in cold storage #1."
        )
        return self.blackboard.post(
            author_agent=self.name,
            topic="Fresh Farm Ingredient Inflow",
            content=content,
            confidence=1.0,
            tags=["ingredient", "honey", "orange", "stock"],
        )


class CafeCuratorAgent:

    def __init__(self, blackboard: SharedSemanticBlackboard):
        self.blackboard = blackboard
        self.name = "CafeCuratorAgent"

    def design_featured_pairing(self) -> Dict[str, Any]:
        """
        Queries blackboard for synergistic flavors across coffee, bakery, and farm inflows,
        then uses Groq LLM to synthesize the daily special pairing promotion.
        """
        # Search the blackboard across peer discoveries
        query = "citrus floral pastry coffee pairing notes"
        matches = self.blackboard.query(query, top_k=3, exclude_author=self.name)

        context_str = "\n".join([
            f"- [{m['entry_id']}] (Author: {m['author_agent']}) {m['topic']}: {m['content']}"
            for m in matches
        ])

        llm = get_llm(temperature=0.3)
        prompt = (
            f"You are the Executive Curator at Cozy Cafe.\n"
            f"Review the following live discoveries posted to the shared agent blackboard by your team:\n\n"
            f"{context_str}\n\n"
            f"Synthesize an elegant, enticing Daily Special Pairing announcement (2-3 sentences). "
            f"Highlight how the coffee flavors complement the bakery creation, referencing team findings."
        )

        response = llm.invoke(prompt)

        return {
            "curator": self.name,
            "blackboard_insights_used": matches,
            "daily_special_synthesis": response.content.strip(),
        }


# =============================================================================
# 4. MAIN DEMONSTRATION RUNNER
# =============================================================================
def main():
    print("=" * 75)
    print("PROJECT 045: VECTORDB + A2A SHARED BLACKBOARD MEMORY")
    print(f"Active Groq Model: {ACTIVE_MODEL}")
    print("=" * 75)

    blackboard = SharedSemanticBlackboard()

    barista = BaristaAgent(blackboard)
    baker = PastryChefAgent(blackboard)
    inventory = InventoryAgent(blackboard)
    curator = CafeCuratorAgent(blackboard)

    # 1. Peer Agents Independently Post Discoveries
    print("\n" + "-" * 75)
    print("1. PRODUCER AGENTS WRITING DISCOVERIES TO THE BLACKBOARD")
    print("-" * 75)

    e1 = barista.record_morning_calibration()
    print(f"[POSTED] {e1.author_agent} -> {e1.entry_id}: '{e1.topic}'")

    e2 = baker.record_morning_bake()
    print(f"[POSTED] {e2.author_agent} -> {e2.entry_id}: '{e2.topic}'")

    e3 = inventory.record_deliveries()
    print(f"[POSTED] {e3.author_agent} -> {e3.entry_id}: '{e3.topic}'")

    # 2. Inspect Blackboard Store
    print(f"\nTotal Active Facts in Shared Blackboard: {len(blackboard.entries)}")

    # 3. Curator Agent Searches Across Peer Knowledge
    print("\n" + "-" * 75)
    print("2. CURATOR AGENT SEMANTIC QUERY: 'citrus floral pastry coffee pairing notes'")
    print("-" * 75)
    search_results = blackboard.query("citrus floral pastry coffee pairing notes", top_k=3)
    for r in search_results:
        print(f"-> [{r['entry_id']}] Similarity: {r['similarity_score']} | Author: {r['author_agent']}")
        print(f"   Topic:   {r['topic']}")
        print(f"   Snippet: {r['content'][:80]}...")

    # 4. Curator Synthesizes Collective Intelligence
    print("\n" + "-" * 75)
    print("3. CURATOR SYNTHESIS VIA GROQ LLM (COLLECTIVE INTELLIGENCE)")
    print("-" * 75)
    curator_result = curator.design_featured_pairing()
    print(curator_result["daily_special_synthesis"])

    print("\n" + "=" * 75)
    print("[SUCCESS] Project 045 demonstration completed cleanly!")


if __name__ == "__main__":
    main()
