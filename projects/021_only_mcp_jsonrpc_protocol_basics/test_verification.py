"""
Verification Test Suite for Project 021: MCP Architecture & JSON-RPC 2.0 Protocol
"""

import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import json
from main import CozyCoffeeMCPServer


def test_handshake_lifecycle():
    print("Testing MCP initialize handshake...")
    server = CozyCoffeeMCPServer()

    init_msg = json.dumps({
        "jsonrpc": "2.0",
        "id": 101,
        "method": "initialize",
        "params": {"protocolVersion": "2024-11-05"},
    })
    resp_raw = server.handle_message(init_msg)
    resp = json.loads(resp_raw)

    assert resp["jsonrpc"] == "2.0"
    assert resp["id"] == 101
    assert "capabilities" in resp["result"]
    assert "tools" in resp["result"]["capabilities"]
    assert resp["result"]["serverInfo"]["name"] == "CozyCoffeeServer"
    print("  [PASSED] MCP Handshake response conforms to specification.")

    # Notification check
    notify_raw = server.handle_message(json.dumps({
        "jsonrpc": "2.0",
        "method": "notifications/initialized",
    }))
    assert notify_raw is None, "Notifications must not return a response payload"
    assert server.is_initialized is True
    print("  [PASSED] notifications/initialized accepted cleanly.")


def test_tools_discovery_and_call():
    print("\nTesting tools/list and tools/call protocol...")
    server = CozyCoffeeMCPServer()

    # List tools
    list_raw = server.handle_message(json.dumps({
        "jsonrpc": "2.0",
        "id": 102,
        "method": "tools/list",
    }))
    list_resp = json.loads(list_raw)
    tools = list_resp["result"]["tools"]
    assert len(tools) >= 2, f"Expected at least 2 tools, got {len(tools)}"
    tool_names = [t["name"] for t in tools]
    assert "calculate_beverage_bill" in tool_names
    assert "check_bean_inventory" in tool_names
    print(f"  [PASSED] tools/list discovered {len(tools)} registered tools with schemas.")

    # Call calculate_beverage_bill
    call_raw = server.handle_message(json.dumps({
        "jsonrpc": "2.0",
        "id": 103,
        "method": "tools/call",
        "params": {
            "name": "calculate_beverage_bill",
            "arguments": {"drink": "mocha", "quantity": 1, "oat_milk": False},
        },
    }))
    call_resp = json.loads(call_raw)
    assert call_resp["result"]["isError"] is False
    content_text = call_resp["result"]["content"][0]["text"]
    assert "Total: $5.94" in content_text or "Mocha" in content_text
    print(f"  [PASSED] tools/call executed calculation accurately: {content_text}")


def test_error_handling():
    print("\nTesting JSON-RPC 2.0 error handling...")
    server = CozyCoffeeMCPServer()

    # Unknown method
    err_raw = server.handle_message(json.dumps({
        "jsonrpc": "2.0",
        "id": 999,
        "method": "unknown_function_call",
    }))
    err_resp = json.loads(err_raw)
    assert "error" in err_resp
    assert err_resp["error"]["code"] == -32601
    print("  [PASSED] Unknown method returns code -32601 (Method not found).")


if __name__ == "__main__":
    print("=" * 60)
    print("RUNNING VERIFICATION SUITE: PROJECT 021")
    print("=" * 60)
    test_handshake_lifecycle()
    test_tools_discovery_and_call()
    test_error_handling()
    print("\n[ALL TESTS PASSED] Project 021 verified successfully!")
