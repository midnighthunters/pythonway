"""
Conditional Edge Routing Logic for the Amex Travel Disruption Graph.
Enforces decision trees, policy validations, and Human-in-the-Loop branching.
"""

from typing import Literal
from app.graph.state import TravelState


def route_after_monitoring(state: TravelState) -> Literal["downstream_impact_node", "END"]:
    """
    Evaluates whether an active flight disruption requires full multi-modal crisis recovery.
    """
    flight = state.get("itinerary", {}).get("flight", {})
    if flight.get("status") in ["CANCELLED", "DELAYED"] or flight.get("is_disrupted"):
        return "downstream_impact_node"
    return "END"


def route_after_hitl(state: TravelState) -> Literal["rebooking_orchestrator_node", "audit_telemetry_node"]:
    """
    Branches based on user decision:
    - Rebooking or modification -> rebooking_orchestrator_node
    - Direct cancellation/abort -> audit_telemetry_node
    """
    selected_option = state.get("selected_option_id")
    if selected_option:
        return "rebooking_orchestrator_node"
    return "audit_telemetry_node"
