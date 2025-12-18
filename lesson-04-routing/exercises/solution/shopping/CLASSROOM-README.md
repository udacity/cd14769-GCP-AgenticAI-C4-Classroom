# Implementing Data Routing in ADK Systems

In this lesson, we learned how to implement custom routing logic in a 
multi-agent system by creating a search router that performs A/B testing 
between two different search strategies.

---

## Overview

### What You'll Learn

The solution demonstrates how to extend the standard ADK routing 
capabilities using a custom agent. It features a router that 
programmatically chooses between two specialized search agents, 
facilitating the evaluation of a new "broad search" implementation.

Learning objectives:
- Implementing a `CustomAgent` by extending the `BaseAgent` class
- Creating programmatic routing logic using Python
- Utilizing A/B testing to evaluate agent performance
- Delegating to sub-agents within a custom router

### Prerequisites

- Basic understanding of ADK agents and orchestration
- Basic understanding of Python classes and the `random` module

---

## Understanding the Concept

### The Problem

When introducing a new version of an agent, you often want to test it 
against the current version without fully replacing it. This is known as 
A/B testing. Relying on an LLM to perform this selection is not ideal 
because we want precise, controlled distribution of traffic between the 
two versions.

### The Solution

A `CustomAgent` allows you to write the routing logic directly in Python. 
By creating a `SearchRouter` that inherits from `BaseAgent`, we use 
the `random` module to decide which search agent to invoke for each 
request, ensuring a reliable split in traffic.

### How It Works

The implementation consists of three main parts:

**Step 1: Specialized Search Agents**
We have `search_agent_exact` (original) and `search_agent_broad` (new). 
Each uses a different search tool and system prompt.

**Step 2: The SearchRouter Class**
This class inherits from `BaseAgent`. Its `_run_async_impl` method 
contains the logic to select an agent based on a random number.

**Step 3: Programmatic Delegation**
Once an agent is selected, the router calls its `run_async` method and 
yields the resulting events back to the session.

### Key Terms

**A/B Testing**: A method of comparing two versions of an agent to 
determine which one performs better.

**Custom Agent**: An agent whose behavior is defined by custom Python 
code rather than a system prompt and LLM instructions.

---

## Code Walkthrough

### Repository Structure

```
shopping/
├── search.py         # Contains the router and search agents
├── search-broad-prompt.txt # Instructions for the experimental agent
└── agent.py          # The main orchestrator
```

### Step 1: Broad Search Tool

The solution implements `search_products_broad` to improve discovery by 
matching any word in the customer's query.

```python
def search_products_broad(query: str):
    """Searches for products matching any word in the query."""
    results = []
    words = query.lower().split()
    for pid, pdata in products.items():
        # ... logic to match any word ...
    return results
```

### Step 2: Custom Router Implementation

The `SearchRouter` handles the selection logic programmatically.

```python
class SearchRouter(BaseAgent):
    async def _run_async_impl(self, context: InvocationContext) -> AsyncGenerator[Event, None]:
        # Simple random routing
        if random.random() < (1 - self.agent_b_rate):
            selected_agent = self.agent_a
        else:
            selected_agent = self.agent_b
            
        async for event in selected_agent.run_async(context):
            yield event
```

**Key points:**
- Inherits from `BaseAgent` for full control over execution.
- Uses `random.random()` for deterministic traffic splitting.
- Uses `async for` to yield events from the selected sub-agent.

### Complete Example

The router is instantiated and used as the primary search agent for the 
system.

```python
# Main Search Agent (Router)
search_agent = SearchRouter(
    name="search_agent_router",
    agent_a=search_agent_exact,
    agent_b=search_agent_broad,
    agent_b_rate=0.5
)
```

**How it works:**
1. The orchestrator receives a search request.
2. It delegates to the `search_agent`, which is actually the `SearchRouter`.
3. The router selects an agent (e.g., `search_agent_broad`).
4. The broad search agent finds products and responds to the customer.

**Expected output:**
Over multiple searches for "blue headphones", the customer will 
sometimes receive only exact matches and other times a broader list of 
relevant products, depending on which path the router chose.

---

## Important Details

### Best Practices

1. **Encapsulation**: The routing logic is isolated within `search.py`, 
   making the system easier to maintain and the experiments easier to swap 
   out.
2. **Transparency**: The router's name `search_agent_router` clearly 
   indicates its role in the architecture.

### Common Errors

**Error**: Inconsistent state distribution
- **Cause**: Using a non-random or biased selection method.
- **Solution**: Use `random.random()` with a well-defined threshold for 
  accurate A/B testing.
