import os
from pydantic import BaseModel, Field
from google.adk.agents import Agent, LlmAgent
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

class InventoryData(BaseModel):
    product_id: str = Field(description="The product ID checked.")
    in_stock: bool = Field(description="Whether the product is in stock.")
    count: int = Field(description="The quantity available.")

# TODO: Create the inventory_data_agent that uses  the check_inventory tool and return structured InventoryData
inventory_data_agent = None