# Implementing Agent Orchestration with ADK

In this exercise, you will implement advanced orchestration patterns (Sequential
and Parallel agents) to create a robust and optimized shopping cart workflow.

---

## Overview

### Your Task

Starting with a shopping cart agent, your goal is to refactor it to use a more 
structured fulfillment process. Instead of a single agent handling multiple 
tools, you will build a hierarchy of agents that prepare the order session 
and check inventory in parallel before proceeding to add the item to the cart.

### Requirements

Your implementation must:

1. **Implement Sub-Agents**: Create `get_order_agent` and `add_item_agent` as
   specialized `LlmAgent`s in `cart.py`.
2. **Structured Data**: Implement `inventory_data_agent` in `inventory.py` to
   return structured inventory information.
3. **Parallel Execution**: Create a `cart_prep_agent` that simultaneously 
   ensures an active order session exists and verifies the  product is in stock.
4. **Sequential Workflow**: Create a `cart_agent` that chains the 
   preparation step with the final action of adding the item to the cart.

### Repository Structure

```
.
├── agent.py          # Main orchestrator
├── agents/
│   ├── cart.py           # TODO: Implement Sequential and Parallel orchestration
│   ├── inventory.py      # TODO: Implement inventory_data_agent
│   ├── search.py         # Product search logic
│   ├── products.py       # Product catalog
│   └── order_data.py     # Order tracking
├── prompts/
│   ├── agent-prompt.txt      # Orchestrator instructions
│   ├── search-prompt.txt     # Search agent instructions
│   ├── inventory-prompt.txt  # Inventory agent instructions
│   ├── cart-prompt.txt       # Main cart agent instructions
│   ├── get-order-prompt.txt  # TODO: Write instructions for order session
│   └── add-item-prompt.txt   # TODO: Write instructions for adding item
├── __init__.py
└── requirements.txt  # Dependencies
```

Make sure you copy ".env-sample" to ".env" and edit it to add the Google
Cloud project you are working with.

Remember that you should **never** check-in your .env file to git.

### Starter Code

The `cart.py` file contains placeholders for the new orchestration logic:

```python
# --- Sub-Agents ---

# TODO: Create the get_order_agent as an LlmAgent
get_order_agent = None

# TODO: Create the add_item_agent as an LlmAgent
add_item_agent = None

# --- Orchestration ---

# TODO: Create a ParallelAgent called cart_prep_agent
# It should run get_order_agent and inventory_data_agent in parallel
cart_prep_agent = None

# TODO: Create a SequentialAgent called cart_agent
cart_agent = None
```

### Expected Behavior

**Running the agent:**

Start the chat environment:

```bash
adk web
```

**Example interaction:**

**User**: "Add Wireless Headphones to my cart."
**System Action**:

1. **Parallel Preparation**:
    - `get_order_agent` ensures an `order_id` is available.
    - `inventory_data_agent` checks if P001 is in stock.
2. **Sequential Step**:
    - `add_item_agent` receives the context (order ID and stock confirmation)
      and adds the item.

### Implementation Hints

1. **Parallel Outputs**: Remember that a `ParallelAgent` combines the outputs of
   its sub-agents. The subsequent agent in a sequence will have access to all
   this information in its context.
2. **Output Schemas**: Use the provided `InventoryData` schema to ensure the LLM
   returns structured data that is easy for the next agent to parse.
3. **Prompts**: Your new specialized agents (like `get_order_agent`) need
   specific instructions in their prompt files (`get-order-prompt.txt`) to focus
   on their narrow task.

---

## Important Details

### Common Misconceptions

**Misconception**: "Sequential agents just call tools in order."
**Reality**: Sequential agents call *other agents* in order. Each agent in the
sequence can have its own tools, prompts, and even its own sub-agents.

### Best Practices

1. **Dependency Management**: Always place agents that provide necessary data 
   (like an order ID) before agents that require that data in a 
   `SequentialAgent` list.
2. **Performance**: Use `ParallelAgent` for any tasks that don't depend on each
   other's results to minimize latency.
