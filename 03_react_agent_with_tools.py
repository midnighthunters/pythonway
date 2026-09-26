"""
===============================================================================
LANGGRAPH CONCEPT 3: CYCLICAL GRAPHS, REACT AGENTS, AND TOOL CALLING
===============================================================================

Why Cycles in LangGraph?
-----------------------
Unlike standard DAG (Directed Acyclic Graph) workflow engines, LangGraph was
designed from the ground up to support LOOPS (cycles).
This makes it the premier framework for building ReAct (Reason + Act) agents:
  1. Agent (LLM) examines conversation history.
  2. Agent decides: "Do I need to call a tool, or do I have the final answer?"
  3. If tool needed: Call Tool -> Feed result back to Agent (LOOP BACK!).
  4. If no tool needed: Finish and reply to user (END).

Key LangGraph building blocks demonstrated:
  - `MessagesState`: Standard state containing `messages: Annotated[list, add_messages]`
  - `@tool` decorator: Transforms Python functions into LLM-callable schemas
  - `llm.bind_tools(tools)`: Informs Groq model of available function signatures
  - `ToolNode`: Prebuilt LangGraph node that automatically executes tool calls
  - `tools_condition`: Prebuilt router that checks for `tool_calls` in the last message
===============================================================================
"""

from typing import Annotated, Sequence
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from typing_extensions import TypedDict
from config import get_llm


# =============================================================================
# 1. DEFINE TOOLS
# =============================================================================
# Each tool has type hints and a clear docstring.
# The LLM reads the docstring to decide WHEN and HOW to call the tool.

@tool
def calculate_expression(expression: str) -> str:
    """
    Safely evaluates a basic mathematical expression (e.g., '120 * 45 + 18').
    Always use this tool for any arithmetic operations.
    """
    print(f"\n   [TOOL EXECUTING] calculate_expression('{expression}')")
    try:
        # Restricted eval for basic math safety
        allowed = set("0123456789+-*/(). ")
        if not all(ch in allowed for ch in expression):
            return "Error: Invalid characters in arithmetic expression."
        result = eval(expression, {"__builtins__": None}, {})
        return f"Result: {result}"
    except Exception as e:
        return f"Calculation Error: {e}"


@tool
def lookup_product_stock(item_name: str) -> str:
    """
    Looks up inventory count, price, and warehouse location for an item in the warehouse.
    Items available: 'laptop', 'monitor', 'keyboard', 'headphones'.
    """
    print(f"\n   [TOOL EXECUTING] lookup_product_stock('{item_name}')")
    catalog = {
        "laptop": {"stock": 14, "price": 999.00, "location": "Warehouse A (Seattle)"},
        "monitor": {"stock": 42, "price": 280.00, "location": "Warehouse B (Austin)"},
        "keyboard": {"stock": 85, "price": 65.00, "location": "Warehouse A (Seattle)"},
        "headphones": {"stock": 0, "price": 120.00, "location": "Out of Stock"},
    }
    clean_name = item_name.strip().lower()
    for key, data in catalog.items():
        if key in clean_name:
            return (
                f"Product: {key.capitalize()} | "
                f"In Stock: {data['stock']} units | "
                f"Unit Price: ${data['price']} | "
                f"Location: {data['location']}"
            )
    return f"Product '{item_name}' was not found in the warehouse database."


# List of tools to equip the agent with
tools = [calculate_expression, lookup_product_stock]


# =============================================================================
# 2. DEFINE STATE WITH MESSAGE REDUCER
# =============================================================================
# LangGraph provides `add_messages` which intelligently appends new messages,
# updates messages with identical IDs, and preserves full message history.
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]


# =============================================================================
# 3. DEFINE THE AGENT NODE
# =============================================================================
# Bind tools to the Groq LLM model
llm = get_llm(temperature=0.0)
llm_with_tools = llm.bind_tools(tools)


def agent_node(state: AgentState) -> dict:
    """
    The reasoning engine:
    Calls Groq LLM with the accumulated message history and bound tools.
    The LLM outputs either:
      - Normal text response (done)
      - OR tool_calls list (requesting tool execution)
    """
    print("\n[AGENT NODE] Thinking and deciding next action...")
    response = llm_with_tools.invoke(state["messages"])
    # Return update to state: append this assistant message
    return {"messages": [response]}


# =============================================================================
# 4. BUILD CYCLICAL GRAPH
# =============================================================================
def build_react_graph():
    r"""
    Graph Topology (Note the Cycle!):

            +--------------+
            |    START     |
            +-------+------+
                    |
                    v
            +-------+------+   has tool_calls?
            |  agent_node  | -----------------> [ tools_condition ]
            +-------+------+                          |
                    ^                                 | YES
                    |                                 v
                    |       loops back         +------+------+
                    +--------------------------|  ToolNode   |
                                               +-------------+
                                                      |
                                                      | NO (finished)
                                                      v
                                               +-------------+
                                               |     END     |
                                               +-------------+
    """
    builder = StateGraph(AgentState)

    # 1. Add Agent Node
    builder.add_node("agent", agent_node)

    # 2. Add Prebuilt ToolNode
    # ToolNode automatically takes tool_calls from the last AIMessage, executes them,
    # and returns ToolMessages to the state.
    builder.add_node("tools", ToolNode(tools))

    # 3. Flow starts at the Agent Node
    builder.add_edge(START, "agent")

    # 4. Add conditional edge from Agent using tools_condition:
    #    - If agent made tool calls -> route to "tools"
    #    - If agent responded with text -> route to END
    builder.add_conditional_edges("agent", tools_condition)

    # 5. CRUCIAL CYCLE: From "tools", ALWAYS route back to "agent"
    #    This allows the LLM to inspect the tool result and answer or call another tool!
    builder.add_edge("tools", "agent")

    return builder.compile()


# =============================================================================
# 5. RUN DEMONSTRATION
# =============================================================================
def main():
    print("=" * 70)
    print("LANGGRAPH LESSON 3: REACT AGENT WITH TOOLS & CYCLES")
    print("=" * 70)

    graph = build_react_graph()

    # Query requiring BOTH tools and multi-step reasoning:
    # 1. Lookup price of 3 laptops
    # 2. Multiply 3 * price using calculator
    user_query = (
        "How many laptops do we have in stock and where are they located? "
        "Also, if I buy 3 laptops, what is the exact total cost?"
    )

    print(f"\nUser Query:\n'{user_query}'\n")

    initial_input = {
        "messages": [HumanMessage(content=user_query)]
    }

    # Execute graph
    final_state = graph.invoke(initial_input)

    print("\n" + "=" * 70)
    print("COMPLETE MESSAGE CONVERSATION TRACE")
    print("=" * 70)

    for i, msg in enumerate(final_state["messages"], 1):
        msg_type = msg.__class__.__name__
        print(f"\n--- [Message {i}] Type: {msg_type} ---")
        if hasattr(msg, "tool_calls") and msg.tool_calls:
            print(f"Tool Calls Requested: {msg.tool_calls}")
        if msg.content:
            print(f"Content:\n{msg.content}")

    print("\n" + "=" * 70)
    print("FINAL AGENT ANSWER:")
    print("=" * 70)
    print(final_state["messages"][-1].content)

    png_bytes = graph.get_graph().draw_mermaid_png()

    with open("support_graph.png", "wb") as f:
        f.write(png_bytes)


if __name__ == "__main__":
    main()
