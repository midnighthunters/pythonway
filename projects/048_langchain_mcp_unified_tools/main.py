"""
===============================================================================
PROJECT 048: LANGCHAIN + MCP: DYNAMICALLY PIPING MCP TOOLS INTO LCEL
Stage 2: Pairwise Combos | Difficulty: 4.5 / 10
===============================================================================

THE BIG QUESTION:
How do developers combine LangChain Expression Language (LCEL) composability
with external Model Context Protocol (MCP) servers without writing boilerplate
tool adapters for every endpoint?

ARCHITECTURE:
1. External MCP Tool Server:
   - Exposes specialized brewing calculation & sensory flavor tools via JSON-RPC.
2. Dynamic Protocol Converter:
   - Fetches JSON Schemas from tools/list and binds them directly to ChatGroq
     via `llm.bind_tools()`.
3. LCEL Execution Pipeline:
   - Generates tool calls, dispatches JSON-RPC execution to MCP server, and
     synthesizes a cohesive final answer.
===============================================================================
"""

import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import json
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, SystemMessage
from langchain_core.tools import StructuredTool

from config import get_llm, ACTIVE_MODEL


# =============================================================================
# 1. EXTERNAL COFFEE MCP SERVER (JSON-RPC 2.0)
# =============================================================================
class BaristaMCPServer:
    """External MCP Server exposing specialized brewing calculation tools."""

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
                            "name": "calculate_grind_setting",
                            "description": "Calculates optimal burr grind setting (microns & collar notch) and water temp for a brew method.",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "brew_method": {
                                        "type": "string",
                                        "description": "Brew method (e.g. 'aeropress', 'v60', 'french_press', 'espresso')",
                                    },
                                    "dose_grams": {"type": "number", "description": "Coffee grounds dose in grams"},
                                },
                                "required": ["brew_method", "dose_grams"],
                            },
                        },
                        {
                            "name": "get_flavor_profile",
                            "description": "Retrieves official cupping notes, processing style, and acidity characteristics for a bean origin.",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "bean_origin": {"type": "string", "description": "Country or region (e.g. 'kenya', 'ethiopia', 'colombia')"},
                                },
                                "required": ["bean_origin"],
                            },
                        },
                    ]
                },
            }

        elif method == "tools/call":
            tool_name = params.get("name")
            args = params.get("arguments", {})

            if tool_name == "calculate_grind_setting":
                method_name = args.get("brew_method", "").lower()
                dose = args.get("dose_grams", 15.0)

                profiles = {
                    "aeropress": {"grind_microns": 550, "collar_notch": "3.5", "temp_f": 195, "ratio": "1:14"},
                    "v60": {"grind_microns": 700, "collar_notch": "5.0", "temp_f": 202, "ratio": "1:16"},
                    "french_press": {"grind_microns": 950, "collar_notch": "7.5", "temp_f": 205, "ratio": "1:15"},
                    "espresso": {"grind_microns": 250, "collar_notch": "1.2", "temp_f": 200, "ratio": "1:2"},
                }
                prof = profiles.get(method_name, {"grind_microns": 650, "collar_notch": "4.5", "temp_f": 200, "ratio": "1:15"})
                water_g = round(dose * float(prof["ratio"].split(":")[1]), 1)

                output = {
                    "brew_method": method_name,
                    "dose_grams": dose,
                    "grind_size_microns": prof["grind_microns"],
                    "grinder_collar_notch": prof["collar_notch"],
                    "water_temp_fahrenheit": prof["temp_f"],
                    "brew_ratio": prof["ratio"],
                    "water_grams": water_g,
                }
                return {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {"content": [{"type": "text", "text": json.dumps(output)}], "isError": False},
                }

            elif tool_name == "get_flavor_profile":
                origin = args.get("bean_origin", "").lower()
                origins = {
                    "kenya": {"notes": ["blackcurrant", "grapefruit", "cane sugar"], "process": "Double-Washed", "acidity": "Bright phosphoric"},
                    "ethiopia": {"notes": ["jasmine", "bergamot", "wild blueberry"], "process": "Natural Heirloom", "acidity": "Vibrant citric"},
                    "colombia": {"notes": ["caramel", "red apple", "milk chocolate"], "process": "Washed Castillo", "acidity": "Balanced malic"},
                }
                info = origins.get(origin, {"notes": ["sweet cocoa", "roasted nuts"], "process": "Traditional Washed", "acidity": "Mellow"})
                output = {"origin": origin, "cupping_notes": info["notes"], "processing": info["process"], "acidity": info["acidity"]}
                return {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {"content": [{"type": "text", "text": json.dumps(output)}], "isError": False},
                }

        return {"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": "Tool not found."}}


