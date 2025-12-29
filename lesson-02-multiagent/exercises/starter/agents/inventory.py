import os
from google.adk.agents import Agent
from .products import products, product_counts

model = "gemini-2.5-flash"

def read_prompt(filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "../prompts", filename)
    with open(file_path, "r") as f:
        return f.read()

def check_inventory(product_id: str):
    """Checks if a product is in stock.

    Args:
        product_id: The ID of the product to check.
    """
    # TODO: Implement inventory check logic using 'product_counts'
    # Return whether it is in stock and the count
    pass

inventory_instruction = read_prompt("inventory-prompt.txt")

# TODO: Create the inventory_agent
# It should use the check_inventory tool
inventory_agent = None
