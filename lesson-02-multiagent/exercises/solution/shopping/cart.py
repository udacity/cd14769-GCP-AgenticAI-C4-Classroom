import os
from google.adk.agents import Agent
from .products import products
from .order_data import orders, OrderStatus

model = "gemini-2.5-flash"

def read_prompt(filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, filename)
    with open(file_path, "r") as f:
        return f.read()

def add_to_cart(order_id: str, product_id: str):
    """Adds a product to the specified order's cart.

    Args:
        order_id: The ID of the order.
        product_id: The ID of the product to add.
    """
    if product_id not in products:
        return {"error": "Product ID not found"}
    
    if order_id not in orders:
        # Create a new order if it doesn't exist, mirroring the demo's order structure
        orders[order_id] = {
            "cart": [],
            "address": None,
            "order_status": None
        }
    
    # Check if the order has already been placed or processed
    if orders[order_id]["order_status"] is not None:
        return {"error": f"Order {order_id} cannot be modified as its status is already set to {orders[order_id]['order_status'].value}"}

    orders[order_id]["cart"].append(product_id)
    return {"status": "success", "message": f"Added {products[product_id]['name']} to order {order_id}'s cart.", "cart": orders[order_id]["cart"]}

cart_instruction = read_prompt("cart-prompt.txt")

cart_agent = Agent(
    name="cart_agent",
    description="Manages user shopping carts.",
    model=model,
    instruction=cart_instruction,
    tools=[add_to_cart],
)
