"""
===============================================================================
PROJECT 037: FASTAPI + LANGGRAPH: STATEFUL MULTI-TURN CHAT WITH WORKING MEMORY
Stage 2: Pairwise Combos | Difficulty: 4.5 / 10
===============================================================================

THE BIG QUESTION:
How do you build a production web service that maintains multi-turn conversation
continuity, extracts customer preferences into working memory, and survives
across distinct HTTP requests without leaking state across users?

ARCHITECTURE:
1. StateGraph with Thread Checkpointer (MemorySaver):
   - Stores conversation message lineage under isolated thread_ids.
2. Dual-Node Stateful Loop:
   - memory_node: Updates turn count and extracts customer profile attributes.
   - barista_node: Leverages cumulative dialogue and working memory to reply.
3. RESTful Thread Management:
   - POST /chat/{thread_id}: Sends message & continues conversation.
   - GET /chat/{thread_id}/state: Inspects current working memory and snapshot.
===============================================================================
"""

import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import json
from typing import Annotated, TypedDict, List, Optional, Dict, Any
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, BaseMessage

from config import get_llm, ACTIVE_MODEL


# =============================================================================
# 1. STATEFUL CONVERSATION SCHEMA & GRAPH DEFINITION
# =============================================================================
class ConversationState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]
    customer_name: Optional[str]
    preferences: List[str]
    turn_count: int


def memory_extractor_node(state: ConversationState) -> Dict[str, Any]:
    """Analyzes customer input to distill persistent profile attributes into working memory."""
    turn = state.get("turn_count", 0) + 1
    prefs = list(state.get("preferences", []))
    name = state.get("customer_name")

    latest_msg = state["messages"][-1].content.lower() if state["messages"] else ""

    # Simple deterministic heuristic extraction for speed & reliability
    if "my name is " in latest_msg:
        parts = latest_msg.split("my name is ")
        if parts[1]:
            candidate = parts[1].split()[0].capitalize().strip(",.!")
            name = candidate

    common_prefs = ["oat milk", "almond milk", "decaf", "cinnamon", "vanilla", "extra hot", "cold brew"]
    for p in common_prefs:
        if p in latest_msg and p not in prefs:
            prefs.append(p)

    return {
        "turn_count": turn,
        "customer_name": name,
        "preferences": prefs,
    }


def barista_agent_node(state: ConversationState) -> Dict[str, Any]:
    """Generates context-aware response using dialogue history and working memory."""
    llm = get_llm(temperature=0.2)

    cust_name = state.get("customer_name") or "friend"
    prefs = ", ".join(state.get("preferences", [])) or "no specific dietary preferences recorded"
    turn = state.get("turn_count", 1)

    system_prompt = (
        f"You are Cozy, the expert AI barista at Cozy Cafe. "
        f"Customer name: {cust_name}. Known preferences: [{prefs}]. "
        f"Conversation turn: {turn}. "
        f"Reply warmly, address the customer by name if known, reference their preferences naturally, "
        f"and answer in 2-3 friendly sentences."
    )

    full_messages = [SystemMessage(content=system_prompt)] + list(state["messages"])
    response = llm.invoke(full_messages)
    return {"messages": [response]}


# Compile Graph with in-memory checkpointer
workflow = StateGraph(ConversationState)
workflow.add_node("memory_extractor", memory_extractor_node)
workflow.add_node("barista_agent", barista_agent_node)

workflow.add_edge(START, "memory_extractor")
workflow.add_edge("memory_extractor", "barista_agent")
workflow.add_edge("barista_agent", END)

checkpointer = MemorySaver()
graph = workflow.compile(checkpointer=checkpointer)


# =============================================================================
# 2. FASTAPI APPLICATION & THREAD ENDPOINTS
# =============================================================================
app = FastAPI(title="Stateful LangGraph Chatbot Gateway", version="1.0.0")


class ChatInput(BaseModel):
    message: str = Field(..., description="Customer message")


class ChatResponse(BaseModel):
    thread_id: str
    reply: str
    working_memory: Dict[str, Any]
    total_messages: int


