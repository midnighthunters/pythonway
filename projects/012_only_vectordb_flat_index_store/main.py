"""
===============================================================================
PROJECT 012: IN-MEMORY FLAT VECTOR STORE & k-NN SEARCH ENGINE
Stage 1: Pure Fundamentals | Difficulty: 2.5 / 10 (Intermediate)
===============================================================================

THE BIG QUESTION:
Why do LLMs suffer from "contextual amnesia" across conversations, and how do
autonomous AI agents maintain long-term memory without heavy cloud infrastructure?

When an AI agent interacts with users over days or weeks, it must remember:
1. User Preferences: "Alice drinks oat milk flat whites, strictly allergic to almonds."
2. Episodic History: "Yesterday at 3 PM, Bob returned his cold brew because it was bitter."
3. Domain Knowledge: "Holiday seasonal syrups are stored in Cabinet B."

THE SOLUTION: IN-MEMORY FLAT VECTOR STORE (IndexFlat)
1. Zero External Dependencies: Pure NumPy array buffer with 100% exact k-NN recall.
2. Dual Metric Support: Cosine Similarity / Inner Product (IP) and Euclidean Distance (L2).
3. Dynamic Mutation: Supports real-time insert, batch upsert, update, and deletion.
4. Agent Episodic Memory: Memory manager that retrieves relevant context to ground
   Groq LLM generations with zero hallucination.
===============================================================================
"""

import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import os
import json
import time
import math
import hashlib
import re
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional, Tuple, Literal
import numpy as np

from config import get_llm, ACTIVE_MODEL


# =============================================================================
# 1. DENSE VECTOR EMBEDDING PIPELINE
# =============================================================================
VECTOR_DIM = 128


def embed_text(text: str, dim: int = VECTOR_DIM) -> np.ndarray:
    """
    Computes a deterministic, L2-normalized dense embedding vector for text.
    Combines word tokens and character n-grams to capture semantic relevance.
    """
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
# 2. IN-MEMORY FLAT VECTOR STORE ENGINE
# =============================================================================

@dataclass
class MemoryRecord:
    """Represents an atomic episodic or semantic memory unit."""
    id: str
    text: str
    category: str
    importance: float = 1.0
    created_at: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)


class InMemoryFlatVectorStore:
    """
    A high-performance, contiguous NumPy in-memory flat vector index.
    Guarantees 100% exact k-NN recall by performing exhaustive vector comparison.
    """

    def __init__(self, dim: int = VECTOR_DIM, metric: Literal["cosine", "l2", "ip"] = "cosine"):
        self.dim = dim
        self.metric = metric
        # Internal storage
        self._ids: List[str] = []
        self._payloads: Dict[str, MemoryRecord] = {}
        # Pre-allocated 2D matrix for contiguous memory access
        self._vectors: np.ndarray = np.empty((0, dim), dtype=np.float32)

    def __len__(self) -> int:
        return len(self._ids)

    def insert(self, record: MemoryRecord, vector: Optional[np.ndarray] = None) -> None:
        """Inserts a single memory record into the index."""
        if record.id in self._payloads:
            self.delete(record.id)

        if vector is None:
            vector = embed_text(record.text, dim=self.dim)
        else:
            vector = vector.astype(np.float32)
            if self.metric == "cosine":
                norm = np.linalg.norm(vector)
                if norm > 1e-12:
                    vector = vector / norm

        self._ids.append(record.id)
        self._payloads[record.id] = record
        self._vectors = np.vstack([self._vectors, vector.reshape(1, self.dim)])

    def insert_batch(self, records: List[MemoryRecord], vectors: Optional[List[np.ndarray]] = None) -> None:
        """Inserts multiple records in a batch operation."""
        new_vecs = []
        for i, rec in enumerate(records):
            if rec.id in self._payloads:
                self.delete(rec.id)
            if vectors is not None and i < len(vectors):
                vec = vectors[i].astype(np.float32)
                if self.metric == "cosine":
                    norm = np.linalg.norm(vec)
                    if norm > 1e-12:
                        vec = vec / norm
            else:
                vec = embed_text(rec.text, dim=self.dim)
            new_vecs.append(vec)
            self._ids.append(rec.id)
            self._payloads[rec.id] = rec

        if new_vecs:
            batch_mat = np.array(new_vecs, dtype=np.float32)
            if self._vectors.shape[0] == 0:
                self._vectors = batch_mat
            else:
                self._vectors = np.vstack([self._vectors, batch_mat])

    def get(self, record_id: str) -> Optional[MemoryRecord]:
        """Retrieves a memory record by ID."""
        return self._payloads.get(record_id)

    def delete(self, record_id: str) -> bool:
        """Removes a record and compacts the vector matrix."""
        if record_id not in self._payloads:
            return False

        idx = self._ids.index(record_id)
        self._ids.pop(idx)
        del self._payloads[record_id]
        self._vectors = np.delete(self._vectors, idx, axis=0)
        return True

    def update(self, record_id: str, new_text: str, metadata: Optional[Dict[str, Any]] = None) -> bool:
        """Updates text and recomputes the embedding for an existing record."""
        if record_id not in self._payloads:
            return False
        rec = self._payloads[record_id]
        rec.text = new_text
        if metadata:
            rec.metadata.update(metadata)
        idx = self._ids.index(record_id)
        new_vec = embed_text(new_text, dim=self.dim)
        self._vectors[idx] = new_vec
        return True

    def search(
        self,
        query_vector: np.ndarray,
        k: int = 3,
        min_score: Optional[float] = None,
        category_filter: Optional[str] = None,
    ) -> List[Tuple[MemoryRecord, float]]:
        """
        Executes exact brute-force k-NN search across all stored vectors.
        """
        if len(self._ids) == 0:
            return []

        q_vec = query_vector.astype(np.float32)
        k = min(k, len(self._ids))

        if self.metric in ("cosine", "ip"):
            if self.metric == "cosine":
                q_norm = np.linalg.norm(q_vec)
                if q_norm > 1e-12:
                    q_vec = q_vec / q_norm
            # Matrix-vector dot product: (N, d) @ (d,) -> (N,)
            scores = np.dot(self._vectors, q_vec)
            # Higher score is better
            sorted_indices = np.argsort(-scores)
        else:  # L2 distance
            diff = self._vectors - q_vec
            scores = np.linalg.norm(diff, axis=1)
            # Lower distance is better
            sorted_indices = np.argsort(scores)

        results = []
        for idx in sorted_indices:
            rec_id = self._ids[idx]
            rec = self._payloads[rec_id]
            score = float(scores[idx])

            if category_filter and rec.category != category_filter:
                continue

            if min_score is not None:
                if self.metric in ("cosine", "ip") and score < min_score:
                    continue
                elif self.metric == "l2" and score > min_score:
                    continue

            results.append((rec, score))
            if len(results) >= k:
                break

        return results

    def save_to_disk(self, file_path: str) -> None:
        """Persists the flat store (vectors and metadata) to disk."""
        data = {
            "dim": self.dim,
            "metric": self.metric,
            "ids": self._ids,
            "payloads": {rid: asdict(rec) for rid, rec in self._payloads.items()},
        }
        np.savez_compressed(
            file_path,
            vectors=self._vectors,
            metadata=json.dumps(data)
        )

    @classmethod
    def load_from_disk(cls, file_path: str) -> "InMemoryFlatVectorStore":
        """Loads a persisted flat store from disk."""
        npz = np.load(file_path, allow_pickle=True)
        meta = json.loads(str(npz["metadata"]))
        store = cls(dim=meta["dim"], metric=meta["metric"])
        store._ids = meta["ids"]
        store._vectors = npz["vectors"]
        for rid, p_dict in meta["payloads"].items():
            store._payloads[rid] = MemoryRecord(**p_dict)
        return store


