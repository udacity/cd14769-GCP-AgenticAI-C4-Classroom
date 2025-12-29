import os
from google.adk.agents import Agent
from .order_data import orders, OrderStatus

model = "gemini-2.5-flash"

def read_prompt(filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "../prompts", filename)
    with open(file_path, "r") as f:
        return f.read()

def get_order_info(order_id: str):
    """Retrieves detailed information for a given order ID.

    Args:
        order_id: The ID of the order to retrieve information for.
    """
    if order_id in orders:
        order = orders[order_id]
        return {
            "cart": order.get("cart"),
            "address": order.get("address"),
            "order_status": order.get("order_status").value if order.get("order_status") else None
        }
    else:
        return {"error": f"Order {order_id} not found."}

inquiry_instruction = read_prompt("inquiry-prompt.txt")

inquiry_agent = Agent(
    name="shipping_inquiry_agent",
    description="Handles questions about shipping policies and tracking.",
    model=model,
    instruction=inquiry_instruction,
    tools=[get_order_info],
)