@app.post("/chat/{thread_id}", response_model=ChatResponse)
async def post_message_to_thread(thread_id: str, req: ChatInput):
    """
    Submits a message to an isolated conversation thread.
    Restores prior state from checkpoint, executes graph nodes, and persists new state.
    """
    config = {"configurable": {"thread_id": thread_id}}

    # Invoke graph with single human message; add_messages appends to existing history
    input_payload = {
        "messages": [HumanMessage(content=req.message)],
    }
    result = graph.invoke(input_payload, config=config)

    last_ai_msg = [m for m in result["messages"] if isinstance(m, AIMessage)][-1]

    return ChatResponse(
        thread_id=thread_id,
        reply=last_ai_msg.content.strip(),
        working_memory={
            "customer_name": result.get("customer_name"),
            "preferences": result.get("preferences", []),
            "turn_count": result.get("turn_count", 0),
        },
        total_messages=len(result["messages"]),
    )


@app.get("/chat/{thread_id}/state")
async def get_thread_state(thread_id: str):
    """Inspects the current checkpoint snapshot and working memory for a thread."""
    config = {"configurable": {"thread_id": thread_id}}
    snapshot = graph.get_state(config)

    if not snapshot or not snapshot.values:
        raise HTTPException(status_code=404, detail=f"Thread '{thread_id}' not found.")

    state_values = snapshot.values
    messages_summary = [
        {"role": "user" if isinstance(m, HumanMessage) else "assistant", "content": m.content}
        for m in state_values.get("messages", [])
    ]

    return {
        "thread_id": thread_id,
        "checkpoint_id": snapshot.config["configurable"].get("checkpoint_id"),
        "working_memory": {
            "customer_name": state_values.get("customer_name"),
            "preferences": state_values.get("preferences", []),
            "turn_count": state_values.get("turn_count", 0),
        },
        "messages": messages_summary,
    }


# =============================================================================
# 3. MAIN DEMONSTRATION RUNNER
# =============================================================================
def main():
    print("=" * 75)
    print("PROJECT 037: FASTAPI + LANGGRAPH STATEFUL CHATBOT")
    print(f"Active Groq Model: {ACTIVE_MODEL}")
    print("=" * 75)

    client = TestClient(app)
    thread_id = "customer_session_7788"

    # Turn 1: Introduce name and preference
    print("\n" + "-" * 75)
    print("TURN 1: Introducing Identity & Dietary Preferences")
    print("-" * 75)
    t1_msg = "Hello! My name is Alice, and I absolutely love oat milk lattes with cinnamon."
    print(f"Customer: '{t1_msg}'")
    t1_res = client.post(f"/chat/{thread_id}", json={"message": t1_msg})
    data1 = t1_res.json()
    print(f"Barista: {data1['reply']}")
    print(f"Working Memory Snapshot: {json.dumps(data1['working_memory'], indent=2)}")

    # Turn 2: Follow-up question relying on memory
    print("\n" + "-" * 75)
    print("TURN 2: Follow-Up Query Testing Working Memory Recall")
    print("-" * 75)
    t2_msg = "Can you recommend a warm pastry that pairs well with my usual drink?"
    print(f"Customer: '{t2_msg}'")
    t2_res = client.post(f"/chat/{thread_id}", json={"message": t2_msg})
    data2 = t2_res.json()
    print(f"Barista: {data2['reply']}")
    print(f"Working Memory Snapshot: {json.dumps(data2['working_memory'], indent=2)}")

    # Turn 3: Inspecting Thread State Snapshot via REST API
    print("\n" + "-" * 75)
    print(f"INSPECTING THREAD STATE: GET /chat/{thread_id}/state")
    print("-" * 75)
    state_res = client.get(f"/chat/{thread_id}/state")
    print(json.dumps(state_res.json(), indent=2))

    print("\n" + "=" * 75)
    print("[SUCCESS] Project 037 demonstration completed cleanly!")


if __name__ == "__main__":
    main()
