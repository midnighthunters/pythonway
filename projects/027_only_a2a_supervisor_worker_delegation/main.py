"""
===============================================================================
PROJECT 027: HIERARCHICAL SUPERVISOR-WORKER DELEGATION PROTOCOL
Stage 1: Pure Fundamentals | Difficulty: 3.0 / 10 (Intermediate)
===============================================================================

THE BIG QUESTION:
How do enterprise multi-agent systems coordinate complex goals that exceed
any single agent's specialization?

THE SUPERVISOR-WORKER PATTERN:
1. Supervisor Agent (The Orchestrator):
   - Receives high-level user goals.
   - Decomposes goals into discrete, specialized sub-tasks.
   - Delegates work to specialized Worker Agents.
   - Monitors status and aggregates individual findings into a unified output.
2. Worker Agents (Domain Specialists):
   - Deep domain focus (e.g. Coffee Sommelier, Bakery Kitchen, Financial Margin).
   - Zero awareness of unrelated business concerns.
   - Execute sub-tasks with high accuracy and report structured findings.
===============================================================================
"""

import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import json
from typing import Dict, Any, List
from dataclasses import dataclass
from config import get_llm, ACTIVE_MODEL


@dataclass
class DelegationTask:
    task_id: str
    target_worker: str
    instruction: str
    context: Dict[str, Any]


@dataclass
class WorkerReport:
    task_id: str
    worker_id: str
    status: str
    findings: str
    metrics: Dict[str, Any]


# =============================================================================
# 1. SPECIALIZED WORKER AGENTS
# =============================================================================
class CoffeeSommelierWorker:
    """Specializes in sensory profiles, roast pairings, and brewing parameters."""
    worker_id = "worker://beverage/sommelier"

    def execute(self, task: DelegationTask) -> WorkerReport:
        target_vibe = task.context.get("theme", "Autumn Harvest")
        llm = get_llm(temperature=0.2)
        prompt = (
            f"You are the Master Coffee Sommelier. For a cafe promotional theme '{target_vibe}', "
            "recommend ONE specific single-origin coffee bean, the roast profile (light/medium/dark), "
            "and 3 key tasting notes. Keep it concise (2-3 sentences)."
        )
        res = llm.invoke(prompt).content.strip()
        return WorkerReport(
            task_id=task.task_id,
            worker_id=self.worker_id,
            status="COMPLETED",
            findings=res,
            metrics={"optimal_brew_temp_f": 201, "recommended_ratio": "1:16"},
        )


class BakeryKitchenWorker:
    """Specializes in batch scaling, recipe ratios, and ingredient costs."""
    worker_id = "worker://kitchen/baker"

    def execute(self, task: DelegationTask) -> WorkerReport:
        headcount = task.context.get("headcount", 50)
        # Scaled calculation for batch
        flour_kg = headcount * 0.08
        butter_kg = headcount * 0.04
        sugar_kg = headcount * 0.03

        findings = (
            f"Scaled production for {headcount} guests: Requires {flour_kg:.1f}kg bread flour, "
            f"{butter_kg:.1f}kg Normandy butter, and {sugar_kg:.1f}kg unrefined cane sugar. "
            "Bake schedule: 3 batches across 2 deck ovens at 380F, total kitchen labor time: 2.5 hours."
        )
        return WorkerReport(
            task_id=task.task_id,
            worker_id=self.worker_id,
            status="COMPLETED",
            findings=findings,
            metrics={"total_prep_hours": 2.5, "yield_count": headcount},
        )


class FinancialAnalystWorker:
    """Specializes in margin calculation, food cost percentage, and retail pricing."""
    worker_id = "worker://finance/analyst"

    def execute(self, task: DelegationTask) -> WorkerReport:
        target_margin = task.context.get("target_margin_pct", 70.0)
        cogs_per_unit = 2.40  # Raw ingredient and packaging cost
        recommended_price = cogs_per_unit / (1 - (target_margin / 100.0))

        findings = (
            f"Cost of Goods Sold (COGS) is calculated at ${cogs_per_unit:.2f}/combo. "
            f"To achieve the targeted {target_margin:.0f}% gross margin, recommended retail price "
            f"is ${recommended_price:.2f}. Projected gross profit per 100 combos sold: ${recommended_price * 100 - cogs_per_unit * 100:.2f}."
        )
        return WorkerReport(
            task_id=task.task_id,
            worker_id=self.worker_id,
            status="COMPLETED",
            findings=findings,
            metrics={"cogs": cogs_per_unit, "retail_price": round(recommended_price, 2), "margin_pct": target_margin},
        )


