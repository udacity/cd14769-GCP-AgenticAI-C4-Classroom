import os
from pydantic import BaseModel, Field
from typing import Optional, AsyncGenerator
from google.adk.agents import Agent, SequentialAgent, ParallelAgent, LlmAgent, InvocationContext, BaseAgent
from google.adk.events import Event
from google.adk.tools.tool_context import ToolContext
from .order_data import orders, OrderStatus
from .rates import SHIPPING_RATES, TAX_RATES
from .products import products

model = "gemini-2.5-flash"

def read_prompt(filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, filename)
    with open(file_path, "r") as f:
        return f.read()

# --- Schemas ---

class ShippingCostOutput(BaseModel):
    shipping_cost: float = Field(description="The calculated shipping cost.")
    shipping_type: str = Field(description="The type of shipping used.")

class TaxCostOutput(BaseModel):
    tax_amount: float = Field(description="The calculated tax amount.")
    state: str = Field(description="The state used for tax calculation.")
    subtotal: float = Field(description="The subtotal of the order.")

class ComputeOrderOutput(BaseModel):
    order_id: str = Field(description="The ID of the order.")
    subtotal: float = Field(description="The order subtotal.")
    shipping_cost: float = Field(description="The shipping cost.")
    tax_amount: float = Field(description="The tax amount.")
    total_cost: float = Field(description="The final total cost.")
    order_status: str = Field(description="The status of the order.")

class AddressOutput(BaseModel):
    name: str
    address_1: str
    address_2: Optional[str] = None
    city: str
    state: str
    postal_code: str

class PlaceOrderOutput(BaseModel):
    cart: list = Field(description="List of items in the cart.")
    address: AddressOutput = Field(description="The shipping address.")

# --- Tools ---

def place_order(order_id: str, address: dict, tool_context: ToolContext ):
    """Places an order by adding the shipping address and setting status to PLACED.
    Also saves the order being worked on in the session state

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
    tool_context.state["order"] = order

    return {
        "cart": order.get("cart"),
        "address": order.get("address"),
    }

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

def compute_subtotal(order) -> float:
    subtotal = 0.0
    cart_items = order.get("cart", [])
    for product_id in cart_items:
        if product_id in products:
            subtotal += products[product_id]["price"]
    return subtotal

def compute_order_cost(order_id: str, shipping_cost: float, tax_amount: float) -> dict:
    """Compute the order cost by adding shipping and taxes, and updates the order.

    Args:
        order_id: The ID of the order.
        shipping_cost: The calculated shipping cost.
        tax_amount: The calculated tax amount.
    """
    if order_id not in orders:
        return {"error": f"Order {order_id} not found."}

    order = orders[order_id]
    subtotal = compute_subtotal(order)
    total_cost = subtotal + shipping_cost + tax_amount
    
    order["shipping_cost"] = shipping_cost
    order["tax_amount"] = tax_amount
    order["total_cost"] = round(total_cost, 2)
    order["order_status"] = OrderStatus.PENDING # Set to PENDING while waiting approval

    return {
        "order_id": order_id,
        "subtotal": round(subtotal, 2),
        "shipping_cost": shipping_cost,
        "tax_amount": tax_amount,
        "total_cost": round(total_cost, 2),
        "order_status": order["order_status"].value
    }

def approve_order(order_id: str) -> dict:
    """Approves the order and sets its status to PLACED.

    Args:
        order_id: The ID of the order to approve.
    """
    if order_id not in orders:
        return {"error": f"Order {order_id} not found."}

    order = orders[order_id]
    order["order_status"] = OrderStatus.PLACED

    return {
        "order_id": order_id,
        "order_status": order["order_status"].value,
        "message": "Order successfully approved and placed."
    }


# --- Sub-Agents --- 

shipping_cost_agent = LlmAgent(
    name="shipping_cost_agent",
    description="Calculates the shipping cost for an order.",
    model=model,
    instruction=read_prompt("shipping-cost-prompt.txt"),
    tools=[calculate_shipping_cost],
    output_schema=ShippingCostOutput,
)

free_shipping_agent = LlmAgent(
    name="free_shipping_agent",
    description="Calculates shipping cost for free shipping eligible orders.",
    model=model,
    instruction=read_prompt("free-shipping-prompt.txt"),
    tools=[calculate_shipping_cost],
    output_schema=ShippingCostOutput,
)

class ShippingRouter(BaseAgent):

    free_threshold: float
    free_agent: Agent
    standard_agent: Agent

    def __init__(self, name: str, free_agent: Agent, standard_agent: Agent, free_threshold: float):
      super().__init__(
          name=name,
          free_threshold=free_threshold,
          free_agent=free_agent,
          standard_agent=standard_agent,
      )

    async def _run_async_impl(self, context: InvocationContext) -> AsyncGenerator[Event, None]:
      order = context.session.state.get("order")
      subtotal = compute_subtotal(order)
      is_free = subtotal >= self.free_threshold

      if is_free:
          subagent = self.free_agent
      else:
          subagent = self.standard_agent

      async for event in subagent.run_async(context):
          yield event

shipping_router_agent = ShippingRouter(
    name="shipping_router_agent",
    free_agent=free_shipping_agent,
    standard_agent=shipping_cost_agent,
    free_threshold=100.00,
)

taxes_cost_agent = LlmAgent(
    name="taxes_cost_agent",
    description="Calculates the tax amount for an order based on the destination state.",
    model=model,
    instruction=read_prompt("taxes-cost-prompt.txt"),
    tools=[calculate_taxes_cost],
    output_schema=TaxCostOutput,
)

costs_agent = ParallelAgent(
    name="other_costs_agent",
    description="Calculates shipping and taxes in parallel.",
    sub_agents=[shipping_router_agent, taxes_cost_agent],
)

compute_order_agent = LlmAgent(
    name="compute_order_agent",
    description="Combines shipping and tax costs to compute the order total.",
    model=model,
    instruction=read_prompt("compute-order-prompt.txt"),
    tools=[compute_order_cost],
    output_schema=ComputeOrderOutput,
)

place_order_agent = LlmAgent(
    name="place_order_agent",
    description="Handles the initial placement of an order by setting the address.",
    model=model,
    instruction=read_prompt("place-order-prompt.txt"),
    tools=[place_order],
    output_schema=PlaceOrderOutput,
)

order_summary_agent = LlmAgent(
    name="order_summary_agent",
    description="Summarizes the order details for the customer.",
    model=model,
    instruction=read_prompt("order-summary-prompt.txt"),
)

approve_order_agent = LlmAgent(
    name="approve_order_agent",
    description="Approves the order and sets status to PLACED upon user confirmation.",
    model=model,
    instruction=read_prompt("approve-order-prompt.txt"),
    tools=[approve_order],
)

# --- Main Shipping Agent ---

shipping_instruction = read_prompt("shipping-prompt.txt")

# The new full fulfillment workflow
fulfillment_workflow_agent = SequentialAgent(
    name="fulfillment_workflow",
    description="Calculates costs after an order is placed.",
    sub_agents=[
        place_order_agent,
        costs_agent,
        compute_order_agent,
        order_summary_agent,
    ],
)

# Main orchestrator for shipping domain
shipping_agent = Agent(
    name="shipping_agent",
    description="Handles all shipping related tasks: placing orders and calculating final costs.",
    model=model,
    instruction=shipping_instruction,
    sub_agents=[fulfillment_workflow_agent, approve_order_agent],
)