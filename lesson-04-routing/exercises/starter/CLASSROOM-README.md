# Implementing Data Routing in ADK Systems

In this lesson, we will learn how to implement custom routing logic in a 
multi-agent system by creating a search router that performs A/B testing 
between two different search strategies, and a sequential inventory agent 
that conditionally checks for reordering.

---

## Overview

### What You'll Learn

In this exercise, you'll learn how to extend the standard ADK routing 
capabilities using custom agents. You will build:
1. A router that programmatically chooses between two specialized search 
   agents, allowing you to evaluate the performance of a new search 
   implementation. 
2. A sequential workflow that conditionally triggers a reorder check based 
   on inventory levels, which will let another back-end system reorder 
   products before they run out.

Learning objectives:
- Create a `CustomAgent` by extending the `BaseAgent` class
- Implement programmatic routing logic using Python
- Understand how to use A/B testing to evaluate agent performance
- Implement conditional logic within a sequential agent chain
- Learn how to delegate to sub-agents within a custom router

### Prerequisites

- Basic understanding of ADK agents and orchestration
- Basic understanding of Python classes and the `random` module

---

## Understanding the Concept

### The Problem

**Scenario 1: A/B Testing**
When introducing a new version of an agent, you often want to test it 
against the current version without fully replacing it. This is known as 
A/B testing. Relying on an LLM to perform this selection is not ideal 
because we want precise, controlled distribution of traffic between the 
two versions.

**Scenario 2: Conditional Execution**
Sometimes, an agent should only run if a specific condition is met by the 
previous agent's output. For example, we only want to check reorder status 
if an item's stock is low.

### The Solution

A `CustomAgent` allows you to write the routing logic directly in Python. 
By creating classes that inherit from `BaseAgent`, you can implement precise
control flow logic.
* We can have a `SearchRouter` that uses the `random` module to decide which 
  search agent to invoke for each request, ensuring a reliable and 
  measurable split in traffic.
* We can also create a `PossiblyReorderAgent` that implements business rules 
  to determine when we should ask another agent to confirm that 
  an item is on order, or if we don't need to worry about it yet.

### How It Works

**Part 1: Search Router (A/B Testing)**
The `SearchRouter` wrapper uses `random.random()` to choose between 
`search_agent_exact` and `search_agent_broad` for each request.

**Part 2: Inventory Workflow (Conditional Logic)**
The `inventory_data_agent` becomes a `SequentialAgent`.
1. `check_inventory_agent` runs first and returns stock levels.
2. `PossiblyReorderAgent` (a custom agent) inspects that output.
3. If stock is low (< 5), it delegates to `reorder_agent`.
4. If stock is sufficient, it does nothing.

### Key Terms

**A/B Testing**: A method of comparing two versions of an agent to 
determine which one performs better.

**Custom Agent**: An agent whose behavior is defined by custom Python 
code rather than a system prompt and LLM instructions.

**Conditional Routing**: Directing control flow based on specific data 
criteria.

---

## Exercise Instructions

### Your Task

You have two main tasks:
1. Implement the `SearchRouter` in `search.py` to split traffic between 
   exact and broad search.
2. Implement the `PossiblyReorderAgent` in `inventory.py` to handle 
   conditional reordering.

### Requirements

**Search Router:**
1. Implement `search_products_broad` to match any word in the query.
2. Create `search_agent_broad` using the `LlmAgent` class.
3. Implement `SearchRouter` class by extending `BaseAgent`.
4. The router must use a random threshold to choose between the two
   agents.
5. Update `search_agent` to use the router.

**Inventory Workflow:**
1. Create `reorder_agent` using `check_reorder_status` and 
   `reorder_instruction`.
2. Implement `PossiblyReorderAgent` to:
   - Find the output event from `check_inventory_agent`.
   - Parse the JSON data.
   - Run `reorder_agent` ONLY if `count < 5`.
3. Define `inventory_data_agent` as a `SequentialAgent` combining 
   `check_inventory_agent` and your custom `possibly_reorder_agent`.

### Repository Structure

