"""
===============================================================================
PROJECT 030: ASYNCHRONOUS PUB/SUB AGENT EVENT BUS WITH DEAD LETTERS
Stage 1: Pure Fundamentals | Difficulty: 3.5 / 10 (Intermediate)
===============================================================================

THE BIG QUESTION:
How do hundreds of autonomous agents publish and consume events without tight
coupling, and what happens when an event fails to process?

THE DISTRIBUTED AGENT EVENT BUS PATTERN:
1. Publisher-Subscriber (Pub/Sub): Agents broadcast events to specific topic hierarchies
   (e.g., 'orders.created', 'kitchen.temperature_alert', 'inventory.low_stock').
2. Topic Filtering: Subscribers declare exact or wildcard topic filters.
3. Decoupled Delivery: Publishers don't know who or how many agents are listening.
4. Dead-Letter Queue (DLQ): If a subscriber crashes, or if an event is unroutable,
   the event is quarantined in the DLQ with full diagnostic metadata rather than lost.
===============================================================================
"""

import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import time
import uuid
import fnmatch
from typing import Dict, Any, List, Callable, Optional
from dataclasses import dataclass, field
from config import get_llm, ACTIVE_MODEL


@dataclass
class AgentEvent:
    topic: str
    publisher_id: str
    payload: Dict[str, Any]
    event_id: str = field(default_factory=lambda: f"evt_{uuid.uuid4().hex[:8]}")
    timestamp: float = field(default_factory=time.time)
    retry_count: int = 0


@dataclass
class DeadLetterRecord:
    event: AgentEvent
    reason: str
    failed_subscriber: Optional[str]
    quarantined_at: float = field(default_factory=time.time)


# =============================================================================
# 1. DISTRIBUTED EVENT BUS WITH DEAD-LETTER QUEUE
# =============================================================================
class DistributedAgentEventBus:
    def __init__(self, max_retries: int = 2):
        self.max_retries = max_retries
        self.subscribers: List[Dict[str, Any]] = []
        self.event_log: List[AgentEvent] = []
        self.dead_letter_queue: List[DeadLetterRecord] = []

    def subscribe(self, agent_id: str, topic_pattern: str, handler: Callable[[AgentEvent], None]):
        """Subscribes an agent callback to topic patterns (supports wildcards e.g. 'order.*')."""
        self.subscribers.append({
            "agent_id": agent_id,
            "pattern": topic_pattern,
            "handler": handler,
        })

    def publish(self, event: AgentEvent) -> int:
        """Publishes an event to matching subscribers; routes failures to DLQ."""
        self.event_log.append(event)
        delivered_count = 0

        # Find matching subscribers
        matching = [
            sub for sub in self.subscribers
            if fnmatch.fnmatch(event.topic, sub["pattern"])
        ]

        if not matching:
            # Unroutable event -> goes directly to DLQ
            self.dead_letter_queue.append(DeadLetterRecord(
                event=event,
                reason="UNROUTABLE_NO_SUBSCRIBERS",
                failed_subscriber=None,
            ))
            return 0

        for sub in matching:
            agent_id = sub["agent_id"]
            handler = sub["handler"]
            success = False

            while event.retry_count <= self.max_retries and not success:
                try:
                    handler(event)
                    success = True
                    delivered_count += 1
                except Exception as e:
                    event.retry_count += 1
                    if event.retry_count > self.max_retries:
                        # Quarantine to Dead-Letter Queue
                        self.dead_letter_queue.append(DeadLetterRecord(
                            event=event,
                            reason=f"EXECUTION_FAILURE: {str(e)}",
                            failed_subscriber=agent_id,
                        ))

        return delivered_count


# =============================================================================
# 2. PARTICIPATING SUBSCRIBER & PUBLISHER AGENTS
# =============================================================================
class BaristaKioskPublisher:
    def __init__(self, bus: DistributedAgentEventBus):
        self.bus = bus
        self.agent_id = "agent://kiosk/front_register"

    def emit_new_order(self, order_id: str, drink: str, customer: str):
        evt = AgentEvent(
            topic="orders.created.express",
            publisher_id=self.agent_id,
            payload={"order_id": order_id, "drink": drink, "customer": customer},
        )
        self.bus.publish(evt)


class KitchenDisplaySubscriber:
    def __init__(self, bus: DistributedAgentEventBus):
        self.agent_id = "agent://kitchen/display"
        self.processed_orders: List[Dict[str, Any]] = []
        bus.subscribe(self.agent_id, "orders.*", self.on_order_event)

    def on_order_event(self, event: AgentEvent):
        self.processed_orders.append(event.payload)


