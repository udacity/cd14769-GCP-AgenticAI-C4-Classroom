import os
from typing import Optional
from google.adk.agents import Agent

from .products import products
from .order_data import orders, OrderStatus, get_next_order_id

model = "gemini-2.5-flash"

def read_prompt(filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "../prompts", filename)
    with open(file_path, "r") as f:
        return f.read()

def get_order(order_id: Optional[str] = None):
    """
    Retrieves the order.
    If no order ID is provided, creates a new one.
    If an order_id has already been created, then you MUST use it.
    
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
    # TODO: Implement add_to_cart logic
    # Check if product exists
    # Get the order (use get_order)
    # Check if order is already processed (order_status is not None)
    # Add to cart
    pass

cart_instruction = read_prompt("cart-prompt.txt")

# TODO: Create the cart_agent
# It should use get_order and add_to_cart tools
cart_agent = None
