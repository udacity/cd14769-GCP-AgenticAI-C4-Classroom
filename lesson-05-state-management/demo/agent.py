import os
from google.adk.agents import Agent
from .agents.shipping import shipping_agent
from .agents.inquiry import inquiry_agent

model = "gemini-2.5-flash"

# Helper to read prompt
def read_prompt(filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "prompts", filename)
    with open(file_path, "r") as f:
        return f.read()

# Read instructions
orchestrator_instruction = read_prompt("agent-prompt.txt")

# Create Orchestrator
root_agent = Agent(
    name="shipping_orchestrator",
    description="Main orchestrator for shipping tasks.",
    model=model,
    instruction=orchestrator_instruction,
    sub_agents=[shipping_agent, inquiry_agent],
)
