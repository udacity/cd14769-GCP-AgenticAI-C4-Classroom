# Implementing Multi-Agent Architectures with ADK

You were asked to implement a modular multi-agent system where specialized
agents handle search, inventory, and cart management, all coordinated by a
central orchestrator.

---

## Overview

### What You'll Learn

Learners will understand the practical implementation of the
"Orchestrator-Workers" pattern using the ADK. You will see how to define agents
with distinct responsibilities and tools, and how a root agent delegates tasks
based on user intent.

Learning objectives:

- Implement specialized agents (`Search`, `Inventory`, `Cart`) with focused
  toolsets.
- Configure a root `Orchestrator` agent to manage sub-agents.
- Handle conversational data flow between agents (like `product_id` and 
  `order_id`).

### Prerequisites

- Basic understanding of Python and the ADK.
- Access to Google Cloud with Vertex AI enabled.

---

## Understanding the Concept

### The Problem

A monolithic agent trying to handle searching, stock checking, and order
management would be complex and error-prone. Its system prompt would be massive,
and it might confuse similar actions (like "checking" a price vs "checking"
stock).

### The Solution

We decompose the problem into three distinct domains:

1. **Discovery**: Finding the right product.
2. **Availability**: Ensuring it can be sold.
3. **Transaction**: Managing the purchase.

The **Orchestrator** sits at the top, acting as the interface to the user. It
doesn't know *how* to search or check stock, but it knows *who* does.

### How It Works

**Step 1: The Request**
The user says, "I want to buy some headphones."

**Step 2: Orchestration**
The `root_agent` analyzes this. It sees the intent is "finding a product" and
delegates to the `search_agent`.

**Step 3: Execution & Handoff**
The `search_agent` uses `search_products` and returns 
"Wireless Headphones (P001)".
The user then says, "Add it to my cart."
The `root_agent` now routes to the `cart_agent`, which needs the `product_id`
found in the previous step.

---

## Code Walkthrough

### Repository Structure

```
.
├── agent.py          # Root orchestrator definition
├── agents/
│   ├── search.py         # Search agent and logic
│   ├── inventory.py      # Inventory agent and logic
│   ├── cart.py           # Cart agent and logic
│   ├── products.py       # Mock product database
│   └── order_data.py     # Mock order database
├── prompts/
│   ├── agent-prompt.txt      # System prompt for orchestrator
│   ├── search-prompt.txt     # System prompt for search agent
│   ├── inventory-prompt.txt  # System prompt for inventory agent
│   └── cart-prompt.txt       # System prompt for cart agent
└── __init__.py
```

### Step 1: The Search Agent

In `agents/search.py`, we define an agent focused solely on the product catalog.

```python
def search_products(query: str):
  """Searches for products by name or description."""
  # ... implementation details ...
  return results


search_agent = Agent(
  name="search_agent",
  description="Searches for products in the catalog.",
  model=model,
  instruction=search_instruction,
  tools=[search_products],
)
```

**Key points:**

- The `search_agent` only has access to the `search_products` tool.
- Its prompt (`prompts/search-prompt.txt`) instructs it to only discuss product
  discovery.

### Step 2: The Inventory Agent

In `agents/inventory.py`, the agent is responsible for stock checks.

```python
def check_inventory(product_id: str):
  """Checks if a product is in stock."""
  # ... checks product_counts ...
  return {"in_stock": count > 0, "count": count}
```

**Key points:**

- This agent isolates the inventory logic. If we changed our inventory system
  later, we'd only need to update this file.

### Step 3: The Cart Agent

In `agents/cart.py`, we handle the transactional state.

```python
def add_to_cart(order_id: str, product_id: str):
  """Adds a product to the specified order's cart."""
  # ... adds to orders dictionary ...
```

**Key points:**

- This agent needs an `order_id` to function.
- It validates that the order is in a state that allows modification.

### Step 4: The Orchestrator

In `agent.py`, we wire it all together.

```python
root_agent = Agent(
  name="shopping_orchestrator",
  description="Orchestrates the shopping experience.",
  model=model,
  instruction=orchestrator_instruction,
  sub_agents=[search_agent, inventory_agent, cart_agent],
)
```

**Key points:**

- The `sub_agents` list makes the specialized agents available to the
  orchestrator.
- The `agent-prompt.txt` guides the orchestrator on which agent to pick for a
  given user request.

### Complete Example

**User**: "Find me a speaker."
**Orchestrator**: (Delegates to Search Agent)
**Search Agent**: "I found a Bluetooth Speaker (P003) for $59.99."
**User**: "Is it in stock?"
**Orchestrator**: (Delegates to Inventory Agent)
**Inventory Agent**: "Unfortunately, the Bluetooth Speaker (P003) is out of
stock."

---

## Important Details

### Best Practices

1. **State Isolation**: Notice how `search.py` doesn't import `order_data.py`.
   It doesn't need to know about orders. Keeping dependencies minimal is key to
   good architecture.
2. **Shared Data**: `products.py` acts as a shared database that multiple
   agents (Search, Inventory) can read from, ensuring consistency.

### Common Errors

**Error**: `Product ID not found`

- **Cause**: The user might be trying to add a product that hasn't been
  identified yet, or the `product_id` wasn't correctly passed from the Search
  Agent's output to the Cart Agent's input.
- **Solution**: The Orchestrator handles the conversation context, ensuring that
  when the user says "buy *it*", the "it" (product ID) is understood from the
  previous turn.
