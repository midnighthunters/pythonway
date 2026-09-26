"""
Test verification suite for Project 048: LangChain + MCP Unified Tools in LCEL
"""

import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import json
from main import BaristaMCPServer, convert_mcp_to_tools, run_lcel_mcp_pipeline


def test_mcp_server_direct_calls():
    server = BaristaMCPServer()

    # List tools
    list_res = server.handle_jsonrpc({"jsonrpc": "2.0", "id": 1, "method": "tools/list"})
    tools = [t["name"] for t in list_res["result"]["tools"]]
    assert "calculate_grind_setting" in tools
    assert "get_flavor_profile" in tools

    # Call calculate_grind_setting
    call_res = server.handle_jsonrpc({
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/call",
        "params": {"name": "calculate_grind_setting", "arguments": {"brew_method": "v60", "dose_grams": 20.0}},
    })
    data = json.loads(call_res["result"]["content"][0]["text"])
    assert data["brew_method"] == "v60"
    assert data["water_grams"] == 320.0
    assert data["grinder_collar_notch"] == "5.0"


def test_tool_conversion():
    server = BaristaMCPServer()
    tools = convert_mcp_to_tools(server)
    assert len(tools) == 2
    tool_names = [t.name for t in tools]
    assert "calculate_grind_setting" in tool_names
    assert "get_flavor_profile" in tool_names


def test_lcel_pipeline_execution():
    server = BaristaMCPServer()
    query = "What grind setting and water temp should I use for French Press with 30g dose?"
    result = run_lcel_mcp_pipeline(query, server)

    assert len(result["tool_executions"]) >= 1
    executed_tools = [c["tool"] for c in result["tool_executions"]]
    assert "calculate_grind_setting" in executed_tools

    guide = result["final_guide"]
    assert isinstance(guide, str)
    assert len(guide) > 20
    # Must mention temperature or notch or french press
    assert ("french" in guide.lower() or "temp" in guide.lower() or "grind" in guide.lower() or "notch" in guide.lower())


if __name__ == "__main__":
    test_mcp_server_direct_calls()
    test_tool_conversion()
    test_lcel_pipeline_execution()
    print("Project 048: All verification tests PASSED successfully!")
