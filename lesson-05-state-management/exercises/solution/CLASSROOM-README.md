# Implementing Advanced State Management with ADK

In this lesson, we updated a shopping agent to use advanced state 
management techniques. We modified the agent to store the current order ID 
in the session state, allowing for persistent and reliable access across 
different turns of conversation.

---

## Overview

### What You'll Learn

The solution demonstrates how to refactor the shopping agent to eliminate 
the reliance on passing `order_id` as a parameter between the customer and 
the tools. By using `ToolContext`, we can save and retrieve data from 
a persistent "backpack" that follows the user throughout the session.

Learning objectives:
- Implementing explicit state management using `ToolContext.state`.
- Decoupling user-facing tool parameters from internal state dependencies.
- Configuring the agent to use Google Cloud Vertex AI Agent Engine for 
  durable session storage.

### Prerequisites

- Understanding of ADK tools and agent orchestration.
- Access to Google Cloud with Vertex AI enabled.

---

## Understanding the Concept

### The Problem

In previous versions, the user had to know their Order ID to add items to 
the cart. If they forgot it, or if the conversation history became too 
long for the LLM to remember, the flow would break.

### The Solution

We use **Session State** to make the Order ID "sticky". 
1.  When `get_order` is first called, it generates an ID and saves it to 
    the backend state.
2.  In every subsequent call, `add_to_cart` looks into that backend state 
    to find the ID. 
The customer never needs to see or type the ID again.

---

## Code Walkthrough

### Repository Structure

```
.
├── agent.py          # Root orchestrator
├── agents/
│   ├── cart.py           # State management with ToolContext
│   ├── inventory.py      # Inventory logic
│   ├── search.py         # SearchRouter and search logic
│   ├── products.py       # Product catalog
│   └── order_data.py     # Shared order storage
├── prompts/
│   ├── agent-prompt.txt        # Orchestrator prompt
│   ├── search-prompt.txt       # Exact search prompt
│   ├── search-broad-prompt.txt # Broad search prompt
│   ├── inventory-prompt.txt    # Inventory agent prompt
│   ├── cart-prompt.txt         # Main cart agent prompt
│   ├── get-order-prompt.txt    # Order session prompt
│   └── add-item-prompt.txt     # Add-to-cart prompt
└── __init__.py
```

### Step 1: Saving the Sticky ID

In `agents/cart.py`, the `get_order` tool is updated to check for existing state 
before generating a new order.

```python
def get_order(tool_context: ToolContext):
    # Check if an order already exists for this session
    order_id = tool_context.state.get("order_id")

    if order_id is None:
        # First time! Create it and save it.
        order_id = get_next_order_id()
        tool_context.state["order_id"] = order_id
        # ... initialize order record ...

    return {"order_id": order_id, "order": orders[order_id]}
```

### Step 2: Retrieving State

In `agents/cart.py`, the `add_to_cart` tool signature is simplified. It no longer needs 
`order_id` passed from the user.

```python
def add_to_cart(product_id: str, tool_context: ToolContext):
    # Retrieve the active ID from the background session
    order_id = tool_context.state.get("order_id")
    
    if not order_id:
        return {"error": "No active order found."}
        
    # Proceed with order logic using order_id...
```

**Key points:**
- The signature is cleaner for the LLM.
- The data is retrieved with 100% reliability from the state dictionary.

---

## Running with Persistence

To see session persistence in action, you can use the Agent Engine to 
host your sessions in the cloud.

1.  **Initialize the Engine**:
    ```bash
    python ../notes/create_agent_engine.py
    ```
2.  **Run with the Cloud URI**:
    ```bash
    adk web --session_service_uri agentengine://YOUR_RESOURCE_NAME
    ```

**Expected output:**
You can start a conversation, stop `adk web`, restart it with the same 
URI, and the agent will still remember your active order ID because it 
was saved in the Vertex AI Agent Engine.

---

## Important Details

### Best Practices

1.  **State Isolation**: Notice how `search.py` remains unaware of the 
    session state. It's a "stateless" agent. Only the `Cart` agent needs 
    to manage transactional state.
2.  **Graceful Fallbacks**: Always handle the case where state might be 
    missing by returning a clear error that helps the LLM recover.

### Common Errors

**Error**: `KeyError: 'order_id'`
- **Cause**: Directly accessing `tool_context.state['order_id']` when the 
  key doesn't exist.
- **Solution**: Always use `.get('order_id')` and check for `None`.
