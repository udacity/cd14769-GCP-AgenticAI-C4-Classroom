import os
from google.adk.agents import Agent
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

search_instruction = read_prompt("search-prompt.txt")

search_agent = Agent(
    name="search_agent",
    description="Searches for products in the catalog.",
    model=model,
    instruction=search_instruction,
    tools=[search_products],
)
