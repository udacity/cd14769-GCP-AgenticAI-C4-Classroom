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
    # TODO: Implement broad search logic
    # Split query into words and check if any word is in name or description
    pass

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

# TODO: Create the New Broad Search Agent
# It should use search_products_broad tool
search_agent_broad = None

# TODO: Implement the SearchRouter class extending BaseAgent
class SearchRouter(BaseAgent):
    """
    Routes to either exact or broad search based on a random threshold (A/B testing).
    """
    # ... implementation ...
    pass

# TODO: Instantiate the Main Search Agent (Router)
# It should switch between search_agent_exact and search_agent_broad
search_agent = None