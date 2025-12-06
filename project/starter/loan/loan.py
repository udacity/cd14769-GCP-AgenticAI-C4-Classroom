import logging
import os
from typing import AsyncGenerator

from google.adk.agents import SequentialAgent, LlmAgent, BaseAgent, InvocationContext
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent, AGENT_CARD_WELL_KNOWN_PATH
from google.adk.events import Event, EventActions
from google.genai.types import Content, Part

def load_instructions( prompt_file: str ):
  script_dir = os.path.dirname(os.path.abspath(__file__))
  instruction_file_path = os.path.join( script_dir, prompt_file )
  with open(instruction_file_path, "r") as f:
    return f.read()

# TODO: Create loan_info_tool (stage 2)

# TODO: Create agent that gets the requested loan value (stage 4)

class TotalValueAgent(BaseAgent):

  def __init__(
    self,
    name: str,
  ):
    super().__init__(
      name=name,
    )

  async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:
    # TODO: Implement

# TODO: Instantiate the TotalValueAgent to use (stage 4)

# TODO: Create agent that checks user's equity (stage 4)

# TODO: Create agent that uses these three agents to approve or not approve of a loan
