"""
FastAPI Backend Application for the Amex Travel Concierge & Disruption Orchestrator.
Exposes REST endpoints, LangGraph streaming, state inspection, HITL interrupts & resumes,
and serves the Amex mobile app UI.
"""

import os
import sys
from typing import Dict, Any, Optional, List
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from langgraph.types import Command

# Ensure path contains package root
APP_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(APP_DIR)
ROOT_DIR = os.path.dirname(PROJECT_DIR)
if PROJECT_DIR not in sys.path:
    sys.path.insert(0, PROJECT_DIR)
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from app.graph.workflow import TRAVEL_GRAPH
from app.graph.state import TravelState
from app.data.default_state import get_fresh_itinerary, get_fresh_user_profile
from app.graph.concierge_chat import chat_with_concierge

app = FastAPI(
    title="American Express Travel Disruption Concierge - LangGraph Pro",
    description="Multi-modal travel tracking & disruption management with LangGraph, Groq, and Amex Mobile App UI",
    version="2.0.0"
)

# Mount static files and templates
STATIC_DIR = os.path.join(APP_DIR, "static")
TEMPLATES_DIR = os.path.join(APP_DIR, "templates")

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

# In-Memory Session Storage
ACTIVE_THREAD_ID = "alex_vance_trip_2026"
SESSION_STORE: Dict[str, Any] = {
    "current_state": {
        "user_id": "usr_amex_centurion_84001",
        "user_profile": get_fresh_user_profile(),
        "itinerary": get_fresh_itinerary(),
        "disruption": None,
        "impact_assessment": [],
        "total_financial_exposure": 0.0,
        "critical_impact_count": 0,
        "policy_benefits": [],
        "options": [],
        "selected_option_id": None,
        "hitl_decision": None,
        "hitl_interrupted": False,
        "rebooking_receipts": [],
        "notifications": [],
        "audit_trail": [
            {
                "timestamp": "Initial",
                "node": "system_bootstrap",
                "action": "ITINERARY_ACTIVE",
                "details": "Itinerary initialized: Flight AA-1420 (JFK->LAX), Blacklane Cab, The Beverly Hills Hotel, Centurion Lounge JFK, Nobu Malibu."
            }
        ],
        "messages": [],
        "workflow_status": "IDLE",
        "active_node": "idle",
        "completion_summary": None
    },
    "chat_history": [
        {
            "role": "assistant",
            "content": "Good day, Mr. Vance. I am your American Express Centurion Travel Concierge. All 5 legs of your journey to Los Angeles are currently tracked and synchronized. Please let me know if you require any assistance.",
            "timestamp": "Just now"
        }
    ]
}


# ==============================================================================
# PYDANTIC REQUEST SCHEMAS
# ==============================================================================
class SimulateDisruptionRequest(BaseModel):
    flight_number: str = "AA-1420"
    reason: str = "Severe convective storm cluster & FAA ground stop at New York JFK"
    event_type: str = "FLIGHT_CANCELLATION"


class ResumeDecisionRequest(BaseModel):
    selected_option_id: str = "opt_express"
    user_notes: Optional[str] = "Approved via Amex Mobile App"


class ConciergeChatRequest(BaseModel):
    message: str


def make_serializable(data: Any) -> Any:
    """Recursively converts non-serializable objects (like LangChain AIMessage) into clean JSON dicts."""
    if isinstance(data, dict):
        return {k: make_serializable(v) for k, v in data.items()}
    elif isinstance(data, (list, tuple)):
        return [make_serializable(v) for v in data]
    elif hasattr(data, "content"):
        role = "assistant" if getattr(data, "type", "") == "ai" or data.__class__.__name__ == "AIMessage" else "user"
        return {"role": role, "content": str(data.content)}
    elif hasattr(data, "model_dump"):
        return data.model_dump()
    elif hasattr(data, "dict"):
        return data.dict()
    return data


# ==============================================================================
# UI ROUTE
# ==============================================================================
@app.get("/", response_class=HTMLResponse)
async def serve_ui(request: Request):
    """Serves the Amex Mobile Application UI."""
    return templates.TemplateResponse(request=request, name="index.html", context={"state": SESSION_STORE["current_state"]})


# ==============================================================================
# API ROUTES: STATE & INSPECTION
# ==============================================================================
@app.get("/api/state")
async def get_state():
    """Returns the current itinerary, profile, disruption, options, and graph status."""
    return JSONResponse(content=SESSION_STORE["current_state"])