class FaultySafetySubscriber:
    """Agent that fails intentionally to demonstrate Dead-Letter Queues."""
    def __init__(self, bus: DistributedAgentEventBus):
        self.agent_id = "agent://safety/sensor_monitor"
        bus.subscribe(self.agent_id, "kitchen.temperature_alert", self.on_temp_alert)

    def on_temp_alert(self, event: AgentEvent):
        # Deliberate failure: attempts to access missing key or divides by zero
        temp = event.payload["current_temp"]
        if temp > 400:
            raise RuntimeError(f"Sensor Overheat Fault! Core thermocouple hardware disconnected at {temp}F")


# =============================================================================
# 3. MAIN DEMONSTRATION
# =============================================================================
def main():
    print("=" * 75)
    print("PROJECT 030: ASYNCHRONOUS PUB/SUB AGENT EVENT BUS WITH DEAD LETTERS")
    print(f"Active Groq Model: {ACTIVE_MODEL}")
    print("=" * 75)

    bus = DistributedAgentEventBus(max_retries=1)

    kiosk = BaristaKioskPublisher(bus)
    kitchen = KitchenDisplaySubscriber(bus)
    faulty_safety = FaultySafetySubscriber(bus)

    # -------------------------------------------------------------------------
    # TEST 1: SUCCESSFUL PUB/SUB (WILDCARD TOPIC MATCHING)
    # -------------------------------------------------------------------------
    print("\n" + "-" * 75)
    print("1. PUB/SUB DELIVERY: 'orders.created.express' -> Matching 'orders.*'")
    print("-" * 75)
    kiosk.emit_new_order("ORD-101", "Salted Caramel Oat Latte", "Sophia Clark")
    print(f"Kitchen Display Inbox Count: {len(kitchen.processed_orders)}")
    print(f"Kitchen Received: {kitchen.processed_orders[0]}")

    # -------------------------------------------------------------------------
    # TEST 2: DEAD-LETTER HANDLING (SUBSCRIBER CRASH QUARANTINE)
    # -------------------------------------------------------------------------
    print("\n" + "-" * 75)
    print("2. FAULT INJECTION & DEAD-LETTER QUEUE (Subscriber Crash)")
    print("-" * 75)
    alert_event = AgentEvent(
        topic="kitchen.temperature_alert",
        publisher_id="agent://oven/deck_01",
        payload={"current_temp": 450, "zone": "Oven Core A"},
    )
    bus.publish(alert_event)

    print(f"Dead-Letter Queue Size: {len(bus.dead_letter_queue)}")
    dlq_record = bus.dead_letter_queue[0]
    print(f"Quarantined Event ID : {dlq_record.event.event_id}")
    print(f"Target Subscriber    : {dlq_record.failed_subscriber}")
    print(f"Failure Diagnosis    : {dlq_record.reason}")

    # -------------------------------------------------------------------------
    # TEST 3: UNROUTABLE EVENT (NO SUBSCRIBERS)
    # -------------------------------------------------------------------------
    print("\n" + "-" * 75)
    print("3. UNROUTABLE EVENT (Topic with 0 Subscribers)")
    print("-" * 75)
    unroutable = AgentEvent(
        topic="music.playlist.changed",
        publisher_id="agent://audio/spotify",
        payload={"song": "Jazz Classics", "volume": 65},
    )
    bus.publish(unroutable)
    print(f"Dead-Letter Queue Size: {len(bus.dead_letter_queue)}")
    print(f"Latest DLQ Entry Reason: {bus.dead_letter_queue[1].reason}")

    # -------------------------------------------------------------------------
    # TEST 4: LLM AUTONOMOUS SRE DIAGNOSTIC ON DEAD LETTERS
    # -------------------------------------------------------------------------
    print("\n" + "=" * 75)
    print("AI SITE RELIABILITY ENGINEER (SRE) DEAD-LETTER DIAGNOSIS")
    print("=" * 75)
    llm = get_llm(temperature=0.0)
    prompt = (
        "You are the Lead Systems Reliability Engineer. An asynchronous agent bus reported "
        f"{len(bus.dead_letter_queue)} dead-letter events:\n"
        f"Event 1: Topic='{dlq_record.event.topic}', Reason='{dlq_record.reason}'\n"
        f"Event 2: Topic='{unroutable.topic}', Reason='{bus.dead_letter_queue[1].reason}'\n\n"
        "Provide a 2-point immediate triage summary explaining the root causes and remediation actions."
    )
    sre_report = llm.invoke(prompt).content.strip()
    print(sre_report)

    print("\n" + "=" * 75)
    print("[SUCCESS] Project 030 demonstration completed cleanly!")


if __name__ == "__main__":
    main()
