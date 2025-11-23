import os
from typing import Optional
from google.adk.agents import Agent

from .products import products
from .order_data import orders, OrderStatus, get_next_order_id

model = "gemini-2.5-flash"

def read_prompt(filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, filename)
    with open(file_path, "r") as f:
        return f.read()

def get_order(order_id: Optional[str] = None):
    """
    Retrieves the order. If no order ID is provided, creates a new one.
    
    Args:
        order_id: Optional existing order ID.
    """
    if order_id is None:
      order_id = get_next_order_id()
      orders[order_id] = {
        "cart": [],
        "address": None,
        "order_status": None
      }

    # Return the order with its ID so the caller knows it
    return {"order_id": order_id, "order": orders[order_id]}

def add_to_cart(order_id: str, product_id: str):
    """Adds a product to the specified order's cart.

    Args:
        order_id: The ID of the order.
        product_id: The ID of the product to add.
    """
    if product_id not in products:
        return {"error": "Product ID not found"}

    order_info = get_order(order_id)
    order = order_info["order"]

    # Check if the order has already been placed or processed
    if order["order_status"] is not None:
        return {"error": f"Order {order_id} cannot be modified as its status is already set to {order['order_status'].value}"}

    order["cart"].append(product_id)
    return {"status": "success", "message": f"Added {products[product_id]['name']} to cart.", "cart": order["cart"]}

cart_instruction = read_prompt("cart-prompt.txt")

cart_agent = Agent(
    name="cart_agent",
    description="Manages user shopping carts.",
    model=model,
    instruction=cart_instruction,
    tools=[get_order, add_to_cart],
)
