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
    if product_id in products:
        count = product_counts.get(product_id, 0)
        return {"product_id": product_id, "in_stock": count > 0, "count": count}
    else:
        return {"error": "Product ID not found"}

inventory_instruction = read_prompt("inventory-prompt.txt")

inventory_agent = Agent(
    name="inventory_agent",
    description="Checks product inventory availability.",
    model=model,
    instruction=inventory_instruction,
    tools=[check_inventory],
)
