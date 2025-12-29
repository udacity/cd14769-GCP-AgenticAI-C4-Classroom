import os
from google.adk.agents import Agent
from .order_data import orders, OrderStatus

model = "gemini-2.5-flash"

def read_prompt(filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "../prompts", filename)
    with open(file_path, "r") as f:
        return f.read()

def place_order(order_id: str, address: dict):
    """
    Places an order given the order ID and the address to ship the order to

    Args:
        order_id: The ID of the order.
        address: Dictionary with name, address_1, address_2, city, state, postal_code.
    """
    if order_id not in orders:
        return {"error": "Order ID not found"}
    
    order = orders[order_id]
    
    if "order_status" in order:
        return {"error": "Order already has a status set"}

    order["address"] = address
    order["order_status"] = OrderStatus.PLACED
    
    return {
        "cart": order.get("cart"),
        "address": order.get("address"),
        "order_status": order["order_status"].value
    }

shipping_instruction = read_prompt("shipping-prompt.txt")

shipping_agent = Agent(
    name="shipping_agent",
    description="Handles order shipping requests.",
    model=model,
    instruction=shipping_instruction,
    tools=[place_order],
)
