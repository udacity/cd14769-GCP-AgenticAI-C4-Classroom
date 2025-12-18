# Implementing Multi-Agent Architectures with ADK

We will learn how to implement a basic multi-agent system using the ADK toolkit
by creating a shipping orchestrator that delegates tasks to specialized
sub-agents.

---

## Overview

### What You'll Learn

Learners will understand how to structure a multi-agent system where a root
agent acts as an orchestrator, delegating specific intents to dedicated
sub-agents. This modular approach improves maintainability and allows for more
complex workflows.

Learning objectives:

- Instantiate multiple ADK agents and connect them as sub-agents.
- Define specialized roles and system prompts for each agent.
- Implement basic tool-calling within individual agents.

### Prerequisites

- Basic understanding of Python.
- Familiarity with the ADK (Agent Development Kit).
- Access to Google Cloud with Vertex AI enabled.

---

## Understanding the Concept

### The Problem

In a complex e-commerce system, a single agent trying to handle everything—from
order placement and shipping to policy inquiries and tracking—can become
bloated, difficult to manage, and prone to errors. Its prompt becomes too long,
and it may struggle to select the right tool or respond accurately to diverse
requests.

### The Solution

A multi-agent architecture solves this by breaking down responsibilities. An
**Orchestrator** acts as the front door, determining the customer's intent and
delegating the task to a specialized **Worker Agent**. This keeps individual
agents focused, their prompts concise, and their toolsets relevant.

### How It Works

**Step 1: Orchestration**
The `root_agent` (Orchestrator) receives the initial customer request. It
may not have tools of its own but knows about its sub-agents. It uses its
instructions to decide where to route the request.

**Step 2: Delegation**
Once an intent is identified, the Orchestrator hands off the conversation to
either the `shipping_agent` or the `inquiry_agent`.

**Step 3: Execution**
The worker agent uses its specialized tools (like `place_order` or
`get_order_info`) to fulfill the request and responds to the customer.

### Key Terms

**Orchestrator**: A high-level agent that manages the flow of conversation and
delegates tasks to other agents.
**Sub-agent**: A specialized agent that performs specific tasks under the
direction of an orchestrator.
**Delegation**: The process where one agent hands off control or a task to
another agent.

---

## Code Walkthrough

### Repository Structure

```
shipping/
├── agent.py          # Root agent configuration and orchestration logic
├── shipping.py       # specialized agent for processing shipments
├── inquiry.py        # specialized agent for handling order inquiries
├── order_data.py     # Mock database of orders
├── agent-prompt.txt  # System prompt for the orchestrator
├── shipping-prompt.txt # System prompt for the shipping agent
└── inquiry-prompt.txt  # System prompt for the inquiry agent
```

### Step 1: Defining the Orchestrator

The orchestrator is defined in `agent.py`. It includes references to its
`sub_agents`.

```python
# Create Orchestrator
root_agent = Agent(
  name="shipping_orchestrator",
  description="Main orchestrator for shipping tasks.",
  model=model,
  instruction=orchestrator_instruction,
  sub_agents=[shipping_agent, inquiry_agent],
)
```

**Key points:**

- The `sub_agents` parameter is crucial for defining the hierarchy.
- A sub-agent may have one, and only one, parent agent. A parent agent may 
  have multiple sub-agents.
- The orchestrator's prompt focuses on routing and delegation logic.

### Step 2: Implementing Specialized Agents

The `shipping_agent` in `shipping.py` is focused on a single task: placing
orders.

```python
shipping_agent = Agent(
  name="shipping_agent",
  description="Handles order shipping requests.",
  model=model,
  instruction=shipping_instruction,
  tools=[place_order],
)
```

**Key points:**

- Each sub-agent has its own specific `instruction` and `tools`.
- This isolation makes debugging and extending the system much easier.

### Complete Example

The system is initialized by importing the sub-agents into the main `agent.py`.

```python
import os
from google.adk.agents import Agent
from .shipping import shipping_agent
from .inquiry import inquiry_agent

model = "gemini-2.5-flash"


# Helper to read prompt
def read_prompt(filename):
  script_dir = os.path.dirname(os.path.abspath(__file__))
  file_path = os.path.join(script_dir, filename)
  with open(file_path, "r") as f:
    return f.read()


# Read instructions
orchestrator_instruction = read_prompt("agent-prompt.txt")

# Create Orchestrator
root_agent = Agent(
  name="shipping_orchestrator",
  description="Main orchestrator for shipping tasks.",
  model=model,
  instruction=orchestrator_instruction,
  sub_agents=[shipping_agent, inquiry_agent],
)
```

**How it works:**

1. **Initialization**: The `root_agent` is created with a list of `sub_agents`.
2. **Intent Discovery**: When a user asks "Where is my order?", the orchestrator
   sees that `shipping_inquiry_agent` is best suited for this.
3. **Execution**: The `inquiry_agent` takes over, asks for the order ID, and
   uses its `get_order_info` tool.

**Expected output:**

```
Customer: I want to check the status of order 1001.
Agent: Order 1001 contains item1 and item2. Its current status is 'placed' and it is being shipped to John Doe at 123 Main St.
```

---

## Important Details

### Common Misconceptions

**Misconception**: "The orchestrator must always be an LLM-based agent."
**Reality**: While ADK makes it easy to use an `Agent` as an orchestrator, you
can also use custom routing logic.

**Misconception**: "Sub-agents can't have their own sub-agents."
**Reality**: ADK supports nested agent hierarchies, allowing for complex
multi-level delegation.

### Best Practices

1. **Clear Boundaries**: Ensure each agent has a well-defined scope. If an
   agent's prompt starts getting too long, consider splitting it into smaller
   sub-agents.
2. **Specific Descriptions**: The `description` field for an `Agent` is often
   used by the orchestrator to understand what that agent does. Make it clear
   and concise.

### Common Errors

**Error**: `Sub-agent not found`

- **Cause**: The sub-agent was not correctly added to the `sub_agents` list of
  the orchestrator.
- **Solution**: Check `agent.py` to ensure all necessary agents are imported and
  included in the `Agent` definition.
