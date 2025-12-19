# Implementing Multi-Agent Architectures with ADK

We will learn how to build a modular multi-agent system by creating a shopping
assistant that delegates product search, inventory checking, and cart management
to specialized sub-agents.

---

## Overview

### What You'll Learn

Learners will practice breaking down a complex application into smaller,
manageable agents. You will implement the logic for individual tools, define the
agents that use them, and wire them together using an orchestrator.

Learning objectives:

- Implement tool logic for searching, inventory, and cart operations.
- define ADK agents with specific roles and toolsets.
- Create an orchestrator agent that routes user requests to the correct
  sub-agent.

### Prerequisites

- Basic understanding of Python.
- Familiarity with the ADK (Agent Development Kit).
- Access to Google Cloud with Vertex AI enabled.

---

## Understanding the Concept

### The Problem

A shopping assistant needs to handle various distinct tasks: finding products,
checking if they are available, and managing a user's shopping cart. Putting all
this logic and instructions into a single agent would result in a massive prompt
and potential confusion between similar actions.

### The Solution

By using a multi-agent architecture, we can create specialized agents:

- **Orchestrator**: Acts as the manager, understanding the user's intent and
  calling the right expert or sub-agent.
- **Search Agent**: Focuses solely on finding items in the catalog.
- **Inventory Agent**: Checks stock levels.
- **Cart Agent**: Manages the user's order.

---

## Exercise Instructions

### Your Task

You need to complete the implementation of a multi-agent shopping system. The
structure is provided, but the core logic and agent definitions are missing.

### Requirements

Your implementation must:

1. **Implement Tools**: Fill in the logic for `search_products`,
   `check_inventory`, and `add_to_cart`.
2. **Define Agents**: Create the `search_agent`, `inventory_agent`, and
   `cart_agent` with appropriate `model`, `instruction`, and `tools`.
3. **Write Prompts**: Update the `*-prompt.txt` files with clear instructions
   for each agent.
4. **Orchestrate**: Configure the `root_agent` in `agent.py` to include all your
   sub-agents.

### Repository Structure

```
.
├── agent.py          # TODO: Define root_agent and sub-agents list
├── agents/
│   ├── search.py         # TODO: Implement search logic and agent
│   ├── inventory.py      # TODO: Implement inventory logic and agent
│   ├── cart.py           # TODO: Implement cart logic and agent
│   ├── products.py       # Shared product data (ReadOnly)
│   └── order_data.py     # Shared order data
├── prompts/
│   ├── agent-prompt.txt      # TODO: Write system prompt for orchestrator
│   ├── search-prompt.txt     # TODO: Write system prompt for search agent
│   ├── inventory-prompt.txt  # TODO: Write system prompt for inventory agent
│   └── cart-prompt.txt       # TODO: Write system prompt for cart agent
├── __init__.py
└── requirements.txt  # Dependencies
```

Make sure you copy `.env-sample` to `.env` and edit it to add the Google Cloud
project you are working with.

Remember that you should **never** check-in your .env file to git.

### Starter Code

The files provided have the imports and function signatures set up. You need to
fill in the bodies of the functions and the agent instantiations.

```python
# Example from search.py

def search_products(query: str):
  """Searches for products by name or description."""
  # TODO: Implement product search logic using the 'products' dictionary
  pass


# ...

# TODO: Create the search_agent
search_agent = None
```

### Expected Behavior

**Running the agent:**

You will run the agent using the `adk web` tool.

```bash
adk web
```

**Example usage:**

**User**: "Find me some headphones."
**Agent**: (Routes to Search Agent) "I found Wireless Headphones (P001) for $
299.99."

**User**: "Are they in stock?"
**Agent**: (Routes to Inventory Agent) "Yes, we have 50 in stock."

**User**: "Add one to my cart."
**Agent**: (Routes to Cart Agent) "Added Wireless Headphones to your cart. You
have 1 item(s)."

### Implementation Hints

1. **Prompts**: Keep your prompts focused. The Search Agent doesn't need to know
   about the Cart. The Orchestrator just needs to know *who* handles what, not
   *how* they do it.
2. **Tools**: Look at the `products` dictionary structure in `products.py` to
   understand how to implement search and inventory checks.
3. **Orchestrator**: In `agent.py`, the `sub_agents` list is the key to making
   the `root_agent` aware of its helpers.

---

## Important Details

### Common Misconceptions

**Misconception**: "I need to explicitly tell the orchestrator which tool to
use."
**Reality**: The orchestrator selects an *agent*, and that agent selects the
*tool*. You just need to describe the agent's purpose well.

### Common Errors

**Error**: `AttributeError: 'NoneType' object has no attribute ...`

- **Cause**: You likely forgot to instantiate one of the agents (left it as
  `None`).
- **Solution**: Ensure all `*_agent` variables are properly assigned an `Agent`
  object.
