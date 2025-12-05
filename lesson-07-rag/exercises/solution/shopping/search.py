import os
import random
from typing import AsyncGenerator
from google.adk.agents import Agent, LlmAgent, BaseAgent, InvocationContext
from google.adk.events import Event
from .products import products

model = "gemini-2.5-flash"

def read_prompt(filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, filename)
    with open(file_path, "r") as f:
        return f.read()

def search_products(query: str):
    """Searches for products by name or description.

    Args:
        query: The search query string.
    """
    results = []
    for pid, pdata in products.items():
        if query.lower() in pdata["name"].lower() or query.lower() in pdata["description"].lower():
            results.append({"id": pid, "name": pdata["name"], "price": pdata["price"]})
    return results

def search_products_broad(query: str):
    """Searches for products matching any word in the query.

    Args:
        query: The search query string.
    """
    results = []
    words = query.lower().split()
    for pid, pdata in products.items():
        name_lower = pdata["name"].lower()
        desc_lower = pdata["description"].lower()
        
        for word in words:
            if word in name_lower or word in desc_lower:
                results.append({"id": pid, "name": pdata["name"], "price": pdata["price"]})
                break # Avoid duplicates if multiple words match
    return results

search_instruction = read_prompt("search-prompt.txt")
search_broad_instruction = read_prompt("search-broad-prompt.txt")

# Original Search Agent (Exact/Phrase match)
search_agent_exact = LlmAgent(
    name="search_agent_exact",
    description="Searches for products using phrase matching.",
    model=model,
    instruction=search_instruction,
    tools=[search_products],
)

# New Broad Search Agent
search_agent_broad = LlmAgent(
    name="search_agent_broad",
    description="Searches for products matching any query word.",
    model=model,
    instruction=search_broad_instruction,
    tools=[search_products_broad],
)

class SearchRouter(BaseAgent):
    """
    Routes to either exact or broad search based on a random threshold (A/B testing).
    The threshold determines what percentage of requests will go to agent_b.
    So a threshold of 0.90 means that 10% of attempts will go to agent_a on average.
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