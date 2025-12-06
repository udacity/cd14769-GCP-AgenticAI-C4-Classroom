import os
from google.adk.agents import Agent, LlmAgent
from .datastore import datastore_search_tool

model = "gemini-2.5-flash"

def read_prompt(filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, filename)
    with open(file_path, "r") as f:
        return f.read()

qa_instruction = """
You are a helpful product expert.
Answer questions about products using the `search_product_info` tool.
If the information is not found, politely say so.
"""

product_qa_agent = LlmAgent(
    name="product_qa_agent",
    description="Answers questions about product details, features, and manuals.",
    model=model,
    instruction=qa_instruction,
    tools=[datastore_search_tool],
)
