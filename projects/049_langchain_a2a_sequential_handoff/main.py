"""
===============================================================================
PROJECT 049: LANGCHAIN + A2A: MULTI-AGENT SEQUENTIAL ROLE HANDOFF
Stage 2: Pairwise Combos | Difficulty: 4.5 / 10
===============================================================================

THE BIG QUESTION:
How do you build a multi-agent sequential pipeline where specialized AI personas
collaborate in an assembly line, passing strongly-typed handoff envelopes with
verified lineage and zero state leakage?

ARCHITECTURE:
1. Pydantic Handoff Envelope:
   - Carries sender, recipient, step metadata, structured payload, and audit lineage.
2. Three Specialized Agent Roles:
   - CoffeeResearcherAgent: Gathers agricultural, terroir, and variety facts.
   - SensoryAnalystAgent: Translates agronomy into brew ratios, roast profiles, and notes.
   - MarketingWriterAgent: Transforms technical analysis into an alluring guest menu feature.
3. Composable LCEL Sequential Pipeline:
   - Connected via LangChain Runnable primitives with envelope validation.
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
import json
from typing import List, Dict, Any
from pydantic import BaseModel, Field

from langchain_core.runnables import RunnableLambda
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from config import get_llm, ACTIVE_MODEL


# =============================================================================
# 1. STRUCTURED HANDOFF ENVELOPE (A2A PROTOCOL)
# =============================================================================
class HandoffEnvelope(BaseModel):
    envelope_id: str = Field(default_factory=lambda: f"env_{uuid.uuid4().hex[:8]}")
    sender_role: str
    recipient_role: str
    step_name: str
    timestamp: float = Field(default_factory=time.time)
    summary: str
    payload: Dict[str, Any]
    lineage: List[Dict[str, Any]] = Field(default_factory=list)

    def record_transition(self, next_recipient: str, next_step: str, new_summary: str, updated_payload: Dict[str, Any]) -> "HandoffEnvelope":
        """Records the current state in lineage and updates envelope for next agent."""
        history = list(self.lineage)
        history.append({
            "step": self.step_name,
            "sender": self.sender_role,
            "recipient": self.recipient_role,
            "summary": self.summary,
            "timestamp": round(self.timestamp, 2),
        })

        return HandoffEnvelope(
            envelope_id=f"env_{uuid.uuid4().hex[:8]}",
            sender_role=self.recipient_role,
            recipient_role=next_recipient,
            step_name=next_step,
            timestamp=time.time(),
            summary=new_summary,
            payload=updated_payload,
            lineage=history,
        )


# =============================================================================
# 2. ROLE AGENTS & RUNNABLE NODES
# =============================================================================
def researcher_agent(topic: str) -> HandoffEnvelope:
    """Role 1: Coffee Agronomist & Sourcing Researcher."""
    llm = get_llm(temperature=0.2)
    prompt = (
        f"You are a World-Class Coffee Agronomist (Researcher Agent).\n"
        f"Analyze the coffee bean topic: '{topic}'.\n"
        f"Identify the region/elevation, varietal, and harvesting processing method in 2 concise sentences."
    )
    res = llm.invoke(prompt)

    payload = {
        "topic": topic,
        "agronomy_research": res.content.strip(),
        "key_attributes": ["high-elevation", "washed", "single-origin"],
    }

    return HandoffEnvelope(
        sender_role="CoffeeResearcherAgent",
        recipient_role="SensoryAnalystAgent",
        step_name="agricultural_fact_extraction",
        summary=f"Extracted terroir and agronomy data for {topic}",
        payload=payload,
    )


def analyst_agent(envelope: HandoffEnvelope) -> HandoffEnvelope:
    """Role 2: Sensory Profiler & Roast Formulation Specialist."""
    llm = get_llm(temperature=0.2)
    research = envelope.payload.get("agronomy_research", "")
    topic = envelope.payload.get("topic", "")

    prompt = (
        f"You are the Head Sensory Cupper & Roast Master (Analyst Agent).\n"
        f"Based on the Researcher's agronomy findings:\n'{research}'\n\n"
        f"Formulate: (1) Recommended roast level, (2) Primary tasting notes, (3) Optimal water brew temperature.\n"
        f"Provide a 2-sentence precise technical assessment."
    )
    res = llm.invoke(prompt)

    updated_payload = dict(envelope.payload)
    updated_payload["sensory_analysis"] = res.content.strip()
    updated_payload["target_temp_f"] = 202

    return envelope.record_transition(
        next_recipient="MarketingWriterAgent",
        next_step="sensory_profile_formulation",
        new_summary="Formulated roast parameters and cupping notes",
        updated_payload=updated_payload,
    )


def writer_agent(envelope: HandoffEnvelope) -> HandoffEnvelope:
    """Role 3: Creative Copywriter & Menu Curator."""
    llm = get_llm(temperature=0.3)
    research = envelope.payload.get("agronomy_research", "")
    sensory = envelope.payload.get("sensory_analysis", "")
    topic = envelope.payload.get("topic", "")

    prompt = (
        f"You are the Creative Brand Storyteller for Cozy Cafe (Writer Agent).\n"
        f"Review the full research and sensory analysis:\n"
        f"AGRONOMY: {research}\n"
        f"SENSORY SPECS: {sensory}\n\n"
        f"Write an irresistible, sophisticated 3-sentence Coffee Feature Card for cafe customers. "
        f"Include a catchy title and tasting highlight."
    )
    res = llm.invoke(prompt)

    updated_payload = dict(envelope.payload)
    updated_payload["menu_feature_card"] = res.content.strip()

    return envelope.record_transition(
        next_recipient="CustomerDeliverySystem",
        next_step="final_menu_copy_synthesis",
        new_summary="Finalized guest-facing menu feature card",
        updated_payload=updated_payload,
    )


# =============================================================================
# 3. LCEL COMPOSABLE SEQUENTIAL PIPELINE
# =============================================================================
def build_sequential_handoff_pipeline():
    """Builds a typed LCEL pipeline composing agent handoff functions."""
    researcher_runnable = RunnableLambda(researcher_agent)
    analyst_runnable = RunnableLambda(analyst_agent)
    writer_runnable = RunnableLambda(writer_agent)

    # Compose sequential assembly pipeline
    pipeline = researcher_runnable | analyst_runnable | writer_runnable
    return pipeline


# =============================================================================
# 4. MAIN DEMONSTRATION RUNNER
# =============================================================================
def main():
    print("=" * 75)
    print("PROJECT 049: LANGCHAIN + A2A SEQUENTIAL ROLE HANDOFF PIPELINE")
    print(f"Active Groq Model: {ACTIVE_MODEL}")
    print("=" * 75)

    topic = "Panama Boquete Geisha harvested at 1750m elevation"
    print(f"\nInitiating Pipeline for: '{topic}'")
    print("-" * 75)

    pipeline = build_sequential_handoff_pipeline()
    final_envelope: HandoffEnvelope = pipeline.invoke(topic)

    # Step-by-step audit trace
    print("\n" + "=" * 75)
    print("A2A HANDOFF LINEAGE AUDIT TRAIL:")
    print("=" * 75)
    for idx, hop in enumerate(final_envelope.lineage, start=1):
        print(f"\nHop #{idx}: [{hop['sender']}] -> [{hop['recipient']}]")
        print(f"  Step:    {hop['step']}")
        print(f"  Summary: {hop['summary']}")

    print("\n" + "-" * 75)
    print("FINAL ENVELOPE PAYLOAD CONTENT:")
    print("-" * 75)
    print("\n[1. AGRONOMY RESEARCH]:")
    print(final_envelope.payload["agronomy_research"])

    print("\n[2. SENSORY PROFILE SPECIFICATIONS]:")
    print(final_envelope.payload["sensory_analysis"])

    print("\n[3. GUEST-FACING MENU FEATURE CARD]:")
    print(final_envelope.payload["menu_feature_card"])

    print("\n" + "=" * 75)
    print("[SUCCESS] Project 049 demonstration completed cleanly!")


if __name__ == "__main__":
    main()
