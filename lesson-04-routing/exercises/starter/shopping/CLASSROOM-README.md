# Implementing Data Routing in ADK Systems

In this lesson, we will learn how to implement custom routing logic in a 
multi-agent system by creating a search router that performs A/B testing 
between two different search strategies.

---

## Overview

### What You'll Learn

In this exercise, you'll learn how to extend the standard ADK routing 
capabilities using a custom agent. You will build a router that 
programmatically chooses between two specialized search agents, allowing 
you to evaluate the performance of a new search implementation.

Learning objectives:
- Create a `CustomAgent` by extending the `BaseAgent` class
- Implement programmatic routing logic using Python
- Understand how to use A/B testing to evaluate agent performance
- Learn how to delegate to sub-agents within a custom router

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
By creating a `SearchRouter` that inherits from `BaseAgent`, you can use 
the `random` module to decide which search agent to invoke for each 
request, ensuring a reliable and measurable split in traffic.

### How It Works

**Step 1: Define Specialized Agents**
You have an existing search agent and a new "broad search" agent that 
uses a different algorithm.

**Step 2: Implement the Router**
The `SearchRouter` acts as a wrapper. When it is invoked, it runs a 
simple piece of Python code to choose one of its sub-agents.

**Step 3: Delegation**
Once an agent is selected, the router delegates the `invocation_context` 
to that agent and yields the events it produces back to the customer.

### Key Terms

**A/B Testing**: A method of comparing two versions of an agent to 
determine which one performs better.

**Custom Agent**: An agent whose behavior is defined by custom Python 
code rather than a system prompt and LLM instructions.

---

## Exercise Instructions

### Your Task

Your task is to implement the `SearchRouter` class in `search.py` and 
configure it to split traffic between the original `search_agent_exact` 
and the new `search_agent_broad`.

### Requirements

Your implementation must:
1. Implement the `search_products_broad` function to match any word in the 
   query.
2. Create the `search_agent_broad` using the `LlmAgent` class.
3. Implement the `SearchRouter` class by extending `BaseAgent`.
4. The router must use a random threshold to choose between the two 
   agents.
5. Update the `search_agent` to use your new `SearchRouter`.

### Repository Structure

```
shopping/
├── search.py         # You will implement the broad search and the router here
├── search-broad-prompt.txt # Instructions for the broad search agent
└── agent.py          # The main orchestrator that uses the search agent
```

Make sure you copy ".env-sample" to ".env" and edit it to add the Google
Cloud project you are working with.

Remember that you should **never** check-in your .env file to git.

### Starter Code

You will be working primarily in `search.py`. Complete the logic where 
marked with TODO.

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

### Expected Behavior


When a customer searches for products, the system should randomly select 
either the exact match or the broad match strategy. Over many requests, 
you should see a distribution of results based on the `agent_b_rate` you 
define.

**Running the agent:**

You will run the agent using the `adk web` tool. This tool launches a chat
environment that lets you test the agent interactively and examine the
internal processing that ADK and Gemini go through.

```bash
adk web
```

**Example usage:**
Search for something like "blue headphones". Depending on which agent is 
selected, you may get an exact match for a product name or a list of any 
product that contains the word "blue" or "headphones".

### Implementation Hints

1. Use `random.random()` to generate a value between 0 and 1.
2. Remember that `_run_async_impl` is an `async` generator, so use `async for` 
   when calling `subagent.run_async()`.
3. The `agent_b_rate` determines the probability of selecting the second 
   agent.

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
- **Cause**: The `_run_async_impl` method must yield events from the 
  sub-agent to the caller.
- **Solution**: Ensure you are iterating over the sub-agent's 
  `run_async` and yielding each event.
