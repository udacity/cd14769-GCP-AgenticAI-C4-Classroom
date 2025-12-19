import os
from google.adk.agents import Agent, LlmAgent
# TODO: Import the datastore_search_tool from .datastore

model = "gemini-2.5-flash"

def read_prompt(filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, filename)
    with open(file_path, "r") as f:
        return f.read()

# TODO: Read the instruction from "product-qa-prompt.txt"

# TODO: Define the product_qa_agent as an LlmAgent
# It should use the datastore_search_tool
