"""
===============================================================================
PROJECT 029: CONTRACT NET PROTOCOL (CNP): MARKET-BASED TASK ALLOCATION
Stage 1: Pure Fundamentals | Difficulty: 3.5 / 10 (Intermediate)
===============================================================================

THE BIG QUESTION:
In decentralized multi-agent networks, how do managers allocate tasks dynamically
without hardcoding which agent does what?

THE FIPA CONTRACT NET PROTOCOL (CNP):
1. Call for Proposals (CFP): Manager broadcasts task specifications to candidate contractors.
2. Proposal / Bid Submission: Contractors evaluate local capacity, price, and SLA to bid.
   Contractors may also issue a REFUSE if over capacity.
3. Multi-Attribute Evaluation: Manager evaluates bids using a utility function (price, SLA, quality).
4. Award & Rejection: Manager issues ACCEPT_PROPOSAL to the winner and REJECT_PROPOSAL to others.
5. Task Execution & Reporting: Winner executes and returns final deliverables.
===============================================================================
"""

import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import time
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from config import get_llm, ACTIVE_MODEL


@dataclass
class CallForProposal:
    task_id: str
    task_description: str
    deadline_minutes: int
    volume_units: int
    max_budget: float


@dataclass
class BidProposal:
    contractor_id: str
    task_id: str
    bid_price: float
    delivery_time_minutes: int
    reputation_score: float  # 0.0 - 10.0
    is_refused: bool = False
    refusal_reason: str = ""


# =============================================================================
# 1. CONTRACTOR AGENTS (BIDDERS)
# =============================================================================
class ContractorAgent:
    def __init__(self, agent_id: str, base_unit_cost: float, prep_speed_factor: float, reputation: float, capacity: int):
        self.agent_id = agent_id
        self.base_unit_cost = base_unit_cost
        self.prep_speed_factor = prep_speed_factor
        self.reputation = reputation
        self.capacity = capacity  # Maximum simultaneous units

    def evaluate_cfp(self, cfp: CallForProposal) -> BidProposal:
        if cfp.volume_units > self.capacity:
            return BidProposal(
                contractor_id=self.agent_id,
                task_id=cfp.task_id,
                bid_price=0.0,
                delivery_time_minutes=0,
                reputation_score=self.reputation,
                is_refused=True,
                refusal_reason=f"Capacity exceeded (Requested: {cfp.volume_units}, Max: {self.capacity})",
            )

        total_cost = self.base_unit_cost * cfp.volume_units * 1.15  # 15% margin
        delivery_time = int(cfp.volume_units * self.prep_speed_factor)

        if total_cost > cfp.max_budget:
            return BidProposal(
                contractor_id=self.agent_id,
                task_id=cfp.task_id,
                bid_price=total_cost,
                delivery_time_minutes=delivery_time,
                reputation_score=self.reputation,
                is_refused=True,
                refusal_reason=f"Cost ${total_cost:.2f} exceeds client max budget ${cfp.max_budget:.2f}",
            )

        return BidProposal(
            contractor_id=self.agent_id,
            task_id=cfp.task_id,
            bid_price=round(total_cost, 2),
            delivery_time_minutes=delivery_time,
            reputation_score=self.reputation,
            is_refused=False,
        )

    def execute_contract(self, cfp: CallForProposal) -> Dict[str, Any]:
        return {
            "status": "COMPLETED",
            "contractor": self.agent_id,
            "units_delivered": cfp.volume_units,
            "quality_certified": True,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        }


# =============================================================================
# 2. MANAGER AGENT (AUCTIONEER & CONTRACT AWARDER)
# =============================================================================
class CateringManagerAgent:
    def __init__(self, agent_id: str = "agent://manager/catering_hub"):
        self.agent_id = agent_id
        self.contractors: List[ContractorAgent] = []

    def register_contractor(self, contractor: ContractorAgent):
        self.contractors.append(contractor)

    def broadcast_cfp(self, cfp: CallForProposal) -> List[BidProposal]:
        """Broadcasts CFP to all registered contractors."""
        return [c.evaluate_cfp(cfp) for c in self.contractors]

    def evaluate_and_award(
        self,
        cfp: CallForProposal,
        bids: List[BidProposal],
        weight_cost: float = 0.4,
        weight_speed: float = 0.3,
        weight_reputation: float = 0.3,
    ) -> Optional[BidProposal]:
        """
        Evaluates valid bids using multi-attribute utility function:
        Utility = (Norm_Rep * W_rep) - (Norm_Cost * W_cost) - (Norm_Time * W_time)
        """
        valid_bids = [b for b in bids if not b.is_refused]
        if not valid_bids:
            return None

        # Min-max normalization helpers
        min_cost = min(b.bid_price for b in valid_bids)
        min_time = min(b.delivery_time_minutes for b in valid_bids)

        best_bid = None
        highest_utility = -float("inf")

        for b in valid_bids:
            # Lower cost and time are better -> inverted score
            cost_score = (min_cost / b.bid_price) * 10.0
            time_score = (min_time / b.delivery_time_minutes) * 10.0
            rep_score = b.reputation_score

            utility = (cost_score * weight_cost) + (time_score * weight_speed) + (rep_score * weight_reputation)
            if utility > highest_utility:
                highest_utility = utility
                best_bid = b

        return best_bid


