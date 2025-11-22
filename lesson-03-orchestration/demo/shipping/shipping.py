import os
from google.adk.agents import Agent, SequentialAgent, ParallelAgent, LlmAgent
from .order_data import orders, OrderStatus
from .rates import SHIPPING_RATES, TAX_RATES
from .products import products

model = "gemini-2.5-flash"

def read_prompt(filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, filename)
    with open(file_path, "r") as f:
        return f.read()

# --- Existing Tool ---
def place_order(order_id: str, address: dict):
    """Places an order by adding the shipping address and setting status to PLACED.

    Args:
        order_id: The ID of the order.
        address: Dictionary with name, address_1, address_2, city, state, postal_code.
    """
    if order_id not in orders:
        return {"error": "Order ID not found"}
    
    order = orders[order_id]
    
    if "order_status" in order and order["order_status"]:
        return {"error": "Order already has a status set"}

    order["address"] = address
    order["order_status"] = OrderStatus.PLACED
    
    return {
        "cart": order.get("cart"),
        "address": order.get("address"),
        "order_status": order["order_status"].value
    }

# --- New Tools --- 

def calculate_shipping_cost(order_id: str, shipping_type: str = "standard") -> dict:
    """Calculates the shipping cost for an order.

    Args:
        order_id: The ID of the order.
        shipping_type: The type of shipping (e.g., "standard", "express"). Defaults to "standard".
    """
    if order_id not in orders:
        return {"error": f"Order {order_id} not found."}

    cost = SHIPPING_RATES.get(shipping_type.lower(), SHIPPING_RATES["standard"])
    return {"shipping_cost": cost, "shipping_type": shipping_type}

def calculate_taxes_cost(order_id: str, state: str) -> dict:
    """Calculates the tax cost for an order based on the shipping state.

    Args:
        order_id: The ID of the order.
        state: The two-letter state code for tax calculation (e.g., "CA", "NY").
    """
    if order_id not in orders:
        return {"error": f"Order {order_id} not found."}

    # Calculate subtotal from cart items
    subtotal = 0.0
    cart_items = orders[order_id].get("cart", [])
    for product_id in cart_items:
        if product_id in products:
            subtotal += products[product_id]["price"]

    rate = TAX_RATES.get(state.upper(), TAX_RATES["default"])
    tax_amount = subtotal * rate
    return {"tax_amount": round(tax_amount, 2), "state": state, "subtotal": subtotal}

def finalize_order_cost(order_id: str, shipping_cost: float, tax_amount: float) -> dict:
    """Finalizes the order cost by adding shipping and taxes, and updates the order.

    Args:
        order_id: The ID of the order.
        shipping_cost: The calculated shipping cost.
        tax_amount: The calculated tax amount.
    """
    if order_id not in orders:
        return {"error": f"Order {order_id} not found."}

    order = orders[order_id]
    
    subtotal = 0.0
    cart_items = order.get("cart", [])
    for product_id in cart_items:
        if product_id in products:
            subtotal += products[product_id]["price"]

    total_cost = subtotal + shipping_cost + tax_amount
    
    order["shipping_cost"] = shipping_cost
    order["tax_amount"] = tax_amount
    order["total_cost"] = round(total_cost, 2)

    return {
        "order_id": order_id,
        "subtotal": round(subtotal, 2),
        "shipping_cost": shipping_cost,
        "tax_amount": tax_amount,
        "total_cost": round(total_cost, 2),
        "order_status": order["order_status"].value
    }

# --- Sub-Agents --- 

shipping_cost_agent = LlmAgent(
    name="shipping_cost_agent",
    description="Calculates the shipping cost for an order.",
    model=model,
    instruction="Given an order ID and a shipping type, calculate the shipping cost using the 'calculate_shipping_cost' tool.",
    tools=[calculate_shipping_cost],
)

taxes_cost_agent = LlmAgent(
    name="taxes_cost_agent",
    description="Calculates the tax amount for an order based on the destination state.",
    model=model,
    instruction="Given an order ID and a state, calculate the tax amount using the 'calculate_taxes_cost' tool.",
    tools=[calculate_taxes_cost],
)

costs_agent = ParallelAgent(
    name="other_costs_agent",
    description="Calculates shipping and taxes in parallel.",
    sub_agents=[shipping_cost_agent, taxes_cost_agent],
)

finalize_agent = LlmAgent(
    name="finalize_order_agent",
    description="Combines shipping and tax costs to finalize the order total.",
    model=model,
    instruction="Given the 'order_id', 'shipping_cost' (from shipping_cost_agent output), and 'tax_amount' (from taxes_cost_agent output), finalize the order's total cost using the 'finalize_order_cost' tool.",
    tools=[finalize_order_cost],
)

# --- Main Shipping Agent (Updated) ---

shipping_instruction = read_prompt("shipping-prompt.txt")

# The original shipping agent functionality (placing an order)
place_order_agent = Agent(
    name="place_order_agent",
    description="Handles the initial placement of an order by setting the address.",
    model=model,
    instruction="Use the 'place_order' tool to add an address and set the order status to PLACED.",
    tools=[place_order],
)

# The new full fulfillment workflow
fulfillment_workflow_agent = SequentialAgent(
    name="fulfillment_workflow",
    description="Calculates costs after an order is placed.",
    sub_agents=[
        place_order_agent,
        costs_agent,
        finalize_agent,
    ],
)

# Main orchestrator for shipping domain
shipping_agent = Agent(
    name="shipping_agent",
    description="Handles all shipping related tasks: placing orders and calculating final costs.",
    model=model,
    instruction=shipping_instruction,
    sub_agents=[fulfillment_workflow_agent],
)