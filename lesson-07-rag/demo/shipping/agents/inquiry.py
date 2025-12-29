import os
from google.adk.agents import Agent
from toolbox_core import ToolboxSyncClient
from .datastore import datastore_search_tool

model = "gemini-2.5-flash"

def read_prompt(filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "../prompts", filename)
    with open(file_path, "r") as f:
        return f.read()

# --- Database Connection ---
toolbox_url = os.environ.get("TOOLBOX_URL", "http://127.0.0.1:5000")
print(f"Connecting to Toolbox at {toolbox_url}")
db_client = ToolboxSyncClient(toolbox_url)

get_order_tool = db_client.load_tool("get-order")
get_order_agent = Agent(
    name="get_order_agent",
    description="Handles questions about the status of orders",
    model=model,
    instruction=read_prompt("inquiry-order-prompt.txt"),
    tools=[get_order_tool],
)

policy_search_agent = Agent(
    name="datastore_search_agent",
    description="Handles questions about corporate store policies, including shipping policies",
    model=model,
    instruction=read_prompt("inquiry-policy-prompt.txt"),
    tools=[datastore_search_tool],
)

inquiry_agent = Agent(
    name="shipping_inquiry_agent",
    description="Handles questions about shipping policies and tracking.",
    model=model,
    instruction=read_prompt("inquiry-prompt.txt"),
    sub_agents=[get_order_agent, policy_search_agent],
)