"""
===============================================================================
PROJECT 008: CHECKPOINTS, MEMORYSAVER & STATE PERSISTENCE
Stage 1: Pure Fundamentals | Difficulty: 3.0 / 10 (Intermediate)
===============================================================================

Core Concepts Demonstrated:
1. Checkpointing: Storing graph execution snapshots after every node execution.
2. MemorySaver: LangGraph's in-memory checkpoint engine.
3. Thread IDs: Providing isolated execution contexts (`configurable: {"thread_id": "..."}`).
4. Multi-turn State Continuity: Conversational state preserved without manual re-injection.
5. Thread Isolation: Demonstrating that independent threads never leak state into one another.
6. State Inspection: Retrieving live state and historical checkpoints via `get_state()` and `get_state_history()`.
===============================================================================
"""

import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from typing import TypedDict, Annotated, List
import operator
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from config import get_llm, ACTIVE_MODEL


# =============================================================================
# 1. STATE DEFINITION
# =============================================================================
class PersistentAssistantState(TypedDict):
    """
    Graph state that automatically tracks conversation messages and notes across turns.
    `add_messages` reducer appends new messages and updates existing ones by message ID.
    `operator.add` reducer accumulates audit notes.
    """
    messages: Annotated[List[BaseMessage], add_messages]
    session_notes: Annotated[List[str], operator.add]


# =============================================================================
# 2. NODES
# =============================================================================
def assistant_node(state: PersistentAssistantState) -> dict:
    """Invokes the LLM with the full conversation history stored in the checkpoint."""
    llm = get_llm(temperature=0.0)

    # Prefix system instructions
    system_prompt = SystemMessage(
        content=(
            "You are a helpful, precise executive assistant. Answer the user's questions "
            "based strictly on your prior conversation in this thread. If information was not "
            "provided in this conversation, state that you do not know."
        )
    )

    all_messages = [system_prompt] + list(state["messages"])
    response = llm.invoke(all_messages)

    turn_count = len([m for m in state["messages"] if isinstance(m, HumanMessage)])
    return {
        "messages": [response],
        "session_notes": [f"Turn {turn_count}: Assistant generated reply ({len(response.content)} chars)"],
    }


# =============================================================================
# 3. GRAPH COMPILATION WITH CHECKPOINTER
# =============================================================================
def build_persistent_graph(checkpointer: MemorySaver = None):
    """
    Builds and compiles the assistant graph.
    If checkpointer is provided, state will be snapshotted after every node.
    """
    if checkpointer is None:
        checkpointer = MemorySaver()

    builder = StateGraph(PersistentAssistantState)

    builder.add_node("assistant", assistant_node)
    builder.add_edge(START, "assistant")
    builder.add_edge("assistant", END)

    # Compile with checkpointer enables thread persistence!
    return builder.compile(checkpointer=checkpointer)


# =============================================================================
# 4. RUN DEMONSTRATION: MULTI-TURN & THREAD ISOLATION
# =============================================================================
def main():
    print("*" * 70)
    print("PROJECT 008: CHECKPOINTS, MEMORYSAVER & STATE PERSISTENCE")
    print(f"Active Groq Model: {ACTIVE_MODEL}")
    print("*" * 70)

    # 1. Initialize MemorySaver and compile graph
    memory = MemorySaver()
    graph = build_persistent_graph(checkpointer=memory)

    # -------------------------------------------------------------------------
    # DEMO PART 1: Multi-Turn Continuity in Thread 1 (Alice)
    # -------------------------------------------------------------------------
    alice_config = {"configurable": {"thread_id": "thread_alice_101"}}
    print("\n" + "=" * 70)
    print("SCENARIO 1: Alice's Thread (thread_id='thread_alice_101')")
    print("=" * 70)

    # Turn 1: Alice introduces herself and shares a secret codename
    print("\n[Alice - Turn 1] User: 'Hello! My name is Alice, and my secret project codename is PROJECT-NEBULA.'")
    res1 = graph.invoke(
        {
            "messages": [HumanMessage(content="Hello! My name is Alice, and my secret project codename is PROJECT-NEBULA.")],
            "session_notes": ["Thread initiated by Alice"],
        },
        config=alice_config,
    )
    print(f"[Assistant Reply]:\n{res1['messages'][-1].content}")

    # Turn 2: Alice asks the assistant to recall her information (NO manual history passed!)
    print("\n[Alice - Turn 2] User: 'Can you recall my name and what my secret project codename is?'")
    res2 = graph.invoke(
        {
            "messages": [HumanMessage(content="Can you recall my name and what my secret project codename is?")],
            "session_notes": [],
        },
        config=alice_config,
    )
    print(f"[Assistant Reply]:\n{res2['messages'][-1].content}")

    # -------------------------------------------------------------------------
    # DEMO PART 2: Complete Thread Isolation in Thread 2 (Bob)
    # -------------------------------------------------------------------------
    bob_config = {"configurable": {"thread_id": "thread_bob_202"}}
    print("\n" + "=" * 70)
    print("SCENARIO 2: Bob's Thread (thread_id='thread_bob_202') - Isolation Verification")
    print("=" * 70)

    # Bob asks what the secret codename is
    print("\n[Bob - Turn 1] User: 'Hello, what is my secret project codename?'")
    res_bob = graph.invoke(
        {
            "messages": [HumanMessage(content="Hello, what is my secret project codename?")],
            "session_notes": ["Thread initiated by Bob"],
        },
        config=bob_config,
    )
    print(f"[Assistant Reply]:\n{res_bob['messages'][-1].content}")

    # -------------------------------------------------------------------------
    # DEMO PART 3: Checkpoint State & History Inspection
    # -------------------------------------------------------------------------
    print("\n" + "=" * 70)
    print("SCENARIO 3: State & History Inspection via Checkpointer")
    print("=" * 70)

    # Inspect Alice's latest checkpoint state
    latest_state = graph.get_state(alice_config)
    print(f"Alice's Checkpoint Values:")
    print(f" - Total Messages in State: {len(latest_state.values['messages'])}")
    print(f" - Audit Notes: {latest_state.values['session_notes']}")
    print(f" - Next Nodes to Execute: {latest_state.next} (Empty tuple () indicates graph is at END)")

    # Inspect checkpoint history
    history = list(graph.get_state_history(alice_config))
    print(f"Total Checkpoint Snapshots in Alice's History: {len(history)}")
    for i, checkpoint in enumerate(history):
        msg_count = len(checkpoint.values.get("messages", []))
        print(f" - Snapshot [{i}] Checkpoint ID: {checkpoint.config['configurable']['checkpoint_id'][:8]}... | Messages: {msg_count}")

    print("\n[SUCCESS] Project 008 executed cleanly end-to-end!")


if __name__ == "__main__":
    main()
