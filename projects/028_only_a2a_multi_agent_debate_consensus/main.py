"""
===============================================================================
PROJECT 028: MULTI-AGENT DIALECTICAL DEBATE & CONSENSUS PROTOCOL
Stage 1: Pure Fundamentals | Difficulty: 3.0 / 10 (Intermediate)
===============================================================================

THE BIG QUESTION:
How do multi-agent systems eliminate single-agent bias and reach objective
truth on controversial strategic decisions?

THE DIALECTICAL DEBATE PROTOCOL:
1. The Thesis (Pro-Agent): Strongly argues in favor of the proposition with empirical points.
2. The Antithesis (Con-Agent): Directly rebuts claims, highlighting edge cases and risks.
3. Multi-Round Cross-Examination: Agents rebut each other's points across rounds.
4. The Synthesis (Judge Agent / Adjudicator): An unbiased evaluator assesses logical
   soundness, flags logical fallacies, and drafts a balanced, compromise-driven consensus.
===============================================================================
"""

import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from typing import Dict, Any, List
from dataclasses import dataclass, field
from config import get_llm, ACTIVE_MODEL


@dataclass
class DebateTurn:
    round_number: int
    speaker: str
    stance: str  # PRO, CON, JUDGE
    argument: str


# =============================================================================
# 1. DEBATING AGENTS
# =============================================================================
class ProAdvocateAgent:
    """Argues strongly in favor of the proposition using data and modernization."""
    agent_id = "agent://debate/pro_modernizer"

    def argue(self, proposition: str, round_num: int, opponent_last_arg: str = "") -> str:
        llm = get_llm(temperature=0.3)
        if round_num == 1:
            prompt = (
                f"You are the Pro-Advocate arguing STRONGLY IN FAVOR of this proposition:\n'{proposition}'\n\n"
                "State your opening argument with 2 concrete, data-backed reasons focusing on efficiency, "
                "scale, and operational consistency. Keep it punchy and persuasive (3-4 sentences)."
            )
        else:
            prompt = (
                f"You are the Pro-Advocate for: '{proposition}'\n"
                f"Your opponent argued:\n\"{opponent_last_arg}\"\n\n"
                "Rebut your opponent's points directly. Explain why their concerns can be mitigated with modern technology. "
                "Keep it punchy (3-4 sentences)."
            )
        return llm.invoke(prompt).content.strip()


class ConAdvocateAgent:
    """Argues strongly against the proposition, defending human craft and brand culture."""
    agent_id = "agent://debate/con_traditionalist"

    def argue(self, proposition: str, round_num: int, opponent_last_arg: str = "") -> str:
        llm = get_llm(temperature=0.3)
        if round_num == 1:
            prompt = (
                f"You are the Con-Advocate arguing STRONGLY AGAINST this proposition:\n'{proposition}'\n\n"
                "State your opening argument with 2 compelling reasons focusing on customer loyalty, "
                "artisan quality, emotional connection, and high capital maintenance risks. Keep it punchy (3-4 sentences)."
            )
        else:
            prompt = (
                f"You are the Con-Advocate against: '{proposition}'\n"
                f"Your opponent argued:\n\"{opponent_last_arg}\"\n\n"
                "Directly expose the flaws in your opponent's argument. Emphasize what machines cannot replicate. "
                "Keep it punchy (3-4 sentences)."
            )
        return llm.invoke(prompt).content.strip()


# =============================================================================
# 2. IMPARTIAL ADJUDICATOR (JUDGE AGENT)
# =============================================================================
class AdjudicatorJudgeAgent:
    """Impartial judge analyzing debate rounds to deliver a synthesized consensus."""
    agent_id = "agent://debate/chief_adjudicator"

    def adjudicate(self, proposition: str, history: List[DebateTurn]) -> str:
        llm = get_llm(temperature=0.0)

        transcript = "\n\n".join([
            f"[Round {t.round_number} - {t.stance} ({t.speaker})]\n{t.argument}"
            for t in history
        ])

        prompt = (
            "You are the Chief AI Adjudicator and Strategic Arbitrator. "
            f"Review this multi-round dialectical debate on the proposition:\n'{proposition}'\n\n"
            f"Debate Transcript:\n{transcript}\n\n"
            "Deliver an impartial, objective ruling with:\n"
            "1. STRENGTHS OF PRO: Best point made by Pro-Advocate\n"
            "2. STRENGTHS OF CON: Best point made by Con-Advocate\n"
            "3. DIALECTICAL CONSENSUS VERDICT: The optimal, pragmatic middle-ground strategy."
        )
        return llm.invoke(prompt).content.strip()


# =============================================================================
# 3. DEBATE ORCHESTRATOR
# =============================================================================
class DialecticalDebateOrchestrator:
    def __init__(self, rounds: int = 2):
        self.rounds = rounds
        self.pro = ProAdvocateAgent()
        self.con = ConAdvocateAgent()
        self.judge = AdjudicatorJudgeAgent()
        self.history: List[DebateTurn] = []

    def run_debate(self, proposition: str) -> str:
        self.history.clear()
        pro_last = ""
        con_last = ""

        for r in range(1, self.rounds + 1):
            # Pro turn
            pro_arg = self.pro.argue(proposition, r, con_last)
            self.history.append(DebateTurn(r, self.pro.agent_id, "PRO", pro_arg))
            pro_last = pro_arg

            # Con turn
            con_arg = self.con.argue(proposition, r, pro_last)
            self.history.append(DebateTurn(r, self.con.agent_id, "CON", con_arg))
            con_last = con_arg

        # Adjudication
        verdict = self.judge.adjudicate(proposition, self.history)
        self.history.append(DebateTurn(self.rounds + 1, self.judge.agent_id, "JUDGE", verdict))
        return verdict


# =============================================================================
# 4. MAIN DEMONSTRATION
# =============================================================================
def main():
    print("=" * 75)
    print("PROJECT 028: MULTI-AGENT DIALECTICAL DEBATE & CONSENSUS PROTOCOL")
    print(f"Active Groq Model: {ACTIVE_MODEL}")
    print("=" * 75)

    proposition = (
        "Should Cozy Coffee replace 100% of human espresso baristas with autonomous "
        "robotic arms to optimize drink speed, reduce payroll, and guarantee zero extraction variance?"
    )

    print(f"\n[DEBATE PROPOSITION]:\n\"{proposition}\"\n")

    orchestrator = DialecticalDebateOrchestrator(rounds=2)
    verdict = orchestrator.run_debate(proposition)

    for turn in orchestrator.history[:-1]:
        prefix = f"--- [ROUND {turn.round_number} | {turn.stance}: {turn.speaker}] ---"
        print("-" * 75)
        print(prefix)
        print("-" * 75)
        print(f"{turn.argument}\n")

    print("=" * 75)
    print("CHIEF ADJUDICATOR CONSENSUS RULING")
    print("=" * 75)
    print(verdict)

    print("\n" + "=" * 75)
    print("[SUCCESS] Project 028 demonstration completed cleanly!")


if __name__ == "__main__":
    main()