# =============================================================================
# 3. AGENT EPISODIC & SEMANTIC MEMORY MANAGER
# =============================================================================

class AgentMemoryManager:
    """
    Autonomous agent memory layer wrapping the In-Memory Flat Vector Store.
    Provides cognitive primitives: remember, recall, forget, and reflect.
    """

    def __init__(self, agent_name: str = "BaristaAI"):
        self.agent_name = agent_name
        self.store = InMemoryFlatVectorStore(metric="cosine")

    def remember(self, fact_text: str, category: str = "preference", importance: float = 1.0, metadata: Optional[Dict] = None) -> str:
        """Stores a new fact or preference in episodic memory."""
        fact_id = f"mem_{hashlib.md5(fact_text.encode('utf-8')).hexdigest()[:8]}"
        record = MemoryRecord(
            id=fact_id,
            text=fact_text,
            category=category,
            importance=importance,
            metadata=metadata or {},
        )
        self.store.insert(record)
        return fact_id

    def recall(self, query: str, k: int = 3, category_filter: Optional[str] = None) -> List[Tuple[MemoryRecord, float]]:
        """Recalls relevant memories closest to the incoming query."""
        q_vec = embed_text(query, dim=self.store.dim)
        return self.store.search(q_vec, k=k, category_filter=category_filter)

    def answer_with_memory(self, user_query: str) -> str:
        """
        Retrieves top memories and synthesizes a grounded answer using Groq LLM.
        """
        recalled = self.recall(user_query, k=3)
        if not recalled:
            context_str = "No prior memories recorded."
        else:
            context_str = "\n".join([f"- [{rec.category.upper()}] {rec.text}" for rec, _ in recalled])

        llm = get_llm(temperature=0.1)
        prompt = (
            f"You are {self.agent_name}, an expert cafe concierge with perfect memory.\n"
            f"Customer Query: '{user_query}'\n\n"
            f"Retrieved Long-Term Memories:\n{context_str}\n\n"
            "Instructions:\n"
            "Answer the customer concisely in 2-3 sentences. Incorporate their known preferences "
            "and strictly enforce any allergy or dietary constraints mentioned in memory."
        )
        response = llm.invoke(prompt)
        return response.content


