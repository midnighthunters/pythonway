"""
===============================================================================
LANGGRAPH MASTER SHOWCASE & INTERACTIVE APPLICATION
===============================================================================

This is the main entry point for the LangGraph Groq project.
You can:
  [1] Run Lesson 1: Basic State, Nodes, and Sequential Edges
  [2] Run Lesson 2: Conditional Routing and Branching
  [3] Run Lesson 3: ReAct Cyclical Agent with Tools
  [4] Run Lesson 4: Persistence, MemorySaver, and Thread Isolation
  [5] Run Lesson 5: Human-in-the-Loop (HITL) and Breakpoints
  [6] Run Lesson 6: Streaming Modes and Time Travel
  [7] Run Full Test Suite (Verifies all lessons end-to-end)
  [8] Launch Live Interactive Chatbot (with Tools + Memory + Groq)
  [0] Exit
===============================================================================
"""

import sys
import os

# Ensure UTF-8 output encoding
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from config import ACTIVE_MODEL, get_llm
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver


# =============================================================================
# INTERACTIVE AGENT (TOOLS + PERSISTENCE)
# =============================================================================
@tool
def calculate(expression: str) -> str:
    """Calculates mathematical expressions safely (e.g., '14 * 8 + 3')."""
    try:
        allowed = set("0123456789+-*/(). ")
        if not all(c in allowed for c in expression):
            return "Error: Invalid characters in math expression."
        return f"Result: {eval(expression, {'__builtins__': None}, {})}"
    except Exception as e:
        return f"Error: {e}"


@tool
def get_system_status() -> str:
    """Returns current system and cluster health status."""
    return (
        "System Status: All services OPERATIONAL | "
        "API Latency: 24ms | Database: Healthy | Cluster: 3 Nodes Active"
    )


def build_interactive_assistant():
    """Builds a full-featured conversational agent with tools and memory."""
    agent_tools = [calculate, get_system_status]
    llm = get_llm(temperature=0.2)
    llm_with_tools = llm.bind_tools(agent_tools)

    def call_model(state: MessagesState):
        response = llm_with_tools.invoke(state["messages"])
        return {"messages": [response]}

    builder = StateGraph(MessagesState)
    builder.add_node("agent", call_model)
    builder.add_node("tools", ToolNode(agent_tools))

    builder.add_edge(START, "agent")
    builder.add_conditional_edges("agent", tools_condition)
    builder.add_edge("tools", "agent")

    memory = MemorySaver()
    return builder.compile(checkpointer=memory)


def launch_interactive_chat():
    """Runs a live chat session in the terminal."""
    print("\n" + "=" * 70)
    print("LIVE INTERACTIVE CHATBOT (Powered by Groq + LangGraph)")
    print(f"Model: {ACTIVE_MODEL} | Memory: MemorySaver Active")
    print("Equipped Tools: [calculate, get_system_status]")
    print("Type 'exit' or 'quit' to return to menu.")
    print("=" * 70)

    graph = build_interactive_assistant()
    thread_id = "interactive-session-1"
    config = {"configurable": {"thread_id": thread_id}}

    while True:
        try:
            user_input = input("\nYou: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ("exit", "quit", "q"):
                print("Returning to main menu...")
                break

            print("\nAgent: ", end="", flush=True)

            # Stream execution
            events = graph.stream(
                {"messages": [HumanMessage(content=user_input)]},
                config=config,
                stream_mode="updates",
            )

            for event in events:
                for node_name, output in event.items():
                    if node_name == "tools":
                        for msg in output.get("messages", []):
                            print(f"\n   [Tool Executed]: {msg.content}")
                        print("Agent: ", end="", flush=True)
                    elif node_name == "agent":
                        for msg in output.get("messages", []):
                            if msg.content:
                                print(msg.content, end="", flush=True)
            print()

        except (KeyboardInterrupt, EOFError):
            print("\nExiting chat...")
            break
        except Exception as e:
            print(f"\nError: {e}")


# =============================================================================
# CLI MENU RUNNER
# =============================================================================
def run_all_tests():
    """Runs every lesson in sequence to verify complete working health."""
    print("\n" + "=" * 70)
    print("RUNNING COMPLETE LANGGRAPH VERIFICATION SUITE")
    print("=" * 70)

    lessons = [
        ("Lesson 1: State & Nodes", "01_basics_state_and_nodes.py"),
        ("Lesson 2: Conditional Routing", "02_conditional_routing.py"),
        ("Lesson 3: ReAct Agent with Tools", "03_react_agent_with_tools.py"),
        ("Lesson 4: Memory & Persistence", "04_persistence_and_memory.py"),
        ("Lesson 5: Human-in-the-Loop", "05_human_in_the_loop.py"),
        ("Lesson 6: Streaming & Time Travel", "06_streaming_and_time_travel.py"),
    ]

    for title, script in lessons:
        print(f"\n>>> Running {title} ({script})...")
        ret = os.system(f'"{sys.executable}" {script}')
        if ret != 0:
            print(f"❌ {title} FAILED with code {ret}")
            return False
        else:
            print(f"✅ {title} PASSED!")

    print("\n" + "=" * 70)
    print("🎉 ALL 6 LANGGRAPH LESSONS PASSED SUCCESSFULLY!")
    print("=" * 70)
    return True


def display_menu():
    print("\n" + "=" * 70)
    print("          LANGGRAPH COMPREHENSIVE LEARNING SUITE")
    print(f"   Provider: Groq | Active Model: {ACTIVE_MODEL}")
    print("=" * 70)
    print(" [1] Lesson 1: State, Nodes, Edges, and Reducers")
    print(" [2] Lesson 2: Conditional Edges & Dynamic Routing")
    print(" [3] Lesson 3: ReAct Cyclical Agent with Tools")
    print(" [4] Lesson 4: Persistence, MemorySaver & Threads")
    print(" [5] Lesson 5: Human-in-the-Loop (HITL) & Breakpoints")
    print(" [6] Lesson 6: Streaming Modes & Time Travel (State Replay)")
    print(" [7] Run All Lessons (Verification Test Suite)")
    print(" [8] Launch Live Interactive Chatbot")
    print(" [9] Launch LangChain Suite (Prompts, LCEL, RAG, Agents)")
    print(" [0] Exit")
    print("=" * 70)


def main():
    while True:
        display_menu()
        choice = input("Enter option (0-9): ").strip()

        if choice == "1":
            import importlib
            mod = importlib.import_module("01_basics_state_and_nodes")
            mod.main()
        elif choice == "2":
            import importlib
            mod = importlib.import_module("02_conditional_routing")
            mod.main()
        elif choice == "3":
            import importlib
            mod = importlib.import_module("03_react_agent_with_tools")
            mod.main()
        elif choice == "4":
            import importlib
            mod = importlib.import_module("04_persistence_and_memory")
            mod.main()
        elif choice == "5":
            import importlib
            mod = importlib.import_module("05_human_in_the_loop")
            mod.main()
        elif choice == "6":
            import importlib
            mod = importlib.import_module("06_streaming_and_time_travel")
            mod.main()
        elif choice == "7":
            run_all_tests()
        elif choice == "8":
            launch_interactive_chat()
        elif choice == "9":
            import importlib
            lc_mod = importlib.import_module("main_langchain")
            lc_mod.main()
        elif choice in ("0", "exit", "quit", "q"):
            print("Exiting. Happy LangGraph hacking!")
            break
        else:
            print("Invalid choice, please select between 0 and 9.")


if __name__ == "__main__":
    main()
