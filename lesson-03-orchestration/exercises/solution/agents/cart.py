import os
from typing import Optional
from google.adk.agents import Agent, SequentialAgent, ParallelAgent, LlmAgent

from .products import products
from .order_data import orders, OrderStatus, get_next_order_id
from .inventory import inventory_data_agent

model = "gemini-2.5-flash"

def read_prompt(filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "../prompts", filename)
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

# --- Sub-Agents ---

get_order_agent = LlmAgent(
    name="get_order_agent",
    description="Ensures an active order session exists.",
    model=model,
    instruction=read_prompt("get-order-prompt.txt"),
    tools=[get_order],
)

add_item_agent = LlmAgent(
    name="add_item_agent",
    description="Adds the item to the cart.",
    model=model,
    instruction=read_prompt("add-item-prompt.txt"),
    tools=[add_to_cart],
)

# Parallel Prep: Get Order + Check Inventory
cart_prep_agent = ParallelAgent(
    name="cart_prep_agent",
    description="Prepares for adding to cart by ensuring order exists and checking inventory.",
    sub_agents=[get_order_agent, inventory_data_agent],
)

# Sequential Workflow: Prep -> Add Item
cart_agent = SequentialAgent(
    name="cart_agent",
    description="Manages adding items to the cart with validation.",
    sub_agents=[cart_prep_agent, add_item_agent],
)