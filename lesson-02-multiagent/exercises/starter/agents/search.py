import os
from google.adk.agents import Agent
from .products import products

model = "gemini-2.5-flash"

def read_prompt(filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "../prompts", filename)
    with open(file_path, "r") as f:
        return f.read()

def search_products(query: str):
    """Searches for products by name or description.

    Args:
        query: The search query string.
    """
    # TODO: Implement product search logic using the 'products' dictionary
    # It should check if the query is in the product name or description (case insensitive)
    # Return a list of matching products (id, name, price)
    pass

search_instruction = read_prompt("search-prompt.txt")

# TODO: Create the search_agent
# It should use the search_products tool
search_agent = None
