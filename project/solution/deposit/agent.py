import os

from google.adk.a2a.utils.agent_to_a2a import to_a2a
from google.adk.agents import Agent
from google.adk.sessions import InMemorySessionService

from toolbox_core import ToolboxSyncClient

# Configure short-term session to use the in-memory service
session_service = InMemorySessionService()

# Read the instructions from a file in the same
# directory as this agent.py file.
script_dir = os.path.dirname(os.path.abspath(__file__))
instruction_file_path = os.path.join(script_dir, "agent-prompt.txt")
with open(instruction_file_path, "r") as f:
  instruction = f.read()

# Set up the tools that we will be using for the root agent
toolbox_url = os.environ.get("TOOLBOX_URL", "http://127.0.0.1:5000")
print(f"Connecting to Toolbox at {toolbox_url}")
db_client = ToolboxSyncClient( toolbox_url )
tools=[
  db_client.load_tool("get-accounts"),
  db_client.load_tool("get-balance"),
  db_client.load_tool("check-minimum-balance"),
  db_client.load_tool("get-transactions"),
]

# Use the Gemini 2.5 Flash model since it performs quickly
# and handles the processing well.
model = "gemini-2.5-pro"

# Create our agent
root_agent = Agent(
  name="deposit_account_agent",
  description=(
    "Agent to answer questions about bank deposit accounts."
  ),
  model=model,
  instruction=instruction,
  tools=tools,
)
