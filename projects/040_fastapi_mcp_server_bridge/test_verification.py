"""
Test verification suite for Project 040: FastAPI + MCP Server Protocol Bridge
"""

import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import json
from main import cafe_api, FastAPIToMCPBridge, ORDERS_DB


def test_mcp_tools_list():
    bridge = FastAPIToMCPBridge(cafe_api)
    rpc = {"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}}
    res = bridge.handle_jsonrpc(rpc)

    assert res["jsonrpc"] == "2.0"
    assert res["id"] == 1
    tools = res["result"]["tools"]
    tool_names = [t["name"] for t in tools]
    assert "get_menu" in tool_names
    assert "create_order" in tool_names
    assert "get_order_status" in tool_names


def test_mcp_get_menu_call():
    bridge = FastAPIToMCPBridge(cafe_api)
    rpc = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/call",
        "params": {"name": "get_menu", "arguments": {}},
    }
    res = bridge.handle_jsonrpc(rpc)
    assert res["result"]["isError"] is False
    content = json.loads(res["result"]["content"][0]["text"])
    assert "menu" in content
    assert len(content["menu"]) > 0


def test_mcp_create_and_fetch_order():
    bridge = FastAPIToMCPBridge(cafe_api)

    # 1. Create Order
    create_rpc = {
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {
            "name": "create_order",
            "arguments": {
                "customer_name": "Test Tester",
                "items": ["Matcha Latte"],
                "special_notes": "Extra cold",
            },
        },
    }
    create_res = bridge.handle_jsonrpc(create_rpc)
    assert create_res["result"]["isError"] is False
    created_data = json.loads(create_res["result"]["content"][0]["text"])
    order_id = created_data["order_id"]
    assert order_id in ORDERS_DB

    # 2. Query Order Status with Path Substitution
    status_rpc = {
        "jsonrpc": "2.0",
        "id": 4,
        "method": "tools/call",
        "params": {
            "name": "get_order_status",
            "arguments": {"order_id": order_id},
        },
    }
    status_res = bridge.handle_jsonrpc(status_rpc)
    assert status_res["result"]["isError"] is False
    status_data = json.loads(status_res["result"]["content"][0]["text"])
    assert status_data["customer_name"] == "Test Tester"
    assert status_data["status"] == "QUEUED_AT_ESPRESSO_BAR"


def test_mcp_unknown_tool_error():
    bridge = FastAPIToMCPBridge(cafe_api)
    rpc = {
        "jsonrpc": "2.0",
        "id": 5,
        "method": "tools/call",
        "params": {"name": "non_existent_tool", "arguments": {}},
    }
    res = bridge.handle_jsonrpc(rpc)
    assert "error" in res
    assert res["error"]["code"] == -32601


def test_mcp_http_404_error_handling():
    bridge = FastAPIToMCPBridge(cafe_api)
    rpc = {
        "jsonrpc": "2.0",
        "id": 6,
        "method": "tools/call",
        "params": {"name": "get_order_status", "arguments": {"order_id": "ORD-NONEXISTENT"}},
    }
    res = bridge.handle_jsonrpc(rpc)
    assert res["result"]["isError"] is True


if __name__ == "__main__":
    test_mcp_tools_list()
    test_mcp_get_menu_call()
    test_mcp_create_and_fetch_order()
    test_mcp_unknown_tool_error()
    test_mcp_http_404_error_handling()
    print("Project 040: All verification tests PASSED successfully!")
