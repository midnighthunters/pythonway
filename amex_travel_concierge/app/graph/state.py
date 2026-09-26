"""
LangGraph State Definitions for the Amex Travel Disruption & Itinerary Orchestrator.
Uses TypedDict, Annotated reducers, and structured Pydantic models for type safety.
"""

from typing import TypedDict, List, Dict, Any, Optional, Annotated
from langgraph.graph.message import add_messages


def append_audit_logs(existing: List[Dict[str, Any]], new_entries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Reducer that appends new audit telemetry events while preserving full event history."""
    if not existing:
        return list(new_entries)
    return existing + list(new_entries)


def append_notifications(existing: List[Dict[str, Any]], new_notifs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Reducer that accumulates notification cards for the Amex mobile app UI."""
    if not existing:
        return list(new_notifs)
    return existing + list(new_notifs)


class TravelState(TypedDict, total=False):
    """
    Comprehensive State Schema for the Amex Multi-Modal Travel Graph.
    Tracks user profile, active multi-modal itinerary, flight disruptions,
    cascaded impact matrix, Amex policy validations, generated recovery options,
    human-in-the-loop decisions, execution receipts, and audit telemetry.
    """
    # User Profile & Amex Membership Context
    user_id: str
    user_profile: Dict[str, Any]

    # Current Itinerary Across 5 Tracking Dimensions
    itinerary: Dict[str, Any]  # keys: 'flight', 'cab', 'hotel', 'lounge', 'dinner'

    # Disruption Trigger & Flight Status Telemetry
    disruption: Optional[Dict[str, Any]]

    # Downstream Cascaded Impact Matrix
    impact_assessment: List[Dict[str, Any]]
    total_financial_exposure: float
    critical_impact_count: int

    # Amex Centurion / Platinum Policy Engine Validations
    policy_benefits: List[Dict[str, Any]]

    # Candidate Multi-Modal Recovery Packages
    options: List[Dict[str, Any]]

    # Human-in-the-Loop Interaction State
    selected_option_id: Optional[str]
    hitl_decision: Optional[Dict[str, Any]]
    hitl_interrupted: bool

    # Execution & Rebooking Telemetry
    rebooking_receipts: List[Dict[str, Any]]

    # Notifications & UI Cards for the Amex Mobile App
    notifications: Annotated[List[Dict[str, Any]], append_notifications]

    # Live Audit & Node Execution Trace
    audit_trail: Annotated[List[Dict[str, Any]], append_audit_logs]

    # Conversational Messages for the Amex Concierge Assistant
    messages: Annotated[List[Any], add_messages]

    # Workflow Status Indicator
    workflow_status: str
    active_node: str
    completion_summary: Optional[Dict[str, Any]]
