import os
import json
from typing import AsyncGenerator, Optional
from pydantic import BaseModel, Field
from google.adk.agents import Agent, LlmAgent, BaseAgent, SequentialAgent, InvocationContext
from google.adk.events import Event
from .products import products, product_counts, reorder_status

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

def check_reorder_status(product_id: str):
    """Checks and sets the reorder status for a product.

    Args:
        product_id: The ID of the product to check.
    """
    base_data = check_inventory(product_id)
    if "error" in base_data:
        return base_data
    
    if product_id not in reorder_status:
        reorder_status[product_id] = "ORDERING"
    
    base_data["reorder_status"] = reorder_status[product_id]
    return base_data

class InventoryData(BaseModel):
    product_id: str = Field(description="The product ID checked.")
    in_stock: bool = Field(description="Whether the product is in stock.")
    count: int = Field(description="The quantity available.")
    reorder_status: Optional[str] = Field(description="The reorder status of the product.", default=None)

inventory_instruction = read_prompt("inventory-prompt.txt")
reorder_instruction = "Check the reorder status for the given product ID using the check_reorder_status tool."

inventory_agent = Agent(
    name="inventory_agent",
    description="Checks product inventory availability.",
    model=model,
    instruction=inventory_instruction,
    tools=[check_inventory],
)

# Renamed from inventory_data_agent to separate concerns
check_inventory_agent = LlmAgent(
    name="check_inventory_agent",
    description="Checks product inventory and returns structured data.",
    model=model,
    instruction="Check the inventory for the given product ID and return the details.",
    tools=[check_inventory],
    output_schema=InventoryData
)

# TODO: Create the reorder_agent
# It should use the `check_reorder_status` tool and `reorder_instruction`
reorder_agent = None

class PossiblyReorderAgent(BaseAgent):
    def __init__(self, name: str, reorder_agent: Agent):
        super().__init__(name=name)
        self.reorder_agent = reorder_agent

    async def _run_async_impl(self, context: InvocationContext) -> AsyncGenerator[Event, None]:
        # TODO: Implement the logic to inspect the previous agent's output

        # TODO: If count < 5, run the reorder_agent
        
        # 4. If count >= 5, do nothing (pass)
        pass

# TODO: Create the possibly_reorder_agent instance
possibly_reorder_agent = None

# TODO: Define the inventory_data_agent as a SequentialAgent
# It should run check_inventory_agent followed by possibly_reorder_agent
inventory_data_agent = None
