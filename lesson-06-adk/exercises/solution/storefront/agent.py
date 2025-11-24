import os
from google.adk.agents import Agent
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent, AGENT_CARD_WELL_KNOWN_PATH

model = "gemini-2.5-flash"

def read_prompt(filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, filename)
    with open(file_path, "r") as f:
        return f.read()

# Define the remote A2A agent for shipping
# Assuming the shipping agent is running on localhost:8000/a2a/shipping
shipping_agent = RemoteA2aAgent(
    name="shipping_agent",
    agent_card=f"http://localhost:8000/a2a/shipping{AGENT_CARD_WELL_KNOWN_PATH}"
)

# Define the remote A2A agent for shopping
# Assuming the shopping agent is running on localhost:8000/a2a/shopping
shopping_agent = RemoteA2aAgent(
    name="shopping_agent",
    agent_card=f"http://localhost:8000/a2a/shopping{AGENT_CARD_WELL_KNOWN_PATH}"
)

storefront_instruction = read_prompt("agent-prompt.txt")

root_agent = Agent(
    name="storefront_agent",
    description="Main storefront orchestrator.",
    model=model,
    instruction=storefront_instruction,
    sub_agents=[shipping_agent, shopping_agent],
)
