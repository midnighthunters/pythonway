"""
Verification Test Suite for Project 026: Peer-to-Peer Agent Messaging Protocol & Addressing
"""

import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from main import (
    MessageEnvelope,
    PeerMessageBus,
    BaristaAgent,
    BakerAgent,
    SupplyAgent,
)


def test_message_envelope_creation():
    print("Testing MessageEnvelope serialization...")
    env = MessageEnvelope(
        sender_id="agent://a",
        recipient_id="agent://b",
        thread_id="thread_test_01",
        performative="REQUEST",
        content={"data": 123},
    )
    d = env.to_dict()
    assert d["sender_id"] == "agent://a"
    assert d["recipient_id"] == "agent://b"
    assert d["performative"] == "REQUEST"
    assert d["content"]["data"] == 123
    print("  [PASSED] MessageEnvelope serializes accurately.")


def test_bus_delivery_and_threading():
    print("\nTesting PeerMessageBus routing and thread separation...")
    bus = PeerMessageBus()
    agent_a = BaristaAgent("agent://barista", bus)
    agent_b = BakerAgent("agent://baker", bus)

    thread_1 = agent_a.order_pastries(agent_b.agent_id, "Croissant", 2)
    thread_2 = agent_a.order_pastries(agent_b.agent_id, "Bagel", 4)

    assert len(agent_b.mailbox.inbox) == 2
    assert len(agent_b.mailbox.threads[thread_1]) == 1
    assert len(agent_b.mailbox.threads[thread_2]) == 1
    print("  [PASSED] Messages cleanly delivered and grouped into independent conversational threads.")


def test_unknown_recipient_rejection():
    print("\nTesting Unknown Agent addressing rejection...")
    bus = PeerMessageBus()
    agent_a = BaristaAgent("agent://barista", bus)

    try:
        agent_a.order_pastries("agent://ghost_nonexistent", "Muffin", 1)
        assert False, "Expected KeyError for unknown recipient"
    except KeyError as e:
        assert "DELIVERY FAILED: Unknown agent" in str(e)
        print("  [PASSED] Bus strictly rejects messages addressed to unregistered peers.")


if __name__ == "__main__":
    print("=" * 60)
    print("RUNNING VERIFICATION SUITE: PROJECT 026")
    print("=" * 60)
    test_message_envelope_creation()
    test_bus_delivery_and_threading()
    test_unknown_recipient_rejection()
    print("\n[ALL TESTS PASSED] Project 026 verified successfully!")
