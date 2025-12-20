# Implementing Data Routing in ADK Systems

In this lesson, we learned how to implement custom routing logic in a 
multi-agent system. We built a search router for A/B testing and a 
smart inventory workflow that conditionally checks for reordering needs.

---

## Overview

### What You'll Learn

The solution demonstrates how to extend standard ADK routing using custom 
agents. It features:
1. A **Search Router** that programmatically chooses between two search 
   strategies (exact vs. broad).
2. An **Inventory Workflow** that conditionally executes a reorder check 
   only when stock levels are low.

Learning objectives:
- Implementing a `CustomAgent` by extending the `BaseAgent` class
- Creating programmatic routing logic using Python
- Utilizing A/B testing to evaluate agent performance
- Implementing conditional logic in a sequential workflow
- Delegating to sub-agents within a custom router

### Prerequisites

- Basic understanding of ADK agents and orchestration
- Basic understanding of Python classes and the `random` module

---

## Understanding the Concept

### The Problems

**A/B Testing**:
When introducing a new version of an agent, you often want to test it
against the current version without fully replacing it. This is known as
A/B testing. Relying on an LLM to perform this selection is not ideal
because we want precise, controlled distribution of traffic between the
two versions.

**Conditional Logic**: 
We want to check reorder status *only* if an item 
is low in stock. Running this check for every item can be inefficient.

### The Solution

We use `CustomAgent` classes inheriting from `BaseAgent` to write this 
logic in Python.

**SearchRouter**: Uses `random.random()` to route traffic.
**PossiblyReorderAgent**: Inspects the event history to see the stock 
count from the previous step and decides whether to run the reorder agent.

---

## Code Walkthrough

### Repository Structure

```
.
├── agent.py          # Root orchestrator
├── agents/
│   ├── search.py         # SearchRouter and search logic
│   ├── inventory.py      # Inventory workflow and reorder logic
│   ├── cart.py           # Shopping cart orchestration
│   ├── products.py       # Product catalog
│   └── order_data.py     # Order tracking
├── prompts/
│   ├── agent-prompt.txt        # Orchestrator prompt
│   ├── search-prompt.txt       # Exact search agent prompt
│   ├── search-broad-prompt.txt # Broad search agent prompt
│   ├── inventory-prompt.txt    # Inventory agent prompt
│   ├── reorder-prompt.txt      # Reorder agent prompt
│   └── ...
└── __init__.py
```

### Part 1: Search Router (A/B Testing)

In `agents/search.py`, `SearchRouter` selects an agent based on a 
probability threshold.

```python
class SearchRouter(BaseAgent):
    async def _run_async_impl(self, context: InvocationContext) -> AsyncGenerator[Event, None]:
        if random.random() < (1 - self.agent_b_rate):
            selected_agent = self.agent_a
        else:
            selected_agent = self.agent_b
            
        async for event in selected_agent.run_async(context):
            yield event
```

### Part 2: Inventory Workflow (Conditional Logic)

In `agents/inventory.py`, we construct a sequential chain where the second 
step may take further action.

**Step 1: The Custom Agent**
`PossiblyReorderAgent` looks at the output of the previous agent.

```python
class PossiblyReorderAgent(BaseAgent):
    async def _run_async_impl(self, context: InvocationContext) -> AsyncGenerator[Event, None]:
        # ... logic to find and parse InventoryData from context.session.events ...
        
        if inventory_data and inventory_data.count < 5:
            # Delegate to reorder agent
            async for event in self.reorder_agent.run_async(context):
                yield event
        # Else: do nothing (yield nothing)
```

If it meets the criteria, it will delegate to the reorder agent. If not, it 
continues.

**Step 2: The Sequential Chain**
We combine the agents into a linear workflow.

```python
inventory_data_agent = SequentialAgent(
    name="inventory_data_agent",
    description="Checks inventory and optionally checks reorder status.",
    sub_agents=[check_inventory_agent, possibly_reorder_agent]
)
```

**How it works:**
1. `check_inventory_agent` runs and outputs stock data (e.g., "Count: 4").
2. `possibly_reorder_agent` reads that event.
3. Seeing the count is 4 (< 5), it invokes `reorder_agent`.
4. `reorder_agent` runs and outputs the reorder status (e.g., "ORDERING").
5. The final output to the user includes both pieces of information.

---

## Important Details

### Best Practices

1. **Encapsulation**: Routing logic is kept inside the custom agent, keeping 
   the main orchestration clean.
2. **Event Inspection**: Using `context.session.events` allows agents to 
   react to what happened previously in the chain without needing explicit 
   variable passing.

### Common Errors

**Error**: Infinite loops or re-execution.
- **Cause**: If a custom agent blindly delegates back to the start of the 
  chain.
- **Solution**: Ensure your custom router always delegates forward to a 
  specific sub-agent, not back to the parent.