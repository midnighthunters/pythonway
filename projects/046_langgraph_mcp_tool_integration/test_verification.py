"""
Test verification suite for Project 046: LangGraph + External MCP Tool Integration
"""

import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import json
from langchain_core.messages import HumanMessage
from main import (
    StandaloneCafeMCPServer,
    convert_mcp_to_langchain_tools,
    build_mcp_react_graph,
)


def test_mcp_server_protocol():
    server = StandaloneCafeMCPServer()

    # Test tools/list
    list_res = server.handle_jsonrpc({"jsonrpc": "2.0", "id": 1, "method": "tools/list"})
    tools = list_res["result"]["tools"]
    tool_names = [t["name"] for t in tools]
    assert "check_inventory" in tool_names
    assert "place_supplier_order" in tool_names

    # Test check_inventory call
    inv_res = server.handle_jsonrpc({
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/call",
        "params": {"name": "check_inventory", "arguments": {"item_key": "colombian_supremo"}},
    })
    inv_data = json.loads(inv_res["result"]["content"][0]["text"])
    assert inv_data["item_key"] == "colombian_supremo"
    assert inv_data["needs_reorder"] is True


def test_tool_conversion():
    server = StandaloneCafeMCPServer()
    tools = convert_mcp_to_langchain_tools(server)
    assert len(tools) == 2
    tool_names = [t.name for t in tools]
    assert "check_inventory" in tool_names
    assert "place_supplier_order" in tool_names

    check_tool = [t for t in tools if t.name == "check_inventory"][0]
    output = check_tool.invoke({"item_key": "colombian_supremo"})
    assert "colombian_supremo" in output


def test_react_graph_mcp_execution():
    server = StandaloneCafeMCPServer()
    graph = build_mcp_react_graph(server)

    user_query = (
        "Check our inventory for 'colombian_supremo'. If it needs reordering, order 20 kg from 'Andean Imports'."
    )
    result = graph.invoke({"messages": [HumanMessage(content=user_query)]})
    messages = result["messages"]

    # Graph must have executed at least 1 tool call
    tool_calls_executed = [m for m in messages if hasattr(m, "tool_calls") and m.tool_calls]
    assert len(tool_calls_executed) >= 1

    # Verify supplier order was dispatched
    assert len(server.orders_log) >= 1
    assert server.orders_log[0]["item_key"] == "colombian_supremo"

    # Final assistant message present
    last_msg = messages[-1]
    assert last_msg.content is not None
    assert len(last_msg.content) > 10


if __name__ == "__main__":
    test_mcp_server_protocol()
    test_tool_conversion()
    test_react_graph_mcp_execution()
    print("Project 046: All verification tests PASSED successfully!")
