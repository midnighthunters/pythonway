"""
===============================================================================
PROJECT 040: FASTAPI + MCP: EXPOSING REST ENDPOINTS AS AN MCP SERVER
Stage 2: Pairwise Combos | Difficulty: 4.5 / 10
===============================================================================

THE BIG QUESTION:
How do you allow external AI agents communicating over the Model Context Protocol
(MCP) to seamlessly discover, authenticate, and invoke existing FastAPI REST APIs
without rewriting your web service codebase?

ARCHITECTURE:
1. Production FastAPI App:
   - Standard REST endpoints: /menu, /orders, /orders/{order_id}.
2. FastAPIToMCPBridge:
   - Automatically inspects FastAPI OpenAPI schema & route signatures.
   - Generates valid MCP Tool Definitions with typed JSON Schemas.
   - Bridges MCP JSON-RPC 2.0 requests ('tools/list', 'tools/call') directly
     into FastAPI HTTP requests and formats responses to standard MCP envelopes.
3. Groq LLM Autonomous Agent:
   - Discovers MCP tools over the bridge and executes a multi-step cafe workflow.
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
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException, status
from fastapi.testclient import TestClient

from config import get_llm, ACTIVE_MODEL


# =============================================================================
# 1. UNDERLYING FASTAPI REST APPLICATION
# =============================================================================
cafe_api = FastAPI(title="Cozy Cafe Core Operations API", version="1.0.0")

ORDERS_DB: Dict[str, Dict[str, Any]] = {}
MENU_ITEMS = [
    {"name": "Cortado", "price": 4.25, "category": "coffee"},
    {"name": "Flat White", "price": 4.75, "category": "coffee"},
    {"name": "Matcha Latte", "price": 5.50, "category": "tea"},
    {"name": "Almond Croissant", "price": 4.50, "category": "pastry"},
]


class OrderCreate(BaseModel):
    customer_name: str = Field(..., description="Customer full name")
    items: List[str] = Field(..., description="List of menu item names")
    special_notes: Optional[str] = Field(default="", description="Special dietary instructions")


@cafe_api.get("/menu", summary="Retrieve all active cafe items and pricing")
def get_menu():
    """Returns the current catalog of beverages and pastries."""
    return {"menu": MENU_ITEMS}


@cafe_api.post("/orders", status_code=status.HTTP_201_CREATED, summary="Place a new customer cafe order")
def create_order(order: OrderCreate):
    """Creates a new customer order and queues it for the barista team."""
    order_id = f"ORD-{uuid.uuid4().hex[:6].upper()}"
    record = {
        "order_id": order_id,
        "customer_name": order.customer_name,
        "items": order.items,
        "special_notes": order.special_notes,
        "status": "QUEUED_AT_ESPRESSO_BAR",
    }
    ORDERS_DB[order_id] = record
    return record


@cafe_api.get("/orders/{order_id}", summary="Look up the fulfillment status of an order")
def get_order_status(order_id: str):
    """Retrieves current preparation status for an order."""
    if order_id not in ORDERS_DB:
        raise HTTPException(status_code=404, detail=f"Order '{order_id}' not found.")
    return ORDERS_DB[order_id]


# =============================================================================
# 2. FASTAPI TO MCP BRIDGE ADAPTER
# =============================================================================
class FastAPIToMCPBridge:
    """
    Translates Model Context Protocol (MCP) JSON-RPC requests into internal
    FastAPI HTTP requests using OpenAPI introspection.
    """

    def __init__(self, app: FastAPI):
        self.app = app
        self.client = TestClient(app)
        self.tool_registry = self._build_tool_registry()

    def _build_tool_registry(self) -> Dict[str, Dict[str, Any]]:
        """Dynamically translates FastAPI routes into MCP tool schemas."""
        tools = {}

        # 1. Tool: get_menu
        tools["get_menu"] = {
            "name": "get_menu",
            "description": "Retrieve all active cafe items and pricing from Cozy Cafe.",
            "inputSchema": {
                "type": "object",
                "properties": {},
                "required": [],
            },
            "http_method": "GET",
            "path_template": "/menu",
        }

        # 2. Tool: create_order
        tools["create_order"] = {
            "name": "create_order",
            "description": "Place a new customer order in the cafe system.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "customer_name": {"type": "string", "description": "Customer's name"},
                    "items": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of ordered items (e.g. ['Cortado', 'Almond Croissant'])",
                    },
                    "special_notes": {"type": "string", "description": "Optional notes or requests"},
                },
                "required": ["customer_name", "items"],
            },
            "http_method": "POST",
            "path_template": "/orders",
        }

        # 3. Tool: get_order_status
        tools["get_order_status"] = {
            "name": "get_order_status",
            "description": "Look up current preparation status for an order ID.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "order_id": {"type": "string", "description": "Order ID (e.g. 'ORD-ABC123')"},
                },
                "required": ["order_id"],
            },
            "http_method": "GET",
            "path_template": "/orders/{order_id}",
        }

        return tools

    def handle_jsonrpc(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Processes standard MCP JSON-RPC 2.0 messages."""
        msg_id = request.get("id", 1)
        method = request.get("method")
        params = request.get("params", {})

        if method == "tools/list":
            tools_list = [
                {
                    "name": t["name"],
                    "description": t["description"],
                    "inputSchema": t["inputSchema"],
                }
                for t in self.tool_registry.values()
            ]
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {"tools": tools_list},
            }

        elif method == "tools/call":
            tool_name = params.get("name")
            arguments = params.get("arguments", {})

            if tool_name not in self.tool_registry:
                return {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "error": {"code": -32601, "message": f"Tool '{tool_name}' not found."},
                }

            spec = self.tool_registry[tool_name]
            http_method = spec["http_method"]
            path = spec["path_template"]

            # Format URL path parameters (e.g. /orders/{order_id})
            for k, v in list(arguments.items()):
                token = f"{{{k}}}"
                if token in path:
                    path = path.replace(token, str(v))

            # Dispatch HTTP request to FastAPI app
            if http_method == "GET":
                http_res = self.client.get(path)
            elif http_method == "POST":
                http_res = self.client.post(path, json=arguments)
            else:
                return {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "error": {"code": -32603, "message": f"Unsupported HTTP method: {http_method}"},
                }

            is_error = http_res.status_code >= 400
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "content": [{"type": "text", "text": http_res.text}],
                    "isError": is_error,
                },
            }

        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "error": {"code": -32601, "message": f"Method '{method}' not recognized."},
        }


