import os
import random
from typing import AsyncGenerator
from google.adk.agents import Agent, LlmAgent, BaseAgent, InvocationContext
from google.adk.events import Event
from toolbox_core import ToolboxSyncClient

model = "gemini-2.5-flash"

def read_prompt(filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "../prompts", filename)
    with open(file_path, "r") as f:
        return f.read()

# Connect to Toolbox
toolbox_url = os.environ.get("TOOLBOX_URL", "http://127.0.0.1:5001")
print(f"Connecting to Toolbox at {toolbox_url}")
db_client = ToolboxSyncClient(toolbox_url)

# Load the tool from the toolbox (MCP)
search_products_tool = db_client.load_tool("search-products")

search_instruction = read_prompt("search-prompt.txt")
search_broad_instruction = read_prompt("search-broad-prompt.txt")

# Original Search Agent (Exact/Phrase match)
# We now use the tool, but the instructions still guide the model to search carefully
search_agent_exact = LlmAgent(
    name="search_agent_exact",
    description="Searches for products.",
    model=model,
    instruction=search_instruction,
    tools=[search_products_tool],
)

# New Broad Search Agent
# We now use the tool, but instructions might encourage trying variations
search_agent_broad = LlmAgent(
    name="search_agent_broad",
    description="Searches for products with broader queries.",
    model=model,
    instruction=search_broad_instruction,
    tools=[search_products_tool],
)

class SearchRouter(BaseAgent):
    """
    Routes to either exact or broad search based on a random threshold (A/B testing).
    """

    agent_a: Agent
    agent_b: Agent
    agent_b_rate: float

    def __init__(self, name: str, agent_a: Agent, agent_b: Agent, agent_b_rate: float = 0.5):
        super().__init__(
            name=name,
            agent_a=agent_a,
            agent_b=agent_b,
            agent_b_rate=agent_b_rate
        )

    async def _run_async_impl(self, context: InvocationContext) -> AsyncGenerator[Event, None]:
        # Simple random routing
        if random.random() < (1-self.agent_b_rate):
            selected_agent = self.agent_a
        else:
            selected_agent = self.agent_b
            
        async for event in selected_agent.run_async(context):
            yield event

# Main Search Agent (Router)
# Default threshold 0.5 means roughly 50/50 split
search_agent = SearchRouter(
    name="search_agent_router",
    agent_a=search_agent_exact,
    agent_b=search_agent_broad,
    agent_b_rate=0.5
)
