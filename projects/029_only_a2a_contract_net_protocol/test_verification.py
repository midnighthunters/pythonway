"""
Verification Test Suite for Project 029: Contract Net Protocol (CNP)
"""

import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from main import (
    CateringManagerAgent,
    ContractorAgent,
    CallForProposal,
)


def test_contractor_capacity_refusal():
    print("Testing Contractor capacity limits and refusal...")
    contractor = ContractorAgent("c1", base_unit_cost=3.0, prep_speed_factor=0.2, reputation=8.0, capacity=50)

    # 1. Valid request
    cfp_ok = CallForProposal("t1", "small batch", 30, 20, 200.0)
    bid_ok = contractor.evaluate_cfp(cfp_ok)
    assert not bid_ok.is_refused
    assert bid_ok.bid_price > 0

    # 2. Over capacity
    cfp_large = CallForProposal("t2", "huge batch", 30, 100, 1000.0)
    bid_refused = contractor.evaluate_cfp(cfp_large)
    assert bid_refused.is_refused
    assert "Capacity exceeded" in bid_refused.refusal_reason
    print("  [PASSED] Contractor correctly issues REFUSE when capacity is exceeded.")


def test_multi_attribute_awarding():
    print("\nTesting Manager multi-attribute utility awarding...")
    manager = CateringManagerAgent()
    c1 = ContractorAgent("fast_agent", base_unit_cost=3.0, prep_speed_factor=0.1, reputation=9.0, capacity=500)
    c2 = ContractorAgent("slow_agent", base_unit_cost=2.0, prep_speed_factor=0.9, reputation=6.0, capacity=500)
    manager.register_contractor(c1)
    manager.register_contractor(c2)

    cfp = CallForProposal("t_test", "event", 60, 50, 500.0)
    bids = manager.broadcast_cfp(cfp)
    winner = manager.evaluate_and_award(cfp, bids, weight_cost=0.1, weight_speed=0.5, weight_reputation=0.4)

    assert winner is not None
    assert winner.contractor_id == "fast_agent", "Expected fast high-reputation agent to win with speed weighting"
    print("  [PASSED] Manager correctly computes utility and awards contract.")


if __name__ == "__main__":
    print("=" * 60)
    print("RUNNING VERIFICATION SUITE: PROJECT 029")
    print("=" * 60)
    test_contractor_capacity_refusal()
    test_multi_attribute_awarding()
    print("\n[ALL TESTS PASSED] Project 029 verified successfully!")
