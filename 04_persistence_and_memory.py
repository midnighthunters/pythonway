"""
===============================================================================
LANGGRAPH CONCEPT 4: PERSISTENCE, MEMORY CHECKPOINTERS, AND THREADS
===============================================================================

Why Persistence & Checkpointers?
--------------------------------
In real production applications:
  - Users talk across multiple turns (multi-turn conversation memory).
  - Conversations can pause and resume days later.
  - Thousands of distinct users interact concurrently without mixing up states.
  - You need to inspect or audit previous conversation snapshots.

How LangGraph Handles Memory:
  1. `checkpointer = MemorySaver()`: Saves a snapshot of State after every node.
     (In production, swap `MemorySaver` for `SqliteSaver` or `PostgresSaver`).
  2. `builder.compile(checkpointer=checkpointer)`: Attaches the checkpointer.
  3. `config = {"configurable": {"thread_id": "thread-123"}}`:
     The `thread_id` identifies the conversation session.
  4. LangGraph automatically fetches the last state checkpoint for that thread,
     merges your new input, runs the graph, and stores the new checkpoint!

In this lesson:
  1. Compile a conversational agent with `MemorySaver`.
  2. Multi-turn dialogue on Thread 1 (remembering name and preference).
  3. Switch to Thread 2 to verify clean session isolation.
  4. Inspect the thread's checkpoint state and revision history.
===============================================================================
"""

from typing import Annotated, Sequence
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from typing_extensions import TypedDict
from config import get_llm


# =============================================================================
# 1. STATE DEFINITION
# =============================================================================
class ChatbotState(TypedDict):
    # Using add_messages reducer so each turn appends to the conversation history
    messages: Annotated[Sequence[BaseMessage], add_messages]


# =============================================================================
# 2. CHATBOT NODE
# =============================================================================
def chatbot_node(state: ChatbotState) -> dict:
    """
    Standard conversational node:
    Receives all accumulated messages in the thread and generates a response.
    """
    llm = get_llm(temperature=0.3)
    response = llm.invoke(state["messages"])
    return {"messages": [response]}


# =============================================================================
# 3. BUILD AND COMPILE GRAPH WITH CHECKPOINTER
# =============================================================================
def build_persistent_bot():
    builder = StateGraph(ChatbotState)

    builder.add_node("chatbot", chatbot_node)
    builder.add_edge(START, "chatbot")
    builder.add_edge("chatbot", END)

    # In-memory checkpointer: records state after every step per thread_id
    memory = MemorySaver()

    # Compile with checkpointer attached!
    compiled_graph = builder.compile(checkpointer=memory)
    return compiled_graph


# =============================================================================
# 4. EXECUTION DEMO: MULTI-TURN & THREAD ISOLATION
# =============================================================================
def main():
    print("=" * 70)
    print("LANGGRAPH LESSON 4: PERSISTENCE, THREADS & CHECKPOINTERS")
    print("=" * 70)

    graph = build_persistent_bot()

    # Define two different conversation thread configurations
    thread_1_config = {"configurable": {"thread_id": "user-session-alice"}}
    thread_2_config = {"configurable": {"thread_id": "user-session-bob"}}

    # -------------------------------------------------------------------------
    # PART 1: Conversation on Thread 1 (Alice) - Turn 1
    # -------------------------------------------------------------------------
    print("\n--- [THREAD 1 - ALICE: TURN 1] ---")
    alice_msg_1 = "Hi! My name is Alice. I am an AI researcher living in Kyoto."
    print(f"Alice: {alice_msg_1}")

    output_1 = graph.invoke(
        {"messages": [HumanMessage(content=alice_msg_1)]},
        config=thread_1_config,  # Thread ID supplied here
    )
    print(f"Bot: {output_1['messages'][-1].content}\n")

    # -------------------------------------------------------------------------
    # PART 2: Conversation on Thread 1 (Alice) - Turn 2 (Testing Memory)
    # -------------------------------------------------------------------------
    print("--- [THREAD 1 - ALICE: TURN 2 - TESTING MEMORY] ---")
    # We DO NOT pass Alice's name or city again. LangGraph restores it from thread_1 checkpoint!
    alice_msg_2 = "Can you remind me where I live and what my profession is?"
    print(f"Alice: {alice_msg_2}")

    output_2 = graph.invoke(
        {"messages": [HumanMessage(content=alice_msg_2)]},
        config=thread_1_config,
    )
    print(f"Bot: {output_2['messages'][-1].content}\n")

    # -------------------------------------------------------------------------
    # PART 3: Conversation on Thread 2 (Bob) - Testing Isolation
    # -------------------------------------------------------------------------
    print("--- [THREAD 2 - BOB: TURN 1 - TESTING ISOLATION] ---")
    # Bob enters a completely separate thread_id
    bob_msg = "What is my name and where do I live?"
    print(f"Bob: {bob_msg}")

    output_3 = graph.invoke(
        {"messages": [HumanMessage(content=bob_msg)]},
        config=thread_2_config,  # Different Thread ID!
    )
    print(f"Bot: {output_3['messages'][-1].content}\n")

    # -------------------------------------------------------------------------
    # PART 4: Inspecting State and Checkpoint History
    # -------------------------------------------------------------------------
    print("=" * 70)
    print("INSPECTING STATE CHECKPOINTS FOR THREAD 1 (ALICE)")
    print("=" * 70)

    # 1. Fetch current snapshot of Thread 1
    current_state = graph.get_state(thread_1_config)
    print(f"\nTotal messages stored in Thread 1 checkpoint: {len(current_state.values['messages'])}")
    print(f"Current Next Node to run: {current_state.next}")  # Empty tuple () means at END

    # 2. View checkpointer history (snapshots over time)
    print("\nCheckpoint History (Chronological steps saved in memory):")
    history = list(graph.get_state_history(thread_1_config))
    for idx, snapshot in enumerate(history, 1):
        step_name = snapshot.metadata.get("step", "N/A")
        print(f"  [{idx}] Checkpoint ID: {snapshot.config['configurable']['checkpoint_id']} | Step: {step_name}")

    png_bytes = graph.get_graph().draw_mermaid_png()

    with open("support_graph.png", "wb") as f:
        f.write(png_bytes)

if __name__ == "__main__":
    main()