# =============================================================================
# 3. MAIN DEMONSTRATION
# =============================================================================
def main():
    print("=" * 75)
    print("PROJECT 029: CONTRACT NET PROTOCOL (CNP): MARKET-BASED TASK ALLOCATION")
    print(f"Active Groq Model: {ACTIVE_MODEL}")
    print("=" * 75)

    manager = CateringManagerAgent()

    # Register 3 distinct contractors with diverse market trade-offs
    c1 = ContractorAgent("agent://contractor/speedy_brew", base_unit_cost=3.20, prep_speed_factor=0.25, reputation=8.5, capacity=250)
    c2 = ContractorAgent("agent://contractor/economy_beans", base_unit_cost=2.10, prep_speed_factor=0.45, reputation=7.2, capacity=300)
    c3 = ContractorAgent("agent://contractor/artisan_roast", base_unit_cost=4.50, prep_speed_factor=0.30, reputation=9.8, capacity=100)

    manager.register_contractor(c1)
    manager.register_contractor(c2)
    manager.register_contractor(c3)

    # Broadcast Call for Proposals (CFP)
    cfp = CallForProposal(
        task_id="cfp_event_882",
        task_description="Supply 120 iced oat matcha lattes for tech conference kickoff",
        deadline_minutes=60,
        volume_units=120,
        max_budget=600.00,
    )

    print("\n" + "-" * 75)
    print(f"1. MANAGER BROADCASTING CALL FOR PROPOSALS (CFP: {cfp.task_id})")
    print("-" * 75)
    print(f"Task: {cfp.task_description}")
    print(f"Volume: {cfp.volume_units} units | Max Budget: ${cfp.max_budget:.2f} | Deadline: {cfp.deadline_minutes} mins")

    # Contractors submit bids
    bids = manager.broadcast_cfp(cfp)

    print("\n" + "-" * 75)
    print("2. CONTRACTOR BIDS RECEIVED")
    print("-" * 75)
    for b in bids:
        if b.is_refused:
            print(f"❌ {b.contractor_id:<32} | REFUSED | Reason: {b.refusal_reason}")
        else:
            print(f"✅ {b.contractor_id:<32} | Bid: ${b.bid_price:>6.2f} | Time: {b.delivery_time_minutes}m | Rep: {b.reputation_score}/10")

    # Manager evaluates and awards contract
    winning_bid = manager.evaluate_and_award(cfp, bids)

    print("\n" + "=" * 75)
    print("3. CONTRACT AWARDED BY MANAGER")
    print("=" * 75)
    print(f"Winning Contractor: {winning_bid.contractor_id}")
    print(f"Price Agreed      : ${winning_bid.bid_price:.2f}")
    print(f"Delivery Target   : {winning_bid.delivery_time_minutes} minutes")

    # Winner executes
    winner_agent = [c for c in manager.contractors if c.agent_id == winning_bid.contractor_id][0]
    exec_result = winner_agent.execute_contract(cfp)
    print(f"\nExecution Result : {exec_result}")

    # LLM Award Justification Letter
    llm = get_llm(temperature=0.0)
    prompt = (
        f"You are the Catering Manager. Explain to the client why {winning_bid.contractor_id} "
        f"won the contract for {cfp.volume_units} drinks at ${winning_bid.bid_price:.2f} in {winning_bid.delivery_time_minutes} mins "
        f"over competing bidders based on multi-attribute utility (balancing price, speed, and reputation). "
        "Keep it concise (2-3 sentences)."
    )
    explanation = llm.invoke(prompt).content.strip()
    print(f"\n[Manager Award Rationale]:\n{explanation}")

    print("\n" + "=" * 75)
    print("[SUCCESS] Project 029 demonstration completed cleanly!")


if __name__ == "__main__":
    main()
