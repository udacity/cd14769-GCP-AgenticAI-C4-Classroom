import os
from google.adk.agents import Agent

model = "gemini-2.5-flash"

# Helper to read prompt
def read_prompt(filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, filename)
    with open(file_path, "r") as f:
        return f.read()

# Read instructions
shipping_instruction = read_prompt("shipping-prompt.txt")
inquiry_instruction = read_prompt("inquiry-prompt.txt")
orchestrator_instruction = read_prompt("agent-prompt.txt")

# Create Sub-agents
shipping_agent = Agent(
    name="shipping_agent",
    description="Handles order shipping requests.",
    model=model,
    instruction=shipping_instruction,
)

inquiry_agent = Agent(
    name="shipping_inquiry_agent",
    description="Handles questions about shipping policies and tracking.",
    model=model,
    instruction=inquiry_instruction,
)

# Create Orchestrator
root_agent = Agent(
    name="shipping_orchestrator",
    description="Main orchestrator for shipping tasks.",
    model=model,
    instruction=orchestrator_instruction,
    sub_agents=[shipping_agent, inquiry_agent],
)
