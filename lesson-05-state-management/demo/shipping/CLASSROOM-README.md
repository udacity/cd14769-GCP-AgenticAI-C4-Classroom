# Implementing Advanced State Management with ADK

We will learn how to move beyond implicit history-based state and implement 
explicit, shared state management in ADK using the `InvocationContext` and 
`ToolContext`.

---

## Overview

### What You'll Learn

Commonly, agents relied on the conversation history (implicit 
state) to share information - the results of each tool call or sub-agent are 
visible to later agents through the conversation context.
In this lesson, you will learn how to use the ADK's session state to store 
and retrieve complex objects, such as an order, across different agents and 
tools.

Learning objectives:
- Understanding the difference between implicit and explicit state
- Reading and writing shared state within tools using `ToolContext`
- Accessing session state within a `CustomAgent` via `InvocationContext`
- Persisting state using Google Cloud Vertex AI Agent Engine

### Prerequisites

- Familiarity with ADK tool and agent definitions
- Access to Google Cloud with Vertex AI enabled

---

## Understanding the Concept

### The Problem

As a conversation progresses, the chat history grows. Relying on the LLM to 
accurately "remember" or extract specific data (like a subtotal or a 
customer ID) from several turns ago becomes unreliable and consumes 
valuable context tokens. Furthermore, passing large data structures 
between agents via chat text is inefficient and messy.

### The Solution

ADK provides a `session.state` dictionary that persists throughout the entire 
conversation session. This allows for **explicit state management**, where 
data is stored "out-of-band" from the conversation text. 
- **Tools** can store results directly into the session state.
- **Agents** (especially Custom Agents) can retrieve that data directly, 
  ensuring 100% accuracy regardless of the conversation length.

In a production environment, this state needs to live somewhere reliable. 
This is where the **Vertex AI Agent Engine** comes in. It acts as the 
backend for your agents, securely storing conversation history and session 
data in the cloud.

### How It Works

**Step 1: Storing State in a Tool**
When a tool is called, ADK can provide a `ToolContext`. The tool logic can 
then save data into `tool_context.state`. This data is now available to 
every other agent and tool in that session.

**Step 2: Retrieving State in an Agent**
A `CustomAgent` receives an `InvocationContext` when it runs. It can 
directly access `invocation_context.session.state` to retrieve the data 
previously saved by a tool or another agent.

**Step 3: Persistence with Agent Engine**
By configuring `adk web` to point to an Agent Engine resource, all 
`session.state` changes are automatically saved to Google Cloud. If the 
server restarts or the user switches devices, the state is preserved.

### Key Terms

**Explicit State**: Data stored in a structured way (like a dictionary) 
that is managed by the system, rather than inferred from text.

**ToolContext**: An object passed to ADK tools that provides access to the 
current session's state and other metadata.

**InvocationContext**: An object passed to agents that contains information 
about the current request, including the full session state.

**Agent Engine**: A managed service on Google Cloud that includes services for 
hosting and managing agent sessions and state.

---

## Setting up Agent Engine

To save session state in the Agent Engine session service,, you need to 
create an Agent Engine instance first.

### Prerequisites

Ensure you have your `.env` file set up with the following variables:

```bash
GOOGLE_GENAI_USE_VERTEXAI=TRUE
GOOGLE_CLOUD_PROJECT=<your project ID>
GOOGLE_CLOUD_LOCATION=us-central1
```

Replace `<your project ID>` with your actual Google Cloud Project ID.
`us-central1` is recommended for the location.

### Creating the Instance

1.  There is a `notes` folder that contains a `create_agent_engine.py` script.
2.  Run the `create_agent_engine.py` script:
    ```bash
    python create_agent_engine.py
    ```
3.  The script will output a **resource name**. Copy this value, since you
    will need it when you start `adk web` later.

If you lose the resource name, you can find it in the Google Cloud Console under
the Agent Engine configuration page.

---

## Code Walkthrough

### Repository Structure

```
shipping/
├── shipping.py       # Updated tool and router using session state
├── agent.py          # Root orchestrator
├── order_data.py     # Mock database
└── ...
```

### Step 1: Saving State in the Tool

In `shipping.py`, we update the `place_order` tool to accept a `ToolContext` 
and save the order object.

