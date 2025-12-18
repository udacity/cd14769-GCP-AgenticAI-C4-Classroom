# Implementing Advanced State Management with ADK

In this lesson, we will update the shopping agent to use advanced state management 
techniques. You will modify the agent to store the current order ID in the 
session state, allowing for persistent and reliable access across different 
turns of conversation.

---

## Overview

### Your Task

Your goal is to refactor the shopping agent so that it no longer relies on 
passing the `order_id` as a parameter between every function call. Instead, 
you will use the `ToolContext` to save the `order_id` into the session state 
when an order is created or retrieved, and use `InvocationContext` (or 
`ToolContext` in other tools) to read it back when needed.

### Requirements

Your implementation must:
1. Update `get_order` to save the `order_id` into `tool_context.state`.
2. Update `add_to_cart` to retrieve the `order_id` from `tool_context.state`.
3. Ensure the system works seamlessly even if the user changes topics in between.
4. Run the agent using Agent Engine to test persistence.

### Repository Structure

```
shopping/
├── cart.py           # TODO: Update tools to use ToolContext
├── agent.py          # Root orchestrator
├── inventory.py      # Inventory logic
├── products.py       # Product catalog
├── order_data.py     # Order tracking
└── ...
```

Make sure you copy ".env-sample" to ".env" and edit it to add the Google
Cloud project you are working with.

Remember that you should **never** check-in your .env file to git.

### Starter Code

The `cart.py` file has been prepared with the `ToolContext` import, but you 
need to update the function signatures and logic.

```python
from google.adk.tools import ToolContext

def get_order(tool_context: ToolContext):
    """
    Retrieves the order. If no order ID is provided, creates a new one.
    Saves the order_id to session state.
    """
    # TODO: Implement logic to check state first, then create if needed
    pass

def add_to_cart(product_id: str, tool_context: ToolContext):
    """Adds a product to the specified order's cart."""
    # TODO: Retrieve order_id from state instead of parameter
    pass
```

### Expected Behavior

**Running the agent:**

To test session persistence, follow these steps to use the Agent Engine:

1.  **Create an Engine Instance**: Run the provided setup script.
    ```bash
    python ../notes/create_agent_engine.py
    ```
    This will print a resource name (e.g., `projects/YOUR_PROJECT/locations/us-central1/agents/YOUR_AGENT_ID`).

2.  **Start the Web Server**:
    ```bash
    adk web --session_service_uri agentengine://projects/YOUR_PROJECT/locations/us-central1/agents/YOUR_AGENT_ID
    ```

**Example interaction:**

**User**: "I'd like to start a new order."
**System**: "Started order 1001." (Implicitly saves 1001 to state)
**User**: "What is the weather?" (Distractor question)
**System**: "I don't know, I'm a shopping agent."
**User**: "Add headphones."
**System**: "Added headphones to order 1001." (Successfully retrieved 1001 from state)

### Implementation Hints

1.  **Signatures**: When you add `tool_context: ToolContext` to a tool's 
    parameters, the ADK automatically handles it. You don't need to change 
    how the LLM calls the tool.
2.  **Checking State**: `tool_context.state.get("order_id")` is the safe way 
    to check if an order already exists.
3.  **Handling Missing State**: In `add_to_cart`, if the order ID is missing 
    from the state, you should return a helpful error message telling the user 
    to start an order first (or call `get_order`).

---

## Important Details

### Common Misconceptions

**Misconception**: "I need to tell the LLM to use the state."
**Reality**: The LLM doesn't know about `ToolContext`. It's a backend 
mechanism. You (the developer) write the code that uses it. The LLM just 
sees "Success" or "Error".

### Best Practices

1.  **Minimal State**: Only store the `order_id` in the session state, not 
    the entire order object if you can avoid it. Fetching the full order from 
    the database (`orders` dict) using the ID is often cleaner and ensures 
    you always have the latest data.

### Common Errors

**Error**: `TypeError: place_order() missing 1 required positional argument: 'tool_context'`
- **Cause**: You might be calling the tool function manually in your code 
  without passing the context.
- **Solution**: If you call a tool function directly from another python 
  function (not via the LLM), you need to pass the context manually or mock it.
