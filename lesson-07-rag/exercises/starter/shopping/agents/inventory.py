import os
from pydantic import BaseModel, Field
from google.adk.agents import Agent, LlmAgent

model = "gemini-2.5-flash"

def read_prompt(filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "../prompts", filename)
    with open(file_path, "r") as f:
        return f.read()

# TODO - Connect to Toolbox and load the tool

inventory_instruction = read_prompt("inventory-prompt.txt")

inventory_agent = Agent(
    name="inventory_agent",
    description="Checks product inventory availability.",
    model=model,
    instruction=inventory_instruction,
    tools=[], # TODO - add tool
)

class InventoryData(BaseModel):
    product_id: str = Field(description="The product ID checked.")
    in_stock: bool = Field(description="Whether the product is in stock.")
    count: int = Field(description="The quantity available.")

inventory_data_agent = LlmAgent(
    name="inventory_data_agent",
    description="Checks product inventory and returns structured data.",
    model=model,
    instruction="Check the inventory for the given product ID and return the details.",
    tools=[], # TODO - add tool
    output_schema=InventoryData
)