@app.get("/api/graph/spec")
async def get_graph_specification():
    """
    Returns the Mermaid flowchart definition and metadata for dynamic visual graph rendering.
    """
    mermaid_diagram = """flowchart TD
    START((Start / Telemetry Ingestion)) --> IN[1. Itinerary Monitor Node]
    IN -->|Flight Disrupted: CANCELLED/DELAYED| DIA[2. Downstream Impact Node]
    IN -->|Normal Operations| END_NODE((End))
    DIA --> POL[3. Amex Policy & Benefits Node]
    POL --> OPT[4. Multi-Modal Option Generator Node]
    OPT --> HITL{{5. Human-In-The-Loop Interrupt Node}}
    HITL -.->|User Approves Option 1, 2, or 3| REB[6. Rebooking Orchestrator Node]
    REB --> NOTIF[7. Amex Notification Synthesizer]
    NOTIF --> AUD[8. Audit & Telemetry Node]
    AUD --> END_NODE((Resolved & Synchronized))

    classDef active fill:#0070d1,stroke:#ffffff,stroke-width:2px,color:#ffffff;
    classDef paused fill:#d97706,stroke:#ffffff,stroke-width:2px,color:#ffffff;
    classDef completed fill:#10b981,stroke:#ffffff,stroke-width:2px,color:#ffffff;
    classDef nodeDefault fill:#002663,stroke:#3b82f6,stroke-width:1px,color:#ffffff;
    class IN,DIA,POL,OPT,REB,NOTIF,AUD nodeDefault;
    """

    nodes = [
        {"id": "itinerary_monitor_node", "name": "1. Itinerary Monitor", "role": "Flight Telemetry & Status Ingestion", "tier": "Monitor"},
        {"id": "downstream_impact_node", "name": "2. Downstream Impact", "role": "Calculates Ripple Effect on Cab, Hotel, Lounge, Dining", "tier": "Reasoning"},
        {"id": "amex_policy_node", "name": "3. Amex Policy Engine", "role": "Centurion / Platinum Protections & Waivers", "tier": "Policy"},
        {"id": "option_generator_node", "name": "4. Option Generator", "role": "Synthesizes 3 Multi-Modal Recovery Packages", "tier": "Planner"},
        {"id": "human_in_the_loop_node", "name": "5. Human-in-the-Loop", "role": "Native interrupt() Breakpoint for Cardmember Review", "tier": "Breakpoint"},
        {"id": "rebooking_orchestrator_node", "name": "6. Rebooking Orchestrator", "role": "Atomic Multi-API Execution (GDS, Blacklane, FHR, Resy)", "tier": "Execution"},
        {"id": "notification_synthesizer_node", "name": "7. Notification Synthesizer", "role": "Amex Push Notifications, Boarding Pass & Wallet Sync", "tier": "Output"},
        {"id": "audit_telemetry_node", "name": "8. Audit & Telemetry", "role": "Loss Avoidance Analytics & Final State Checkpoint", "tier": "Audit"}
    ]

    return {
        "mermaid": mermaid_diagram,
        "nodes": nodes,
        "active_node": SESSION_STORE["current_state"].get("active_node", "idle"),
        "workflow_status": SESSION_STORE["current_state"].get("workflow_status", "IDLE")
    }


# ==============================================================================
# API ROUTES: LANGGRAPH DISRUPTION PIPELINE (HITL STEP 1 & 2)
# ==============================================================================
@app.post("/api/disruption/simulate")
async def simulate_disruption(payload: SimulateDisruptionRequest):
    """
    STEP 1: Triggers flight disruption, runs the LangGraph workflow through
    Nodes 1-4, and PAUSES at Node 5 (human_in_the_loop_node) using native interrupt().
    """
    config = {"configurable": {"thread_id": ACTIVE_THREAD_ID}}

    current_state = SESSION_STORE["current_state"]
    # Prepare initial state for the graph run
    initial_input = {
        "user_id": current_state["user_id"],
        "user_profile": current_state["user_profile"],
        "itinerary": current_state["itinerary"],
        "disruption": {
            "flight_number": payload.flight_number,
            "reason": payload.reason,
            "event_type": payload.event_type
        },
        "workflow_status": "MONITORING"
    }

    try:
        # Run graph until it encounters interrupt() at human_in_the_loop_node
        events = []
        for event in TRAVEL_GRAPH.stream(initial_input, config=config):
            events.append(list(event.keys()))

        # Check graph state from checkpointer
        graph_snapshot = TRAVEL_GRAPH.get_state(config)
        state_values = make_serializable(dict(graph_snapshot.values))

        state_values["hitl_interrupted"] = True
        state_values["workflow_status"] = "AWAITING_USER_APPROVAL"
        state_values["active_node"] = "human_in_the_loop_node"

        # Update in-memory session
        SESSION_STORE["current_state"].update(state_values)

        # Append alert to chat
        SESSION_STORE["chat_history"].append({
            "role": "assistant",
            "content": (
                f"🚨 **Urgent Travel Disruption Notice**: Flight {payload.flight_number} has been cancelled by the airline due to {payload.reason}. "
                f"I have automatically held your Blacklane chauffeur, protected your reservation at The Beverly Hills Hotel, extended your Centurion Lounge access, "
                f"and waived your dining penalty at Nobu Malibu. Three complete recovery packages are ready for your review in the Disruption Hub."
            ),
            "timestamp": "Just now"
        })

        return JSONResponse(content={
            "success": True,
            "step": "INTERRUPT_HITL_PAUSED",
            "message": "Graph paused at Human-In-The-Loop breakpoint. Options ready for user selection.",
            "state": SESSION_STORE["current_state"],
            "interrupted_at": "human_in_the_loop_node"
        })
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/disruption/resume")
async def resume_disruption(payload: ResumeDecisionRequest):
    """
    STEP 2: Resumes the paused LangGraph workflow with the user's selected option!
    Executes Nodes 6, 7, and 8, resolving the multi-modal itinerary.
    """
    config = {"configurable": {"thread_id": ACTIVE_THREAD_ID}}

    try:
        resume_cmd = Command(
            resume={
                "selected_option_id": payload.selected_option_id,
                "user_notes": payload.user_notes,
                "action": "APPROVE"
            }
        )

        events = []
        for event in TRAVEL_GRAPH.stream(resume_cmd, config=config):
            events.append(list(event.keys()))

        # Fetch finalized state
        graph_snapshot = TRAVEL_GRAPH.get_state(config)
        state_values = make_serializable(dict(graph_snapshot.values))

        state_values["hitl_interrupted"] = False
        state_values["workflow_status"] = "RESOLVED"
        state_values["active_node"] = "audit_telemetry_node"

        SESSION_STORE["current_state"].update(state_values)

        # Notify in chat
        flight = state_values.get("itinerary", {}).get("flight", {})
        cab = state_values.get("itinerary", {}).get("cab", {})
        opt_title = payload.selected_option_id.replace("_", " ").title()

        SESSION_STORE["chat_history"].append({
            "role": "assistant",
            "content": (
                f"✅ **Itinerary Successfully Re-Synchronized ({opt_title})**: "
                f"You are confirmed on {flight.get('airline')} {flight.get('flight_number')} in {flight.get('seat')}. "
                f"Chauffeur pickup shifted to {cab.get('pickup_time')} at {cab.get('pickup_location')}. "
                f"Your hotel check-in has been extended, lounge pass refreshed, and dining synchronized with $0 cancellation penalties."
            ),
            "timestamp": "Just now"
        })

        return JSONResponse(content={
            "success": True,
            "step": "GRAPH_COMPLETED_RESOLVED",
            "message": "Itinerary successfully rebooked and synchronized across all 5 dimensions.",
            "state": SESSION_STORE["current_state"]
        })
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


