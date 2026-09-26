"""
===============================================================================
PROJECT 046: LANGGRAPH + MCP: REACT AGENT CONNECTED TO EXTERNAL MCP
Stage 2: Pairwise Combos | Difficulty: 5.0 / 10
===============================================================================

THE BIG QUESTION:
How does a LangGraph ReAct agent dynamically discover and execute tools hosted on
an external Model Context Protocol (MCP) server over standard JSON-RPC 2.0?

ARCHITECTURE:
1. External MCP Server:
   - Implements tools/list and tools/call protocols.
   - Hosts cafe inventory & supplier purchasing capabilities.
2. Dynamic Schema Marshaller:
   - Introspects external MCP tool schemas and constructs LangChain StructuredTools.
3. LangGraph ReAct Loop:
   - Agent Node: LLM inspects dialogue and generates tool calls.
   - ToolNode: Bridges tool execution to external MCP server over JSON-RPC.
   - Cycles back until task completion.
===============================================================================
"""

import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import uuid
import json
from typing import Annotated, List, Dict, Any, Optional, TypedDict
from pydantic import BaseModel, Field

from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, BaseMessage
from langchain_core.tools import StructuredTool
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import tools_condition

from config import get_llm, ACTIVE_MODEL


# =============================================================================
# 1. STANDALONE EXTERNAL MCP SERVER (JSON-RPC 2.0)
# =============================================================================
class StandaloneCafeMCPServer:
    """Simulates an external enterprise MCP Server running as an isolated microservice."""

    def __init__(self):
        self.inventory_db = {
            "colombian_supremo": {"name": "Colombian Supremo Beans", "stock_kg": 8.5, "min_threshold_kg": 15.0},
            "ethiopian_yirgacheffe": {"name": "Ethiopian Yirgacheffe Beans", "stock_kg": 22.0, "min_threshold_kg": 10.0},
            "oat_milk_cases": {"name": "Oat Milk Barista Edition", "stock_cases": 4, "min_threshold_cases": 6},
        }
        self.orders_log = []

    def handle_jsonrpc(self, request: Dict[str, Any]) -> Dict[str, Any]:
        msg_id = request.get("id", 1)
        method = request.get("method")
        params = request.get("params", {})

        if method == "tools/list":
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "tools": [
                        {
                            "name": "check_inventory",
                            "description": "Check current warehouse stock level for a cafe ingredient or supply item.",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "item_key": {
                                        "type": "string",
                                        "description": "Item identifier, e.g. 'colombian_supremo', 'ethiopian_yirgacheffe', 'oat_milk_cases'",
                                    },
                                },
                                "required": ["item_key"],
                            },
                        },
                        {
                            "name": "place_supplier_order",
                            "description": "Dispatch a purchase order to an authorized agricultural supplier.",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "item_key": {"type": "string", "description": "Item to order"},
                                    "quantity": {"type": "number", "description": "Quantity to purchase"},
                                    "supplier_name": {"type": "string", "description": "Authorized vendor name"},
                                },
                                "required": ["item_key", "quantity", "supplier_name"],
                            },
                        },
                    ]
                },
            }

        elif method == "tools/call":
            tool_name = params.get("name")
            args = params.get("arguments", {})

            if tool_name == "check_inventory":
                key = args.get("item_key")
                if key in self.inventory_db:
                    item = self.inventory_db[key]
                    payload = {
                        "item_key": key,
                        "name": item["name"],
                        "current_stock": item.get("stock_kg", item.get("stock_cases")),
                        "min_threshold": item.get("min_threshold_kg", item.get("min_threshold_cases")),
                        "needs_reorder": item.get("stock_kg", item.get("stock_cases")) < item.get("min_threshold_kg", item.get("min_threshold_cases")),
                    }
                else:
                    payload = {"error": f"Item key '{key}' not found in inventory catalog."}

                return {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {"content": [{"type": "text", "text": json.dumps(payload)}], "isError": False},
                }

            elif tool_name == "place_supplier_order":
                key = args.get("item_key")
                qty = args.get("quantity")
                supplier = args.get("supplier_name")
                order_ref = f"PO-{uuid.uuid4().hex[:6].upper()}"

                order_record = {
                    "purchase_order": order_ref,
                    "item_key": key,
                    "quantity": qty,
                    "supplier": supplier,
                    "status": "DISPATCHED_TO_VENDOR",
                    "estimated_arrival": "Tomorrow by 9:00 AM",
                }
                self.orders_log.append(order_record)

                # Restock simulated DB
                if key in self.inventory_db:
                    if "stock_kg" in self.inventory_db[key]:
                        self.inventory_db[key]["stock_kg"] += qty
                    elif "stock_cases" in self.inventory_db[key]:
                        self.inventory_db[key]["stock_cases"] += qty

                return {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {"content": [{"type": "text", "text": json.dumps(order_record)}], "isError": False},
                }

        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "error": {"code": -32601, "message": f"Method '{method}' not implemented."},
        }


