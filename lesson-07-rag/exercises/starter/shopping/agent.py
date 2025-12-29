import os
from google.adk.agents import Agent
from .agents.search import search_agent
from .agents.inventory import inventory_agent
from .agents.cart import cart_agent
# TODO: Import the product_qa_agent

model = "gemini-2.5-flash"

def read_prompt(filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "prompts", filename)
    with open(file_path, "r") as f:
        return f.read()

orchestrator_instruction = read_prompt("agent-prompt.txt")

root_agent = Agent(
    name="shopping_orchestrator",
    description="Orchestrates the shopping experience.",
    model=model,
    instruction=orchestrator_instruction,
    sub_agents=[search_agent, inventory_agent, cart_agent], # TODO: Add product_qa_agent
)