import logging
import os
from typing import AsyncGenerator

from google.adk.agents import SequentialAgent, LlmAgent, BaseAgent, InvocationContext, ParallelAgent
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent, AGENT_CARD_WELL_KNOWN_PATH
from google.adk.events import Event, EventActions
from google.adk.tools.agent_tool import AgentTool
from google.genai.types import Content, Part

from toolbox_core import ToolboxSyncClient

from pydantic import BaseModel, Field
from typing import Literal

logger = logging.getLogger("google_adk.loan")

def load_instructions( prompt_file: str ):
  script_dir = os.path.dirname(os.path.abspath(__file__))
  instruction_file_path = os.path.join( script_dir, prompt_file )
  with open(instruction_file_path, "r") as f:
    return f.read()

toolbox_url = os.environ.get("TOOLBOX_URL", "http://127.0.0.1:5000")
print(f"Connecting to Toolbox at {toolbox_url}")
db_client = ToolboxSyncClient( toolbox_url )
loan_info_tool = db_client.load_tool("get-loan-info")
outstanding_balance_tool = db_client.load_tool("get-total-outstanding-balance")

class LoanRequest(BaseModel):
  amount: int | float = Field(description="The amount of the loan requested.")
  loan_type: Literal["auto", "rv", "home improvement", "personal"] = Field(description="The type of loan.")

loan_approval_get_requested_value_agent = LlmAgent(
  name="loan_approval_get_requested_value_agent",
  description="Get how much the user has requested for their loan and what type of loan they are requesting.",
  model="gemini-2.5-flash-lite",
  instruction=load_instructions( "loan-request-prompt.txt" ),
  output_schema=LoanRequest,
  output_key="requested"
)

class OutstandingBalance(BaseModel):
  total: float = Field(description="The total balance of outstanding loans.")

loan_approval_get_outstanding_balance_agent = LlmAgent(
  name="loan_approval_get_outstanding_balance_agent",
  description="Get the current outstanding balance the user has on their loans.",
  model="gemini-2.5-flash",
  instruction=load_instructions( "outstanding-balance-prompt.txt" ),
  output_schema=OutstandingBalance,
  output_key="outstanding_balance",
  tools=[outstanding_balance_tool]
)

loan_approval_data_agent = SequentialAgent(
  name="loan_approval_data_agent",
  sub_agents=[
    loan_approval_get_requested_value_agent,
    loan_approval_get_outstanding_balance_agent,
  ],
)

policy_static_instruction_uri="gs://example-bank-info/loan-policy.pdf"

policy_static_instruction=[
    Part(text="""Please act as a loan officer. Your only task is to look at the attached loan policy and extract the loan approval criteria."""),
    Part.from_uri(
      file_uri=policy_static_instruction_uri,
      mime_type="application/pdf"
    )
]

CustomerRating = Literal["excellent", "great", "good", "fair", "poor"]

class Policy(BaseModel):
  debt_equity_ratio: int
  minimum_rating: CustomerRating = Field(description="The minimum customer rating")

loan_approval_policy_agent = LlmAgent(
  name="loan_approval_policy_agent",
  description="Given a pdf file with the current loan policy, and previous information about the customer's request, get the criteria to be used to evaluate a loan.",
  model="gemini-2.5-flash",
  static_instruction=Content(parts=policy_static_instruction),
  output_schema=Policy,
  output_key="policy"
)

class TotalValueAgent(BaseAgent):

  def __init__(
    self,
    name: str,
  ):
    super().__init__(
      name=name,
    )

  async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:
    requested = ctx.session.state["requested"]
    outstanding_balance = ctx.session.state["outstanding_balance"]
    policy = ctx.session.state["policy"]

    logger.info(f"requested {requested}")
    logger.info(f"outstanding_balance {outstanding_balance}")

    total_loans = outstanding_balance["total"] + requested["amount"]
    min_equity = total_loans / policy["debt_equity_ratio"]
    total_value = {
      "current_loans": outstanding_balance,
      "total_loans": total_loans,
      "min_equity": min_equity,
    }
    state_delta = {
      "total_value": total_value,
      "min_equity": min_equity,
    }
    actions = EventActions( state_delta=state_delta )
    yield Event(
      author=self.name,
      content=Content(
        parts=[
          Part(
            text=f"Is the total balance of all my deposit accounts greater than {min_equity}?"
          )
        ]
      ),
      actions=actions,
    )


loan_approval_get_total_value_agent = TotalValueAgent(
  name="loan_approval_get_total_value_agent",
)

deposit_equity_agent = RemoteA2aAgent(
  name="deposit_equity_agent",
  agent_card=f"http://localhost:8000/a2a/deposit{AGENT_CARD_WELL_KNOWN_PATH}",
)

class CheckEquity(BaseModel):
  sufficient_equity: bool = Field(description="True if the equity on deposit is greater than the value requested. False if less.")

loan_approval_check_equity_agent = LlmAgent(
  name="loan_approval_check_equity_agent",
  model="gemini-2.5-flash",
  instruction=load_instructions( "check-equity-prompt.txt" ),
  tools=[
    AgentTool(agent=deposit_equity_agent)
  ],
  output_schema=CheckEquity,
  output_key="check_equity",
)

loan_approval_debt_equity_agent = SequentialAgent(
  name="loan_approval_debt_equity_agent",
  sub_agents=[
    loan_approval_get_total_value_agent,
    loan_approval_check_equity_agent,
  ]
)

# Note: It also may be reasonable to have the total value computed
# as part of a tool, and then to have the debt_equity_agent access
# both this total value tool and the deposit equity tool.

user_profile_base_instruction = load_instructions( "user-profile-base-prompt.txt" )

user_profile_uri = "gs://example-bank-info/loan-customer-info.pdf"

user_profile_instruction=[
  Part(text=user_profile_base_instruction),
  Part(text="""Here is the loan policy:"""),
  Part.from_uri(
    file_uri=policy_static_instruction_uri,
    mime_type="application/pdf"
  ),
  Part(text="""Here is the customer profile:"""),
  Part.from_uri(
    file_uri=user_profile_uri,
    mime_type="application/pdf"
  )
]

class UserProfile(BaseModel):
  customer_rating: CustomerRating = Field(description="Based on the criteria and the customer info, how would we rate this customer?")
  justification: str = Field(description="Why do we give the customer the rating we have?")

loan_approval_user_profile_agent = LlmAgent(
  name="loan_approval_user_profile_agent",
  model="gemini-2.5-flash",
  static_instruction=Content(parts=user_profile_instruction),
  output_schema=UserProfile,
  output_key="user_profile",
)

loan_approval_review_agent = ParallelAgent(
  name="loan_approval_review_agent",
  sub_agents=[
    loan_approval_user_profile_agent,
    loan_approval_debt_equity_agent,
  ]
)

loan_approval_report_agent = LlmAgent(
  name="loan_approval_report_agent",
  description="Report if a loan would be approved or not",
  model="gemini-2.5-pro",
  instruction=load_instructions( "approval-report-prompt.txt" ),
)

loan_approval_agent = SequentialAgent(
  name="loan_approval_agent",
  description="Based on current account balances and the requested value, approve or decline the loan.",
  sub_agents=[
    loan_approval_data_agent,
    loan_approval_policy_agent,
    loan_approval_review_agent,
    loan_approval_report_agent,
  ],
)