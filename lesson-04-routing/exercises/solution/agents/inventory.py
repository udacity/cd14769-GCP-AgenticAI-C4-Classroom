import os
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
reorder_instruction = read_prompt("reorder-prompt.txt")

# Renamed from inventory_data_agent
check_inventory_agent = LlmAgent(
    name="check_inventory_agent",
    description="Checks product inventory and returns structured data.",
    model=model,
    instruction="Check the inventory for the given product ID and return the details.",
    tools=[check_inventory],
    output_schema=InventoryData
)

reorder_agent = LlmAgent(
    name="reorder_agent",
    description="Checks and updates reorder status.",
    model=model,
    instruction=reorder_instruction,
    tools=[check_reorder_status],
    output_schema=InventoryData
)

class PossiblyReorderAgent(BaseAgent):
    def __init__(self, name: str, reorder_agent: Agent):
        super().__init__(name=name)
        self.reorder_agent = reorder_agent

    async def _run_async_impl(self, context: InvocationContext) -> AsyncGenerator[Event, None]:
        # context.input is the output of the previous agent (check_inventory_agent)
        # It should be an instance of InventoryData
        input_data = context.input
        
        if isinstance(input_data, InventoryData) and input_data.count < 5:
            # Create a new context for the reorder agent
            reorder_context = InvocationContext(input=f"Check reorder status for {input_data.product_id}")
            async for event in self.reorder_agent.run_async(reorder_context):
                yield event
        else:
            # If not reordering, we just yield (effectively passing through or ending this step)
            # In a SequentialAgent, if this agent yields nothing, the previous output might be preserved 
            # or the chain ends. Assuming "just yields" means no action.
            pass

possibly_reorder_agent = PossiblyReorderAgent(
    name="possibly_reorder_agent",
    reorder_agent=reorder_agent
)

inventory_data_agent = SequentialAgent(
    name="inventory_data_agent",
    description="Checks inventory and optionally checks reorder status if stock is low.",
    sub_agents=[check_inventory_agent, possibly_reorder_agent]
)
