import os
from typing import Optional
from google.adk.agents import Agent, SequentialAgent, ParallelAgent, LlmAgent
# TODO: Import ToolContext from google.adk.tools
from google.adk.tools import ToolContext

from .products import products
from .order_data import orders, OrderStatus, get_next_order_id
from .inventory import inventory_data_agent

model = "gemini-2.5-flash"

def read_prompt(filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, filename)
    with open(file_path, "r") as f:
        return f.read()

# TODO: Update get_order to accept tool_context and use session state
def get_order(tool_context: ToolContext):
    """
    Retrieves the order for the current session.
    If no order exists, creates a new one and saves the ID to state.
    """
    # TODO: Check if "order_id" exists in tool_context.state
    # TODO: If not, generate a new one, save it to state, and initialize the order
    # TODO: Return the order_id and order object
    pass

# TODO: Update add_to_cart to retrieve order_id from session state
def add_to_cart(product_id: str, tool_context: ToolContext):
    """Adds a product to the specified order's cart.

    Args:
        product_id: The ID of the product to add.
    """
    # TODO: Retrieve order_id from tool_context.state
    # TODO: Return an error if no active session is found
    # TODO: Implement adding to cart logic as before
    pass

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
