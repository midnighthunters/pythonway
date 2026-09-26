"""
LangGraph Workflow Builder & Compiler.
Assembles the multi-modal travel recovery graph with persistent MemorySaver checkpoints,
interrupt breakpoints, and state inspection capabilities.
"""

from typing import Dict, Any, Optional
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import Command

from app.graph.state import TravelState
from app.graph.nodes import (
    itinerary_monitor_node,
    downstream_impact_node,
    amex_policy_node,
    option_generator_node,
    human_in_the_loop_node,
    rebooking_orchestrator_node,
    notification_synthesizer_node,
    audit_telemetry_node
)
from app.graph.edges import route_after_monitoring, route_after_hitl


def build_travel_graph():
    """
    Constructs and compiles the advanced 8-node LangGraph for Amex Travel Concierge.
    """
    builder = StateGraph(TravelState)

    # 1. Register All Nodes
    builder.add_node("itinerary_monitor_node", itinerary_monitor_node)
    builder.add_node("downstream_impact_node", downstream_impact_node)
    builder.add_node("amex_policy_node", amex_policy_node)
    builder.add_node("option_generator_node", option_generator_node)
    builder.add_node("human_in_the_loop_node", human_in_the_loop_node)
    builder.add_node("rebooking_orchestrator_node", rebooking_orchestrator_node)
    builder.add_node("notification_synthesizer_node", notification_synthesizer_node)
    builder.add_node("audit_telemetry_node", audit_telemetry_node)

    # 2. Add Graph Control Edges
    builder.add_edge(START, "itinerary_monitor_node")

    builder.add_conditional_edges(
        "itinerary_monitor_node",
        route_after_monitoring,
        {
            "downstream_impact_node": "downstream_impact_node",
            "END": END
        }
    )

    builder.add_edge("downstream_impact_node", "amex_policy_node")
    builder.add_edge("amex_policy_node", "option_generator_node")
    builder.add_edge("option_generator_node", "human_in_the_loop_node")

    builder.add_conditional_edges(
        "human_in_the_loop_node",
        route_after_hitl,
        {
            "rebooking_orchestrator_node": "rebooking_orchestrator_node",
            "audit_telemetry_node": "audit_telemetry_node"
        }
    )

    builder.add_edge("rebooking_orchestrator_node", "notification_synthesizer_node")
    builder.add_edge("notification_synthesizer_node", "audit_telemetry_node")
    builder.add_edge("audit_telemetry_node", END)

    # 3. Persistent Checkpointer
    checkpointer = MemorySaver()

    # Compile the graph
    app = builder.compile(checkpointer=checkpointer)
    return app


# Singleton instance for the application
TRAVEL_GRAPH = build_travel_graph()
