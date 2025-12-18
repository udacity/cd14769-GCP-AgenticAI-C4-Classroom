import os
from google.adk.agents import Agent
# TODO: Import your sub-agents here

model = "gemini-2.5-flash"

def read_prompt(filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, filename)
    with open(file_path, "r") as f:
        return f.read()

orchestrator_instruction = read_prompt("agent-prompt.txt")

root_agent = Agent(
    name="shopping_orchestrator",
    description="Orchestrates the shopping experience.",
    model=model,
    instruction=orchestrator_instruction,
    sub_agents= # TODO: Specify your sub-agents
)
