"""
Verification Test Suite for Project 027: Hierarchical Supervisor-Worker Delegation
"""

import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from main import (
    CafeSupervisorAgent,
    CoffeeSommelierWorker,
    BakeryKitchenWorker,
    FinancialAnalystWorker,
    DelegationTask,
)


def test_specialized_workers_execution():
    print("Testing specialized workers independently...")
    ctx = {"theme": "Winter Warmth", "headcount": 100, "target_margin_pct": 75.0}

    sommelier = CoffeeSommelierWorker()
    rep1 = sommelier.execute(DelegationTask("t1", sommelier.worker_id, "taste", ctx))
    assert rep1.status == "COMPLETED"
    assert len(rep1.findings) > 10

    baker = BakeryKitchenWorker()
    rep2 = baker.execute(DelegationTask("t2", baker.worker_id, "bake", ctx))
    assert rep2.metrics["yield_count"] == 100
    assert rep2.status == "COMPLETED"

    analyst = FinancialAnalystWorker()
    rep3 = analyst.execute(DelegationTask("t3", analyst.worker_id, "cost", ctx))
    assert rep3.metrics["retail_price"] == 9.60  # 2.40 / 0.25 = 9.60
    assert rep3.status == "COMPLETED"
    print("  [PASSED] All 3 specialized worker agents execute with high fidelity.")


def test_supervisor_orchestration_cycle():
    print("\nTesting Supervisor decomposition and aggregation...")
    supervisor = CafeSupervisorAgent()
    assert len(supervisor.workers) == 3

    reports = supervisor.decompose_and_delegate("Corporate event package", {"headcount": 25, "theme": "Spring"})
    assert len(reports) == 3
    for r in reports:
        assert r.status == "COMPLETED"

    print("  [PASSED] Supervisor cleanly decomposes tasks and collects worker reports.")


if __name__ == "__main__":
    print("=" * 60)
    print("RUNNING VERIFICATION SUITE: PROJECT 027")
    print("=" * 60)
    test_specialized_workers_execution()
    test_supervisor_orchestration_cycle()
    print("\n[ALL TESTS PASSED] Project 027 verified successfully!")
