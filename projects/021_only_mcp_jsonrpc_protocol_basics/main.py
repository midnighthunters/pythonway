"""
===============================================================================
PROJECT 021: MCP ARCHITECTURE: JSON-RPC 2.0 & HANDSHAKE PROTOCOL
Stage 1: Pure Fundamentals | Difficulty: 2.5 / 10 (Beginner Friendly)
===============================================================================

THE BIG QUESTION:
What is the Model Context Protocol (MCP), and how does it work under the hood?

Think of MCP as "USB-C for Artificial Intelligence":
Before USB-C, every phone and accessory had a different custom cable.
Before MCP, every AI agent framework had a custom tool integration format.

MCP standardizes how an AI Host (Client) talks to an external Tool Provider (Server)
using the universal JSON-RPC 2.0 protocol over standard input/output (stdio) or HTTP/SSE.

THE MCP LIFECYCLE HANDSHAKE:
1. Client -> Server: `initialize` (Negotiates capabilities and protocol versions)
2. Server -> Client: Returns server info and supported capabilities
3. Client -> Server: `notifications/initialized` (Confirms ready state)
4. Client -> Server: `tools/list` (Discovers available tools and JSON schemas)
5. Client -> Server: `tools/call` (Executes a tool with arguments)
6. Server -> Client: Returns structured result content `[{"type": "text", "text": "..."}]`
===============================================================================
"""

import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import json
from typing import Dict, Any, List, Optional
from config import get_llm, ACTIVE_MODEL


# =============================================================================
# 1. MCP COFFEE SHOP SERVER ENGINE (JSON-RPC 2.0 SPECIFICATION)
# =============================================================================
class CozyCoffeeMCPServer:
    """
    An educational, spec-compliant Model Context Protocol (MCP) server.
    Demonstrates low-level JSON-RPC 2.0 message handling and tool registry.
    """

    PROTOCOL_VERSION = "2024-11-05"

    def __init__(self, name: str = "CozyCoffeeServer", version: str = "1.0.0"):
        self.name = name
        self.version = version
        self.is_initialized = False

        # Internal coffee shop state
        self.menu_prices = {
            "espresso": 3.50,
            "americano": 4.00,
            "cappuccino": 4.75,
            "latte": 5.00,
            "mocha": 5.50,
        }
        self.bean_inventory_lbs = {
            "Ethiopian Yirgacheffe": 25.0,
            "Colombian Supremo": 40.0,
            "Sumatra Mandheling": 15.0,
        }

    # -------------------------------------------------------------------------
    # TOOL DEFINITIONS & JSON SCHEMAS
    # -------------------------------------------------------------------------
    def get_tool_definitions(self) -> List[Dict[str, Any]]:
        return [
            {
                "name": "calculate_beverage_bill",
                "description": "Calculates the total customer bill for coffee orders including tax and milk add-ons.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "drink": {
                            "type": "string",
                            "enum": ["espresso", "americano", "cappuccino", "latte", "mocha"],
                            "description": "The coffee drink name",
                        },
                        "quantity": {
                            "type": "integer",
                            "minimum": 1,
                            "description": "Number of drinks ordered",
                        },
                        "oat_milk": {
                            "type": "boolean",
                            "description": "Whether to add oat milk ($0.75 surcharge per drink)",
                        },
                    },
                    "required": ["drink", "quantity"],
                },
            },
            {
                "name": "check_bean_inventory",
                "description": "Checks the current warehouse stock of whole-bean coffee varieties in pounds.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "variety": {
                            "type": "string",
                            "description": "The bean variety name, or 'all' to list all",
                        },
                    },
                    "required": ["variety"],
                },
            },
        ]

    # -------------------------------------------------------------------------
    # TOOL EXECUTION HANDLERS
    # -------------------------------------------------------------------------
    def execute_tool(self, name: str, arguments: Dict[str, Any]) -> List[Dict[str, str]]:
        if name == "calculate_beverage_bill":
            drink = arguments.get("drink", "").lower()
            qty = arguments.get("quantity", 1)
            oat = arguments.get("oat_milk", False)

            if drink not in self.menu_prices:
                return [{"type": "text", "text": f"Error: Unknown drink '{drink}'. Available: {list(self.menu_prices.keys())}"}]

            base_price = self.menu_prices[drink] * qty
            addon_price = (0.75 * qty) if oat else 0.0
            subtotal = base_price + addon_price
            tax = subtotal * 0.08  # 8% sales tax
            total = subtotal + tax

            result_str = (
                f"Receipt: {qty}x {drink.title()} "
                f"{'(with Oat Milk)' if oat else ''} = Subtotal: ${subtotal:.2f}, "
                f"Tax (8%): ${tax:.2f}, Total: ${total:.2f}"
            )
            return [{"type": "text", "text": result_str}]

        elif name == "check_bean_inventory":
            variety = arguments.get("variety", "all")
            if variety == "all":
                lines = [f"- {v}: {lbs:.1f} lbs in stock" for v, lbs in self.bean_inventory_lbs.items()]
                return [{"type": "text", "text": "Warehouse Inventory:\n" + "\n".join(lines)}]
            elif variety in self.bean_inventory_lbs:
                return [{"type": "text", "text": f"{variety}: {self.bean_inventory_lbs[variety]:.1f} lbs available."}]
            else:
                return [{"type": "text", "text": f"Variety '{variety}' not found in catalog."}]

        else:
            raise ValueError(f"Unknown tool '{name}'")

    # -------------------------------------------------------------------------
    # JSON-RPC 2.0 PROTOCOL DISPATCHER
    # -------------------------------------------------------------------------
    def handle_message(self, request_json: str) -> Optional[str]:
        """
        Receives raw JSON-RPC 2.0 message, routes to protocol method, returns JSON response.
        """
        try:
            req = json.loads(request_json)
        except json.JSONDecodeError as e:
            return json.dumps({
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32700, "message": f"Parse error: {str(e)}"},
            })

        req_id = req.get("id")
        method = req.get("method")
        params = req.get("params", {})

        # Handle Notification (No response required)
        if method == "notifications/initialized":
            self.is_initialized = True
            return None

        # 1. MCP initialize handshake
        if method == "initialize":
            self.is_initialized = True
            return json.dumps({
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "protocolVersion": self.PROTOCOL_VERSION,
                    "capabilities": {
                        "tools": {"listChanged": False},
                        "resources": {"subscribe": False},
                        "prompts": {},
                    },
                    "serverInfo": {
                        "name": self.name,
                        "version": self.version,
                    },
                },
            })

        # 2. Ping method
        if method == "ping":
            return json.dumps({"jsonrpc": "2.0", "id": req_id, "result": {}})

        # 3. tools/list discovery
        if method == "tools/list":
            return json.dumps({
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "tools": self.get_tool_definitions(),
                },
            })

        # 4. tools/call execution
        if method == "tools/call":
            tool_name = params.get("name")
            arguments = params.get("arguments", {})
            try:
                content = self.execute_tool(tool_name, arguments)
                return json.dumps({
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": content,
                        "isError": False,
                    },
                })
            except Exception as e:
                return json.dumps({
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [{"type": "text", "text": f"Execution error: {str(e)}"}],
                        "isError": True,
                    },
                })

        # Unknown method
        return json.dumps({
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {"code": -32601, "message": f"Method '{method}' not found"},
        })


