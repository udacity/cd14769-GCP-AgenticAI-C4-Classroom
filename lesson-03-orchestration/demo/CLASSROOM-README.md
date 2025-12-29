# Implementing Agent Orchestration with ADK

We will learn how to implement advanced orchestration patterns using ADK,
specifically "Sequential" (Series) and "Parallel" execution, to build a robust
order fulfillment system.

---

## Overview

### What You'll Learn

Learners will move beyond simple delegation and implement structured workflows.
You will see how to chain agents together so that the output of one becomes the
input of another (Sequential) and how to run independent tasks simultaneously
(Parallel).

Learning objectives:

- Implement `SequentialAgent` to enforce a specific order of operations.
- Implement `ParallelAgent` to optimize performance for independent tasks.
- Combine these patterns to create a complex business process.

### Prerequisites

- Understanding of basic ADK Agent instantiation.
- Familiarity with Python dictionaries and data structures.
- Access to Google Cloud with Vertex AI enabled.

---

## Understanding the Concept

### The Problem

In a real-world shipping process, certain things *must* happen in order (you
can't calculate taxes until you know the address), while others *can* happen at
the same time (calculating shipping costs and tax rates). A simple "router"
orchestrator (like in Lesson 2) isn't enough to enforce these dependencies or
optimizations.

### The Solution

ADK provides specialized agent types for this:

- **SequentialAgent**: Executes a list of sub-agents one after another. This is
  perfect for the "Place Order -> Calculate Costs -> Summarize" pipeline.
- **ParallelAgent**: Executes a list of sub-agents simultaneously. This is ideal
  for the "Calculate Shipping" and "Calculate Taxes" step.

### How It Works

**Step 1: Place Order**
The user provides an address. The `place_order_agent` updates the order record.

**Step 2: Calculate Costs (Parallel)**
Now that we have the address (and thus the state), we can calculate costs. The
`costs_agent` (a ParallelAgent) triggers both:

- `shipping_cost_agent`: Determines cost based on method (Standard/Express).
- `taxes_cost_agent`: Determines tax based on the destination state.
  These run at the same time to save time.

**Step 3: Compute Total**
Once the parallel tasks return, the `compute_order_agent` aggregates the results
to find the final total.

**Step 4: Summary & Approval**
Finally, the `order_summary_agent` presents the deal to the user for final
confirmation.

---

## Code Walkthrough

### Repository Structure

```
.
├── agent.py          # Root agent configuration and orchestration logic
├── agents/
│   ├── shipping.py   # Full fulfillment workflow (Sequential/Parallel)
│   ├── inquiry.py    # Order inquiry handling
│   ├── order_data.py # Mock database of orders
│   ├── products.py   # Mock database of products
│   └── rates.py      # Mock data for shipping and tax rates
├── prompts/
│   ├── agent-prompt.txt           # Orchestrator prompt
│   ├── shipping-prompt.txt        # Main shipping agent prompt
│   ├── shipping-cost-prompt.txt   # Shipping cost calculation prompt
│   ├── taxes-cost-prompt.txt      # Tax calculation prompt
│   ├── compute-order-prompt.txt   # Order total calculation prompt
│   ├── place-order-prompt.txt     # Order placement prompt
│   ├── order-summary-prompt.txt   # Final summary prompt
│   └── approve-order-prompt.txt   # Final approval prompt
└── __init__.py
```

### Step 1: Parallel Execution

In `agents/shipping.py`, look at how we define the `costs_agent`.

```python
costs_agent = ParallelAgent(
  name="other_costs_agent",
  description="Calculates shipping and taxes in parallel.",
  sub_agents=[shipping_cost_agent, taxes_cost_agent],
)
```

**Key points:**

- `ParallelAgent` takes a list of `sub_agents`.
- It aggregates the outputs of all sub-agents.

### Step 2: Sequential Workflow

The `fulfillment_workflow_agent` chains everything together in `agents/shipping.py`.

```python
fulfillment_workflow_agent = SequentialAgent(
  name="fulfillment_workflow",
  description="Calculates costs after an order is placed.",
  sub_agents=[
    place_order_agent,
    costs_agent,  # Note: This is the parallel agent from Step 1
    compute_order_agent,
    order_summary_agent,
  ],
)
```

**Key points:**

- The order is critical. `place_order_agent` must run first to set the address.
- `costs_agent` runs second, using the address from step 1.
- `compute_order_agent` runs third, using the costs from step 2.

### Complete Example

**User**: "Ship order 1001 to John Doe, 123 Main St, New York, NY 10001."

**System Action**:

1. **Place Order**: Updates order 1001 with the NY address.
2. **Costs (Parallel)**:
    - *Shipping*: $5.00 (Standard)
    - *Taxes*: $25.00 (8% of subtotal)
3. **Compute**: Adds subtotal + $5 + $25 = Total.
4. **Summary**: "Order 1001 to NY. Total: $330.00. Ready to approve?"

---

## Important Details

### Best Practices

1. **Granularity**: Break down tasks into the smallest logical units. This makes
   them easier to parallelize.
2. **Data Flow**: Ensure that the output of one agent in a sequence provides the
   necessary context for the next agent.

### Common Errors

**Error**: `KeyError: 'state'`

- **Cause**: The `taxes_cost_agent` tried to run before the address was set.
- **Solution**: Ensure `place_order_agent` is placed *before* the tax
  calculation in the `SequentialAgent` list.
