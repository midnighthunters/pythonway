"""
===============================================================================
PROJECT 026: PEER-TO-PEER AGENT MESSAGING PROTOCOL & ADDRESSING
Stage 1: Pure Fundamentals | Difficulty: 2.5 / 10 (Intermediate)
===============================================================================

THE BIG QUESTION:
How do independent AI agents communicate directly with each other without
chaotic spaghetti function calls?

In Agent-to-Agent (A2A) architectures:
1. Message Envelope Standard: Every inter-agent payload is wrapped in a strict
   envelope containing sender, recipient, thread ID, and speech-act performative.
2. Unique Agent Addressing: Every agent has a registered URI or ID (e.g. 'agent://barista_front').
3. Conversation Threading: Messages carry thread IDs so agents can maintain
   isolated conversational contexts across concurrent multi-agent discussions.
4. Asynchronous Mailboxes: Agents receive messages into private inboxes, allowing
   decoupled processing and reply dispatch.
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
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from config import get_llm, ACTIVE_MODEL


# =============================================================================
# 1. A2A MESSAGE ENVELOPE SPECIFICATION
# =============================================================================
@dataclass
class MessageEnvelope:
    """Standardized message packet for peer-to-peer agent communications."""
    sender_id: str
    recipient_id: str
    thread_id: str
    performative: str  # REQUEST, INFORM, CONFIRM, REFUSE
    content: Dict[str, Any]
    message_id: str = field(default_factory=lambda: f"msg_{uuid.uuid4().hex[:8]}")
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "message_id": self.message_id,
            "sender_id": self.sender_id,
            "recipient_id": self.recipient_id,
            "thread_id": self.thread_id,
            "performative": self.performative,
            "content": self.content,
            "timestamp": self.timestamp,
        }


# =============================================================================
# 2. AGENT MAILBOX & PEER MESSAGE BUS
# =============================================================================
class AgentMailbox:
    """Private queue and conversation thread storage for an autonomous agent."""
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.inbox: List[MessageEnvelope] = []
        self.threads: Dict[str, List[MessageEnvelope]] = {}

    def receive(self, envelope: MessageEnvelope):
        self.inbox.append(envelope)
        if envelope.thread_id not in self.threads:
            self.threads[envelope.thread_id] = []
        self.threads[envelope.thread_id].append(envelope)

    def get_unread(self) -> List[MessageEnvelope]:
        unread = list(self.inbox)
        self.inbox.clear()
        return unread


class PeerMessageBus:
    """Central router directing envelopes between registered peer agents."""
    def __init__(self):
        self.registry: Dict[str, AgentMailbox] = {}
        self.delivery_history: List[MessageEnvelope] = []

    def register_agent(self, agent_id: str) -> AgentMailbox:
        if agent_id in self.registry:
            return self.registry[agent_id]
        mailbox = AgentMailbox(agent_id)
        self.registry[agent_id] = mailbox
        return mailbox

    def send(self, envelope: MessageEnvelope) -> bool:
        if envelope.recipient_id not in self.registry:
            raise KeyError(f"DELIVERY FAILED: Unknown agent '{envelope.recipient_id}'")

        self.registry[envelope.recipient_id].receive(envelope)
        self.delivery_history.append(envelope)
        return True


# =============================================================================
# 3. AUTONOMOUS PEER AGENTS
# =============================================================================
class BasePeerAgent:
    def __init__(self, agent_id: str, bus: PeerMessageBus):
        self.agent_id = agent_id
        self.bus = bus
        self.mailbox = bus.register_agent(agent_id)

    def send_to_peer(self, recipient_id: str, thread_id: str, performative: str, content: Dict[str, Any]):
        env = MessageEnvelope(
            sender_id=self.agent_id,
            recipient_id=recipient_id,
            thread_id=thread_id,
            performative=performative,
            content=content,
        )
        self.bus.send(env)
        return env


class BaristaAgent(BasePeerAgent):
    """Front-of-house agent managing customer coffee & pastry orders."""
    def order_pastries(self, baker_id: str, pastry: str, quantity: int) -> str:
        thread_id = f"thread_order_{uuid.uuid4().hex[:6]}"
        self.send_to_peer(
            recipient_id=baker_id,
            thread_id=thread_id,
            performative="REQUEST",
            content={"item": pastry, "quantity": quantity},
        )
        return thread_id


class BakerAgent(BasePeerAgent):
    """Kitchen agent that bakes fresh items and coordinates supplies."""
    def process_incoming_orders(self, supply_id: str):
        for msg in self.mailbox.get_unread():
            if msg.performative == "REQUEST":
                item = msg.content.get("item", "pastry")
                qty = msg.content.get("quantity", 1)

                # Check with inventory agent first
                supply_thread = f"thread_supply_{msg.thread_id}"
                self.send_to_peer(
                    recipient_id=supply_id,
                    thread_id=supply_thread,
                    performative="QUERY",
                    content={"ingredient": "organic_flour_lbs", "needed": qty * 0.5},
                )
                return msg.thread_id, item, qty
        return None, None, None


class SupplyAgent(BasePeerAgent):
    """Warehouse inventory agent tracking stock levels."""
    def __init__(self, agent_id: str, bus: PeerMessageBus):
        super().__init__(agent_id, bus)
        self.stock = {"organic_flour_lbs": 50.0, "butter_kg": 20.0}

    def process_inquiries(self):
        for msg in self.mailbox.get_unread():
            if msg.performative == "QUERY":
                ing = msg.content.get("ingredient")
                needed = msg.content.get("needed", 1.0)
                available = self.stock.get(ing, 0.0) >= needed

                self.send_to_peer(
                    recipient_id=msg.sender_id,
                    thread_id=msg.thread_id,
                    performative="INFORM",
                    content={"ingredient": ing, "available": available, "current_stock": self.stock.get(ing, 0.0)},
                )


# =============================================================================
# 4. MAIN DEMONSTRATION
# =============================================================================
def main():
    print("=" * 75)
    print("PROJECT 026: PEER-TO-PEER AGENT MESSAGING PROTOCOL & ADDRESSING")
    print(f"Active Groq Model: {ACTIVE_MODEL}")
    print("=" * 75)

    bus = PeerMessageBus()

    barista = BaristaAgent("agent://front/barista_01", bus)
    baker = BakerAgent("agent://kitchen/baker_01", bus)
    supplier = SupplyAgent("agent://warehouse/supply_01", bus)

    print("\n[STEP 1: REGISTRATION]")
    print(f"Registered Agents on Bus: {list(bus.registry.keys())}")

    # Step 1: Barista orders from Baker
    print("\n" + "-" * 75)
    print("STEP 2: Barista sends REQUEST to Baker")
    print("-" * 75)
    thread = barista.order_pastries(baker.agent_id, "Almond Croissants", 6)
    print(f"Dispatched order on Thread: '{thread}'")

    # Step 2: Baker processes order and queries Supply
    print("\n" + "-" * 75)
    print("STEP 3: Baker checks ingredients with Warehouse Supplier")
    print("-" * 75)
    _, item, qty = baker.process_incoming_orders(supplier.agent_id)
    print(f"Baker processed request for {qty}x {item}. Sent QUERY to Supply Agent.")

    # Step 3: Supplier answers Baker
    print("\n" + "-" * 75)
    print("STEP 4: Warehouse Supplier responds with stock confirmation")
    print("-" * 75)
    supplier.process_inquiries()

    # Step 4: Baker confirms back to Barista using Groq LLM synthesis
    supply_replies = baker.mailbox.get_unread()
    supply_status = supply_replies[0].content if supply_replies else {}
    print(f"Baker received supply update: {supply_status}")

    llm = get_llm(temperature=0.0)
    prompt = (
        f"You are {baker.agent_id}. The barista requested {qty}x {item}. "
        f"Supply status confirms flour is available (in stock: {supply_status.get('current_stock')} lbs). "
        "Write a 1-sentence friendly confirmation message to the barista confirming the bake time (25 mins)."
    )
    baker_confirm = llm.invoke(prompt).content.strip()

    baker.send_to_peer(
        recipient_id=barista.agent_id,
        thread_id=thread,
        performative="CONFIRM",
        content={"message": baker_confirm, "estimated_minutes": 25},
    )

    # Barista reads confirmation
    final_inbox = barista.mailbox.get_unread()
    final_msg = final_inbox[0]
    print(f"\n<<< Barista received CONFIRM on thread '{final_msg.thread_id}':")
    print(f"    Message: \"{final_msg.content['message']}\"")
    print(f"    Ready in: {final_msg.content['estimated_minutes']} minutes")

    print("\n" + "=" * 75)
    print(f"Total Envelopes Exchanged Across Peer Bus: {len(bus.delivery_history)}")
    print("=" * 75)
    print("[SUCCESS] Project 026 demonstration completed cleanly!")


if __name__ == "__main__":
    main()