# =============================================================================
# 2. DYNAMIC PROTOCOL CONVERTER (MCP -> LANGCHAIN STRUCTURED TOOLS)
# =============================================================================
def convert_mcp_to_tools(mcp_server: BaristaMCPServer) -> List[StructuredTool]:
    """Dynamically converts MCP server tool declarations into LangChain StructuredTools."""
    list_rpc = {"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}}
    res = mcp_server.handle_jsonrpc(list_rpc)
    tools_list = res["result"]["tools"]

    langchain_tools = []
    for t in tools_list:
        name = t["name"]
        desc = t["description"]

        def make_caller(t_name: str):
            def caller(**kwargs) -> str:
                call_rpc = {
                    "jsonrpc": "2.0",
                    "id": 42,
                    "method": "tools/call",
                    "params": {"name": t_name, "arguments": kwargs},
                }
                resp = mcp_server.handle_jsonrpc(call_rpc)
                return resp["result"]["content"][0]["text"]
            return caller

        if name == "calculate_grind_setting":
            class GrindArgs(BaseModel):
                brew_method: str = Field(..., description="Brewing equipment (aeropress, v60, etc.)")
                dose_grams: float = Field(..., description="Dose in grams")
            st = StructuredTool.from_function(func=make_caller(name), name=name, description=desc, args_schema=GrindArgs)
        elif name == "get_flavor_profile":
            class FlavorArgs(BaseModel):
                bean_origin: str = Field(..., description="Country or region of origin")
            st = StructuredTool.from_function(func=make_caller(name), name=name, description=desc, args_schema=FlavorArgs)
        else:
            st = StructuredTool.from_function(func=make_caller(name), name=name, description=desc)

        langchain_tools.append(st)

    return langchain_tools


# =============================================================================
# 3. LCEL COMPOSABLE EXECUTION PIPELINE
# =============================================================================
def run_lcel_mcp_pipeline(query: str, mcp_server: BaristaMCPServer) -> Dict[str, Any]:
    """Pipes dynamically bound MCP tools through a LangChain LCEL pipeline."""
    tools = convert_mcp_to_tools(mcp_server)
    tools_by_name = {t.name: t for t in tools}

    llm = get_llm(temperature=0.0)
    llm_with_tools = llm.bind_tools(tools)

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "You are Cozy Cafe's AI Barista Master. "
            "Use the provided tools to fetch exact grinding parameters and flavor profiles. "
            "Always synthesize tool outputs into a clear, enthusiastic guide.",
        ),
        ("human", "{query}"),
    ])

    chain = prompt | llm_with_tools
    ai_response = chain.invoke({"query": query})

    tool_executions = []
    tool_messages = []

    if ai_response.tool_calls:
        for call in ai_response.tool_calls:
            t_name = call["name"]
            t_args = call["args"]
            t_id = call["id"]

            tool_obj = tools_by_name[t_name]
            raw_result = tool_obj.invoke(t_args)

            tool_executions.append({"tool": t_name, "args": t_args, "result": json.loads(raw_result)})
            tool_messages.append(ToolMessage(content=raw_result, tool_call_id=t_id))

        # Final synthesis step
        synthesis_messages = [
            SystemMessage(content="You are Cozy Cafe's AI Barista Master."),
            HumanMessage(content=query),
            ai_response,
        ] + tool_messages

        final_res = llm.invoke(synthesis_messages)
        final_text = final_res.content.strip()
    else:
        final_text = ai_response.content.strip()

    return {
        "query": query,
        "tools_discovered_from_mcp": [t.name for t in tools],
        "tool_executions": tool_executions,
        "final_guide": final_text,
    }


# =============================================================================
# 4. MAIN DEMONSTRATION RUNNER
# =============================================================================
def main():
    print("=" * 75)
    print("PROJECT 048: LANGCHAIN + MCP UNIFIED TOOLS IN LCEL")
    print(f"Active Groq Model: {ACTIVE_MODEL}")
    print("=" * 75)

    mcp_server = BaristaMCPServer()

    query = (
        "I'm brewing an AeroPress cup using 16.5 grams of Kenyan specialty beans. "
        "What exact grind collar setting and water temperature should I use, "
        "and what tasting notes can I expect in the cup?"
    )

    print(f"\nUser Query:\n\"{query}\"")
    print("\n" + "-" * 75)
    print("Executing LCEL Pipeline with Dynamically Discovered MCP Tools:")
    print("-" * 75)

    result = run_lcel_mcp_pipeline(query, mcp_server)

    print(f"Discovered MCP Tools: {result['tools_discovered_from_mcp']}")
    print(f"\nExecuted Tool Calls ({len(result['tool_executions'])}):")
    for call in result["tool_executions"]:
        print(f"\n-> Tool: {call['tool']}")
        print(f"   Input Arguments:  {call['args']}")
        print(f"   MCP Server Return: {json.dumps(call['result'], indent=2)}")

    print("\n" + "-" * 75)
    print("FINAL SYNTHESIZED BREWING GUIDE (From LCEL Chain):")
    print("-" * 75)
    print(result["final_guide"])

    print("\n" + "=" * 75)
    print("[SUCCESS] Project 048 demonstration completed cleanly!")


if __name__ == "__main__":
    main()
