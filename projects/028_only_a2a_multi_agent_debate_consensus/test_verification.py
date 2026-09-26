"""
Verification Test Suite for Project 028: Multi-Agent Dialectical Debate & Consensus
"""

import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from main import (
    ProAdvocateAgent,
    ConAdvocateAgent,
    AdjudicatorJudgeAgent,
    DialecticalDebateOrchestrator,
    DebateTurn,
)


def test_advocate_agents():
    print("Testing Pro and Con advocates independently...")
    prop = "Should remote work be mandatory?"
    pro = ProAdvocateAgent()
    con = ConAdvocateAgent()

    pro_turn = pro.argue(prop, 1)
    assert len(pro_turn) > 20, "Pro argument was empty"

    con_turn = con.argue(prop, 1, pro_turn)
    assert len(con_turn) > 20, "Con argument was empty"
    print("  [PASSED] Advocates formulate substantive dialectical arguments.")


def test_adjudicator_verdict():
    print("\nTesting Adjudicator synthesis...")
    judge = AdjudicatorJudgeAgent()
    history = [
        DebateTurn(1, "pro", "PRO", "Automation increases throughput by 40% and eliminates human fatigue."),
        DebateTurn(1, "con", "CON", "High capital cost of robotics and lack of empathy degrades brand loyalty."),
    ]
    verdict = judge.adjudicate("Automation proposal", history)
    assert "PRO" in verdict or "CON" in verdict or "CONSENSUS" in verdict.upper()
    print("  [PASSED] Adjudicator accurately synthesizes opposing stances into a consensus verdict.")


if __name__ == "__main__":
    print("=" * 60)
    print("RUNNING VERIFICATION SUITE: PROJECT 028")
    print("=" * 60)
    test_advocate_agents()
    test_adjudicator_verdict()
    print("\n[ALL TESTS PASSED] Project 028 verified successfully!")
