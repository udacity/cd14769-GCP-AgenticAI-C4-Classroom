import os
from google.adk.agents import Agent
from toolbox_core import ToolboxSyncClient
from .datastore import datastore_search_tool

model = "gemini-2.5-flash"

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

inquiry_instruction = read_prompt("inquiry-prompt.txt")

inquiry_agent = Agent(
    name="shipping_inquiry_agent",
    description="Handles questions about shipping policies and tracking.",
    model=model,
    instruction=inquiry_instruction,
    tools=[get_order_tool, datastore_search_tool],
)