# ==============================================================================
# API ROUTES: CONCIERGE CHAT & RESET
# ==============================================================================
@app.post("/api/chat")
async def chat_concierge(payload: ConciergeChatRequest):
    """
    Interactive conversation with the Amex Travel Concierge using Groq LLM.
    Has full contextual awareness of the LangGraph state.
    """
    user_msg = payload.message.strip()
    if not user_msg:
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    SESSION_STORE["chat_history"].append({
        "role": "user",
        "content": user_msg,
        "timestamp": "Just now"
    })

    reply = chat_with_concierge(
        user_message=user_msg,
        current_state=SESSION_STORE["current_state"],
        chat_history=SESSION_STORE["chat_history"]
    )

    SESSION_STORE["chat_history"].append({
        "role": "assistant",
        "content": reply,
        "timestamp": "Just now"
    })

    return {
        "reply": reply,
        "chat_history": SESSION_STORE["chat_history"]
    }


@app.get("/api/chat/history")
async def get_chat_history():
    return {"history": SESSION_STORE["chat_history"]}


@app.post("/api/reset")
async def reset_itinerary():
    """Resets the entire itinerary back to initial pristine state."""
    SESSION_STORE["current_state"] = {
        "user_id": "usr_amex_centurion_84001",
        "user_profile": get_fresh_user_profile(),
        "itinerary": get_fresh_itinerary(),
        "disruption": None,
        "impact_assessment": [],
        "total_financial_exposure": 0.0,
        "critical_impact_count": 0,
        "policy_benefits": [],
        "options": [],
        "selected_option_id": None,
        "hitl_decision": None,
        "hitl_interrupted": False,
        "rebooking_receipts": [],
        "notifications": [],
        "audit_trail": [
            {
                "timestamp": "Just now",
                "node": "system_bootstrap",
                "action": "ITINERARY_RESET",
                "details": "Itinerary restored to pristine state: Flight AA-1420 scheduled on time."
            }
        ],
        "messages": [],
        "workflow_status": "IDLE",
        "active_node": "idle",
        "completion_summary": None
    }
    SESSION_STORE["chat_history"] = [
        {
            "role": "assistant",
            "content": "Itinerary has been reset. All 5 services (Flight, Cab, Hotel, Lounge, Dinner) are in pristine, on-time status.",
            "timestamp": "Just now"
        }
    ]
    return {"success": True, "state": SESSION_STORE["current_state"]}


@app.get("/api/audit")
async def get_audit_trail():
    """Returns the full LangGraph audit trail and telemetry events."""
    return {
        "audit_trail": SESSION_STORE["current_state"].get("audit_trail", []),
        "workflow_status": SESSION_STORE["current_state"].get("workflow_status"),
        "completion_summary": SESSION_STORE["current_state"].get("completion_summary")
    }