# =============================================================================
# 2. HIERARCHICAL SUPERVISOR AGENT
# =============================================================================
class CafeSupervisorAgent:
    """Orchestrator that plans sub-tasks, dispatches to workers, and synthesizes output."""
    def __init__(self):
        self.workers = {
            CoffeeSommelierWorker.worker_id: CoffeeSommelierWorker(),
            BakeryKitchenWorker.worker_id: BakeryKitchenWorker(),
            FinancialAnalystWorker.worker_id: FinancialAnalystWorker(),
        }

    def decompose_and_delegate(self, user_objective: str, context: Dict[str, Any]) -> List[WorkerReport]:
        """Creates delegation tasks and dispatches to specialized workers."""
        tasks = [
            DelegationTask(
                task_id="task_001_sommelier",
                target_worker=CoffeeSommelierWorker.worker_id,
                instruction="Select optimal coffee roast pairing",
                context=context,
            ),
            DelegationTask(
                task_id="task_002_kitchen",
                target_worker=BakeryKitchenWorker.worker_id,
                instruction="Calculate scaled batch ingredients and kitchen labor",
                context=context,
            ),
            DelegationTask(
                task_id="task_003_finance",
                target_worker=FinancialAnalystWorker.worker_id,
                instruction="Determine pricing and unit margins",
                context=context,
            ),
        ]

        reports = []
        for t in tasks:
            worker = self.workers[t.target_worker]
            rep = worker.execute(t)
            reports.append(rep)
        return reports

    def aggregate_and_synthesize(self, user_objective: str, reports: List[WorkerReport]) -> str:
        """Synthesizes worker reports into a coherent executive plan."""
        llm = get_llm(temperature=0.0)

        dossier = "\n\n".join([
            f"[{r.worker_id}]\nStatus: {r.status}\nFindings: {r.findings}\nMetrics: {json.dumps(r.metrics)}"
            for r in reports
        ])

        prompt = (
            "You are the Cafe General Manager & Executive Supervisor. You delegated a strategic initiative "
            f"to your three expert teams. Here is the objective:\n'{user_objective}'\n\n"
            f"Here are the reports from your specialized workers:\n{dossier}\n\n"
            "Synthesize these findings into an actionable 3-part Executive Launch Plan with clear headers. "
            "Be authoritative, concise, and professional."
        )
        return llm.invoke(prompt).content.strip()


# =============================================================================
# 3. MAIN DEMONSTRATION
# =============================================================================
def main():
    print("=" * 75)
    print("PROJECT 027: HIERARCHICAL SUPERVISOR-WORKER DELEGATION PROTOCOL")
    print(f"Active Groq Model: {ACTIVE_MODEL}")
    print("=" * 75)

    objective = "Launch a high-margin Autumn Harvest Coffee & Bakery Pairing Special for 50 attendees"
    context = {"theme": "Autumn Harvest Cinnamon & Maple", "headcount": 50, "target_margin_pct": 70.0}

    print(f"\n[CLIENT INITIATIVE]:\n\"{objective}\"")

    supervisor = CafeSupervisorAgent()

    # Step 1: Supervisor delegates
    print("\n" + "-" * 75)
    print("SUPERVISOR DELEGATION DISPATCH")
    print("-" * 75)
    reports = supervisor.decompose_and_delegate(objective, context)

    for i, rep in enumerate(reports, 1):
        print(f"\n[Worker Report #{i}] From: {rep.worker_id}")
        print(f"Status  : {rep.status}")
        print(f"Findings: {rep.findings}")
        print(f"Metrics : {rep.metrics}")

    # Step 2: Supervisor synthesizes
    print("\n" + "=" * 75)
    print("SUPERVISOR EXECUTIVE SYNTHESIS (Aggregated Strategic Plan)")
    print("=" * 75)
    final_plan = supervisor.aggregate_and_synthesize(objective, reports)
    print(final_plan)

    print("\n" + "=" * 75)
    print("[SUCCESS] Project 027 demonstration completed cleanly!")


if __name__ == "__main__":
    main()
