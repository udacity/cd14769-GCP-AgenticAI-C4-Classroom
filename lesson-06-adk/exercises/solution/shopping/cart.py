import os
import logging
from google.adk.agents import Agent, SequentialAgent, ParallelAgent, LlmAgent
from google.adk.tools import ToolContext
from toolbox_core import ToolboxSyncClient

from .products import products
from .inventory import inventory_data_agent

model = "gemini-2.5-flash"
logger = logging.getLogger(__name__)

def read_prompt(filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, filename)
    with open(file_path, "r") as f:
        return f.read()

# --- Database Connection ---
toolbox_url = os.environ.get("TOOLBOX_URL", "http://127.0.0.1:5000")
print(f"Connecting to Toolbox at {toolbox_url}")
db_client = ToolboxSyncClient(toolbox_url)

get_order_tool = db_client.load_tool("get-order")
create_order_tool = db_client.load_tool("create-order")
add_item_to_cart_tool = db_client.load_tool("add-item-to-cart")
get_open_order_for_user_tool = db_client.load_tool("get-open-order-for-user")

# --- Tools ---

def get_user_id(tool_context: ToolContext):
    """Returns the user ID for the current session."""
    logger.info(f"********** ToolContext in get_user_id: {tool_context}")
    logger.info(f"********** InvocationContext in get_user_id: {tool_context._invocation_context}")
    logger.info(f"********** Session in get_user_id: {tool_context.session}")
    logger.info(f"********** UserContent in get_user_id: {tool_context.user_content}")
    return {
        "user_id": tool_context.session.user_id
    }

# --- Sub-Agents ---

get_order_agent = LlmAgent(
    name="get_order_agent",
    description="Ensures an active order session exists.",
    model=model,
    instruction=read_prompt("get-order-prompt.txt"),
    tools=[get_user_id, get_open_order_for_user_tool, create_order_tool],
)

add_item_agent = LlmAgent(
    name="add_item_agent",
    description="Adds the item to the cart.",
    model=model,
    instruction=read_prompt("add-item-prompt.txt"),
    tools=[get_order_tool, add_item_to_cart_tool],
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