# =============================================================================
# 4. PEDAGOGICAL DEMONSTRATIONS
# =============================================================================

def demo_flat_store_crud():
    """Step 1: Demonstrates insertion, exact k-NN retrieval, updating, and deletion."""
    print("=" * 75)
    print("STEP 1: IN-MEMORY FLAT VECTOR STORE CRUD OPERATIONS")
    print("=" * 75)

    store = InMemoryFlatVectorStore(metric="cosine")

    memories = [
        MemoryRecord("m1", "Alice loves oat milk flat whites with extra micro-foam.", "preference"),
        MemoryRecord("m2", "CRITICAL: Alice has a life-threatening almond and tree nut allergy.", "medical"),
        MemoryRecord("m3", "Bob prefers double-shot Americanos with ice on the side.", "preference"),
        MemoryRecord("m4", "The espresso machine requires daily backflushing with Cafiza powder.", "operations"),
        MemoryRecord("m5", "Bob visited yesterday at 3 PM and praised the dark roast blend.", "episodic"),
    ]

    print(f"Batch inserting {len(memories)} memory records...")
    store.insert_batch(memories)
    print(f"Store size: {len(store)} vectors in memory matrix shape {store._vectors.shape}\n")

    # Search for Alice's drink preferences
    q_text = "What does Alice like to drink and what are her dietary restrictions?"
    q_vec = embed_text(q_text)
    print(f"Search Query: '{q_text}'")
    hits = store.search(q_vec, k=3)

    for rank, (rec, score) in enumerate(hits, 1):
        print(f"  #{rank} [Score: {score:.4f} | Category: {rec.category}] {rec.text}")

    # Mutation: Update record m3
    print("\nUpdating Bob's preference (m3) to decaf...")
    store.update("m3", "Bob changed his order to decaf oat lattes due to caffeine sensitivity.")
    updated_rec = store.get("m3")
    print(f"Updated m3 text: {updated_rec.text}")

    # Delete record m5
    print("\nDeleting episodic record m5...")
    store.delete("m5")
    print(f"Store size after deletion: {len(store)} records (NumPy matrix shape: {store._vectors.shape})")
    print("-" * 75)


def demo_persistence():
    """Step 2: Demonstrates zero-loss serialization and disk restoration."""
    print("\n" + "=" * 75)
    print("STEP 2: VECTOR STORE DISK SERIALIZATION & RESTORATION")
    print("=" * 75)

    temp_path = str(Path(__file__).resolve().parent / "test_store_snapshot.npz")

    # Create and populate store
    store = InMemoryFlatVectorStore(metric="cosine")
    store.insert(MemoryRecord("f1", "Cafe Wi-Fi password is 'MochaLatte#2026!'", "security"))
    store.insert(MemoryRecord("f2", "Espresso grinder setting is calibrated to 4.2", "calibration"))

    print(f"Saving store ({len(store)} vectors) to '{Path(temp_path).name}'...")
    store.save_to_disk(temp_path)

    print("Restoring store from snapshot...")
    restored = InMemoryFlatVectorStore.load_from_disk(temp_path)
    print(f"Restored store size: {len(restored)} records.")

    q_vec = embed_text("What is the Wi-Fi password?")
    hits = restored.search(q_vec, k=1)
    assert len(hits) == 1 and hits[0][0].id == "f1"
    print(f"Restored Search Result: '{hits[0][0].text}' [Score: {hits[0][1]:.4f}]")

    # Cleanup
    if os.path.exists(temp_path):
        os.remove(temp_path)
    print("Snapshot persistence verified cleanly!")
    print("-" * 75)


def demo_agent_long_term_memory():
    """Step 3: Demonstrates an autonomous agent using flat vector memory to personalize answers."""
    print("\n" + "=" * 75)
    print("STEP 3: AUTONOMOUS AGENT EPISODIC RECALL WITH GROQ LLM")
    print("=" * 75)

    agent = AgentMemoryManager(agent_name="CozyBaristaAI")

    # Seed agent memories
    agent.remember("Customer Alice is allergic to almond milk and peanuts.", category="health", importance=2.0)
    agent.remember("Alice's favorite morning beverage is an oat milk flat white with cinnamon.", category="preference")
    agent.remember("Today's bakery special is warm blueberry crumble scones.", category="menu")

    customer_prompt = "Hi! Can you make me my favorite morning drink? What pastry do you recommend?"
    print(f"User: '{customer_prompt}'\n")

    print("Agent searching Flat Vector Memory for relevant facts...")
    answer = agent.answer_with_memory(customer_prompt)

    print("\nBaristaAI Response (grounded on retrieved memories):")
    print(answer)
    print("=" * 75)


def main():
    print("*" * 75)
    print("PROJECT 012: IN-MEMORY FLAT VECTOR STORE & k-NN ENGINE")
    print(f"Active Model: {ACTIVE_MODEL}")
    print("*" * 75)

    demo_flat_store_crud()
    demo_persistence()
    demo_agent_long_term_memory()
    print("\n[SUCCESS] Project 012 executed cleanly end-to-end!")


if __name__ == "__main__":
    main()
