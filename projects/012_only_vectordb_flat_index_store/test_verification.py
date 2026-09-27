"""
Automated Verification Suite for Project 012: In-Memory Flat Vector Store & k-NN Search Engine.
Validates CRUD operations, exact k-NN retrieval, vector buffer compaction, persistence,
and agent memory integration.
"""

import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import os
from pathlib import Path
import numpy as np
from main import (
    InMemoryFlatVectorStore,
    MemoryRecord,
    AgentMemoryManager,
    embed_text,
)


def test_insert_and_retrieval():
    print("Testing Vector Store Insertion and Length...")
    store = InMemoryFlatVectorStore(metric="cosine")
    r1 = MemoryRecord("r1", "Latte art with steamed whole milk", "latte")
    r2 = MemoryRecord("r2", "Cold brew coffee concentrate", "coldbrew")
    store.insert(r1)
    store.insert(r2)

    assert len(store) == 2, f"Expected 2 records, got {len(store)}"
    assert store._vectors.shape == (2, store.dim), f"Unexpected shape {store._vectors.shape}"
    assert store.get("r1").text == "Latte art with steamed whole milk"
    print("  [PASSED] Insertion and retrieval verified.")


def test_knn_exact_search():
    print("Testing Exact k-NN Search Accuracy...")
    store = InMemoryFlatVectorStore(metric="cosine")
    docs = [
        MemoryRecord("doc_chem", "Chemistry molecular bonds and covalent reactions", "science"),
        MemoryRecord("doc_bake", "Baking artisan sourdough bread with flour and yeast", "culinary"),
        MemoryRecord("doc_code", "Writing asynchronous Python code with asyncio and coroutines", "tech"),
    ]
    store.insert_batch(docs)

    q = embed_text("Python programming with async await functions")
    hits = store.search(q, k=2)

    assert len(hits) == 2
    assert hits[0][0].id == "doc_code", f"Expected top match doc_code, got {hits[0][0].id}"
    assert hits[0][1] > 0.3, f"Score should be significant, got {hits[0][1]}"
    print("  [PASSED] Exact k-NN search accuracy verified.")


def test_update_and_delete():
    print("Testing Update, Delete, and Array Compaction...")
    store = InMemoryFlatVectorStore(metric="cosine")
    r1 = MemoryRecord("id_1", "Original text A", "test")
    r2 = MemoryRecord("id_2", "Original text B", "test")
    r3 = MemoryRecord("id_3", "Original text C", "test")
    store.insert_batch([r1, r2, r3])

    assert len(store) == 3
    assert store._vectors.shape[0] == 3

    # Update id_2
    store.update("id_2", "Completely rewritten text for item 2")
    assert store.get("id_2").text == "Completely rewritten text for item 2"

    # Delete id_1
    deleted = store.delete("id_1")
    assert deleted is True
    assert len(store) == 2
    assert store._vectors.shape[0] == 2
    assert store.get("id_1") is None
    assert "id_1" not in store._ids

    # Delete nonexistent
    assert store.delete("nonexistent_id") is False
    print("  [PASSED] Update and deletion with array compaction verified.")


def test_metric_switching():
    print("Testing Metric Switching (Cosine vs L2)...")
    store_l2 = InMemoryFlatVectorStore(metric="l2")
    store_cos = InMemoryFlatVectorStore(metric="cosine")

    records = [
        MemoryRecord("p1", "Espresso coffee machine steam wand cleaning", "maintenance"),
        MemoryRecord("p2", "Baking cinnamon rolls with sugar glaze", "food"),
    ]
    store_l2.insert_batch(records)
    store_cos.insert_batch(records)

    q = embed_text("Espresso wand descaling and backflush")
    hits_l2 = store_l2.search(q, k=1)
    hits_cos = store_cos.search(q, k=1)

    assert hits_l2[0][0].id == "p1"
    assert hits_cos[0][0].id == "p1"
    # L2 distance is non-negative and smaller is better
    assert hits_l2[0][1] >= 0.0
    print("  [PASSED] Metric switching verified.")


def test_serialization_roundtrip():
    print("Testing Serialization and Disk Snapshot...")
    temp_file = str(Path(__file__).resolve().parent / "test_snapshot.npz")
    try:
        store = InMemoryFlatVectorStore(metric="cosine")
        store.insert(MemoryRecord("s1", "Special coffee recipe with cardamom", "recipe"))
        store.insert(MemoryRecord("s2", "Employee code of conduct and break policy", "hr"))
        store.save_to_disk(temp_file)

        assert os.path.exists(temp_file), "Snapshot file was not created"

        loaded = InMemoryFlatVectorStore.load_from_disk(temp_file)
        assert len(loaded) == 2
        assert loaded.get("s1").text == "Special coffee recipe with cardamom"

        q = embed_text("cardamom spice recipe")
        hits = loaded.search(q, k=1)
        assert hits[0][0].id == "s1"
        print("  [PASSED] Serialization roundtrip verified.")
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)


def test_agent_memory_manager():
    print("Testing Agent Memory Manager High-Level Layer...")
    mgr = AgentMemoryManager(agent_name="TestBot")
    mem_id = mgr.remember("Customer hates dairy milk; drinks exclusively oat milk", category="dietary")
    assert mem_id.startswith("mem_")

    recalled = mgr.recall("What milk should I use?", k=1)
    assert len(recalled) == 1
    assert "oat milk" in recalled[0][0].text
    print("  [PASSED] Agent memory manager verified.")


if __name__ == "__main__":
    print("=" * 60)
    print("RUNNING VERIFICATION SUITE: PROJECT 012")
    print("=" * 60)
    test_insert_and_retrieval()
    test_knn_exact_search()
    test_update_and_delete()
    test_metric_switching()
    test_serialization_roundtrip()
    test_agent_memory_manager()
    print("\n[ALL TESTS PASSED] Project 012 verified successfully!")