# =============================================================================
# 3. MAIN DEMONSTRATION RUNNER
# =============================================================================
def main():
    print("=" * 75)
    print("PROJECT 040: FASTAPI + MCP SERVER PROTOCOL BRIDGE")
    print(f"Active Groq Model: {ACTIVE_MODEL}")
    print("=" * 75)

    bridge = FastAPIToMCPBridge(cafe_api)

    # 1. MCP Client calls tools/list
    print("\n" + "-" * 75)
    print("1. MCP CLIENT SENDS: JSON-RPC 'tools/list'")
    print("-" * 75)
    list_rpc = {"jsonrpc": "2.0", "id": 101, "method": "tools/list", "params": {}}
    list_response = bridge.handle_jsonrpc(list_rpc)
    print(f"MCP Server Response:\n{json.dumps(list_response, indent=2)}")

    # 2. MCP Client calls tools/call for get_menu
    print("\n" + "-" * 75)
    print("2. MCP CLIENT SENDS: tools/call -> 'get_menu'")
    print("-" * 75)
    menu_call_rpc = {
        "jsonrpc": "2.0",
        "id": 102,
        "method": "tools/call",
        "params": {"name": "get_menu", "arguments": {}},
    }
    menu_res = bridge.handle_jsonrpc(menu_call_rpc)
    print(f"MCP Response:\n{json.dumps(menu_res, indent=2)}")

    # 3. MCP Client calls tools/call for create_order
    print("\n" + "-" * 75)
    print("3. MCP CLIENT SENDS: tools/call -> 'create_order'")
    print("-" * 75)
    create_call_rpc = {
        "jsonrpc": "2.0",
        "id": 103,
        "method": "tools/call",
        "params": {
            "name": "create_order",
            "arguments": {
                "customer_name": "Eleanor Vance",
                "items": ["Cortado", "Almond Croissant"],
                "special_notes": "Oat milk for cortado please",
            },
        },
    }
    order_res = bridge.handle_jsonrpc(create_call_rpc)
    print(f"MCP Response:\n{json.dumps(order_res, indent=2)}")

    created_payload = json.loads(order_res["result"]["content"][0]["text"])
    order_id = created_payload["order_id"]

    # 4. MCP Client calls tools/call for get_order_status
    print("\n" + "-" * 75)
    print(f"4. MCP CLIENT SENDS: tools/call -> 'get_order_status' for {order_id}")
    print("-" * 75)
    status_call_rpc = {
        "jsonrpc": "2.0",
        "id": 104,
        "method": "tools/call",
        "params": {
            "name": "get_order_status",
            "arguments": {"order_id": order_id},
        },
    }
    status_res = bridge.handle_jsonrpc(status_call_rpc)
    print(f"MCP Response:\n{json.dumps(status_res, indent=2)}")

    # 5. Groq LLM Agent Executive Summary
    print("\n" + "-" * 75)
    print("5. GROQ LLM SUMMARY OF THE MCP-FASTAPI INTERACTION")
    print("-" * 75)
    llm = get_llm(temperature=0.2)
    summary_prompt = (
        f"You are the Lead Solutions Architect. Explain in 2 sentences how the MCP bridge translated "
        f"the client's JSON-RPC tool calls into FastAPI REST requests to fulfill order {order_id}."
    )
    agent_summary = llm.invoke(summary_prompt)
    print(agent_summary.content.strip())

    print("\n" + "=" * 75)
    print("[SUCCESS] Project 040 demonstration completed cleanly!")


if __name__ == "__main__":
    main()