# =============================================================================
# 2. SIMULATED CLIENT / HOST DEMONSTRATION
# =============================================================================
def main():
    print("=" * 75)
    print("PROJECT 021: MCP ARCHITECTURE: JSON-RPC 2.0 & HANDSHAKE PROTOCOL")
    print(f"Active Groq Model: {ACTIVE_MODEL}")
    print("=" * 75)

    server = CozyCoffeeMCPServer()

    def send_and_receive(label: str, message: dict):
        print("\n" + "-" * 75)
        print(f"STEP: {label}")
        print("-" * 75)
        raw_req = json.dumps(message)
        print(f">>> [CLIENT OUTGOING]:\n{json.dumps(message, indent=2)}")

        raw_resp = server.handle_message(raw_req)
        if raw_resp:
            resp_obj = json.loads(raw_resp)
            print(f"\n<<< [SERVER INCOMING]:\n{json.dumps(resp_obj, indent=2)}")
            return resp_obj
        else:
            print("\n<<< [SERVER]: (Notification accepted, zero response payload)")
            return None

    # Step 1: Handshake initialize
    init_req = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "TestAIClient", "version": "1.0"},
        },
    }
    send_and_receive("1. Protocol Handshake (initialize)", init_req)

    # Step 2: Handshake confirmation notification
    notify_req = {
        "jsonrpc": "2.0",
        "method": "notifications/initialized",
    }
    send_and_receive("2. Handshake Complete Notification", notify_req)

    # Step 3: Tool Discovery (tools/list)
    list_req = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/list",
    }
    send_and_receive("3. Tool Discovery (tools/list)", list_req)

    # Step 4: Tool Execution (tools/call: Calculate Bill)
    call_req = {
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {
            "name": "calculate_beverage_bill",
            "arguments": {
                "drink": "latte",
                "quantity": 2,
                "oat_milk": True,
            },
        },
    }
    send_and_receive("4. Tool Execution (tools/call: calculate_beverage_bill)", call_req)

    # Step 5: Tool Execution (tools/call: Inventory check)
    call_inv = {
        "jsonrpc": "2.0",
        "id": 4,
        "method": "tools/call",
        "params": {
            "name": "check_bean_inventory",
            "arguments": {"variety": "all"},
        },
    }
    send_and_receive("5. Tool Execution (tools/call: check_bean_inventory)", call_inv)

    print("\n" + "=" * 75)
    print("[SUCCESS] Project 021 demonstration completed cleanly!")


if __name__ == "__main__":
    main()