```
.
├── agent.py          # Main orchestrator
├── agents/
│   ├── search.py         # TODO: Implement broad search and router
│   ├── inventory.py      # TODO: Implement conditional reorder logic
│   ├── cart.py           # Shopping cart orchestration
│   ├── products.py       # Product catalog
│   └── order_data.py     # Order tracking
├── prompts/
│   ├── agent-prompt.txt        # Orchestrator instructions
│   ├── search-prompt.txt       # Exact search instructions
│   ├── search-broad-prompt.txt # Broad search instructions
│   ├── inventory-prompt.txt    # Inventory instructions
│   ├── reorder-prompt.txt      # Reorder instructions
│   ├── cart-prompt.txt         # Main cart instructions
│   ├── get-order-prompt.txt    # Order session instructions
│   └── add-item-prompt.txt     # Add-to-cart instructions
├── __init__.py
└── requirements.txt  # Dependencies
```

Make sure you copy ".env-sample" to ".env" and edit it to add the Google
Cloud project you are working with.

Remember that you should **never** check-in your .env file to git.

### Starter Code

**search.py**
```python
def search_products_broad(query: str):
    """Searches for products matching any word in the query."""
    # TODO: Implement broad search logic
    pass

# TODO: Create the New Broad Search Agent
search_agent_broad = None

class SearchRouter(BaseAgent):
    """
    Routes to either exact or broad search based on a random threshold.
    """
    # TODO: Implement the constructor and _run_async_impl
    pass
```

**inventory.py**
```python
class PossiblyReorderAgent(BaseAgent):
    async def _run_async_impl(self, context: InvocationContext) -> AsyncGenerator[Event, None]:
       # TODO: Implement the logic to inspect the previous agent's output

       # TODO: If count < 5, run the reorder_agent

       # If count >= 5, do nothing (pass)
       pass

# TODO: Create the possibly_reorder_agent instance
possibly_reorder_agent = None

# TODO: Define the inventory_data_agent as a SequentialAgent
# It should run check_inventory_agent followed by possibly_reorder_agent
inventory_data_agent = None
```

### Expected Behavior

1. **Search**: Searching for "blue headphones" should vary between exact 
   matches and broad matches over time.
2. **Inventory**: 
   - Check a high-stock item (e.g., P001): Returns just inventory data.
   - Check a low-stock item (e.g., P012): Returns inventory data AND 
     triggers a "Check reorder status" action, adding `reorder_status` 
     to the output.

**Running the agent:**

You will run the agent using the `adk web` tool. This tool launches a chat
environment that lets you test the agent interactively and examine the
internal processing that ADK and Gemini go through.

```bash
adk web
```

**Example usage:**
- "Do you have the webcam in stock?" (P012 is low stock -> triggers reorder check)
- "Do you have headphones?" (P001 is high stock -> no reorder check)

### Implementation Hints

1. **Event History**: Use `context.session.events` to look back at what 
   happened. Iterate in reverse to find the most recent output.
2. **JSON Parsing**: The model output is text. You need to parse it as JSON 
   to read the `count`.
3. **Delegation**: Remember that `_run_async_impl` is an `async` generator, 
   so use `async for` when calling `subagent.run_async()`.

---

## Important Details

### Common Misconceptions

**Misconception**: "A router agent must always use an LLM to decide where 
to go."
**Reality**: Custom agents allow for deterministic, programmatic routing 
using standard Python logic.

**Misconception**: "I need to modify the main orchestrator to support 
A/B testing."
**Reality**: Because the `SearchRouter` behaves like any other agent, 
the orchestrator doesn't need to know that A/B testing is happening.

### Best Practices

1. **Encapsulation**: Keep the routing logic hidden within the router 
   agent to maintain a clean architecture.
2. **Measurability**: In a real system, you would log which agent was 
   chosen to evaluate the A/B test results later.

### Common Errors

**Error**: Forgetting `yield event`
- **Cause**: The `_run_async_impl` method must either yield events from the 
  sub-agent to the caller or `pass` if there are no sub-agents.
- **Solution**: Ensure you are iterating over the sub-agent's 
  `run_async` and yielding each event or `pass` if you don't have a sub-agent.