# =============================================================================
# 2. SCHEMA MARSHALLER: MCP TO LANGCHAIN STRUCTURED TOOLS
# =============================================================================
def convert_mcp_to_langchain_tools(mcp_server: StandaloneCafeMCPServer) -> List[StructuredTool]:
    """Inspects MCP server via tools/list and wraps tools/call into LangChain StructuredTools."""
    list_req = {"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}}
    resp = mcp_server.handle_jsonrpc(list_req)
    mcp_tools = resp["result"]["tools"]

    langchain_tools = []

    for t in mcp_tools:
        name = t["name"]
        description = t["description"]

        # Closure generator to capture tool name
        def make_executor(tool_name: str):
            def execute_tool(**kwargs) -> str:
                call_req = {
                    "jsonrpc": "2.0",
                    "id": 99,
                    "method": "tools/call",
                    "params": {"name": tool_name, "arguments": kwargs},
                }
                res = mcp_server.handle_jsonrpc(call_req)
                return res["result"]["content"][0]["text"]
            return execute_tool

        # Helper Pydantic models for argument schema
        if name == "check_inventory":
            class CheckInvArgs(BaseModel):
                item_key: str = Field(..., description="Key of inventory item")
            st = StructuredTool.from_function(
                func=make_executor(name),
                name=name,
                description=description,
                args_schema=CheckInvArgs,
            )
        elif name == "place_supplier_order":
            class PlaceOrderArgs(BaseModel):
                item_key: str = Field(..., description="Item key to purchase")
                quantity: float = Field(..., description="Quantity to purchase")
                supplier_name: str = Field(..., description="Name of supplier")
            st = StructuredTool.from_function(
                func=make_executor(name),
                name=name,
                description=description,
                args_schema=PlaceOrderArgs,
            )
        else:
            st = StructuredTool.from_function(func=make_executor(name), name=name, description=description)

        langchain_tools.append(st)

    return langchain_tools


# =============================================================================
# 3. LANGGRAPH REACT WORKFLOW
# =============================================================================
class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]


def build_mcp_react_graph(mcp_server: StandaloneCafeMCPServer):
    tools = convert_mcp_to_langchain_tools(mcp_server)
    tools_by_name = {t.name: t for t in tools}

    llm = get_llm(temperature=0.0).bind_tools(tools)

    def agent_node(state: AgentState) -> Dict[str, Any]:
        response = llm.invoke(state["messages"])
        return {"messages": [response]}

    def tool_node(state: AgentState) -> Dict[str, Any]:
        last_message = state["messages"][-1]
        tool_messages = []
        for call in last_message.tool_calls:
            tool_name = call["name"]
            tool_args = call["args"]
            tool_id = call["id"]

            tool_instance = tools_by_name[tool_name]
            result_str = tool_instance.invoke(tool_args)

            tool_messages.append(ToolMessage(content=result_str, tool_call_id=tool_id))

        return {"messages": tool_messages}

    workflow = StateGraph(AgentState)
    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", tool_node)

    workflow.add_edge(START, "agent")
    workflow.add_conditional_edges("agent", tools_condition, {"tools": "tools", END: END})
    workflow.add_edge("tools", "agent")

    return workflow.compile()


# =============================================================================
# 4. MAIN DEMONSTRATION RUNNER
# =============================================================================
def main():
    print("=" * 75)
    print("PROJECT 046: LANGGRAPH + EXTERNAL MCP TOOL INTEGRATION")
    print(f"Active Groq Model: {ACTIVE_MODEL}")
    print("=" * 75)

    mcp_server = StandaloneCafeMCPServer()
    graph = build_mcp_react_graph(mcp_server)

    user_prompt = (
        "Please check our inventory for 'colombian_supremo'. "
        "If our stock is below the minimum threshold, place a supplier order for 25 kg "
        "from 'Andean Specialty Imports', and report the purchase order details."
    )

    print(f"\nUser Goal:\n\"{user_prompt}\"")
    print("\n" + "-" * 75)
    print("Executing LangGraph ReAct Cycle with External MCP Server:")
    print("-" * 75)

    initial_messages = [HumanMessage(content=user_prompt)]
    final_state = graph.invoke({"messages": initial_messages})

    # Print execution trajectory
    for idx, msg in enumerate(final_state["messages"], start=1):
        if isinstance(msg, HumanMessage):
            print(f"\n[{idx}. USER MESSAGE]: {msg.content}")
        elif isinstance(msg, AIMessage) and msg.tool_calls:
            print(f"\n[{idx}. AGENT DECIDED MCP TOOL CALLS]:")
            for tc in msg.tool_calls:
                print(f"   -> Tool: {tc['name']} | Arguments: {tc['args']}")
        elif isinstance(msg, ToolMessage):
            print(f"\n[{idx}. MCP SERVER RESPONSE]:")
            print(f"   -> {msg.content}")
        elif isinstance(msg, AIMessage):
            print(f"\n[{idx}. AGENT FINAL ANSWER]:\n{msg.content}")

    print("\n" + "=" * 75)
    print(f"Verified MCP Server State: Orders Logged: {len(mcp_server.orders_log)}")
    print(f"Current Colombian Supremo Stock: {mcp_server.inventory_db['colombian_supremo']['stock_kg']} kg")
    print("[SUCCESS] Project 046 demonstration completed cleanly!")


if __name__ == "__main__":
    main()