```python
def place_order(order_id: str, address: dict, tool_context: ToolContext):
    """Places an order and saves it to session state."""
    # ... logic to find and update order ...
    
    order = orders[order_id]
    order["address"] = address
    
    # Save the order object to the session state
    tool_context.state["order"] = order

    return {
        "cart": order.get("cart"),
        "address": order.get("address"),
    }
```

**Key points:**
- The `tool_context` is automatically injected by ADK.
- `tool_context.state` is where we store our explicit data.

### Step 2: Accessing State in the Custom Router

The `ShippingRouter` now retrieves the order directly from the session state 
instead of searching through previous events.

```python
class ShippingRouter(BaseAgent):
    async def _run_async_impl(self, context: InvocationContext) -> AsyncGenerator[Event, None]:
        # Retrieve the order directly from session state
        order = context.session.state.get("order")
        
        # Calculate subtotal using the retrieved object
        subtotal = compute_subtotal(order)
        
        # Programmatic routing based on the subtotal
        if subtotal >= self.free_threshold:
            subagent = self.free_agent
        else:
            subagent = self.standard_agent

        async for event in subagent.run_async(context):
            yield event
```

**Key points:**
- `context.session.state` provides direct access to the "backpack".
- This method is much more robust than parsing JSON from previous chat 
  messages.

### Complete Example

The integration remains the same in the `SequentialAgent`, but the 
underlying data flow is much more reliable.

```python
# The fulfillment workflow remains sequentially structured
fulfillment_workflow_agent = SequentialAgent(
    name="fulfillment_workflow",
    sub_agents=[
        place_order_agent,   # This agent's tool SETS the state
        costs_agent,         # This agent's router READS the state
        compute_order_agent,
        order_summary_agent,
    ],
)
```

**How it works:**
1. The customer provides their address.
2. `place_order_agent` invokes the tool, which saves the order to state.
3. `costs_agent` (containing the router) reads that order directly from 
   state to determine if free shipping applies.
4. The workflow continues with 100% data consistency.

Note that nowhere in our code do we specify that the session state is saved 
to Agent Engine. This is a runtime configuration and ADK handles the details 
for us automatically. This allows us to use other session services to save 
the information elsewhere depending on business and technical needs. If we 
do not specify a session service, `adk web` defaults to using a memory-only 
service that is cleared when `adk web` is restarted.

**Running the agent:**

To see session persistence in action, you need to use the Agent Engine.

1.  **Create an Engine Instance**: Run the provided setup script.
    ```bash
    python ../notes/create_agent_engine.py
    ```
    This will print a resource name (e.g., `projects/YOUR_PROJECT/locations/us-central1/agents/YOUR_AGENT_ID`).

2.  **Start the Web Server**:
    ```bash
    adk web --session_service_uri agentengine://projects/YOUR_PROJECT/locations/us-central1/agents/YOUR_AGENT_ID
    ```

**Expected output:**
Regardless of how much the customer chats in between, the system always 
knows the correct subtotal for the order because it is reading from the 
explicit session state stored in the cloud.

---

## Important Details

### Common Misconceptions

**Misconception**: "If I use session state, I don't need to return values 
from my tools."
**Reality**: You should still return values from tools so the LLM can 
inform the customer of what happened. Session state is for *internal* 
coordination between agents.

### Best Practices

1. **State Granularity**: Only store what is necessary in the session 
   state. Overloading it with too much data can make management difficult.
2. **Key Consistency**: Use clear and consistent keys (like "order" or 
   "customer_id") throughout your application.

### Common Errors

**Error**: `AttributeError: 'NoneType' object has no attribute 'get'`
- **Cause**: The agent tried to access a key in `session.state` that hasn't 
  been set yet.
- **Solution**: Always use `.get("key")` which returns `None` if the key is 
  missing, and handle the missing data case gracefully in your logic.

**Error**: "Errors related to Memory Bank connection or permissions."
- **Cause**: The service account running the agent may not have the necessary
  IAM permissions to access Vertex AI Agent Engine Memory Bank or you gave
  the incorrect resource name for the Memory Bank.
- **Solution**: Grant the required IAM roles (e.g., `Agent Engine User`) to the
  service account. Ensure the project ID and location are accurate.