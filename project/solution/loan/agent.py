import os
from google.adk.a2a.utils.agent_to_a2a import to_a2a
from google.adk.agents import Agent
from google.adk.sessions import InMemorySessionService
from .loan import loan_info_tool, loan_approval_agent

# Configure short-term session to use the in-memory service
session_service = InMemorySessionService()

# Read the instructions from a file in the same
# directory as this agent.py file.
script_dir = os.path.dirname(os.path.abspath(__file__))
instruction_file_path = os.path.join(script_dir, "agent-prompt.txt")
with open(instruction_file_path, "r") as f:
  instruction = f.read()

# Set up the tools that we will be using for the root agent
tools=[
  loan_info_tool
]

sub_agents = [
  loan_approval_agent,
]

# Use the Gemini 2.5 Flash model since it performs quickly
# and handles the processing well.
model = "gemini-2.5-pro"

# Create our agent
root_agent = Agent(
  name="loan_account_agent",
  description=(
    "Agent to answer questions about bank loan accounts."
  ),
  model=model,
  instruction=instruction,
  tools=tools,
  sub_agents=sub_agents,
)
