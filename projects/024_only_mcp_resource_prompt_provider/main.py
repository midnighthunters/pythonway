"""
===============================================================================
PROJECT 024: DYNAMIC RESOURCES & REUSABLE PROMPT TEMPLATES VIA MCP
Stage 1: Pure Fundamentals | Difficulty: 3.5 / 10 (Intermediate)
===============================================================================

THE BIG QUESTION:
Beyond "Tools", what other essential capabilities does the MCP standard provide?

MCP is not just a tool-calling framework. It has THREE core pillars:
1. TOOLS (`tools/call`): Executable functions with side effects (write files, calc bills).
2. RESOURCES (`resources/read`): Read-only data streams identified by URIs (e.g.
   `coffee://menu/seasonal`, `git://diff/head`). Resources provide context to the LLM
   without needing function execution.
3. PROMPTS (`prompts/get`): Reusable, parameterized prompt templates stored on the
   server. The server defines the best way to prompt models for its specific domain!

In this project, we implement an MCP server that provides live coffee shop
resources and expert barista prompt templates.
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
# 1. MCP RESOURCE & PROMPT PROVIDER SERVER
# =============================================================================
class CoffeeResourceAndPromptMCPServer:
    """
    Model Context Protocol server implementing the 'resources' and 'prompts'
    primitives for dynamic context injection and reusable domain prompts.
    """

    def __init__(self):
        # In-memory resource store
        self.resources_store = {
            "coffee://menu/seasonal": {
                "name": "Autumn Seasonal Drinks Menu",
                "mimeType": "application/json",
                "description": "Current limited-time seasonal beverages with ingredients and prices.",
                "data": json.dumps({
                    "season": "Autumn 2026",
                    "specials": [
                        {
                            "name": "Pumpkin Spiced Maple Cold Brew",
                            "price": 5.75,
                            "profile": "Warm spices, real Vermont maple syrup, vanilla sweet cream.",
                            "vegan_adaptable": True,
                        },
                        {
                            "name": "Salted Caramel Apple Cider Latte",
                            "price": 5.50,
                            "profile": "Spiced honeycrisp cider, steamed oat milk, Maldon sea salt.",
                            "vegan_adaptable": True,
                        },
                        {
                            "name": "Hazelnut Praline Cortado",
                            "price": 4.50,
                            "profile": "Double ristretto, toasted hazelnut paste, velvety microfoam.",
                            "vegan_adaptable": False,
                        },
                    ],
                }, indent=2),
            },
            "coffee://operations/roast-schedule": {
                "name": "Weekly Master Roaster Log",
                "mimeType": "text/plain",
                "description": "Log of bean roasting batches and freshness degas dates.",
                "data": (
                    "COZY ROASTERY SCHEDULE (Current Week):\n"
                    "- Batch #401: Ethiopian Yirgacheffe (Light Roast, Roasted Yesterday) -> Peak: Oct 1\n"
                    "- Batch #402: Colombian Huila (Medium Roast, Roasted 3 days ago) -> Ready to brew\n"
                    "- Batch #403: Guatemala Antigua Decaf (Swiss Water, Roasted 5 days ago) -> Ready to brew\n"
                ),
            },
        }

        # Prompt template definitions
        self.prompts_catalog = {
            "barista_upsell_recommender": {
                "name": "barista_upsell_recommender",
                "description": "Generates a charming, personalized barista drink recommendation based on customer mood and dietary needs.",
                "arguments": [
                    {
                        "name": "customer_mood",
                        "description": "How the customer is feeling (e.g. exhausted, celebratory, chilly)",
                        "required": True,
                    },
                    {
                        "name": "dietary_preference",
                        "description": "Dietary constraints (e.g. vegan, dairy-free, decaf, low-sugar)",
                        "required": False,
                    },
                ],
            },
            "customer_service_recovery": {
                "name": "customer_service_recovery",
                "description": "Generates an empathetic response to a customer order issue with a recovery voucher.",
                "arguments": [
                    {
                        "name": "customer_name",
                        "description": "Customer's first name",
                        "required": True,
                    },
                    {
                        "name": "issue_description",
                        "description": "What went wrong with their order",
                        "required": True,
                    },
                ],
            },
        }

    # -------------------------------------------------------------------------
    # MCP RESOURCES HANDLERS (resources/list & resources/read)
    # -------------------------------------------------------------------------
    def list_resources(self) -> List[Dict[str, Any]]:
        """Returns catalog of all registered resource URIs and metadata."""
        return [
            {
                "uri": uri,
                "name": info["name"],
                "description": info["description"],
                "mimeType": info["mimeType"],
            }
            for uri, info in self.resources_store.items()
        ]

    def read_resource(self, uri: str) -> List[Dict[str, Any]]:
        """Fetches the contents of a specific resource URI."""
        if uri not in self.resources_store:
            raise KeyError(f"Resource URI '{uri}' not found on server.")

        entry = self.resources_store[uri]
        return [
            {
                "uri": uri,
                "mimeType": entry["mimeType"],
                "text": entry["data"],
            }
        ]

    # -------------------------------------------------------------------------
    # MCP PROMPTS HANDLERS (prompts/list & prompts/get)
    # -------------------------------------------------------------------------
    def list_prompts(self) -> List[Dict[str, Any]]:
        """Returns catalog of registered prompt templates and their arguments."""
        return list(self.prompts_catalog.values())

    def get_prompt(self, name: str, arguments: Dict[str, str]) -> Dict[str, Any]:
        """Renders parameterized messages for a given prompt template."""
        if name not in self.prompts_catalog:
            raise KeyError(f"Prompt template '{name}' not found.")

        if name == "barista_upsell_recommender":
            mood = arguments.get("customer_mood", "cheerful")
            diet = arguments.get("dietary_preference", "None")

            system_instruction = (
                "You are an energetic, warm Master Barista at Cozy Coffee. "
                "Recommend one drink from our seasonal menu that perfectly matches the customer's mood. "
                "Always suggest a complementary pastry pairing."
            )
            user_msg = (
                f"Customer Mood: {mood}\n"
                f"Dietary Restrictions: {diet}\n\n"
                "Please recommend the ideal drink and tell me why it fits my mood today!"
            )
            return {
                "description": "Barista recommendation tailored to customer mood",
                "messages": [
                    {"role": "user", "content": {"type": "text", "text": f"{system_instruction}\n\n{user_msg}"}},
                ],
            }

        elif name == "customer_service_recovery":
            name_val = arguments.get("customer_name", "Valued Customer")
            issue = arguments.get("issue_description", "an issue with the order")

            template = (
                f"Dear {name_val},\n\n"
                f"We are truly sorry to hear that {issue}. "
                "At Cozy Coffee, every single cup should be a moment of delight. "
                "We have applied a $10 courtesy credit to your account and would love to remake your drink on us next time!"
            )
            return {
                "description": "Customer service resolution letter",
                "messages": [
                    {"role": "user", "content": {"type": "text", "text": template}},
                ],
            }

        raise ValueError(f"Unimplemented prompt: {name}")

    # -------------------------------------------------------------------------
    # JSON-RPC DISPATCHER
    # -------------------------------------------------------------------------
    def handle_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        req_id = message.get("id")
        method = message.get("method")
        params = message.get("params", {})

        try:
            if method == "resources/list":
                return {"jsonrpc": "2.0", "id": req_id, "result": {"resources": self.list_resources()}}

            elif method == "resources/read":
                uri = params.get("uri")
                contents = self.read_resource(uri)
                return {"jsonrpc": "2.0", "id": req_id, "result": {"contents": contents}}

            elif method == "prompts/list":
                return {"jsonrpc": "2.0", "id": req_id, "result": {"prompts": self.list_prompts()}}

            elif method == "prompts/get":
                name = params.get("name")
                args = params.get("arguments", {})
                prompt_res = self.get_prompt(name, args)
                return {"jsonrpc": "2.0", "id": req_id, "result": prompt_res}

            else:
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32601, "message": f"Method '{method}' not implemented."},
                }

        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32000, "message": str(e)},
            }


# =============================================================================
# 2. RUN DEMONSTRATION
# =============================================================================
def main():
    print("=" * 75)
    print("PROJECT 024: DYNAMIC RESOURCES & REUSABLE PROMPTS VIA MCP")
    print(f"Active Groq Model: {ACTIVE_MODEL}")
    print("=" * 75)

    server = CoffeeResourceAndPromptMCPServer()

    # -------------------------------------------------------------------------
    # PART 1: DISCOVER AND READ RESOURCES
    # -------------------------------------------------------------------------
    print("\n" + "-" * 75)
    print("1. DISCOVERING RESOURCES (resources/list)")
    print("-" * 75)
    list_res = server.handle_message({"id": 1, "method": "resources/list"})
    resources = list_res["result"]["resources"]
    for r in resources:
        print(f" • URI: {r['uri']} ({r['mimeType']}) - {r['name']}")

    print("\n" + "-" * 75)
    print("2. READING RESOURCE DATA (resources/read: 'coffee://menu/seasonal')")
    print("-" * 75)
    read_res = server.handle_message({
        "id": 2,
        "method": "resources/read",
        "params": {"uri": "coffee://menu/seasonal"},
    })
    menu_payload = read_res["result"]["contents"][0]["text"]
    print(menu_payload)

    # -------------------------------------------------------------------------
    # PART 2: DISCOVER AND RENDER PROMPTS
    # -------------------------------------------------------------------------
    print("\n" + "-" * 75)
    print("3. DISCOVERING PROMPT TEMPLATES (prompts/list)")
    print("-" * 75)
    prompts_res = server.handle_message({"id": 3, "method": "prompts/list"})
    for p in prompts_res["result"]["prompts"]:
        print(f" • Prompt: '{p['name']}' -> {p['description']}")

    print("\n" + "-" * 75)
    print("4. FETCHING PARAMETERIZED PROMPT (prompts/get: 'barista_upsell_recommender')")
    print("-" * 75)
    rendered = server.handle_message({
        "id": 4,
        "method": "prompts/get",
        "params": {
            "name": "barista_upsell_recommender",
            "arguments": {
                "customer_mood": "freezing cold and low energy",
                "dietary_preference": "vegan / 100% plant-based",
            },
        },
    })
    prompt_text = rendered["result"]["messages"][0]["content"]["text"]
    print(f"Rendered Prompt:\n\"\"\"\n{prompt_text}\n\"\"\"")

    # -------------------------------------------------------------------------
    # PART 3: CONNECTING RESOURCE DATA + PROMPT TEMPLATE TO GROQ LLM
    # -------------------------------------------------------------------------
    print("\n" + "=" * 75)
    print("LIVE LLM GENERATION (Combining MCP Resource + MCP Prompt Template)")
    print("=" * 75)

    llm = get_llm(temperature=0.3)
    final_input = (
        f"Available Resource Data:\n{menu_payload}\n\n"
        f"Barista Instruction & Customer Request:\n{prompt_text}"
    )
    answer = llm.invoke(final_input)
    print(answer.content.strip())

    print("\n" + "=" * 75)
    print("[SUCCESS] Project 024 demonstration completed cleanly!")


if __name__ == "__main__":
    main()
