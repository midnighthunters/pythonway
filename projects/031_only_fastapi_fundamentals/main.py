"""
===============================================================================
PROJECT 031: FASTAPI CORE: PYDANTIC V2 MODELS & OPENAPI SPECS
Stage 1: Pure Fundamentals | Difficulty: 1.5 / 10 (Beginner Friendly)
===============================================================================

THE BIG QUESTION:
Why has FastAPI become the universal standard for deploying AI services?

FASTAPI ARCHITECTURAL FOUNDATIONS:
1. Pydantic v2 Strong Typing: Automatic validation, type casting, and serialization.
2. Self-Documenting OpenAPI: Auto-generates Swagger UI (`/docs`) and ReDoc schemas.
3. Modular APIRouters: Clean microservice domain separation.
4. Native Async/Await Concurrency: Ultra-low latency for IO-bound AI model calls.
===============================================================================
"""

import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import time
import json
from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator
from fastapi import FastAPI, APIRouter, HTTPException, Query, status
from fastapi.testclient import TestClient
from config import get_llm, ACTIVE_MODEL


# =============================================================================
# 1. PYDANTIC V2 DATA SCHEMAS
# =============================================================================
class CategoryEnum(str, Enum):
    COFFEE = "coffee"
    TEA = "tea"
    BAKERY = "bakery"


class MenuItem(BaseModel):
    id: int
    name: str = Field(min_length=2, max_length=50)
    category: CategoryEnum
    price: float = Field(gt=0.0, description="Base price in USD")
    in_stock: bool = True


class OrderItemRequest(BaseModel):
    menu_item_id: int
    quantity: int = Field(gt=0, le=20, description="Between 1 and 20 items")
    oat_milk: bool = False


