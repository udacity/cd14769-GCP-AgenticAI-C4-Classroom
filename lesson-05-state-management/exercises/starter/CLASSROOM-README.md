# Implementing Advanced State Management with ADK

In this lesson, we will update the shopping agent to use advanced state 
management techniques. You will modify the agent to store the current order ID 
in the session state, allowing for persistent and reliable access across 
different turns of conversation.

---

## Overview

### Your Task

Your goal is to refactor the shopping agent so that it no longer relies on 
passing the `order_id` as a parameter between the customer and the tools. 
Instead, you will use the `ToolContext` to save the `order_id` into the 
session state when an order is created or retrieved, and read it back when 
needed for subsequent actions like adding items to the cart.

### Requirements

Your implementation must:
1.  **Update Tool Signatures**: Modify `get_order` and `add_to_cart` to 
    accept `tool_context: ToolContext`.
2.  **Explicit State**: In `get_order`, check the session state for an 
    existing `order_id` before creating a new one. Save the ID to state.
3.  **Context Retrieval**: In `add_to_cart`, retrieve the `order_id` from 
    the session state instead of asking the user for it.
4.  **Persistence**: Run the agent using the Vertex AI Agent Engine to 
    store session state.

### Repository Structure

```
shopping/
├── cart.py           # TODO: Update tools to use session state
├── agent.py          # Root orchestrator
├── inventory.py      # Inventory logic
├── products.py       # Product catalog
└── order_data.py     # Shared order storage
```

Make sure you copy ".env-sample" to ".env" and edit it to add the Google
Cloud project you are working with.

Remember that you should **never** check-in your .env file to git.

### Starter Code

The `cart.py` file contains TODOs where you need to implement the state 
management logic:

```python
from google.adk.tools import ToolContext

# TODO: Update get_order to accept tool_context and use session state
def get_order(tool_context: ToolContext):
    # TODO: Check if "order_id" exists in tool_context.state
    pass

# TODO: Update add_to_cart to retrieve order_id from session state
def add_to_cart(product_id: str, tool_context: ToolContext):
    # TODO: Retrieve order_id from tool_context.state
    pass
```

### Expected Behavior

**Running the agent:**

To test session persistence, follow these steps to use the Agent Engine:

1.  **Create an Engine Instance**: Run the provided setup script.
    ```bash
    python ../notes/create_agent_engine.py
    ```
    This will print a **resource name**.

2.  **Start the Web Server**:
    ```bash
    adk web --session_service_uri agentengine://YOUR_RESOURCE_NAME
    ```

**Example interaction:**

**User**: "Find me some headphones."
**System**: "I found Wireless Headphones (P001)."
**User**: "Add them to my cart."
**System**: "Added Wireless Headphones to your order (ORDER_1001)."

Notice that the system didn't ask for an Order ID—it retrieved the 
active session from the cloud!

### Implementation Hints

1.  **Tool Context**: Adding `tool_context: ToolContext` to your function 
    parameters tells ADK to inject the session information automatically.
2.  **Sticky State**: Once you set `tool_context.state["order_id"] = "xyz"`, 
    that value remains available for every future turn in that conversation.

---

## Important Details

### Best Practices

1.  **Check Before Create**: In `get_order`, always check if an ID already 
    exists in state. You don't want to create a brand new cart every time 
    the customer asks "What's in my cart?".
2.  **Error Handling**: If `add_to_cart` is called but no `order_id` is 
    found in state, return a message like "No active session found. Would 
    you like to start a new order?".

### Common Errors

**Error**: `AttributeError: 'ToolContext' object has no attribute 'get'`
- **Cause**: Trying to call `.get()` on the context object itself instead of 
  the `.state` dictionary.
- **Solution**: Use `tool_context.state.get("key")`.