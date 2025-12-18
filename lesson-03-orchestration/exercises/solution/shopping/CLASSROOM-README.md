# Implementing Agent Orchestration with ADK

We will learn how to implement advanced orchestration patterns (Sequential and
Parallel agents) to create a robust and optimized shopping cart workflow.

---

## Overview

### What You'll Learn

Learners will see a complete implementation of `SequentialAgent` and
`ParallelAgent` used to refactor a monolithic shopping cart agent into a clean,
modular pipeline.

Learning objectives:

- Decompose complex tasks into specialized agents.
- Orchestrate concurrent operations (Inventory Check + Order Session).
- Enforce dependency chains (Preparation -> Execution).

### Prerequisites

- Understanding of basic ADK Agent instantiation.
- Familiarity with Python dictionaries and data structures.
- Access to Google Cloud with Vertex AI enabled.

---

## Understanding the Concept

### The Problem

Adding an item to a cart isn't just one action. It requires:

1. Knowing *which* cart (order ID).
2. Knowing *if* the item is available (inventory).
3. Actually performing the addition.

Doing (1) and (2) sequentially may be slow, and they don't depend on each 
other for anything. Doing (3) before (1) or (2) is impossible.

### The Solution

We use a **ParallelAgent** to handle the prerequisites simultaneously:

- `get_order_agent`: "Do we have a cart? If not, make one."
- `inventory_data_agent`: "Is the item in stock?"

Then, we use a **SequentialAgent** to ensure these prerequisites are met before
the final step:

- `cart_prep_agent` (The parallel block above)
- `add_item_agent` (The final commit)

---

## Code Walkthrough

### Repository Structure

```
shopping/
├── cart.py           # The core logic containing the orchestration
├── inventory.py      # Structured inventory agent
├── agent.py          # Root orchestrator
└── ...
```

### Step 1: Structured Inventory

In `inventory.py`, we use `output_schema` to ensure the inventory check returns
machine-readable data, not just text.

```python
class InventoryData(BaseModel):
  product_id: str
  in_stock: bool
  count: int


inventory_data_agent = LlmAgent(
  # ...
  output_schema=InventoryData
)
```

### Step 2: Parallel Preparation

In `cart.py`, we define the `cart_prep_agent`.

```python
cart_prep_agent = ParallelAgent(
  name="cart_prep_agent",
  description="Prepares for adding to cart by ensuring order exists and checking inventory.",
  sub_agents=[get_order_agent, inventory_data_agent],
)
```

**Key points:**

- This agent may run both sub-agents at the same time.
- There is no guarantee they will run at the same time - but the ADK may 
  choose to do so to optimize operations.
- The output will contain both the `order_id` (from `get_order_agent`) and the
  `InventoryData` (from `inventory_data_agent`).

### Step 3: Sequential Execution

Finally, we chain it all together.

```python
cart_agent = SequentialAgent(
  name="cart_agent",
  description="Manages adding items to the cart with validation.",
  sub_agents=[cart_prep_agent, add_item_agent],
)
```

**Key points:**

- `add_item_agent` will only run after `cart_prep_agent` completes since 
  agents run in the order listed in a `SequentialAgent`
- It will have access to the combined context, allowing it to verify `in_stock`
  is true and use the correct `order_id`.

### Complete Example

**User**: "Add the headphones."
**Orchestrator**: Routes to `cart_agent`.
**Cart Agent**:

1. **Prep (Parallel)**:
    - *Order*: "Using Order ID 1001."
    - *Inventory*: "P001 is In Stock."
2. **Add (Sequential)**:
    - "Adding P001 to Order 1001."

---

## Important Details

### Best Practices

1. **Structured Outputs**: Using Pydantic models (like `InventoryData`) makes
   passing data between agents much more reliable than parsing natural language.
2. **Clear Roles**: Each sub-agent (`get_order_agent`, `add_item_agent`) has a
   very narrow responsibility, making them easy to test and prompt.

### Common Errors

**Error**: `Product ID not found`

- **Cause**: The `add_item_agent` tried to add a product before the
  `inventory_data_agent` successfully identified it.
- **Solution**: Ensure the flow is correct and the product ID is properly
  propagated through the context.