class OrderCreateRequest(BaseModel):
    customer_name: str = Field(min_length=2, description="Customer full name")
    items: List[OrderItemRequest] = Field(min_length=1, description="At least one item required")
    loyalty_number: Optional[str] = None

    @field_validator("customer_name")
    def validate_name(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Customer name cannot be purely whitespace")
        return v.strip().title()


class OrderResponse(BaseModel):
    order_id: str
    customer_name: str
    subtotal: float
    tax: float
    total: float
    estimated_ready_minutes: int
    created_at: str


# =============================================================================
# 2. IN-MEMORY DATABASE & FASTAPI ROUTERS
# =============================================================================
MENU_DB: Dict[int, MenuItem] = {
    1: MenuItem(id=1, name="Single Origin Espresso", category=CategoryEnum.COFFEE, price=3.50),
    2: MenuItem(id=2, name="Salted Caramel Oat Latte", category=CategoryEnum.COFFEE, price=5.25),
    3: MenuItem(id=3, name="Ceremonial Uji Matcha", category=CategoryEnum.TEA, price=4.75),
    4: MenuItem(id=4, name="Almond Butter Croissant", category=CategoryEnum.BAKERY, price=4.25),
}

ORDERS_DB: Dict[str, OrderResponse] = {}

menu_router = APIRouter(prefix="/menu", tags=["Menu"])
orders_router = APIRouter(prefix="/orders", tags=["Orders"])


@menu_router.get("", response_model=List[MenuItem])
def get_menu_items(
    category: Optional[CategoryEnum] = None,
    max_price: Optional[float] = Query(default=None, gt=0.0),
):
    """Fetches catalog items with optional category and price filters."""
    items = list(MENU_DB.values())
    if category:
        items = [i for i in items if i.category == category]
    if max_price is not None:
        items = [i for i in items if i.price <= max_price]
    return items


@menu_router.get("/{item_id}", response_model=MenuItem)
def get_menu_item_by_id(item_id: int):
    if item_id not in MENU_DB:
        raise HTTPException(status_code=404, detail=f"Menu item #{item_id} not found")
    return MENU_DB[item_id]


@orders_router.post("", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_customer_order(order_req: OrderCreateRequest):
    """Calculates order totals, sales tax, and saves customer order."""
    subtotal = 0.0
    for itm in order_req.items:
        if itm.menu_item_id not in MENU_DB:
            raise HTTPException(status_code=400, detail=f"Invalid menu item ID: {itm.menu_item_id}")
        base = MENU_DB[itm.menu_item_id].price * itm.quantity
        addon = (0.75 * itm.quantity) if itm.oat_milk else 0.0
        subtotal += (base + addon)

    tax = subtotal * 0.08  # 8% tax
    total = round(subtotal + tax, 2)
    order_id = f"ORD-{int(time.time() * 1000) % 100000:05d}"

    resp = OrderResponse(
        order_id=order_id,
        customer_name=order_req.customer_name,
        subtotal=round(subtotal, 2),
        tax=round(tax, 2),
        total=total,
        estimated_ready_minutes=max(3, len(order_req.items) * 2),
        created_at=time.strftime("%Y-%m-%d %H:%M:%S"),
    )
    ORDERS_DB[order_id] = resp
    return resp


# =============================================================================
# 3. ROOT FASTAPI APPLICATION
# =============================================================================
app = FastAPI(
    title="Cozy Coffee & Bakery Microservice",
    version="1.0.0",
    description="High-performance FastAPI service powering digital orders and AI specials.",
)
app.include_router(menu_router)
app.include_router(orders_router)


@app.get("/health", tags=["System"])
def health_check():
    return {"status": "HEALTHY", "active_model": ACTIVE_MODEL, "timestamp": time.time()}


@app.post("/ai/daily-special", tags=["AI"])
def generate_ai_daily_special(theme: str = "Rainy Morning"):
    """Uses Groq LLM to generate an enticing daily special based on active menu items."""
    llm = get_llm(temperature=0.3)
    catalog_str = ", ".join([f"{item.name} (${item.price})" for item in MENU_DB.values()])
    prompt = (
        f"You are the Head Barista. For the theme '{theme}', create an enticing daily bundle "
        f"using 1 beverage and 1 bakery item from our catalog: [{catalog_str}]. "
        "Provide a catchy bundle name and a 2-sentence marketing teaser."
    )
    res = llm.invoke(prompt).content.strip()
    return {"theme": theme, "recommendation": res}


# =============================================================================
# 4. MAIN DEMONSTRATION
# =============================================================================
def main():
    print("=" * 75)
    print("PROJECT 031: FASTAPI CORE: PYDANTIC V2 MODELS & OPENAPI SPECS")
    print(f"Active Groq Model: {ACTIVE_MODEL}")
    print("=" * 75)

    client = TestClient(app)

    # 1. Health check
    print("\n" + "-" * 75)
    print("1. GET /health")
    print("-" * 75)
    res = client.get("/health")
    print(f"Status Code: {res.status_code}")
    print(f"Response Body:\n{json.dumps(res.json(), indent=2)}")

    # 2. Get Menu Items
    print("\n" + "-" * 75)
    print("2. GET /menu?category=coffee&max_price=6.00")
    print("-" * 75)
    res = client.get("/menu", params={"category": "coffee", "max_price": 6.00})
    print(f"Status Code: {res.status_code}")
    print(f"Items Returned: {len(res.json())}")
    print(json.dumps(res.json(), indent=2))

    # 3. Create Valid Order
    print("\n" + "-" * 75)
    print("3. POST /orders (Valid Pydantic v2 Request)")
    print("-" * 75)
    order_payload = {
        "customer_name": "  lucas vance  ",  # Tests automatic strip and title-case validator
        "items": [
            {"menu_item_id": 2, "quantity": 2, "oat_milk": True},
            {"menu_item_id": 4, "quantity": 1, "oat_milk": False},
        ],
    }
    res = client.post("/orders", json=order_payload)
    print(f"Status Code: {res.status_code}")
    print(f"Receipt Generated:\n{json.dumps(res.json(), indent=2)}")

    # 4. Validation Rejection (Negative quantity)
    print("\n" + "-" * 75)
    print("4. POST /orders (Invalid Request: quantity = -5)")
    print("-" * 75)
    bad_payload = {
        "customer_name": "Bad Customer",
        "items": [{"menu_item_id": 1, "quantity": -5}],
    }
    res_bad = client.post("/orders", json=bad_payload)
    print(f"Status Code: {res_bad.status_code} (Pydantic Validation Error caught!)")
    print(f"Validation Error Body:\n{json.dumps(res_bad.json(), indent=2)}")

    # 5. Live AI Endpoint
    print("\n" + "=" * 75)
    print("5. POST /ai/daily-special?theme=Autumn+Breeze")
    print("=" * 75)
    ai_res = client.post("/ai/daily-special", params={"theme": "Autumn Breeze"})
    print(f"Status Code: {ai_res.status_code}")
    print(ai_res.json()["recommendation"])

    print("\n" + "=" * 75)
    print("[SUCCESS] Project 031 demonstration completed cleanly!")


if __name__ == "__main__":
    main()
