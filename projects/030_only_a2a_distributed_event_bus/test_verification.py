"""
Verification Test Suite for Project 030: Distributed Agent Event Bus with Dead Letters
"""

import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from main import (
    DistributedAgentEventBus,
    AgentEvent,
)


def test_pubsub_wildcard_matching():
    print("Testing Pub/Sub wildcard delivery...")
    bus = DistributedAgentEventBus()
    received = []

    bus.subscribe("test_sub", "iot.sensor.*", lambda e: received.append(e.payload))

    # Match 1
    bus.publish(AgentEvent("iot.sensor.temp", "pub1", {"val": 72}))
    # Match 2
    bus.publish(AgentEvent("iot.sensor.humidity", "pub1", {"val": 45}))
    # No match
    bus.publish(AgentEvent("iot.device.status", "pub1", {"val": "online"}))

    assert len(received) == 2
    assert received[0]["val"] == 72
    assert received[1]["val"] == 45
    print("  [PASSED] Wildcard topic matching delivered events reliably.")


def test_dead_letter_quarantine():
    print("\nTesting Dead-Letter Queue quarantine on crash...")
    bus = DistributedAgentEventBus(max_retries=1)

    def crashing_handler(event: AgentEvent):
        raise ValueError("Fatal parser crash")

    bus.subscribe("broken_agent", "finance.txn", crashing_handler)

    bus.publish(AgentEvent("finance.txn", "pos", {"amount": 100}))

    assert len(bus.dead_letter_queue) == 1
    dlq = bus.dead_letter_queue[0]
    assert "Fatal parser crash" in dlq.reason
    assert dlq.failed_subscriber == "broken_agent"
    print("  [PASSED] Failed event quarantined in DLQ with diagnostic error.")


if __name__ == "__main__":
    print("=" * 60)
    print("RUNNING VERIFICATION SUITE: PROJECT 030")
    print("=" * 60)
    test_pubsub_wildcard_matching()
    test_dead_letter_quarantine()
    print("\n[ALL TESTS PASSED] Project 030 verified successfully!")
