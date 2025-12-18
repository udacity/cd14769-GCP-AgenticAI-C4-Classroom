# Implementing Multi-Agent State Coordination with ADK & A2A

We will learn how to build a distributed multi-agent system where agents running 
as separate services coordinate to fulfill a user's request. We will use the 
Agent-to-Agent (A2A) protocol for communication and a shared database for 
state management.

---

## Overview

### What You'll Learn

In previous lessons, all agents ran within a single Python process. In this 
lesson, we will split the system into two independent services: a **Storefront 
Agent** (the user interface) and a **Shipping Agent** (the fulfillment 
backend). You will learn how to connect them using A2A and how they share data 
using a MySQL database via the MCP Database Toolbox.

Learning objectives:
- Configuring `RemoteA2aAgent` to connect to external services.
- Defining an Agent Card (`agent.json`) to publish capabilities.
- Using the MCP Database Toolbox to read/write shared state.

### Prerequisites

- Understanding of ADK orchestration.
- Basic familiarity with SQL.
- Access to Google Cloud with Vertex AI enabled.

---

## Understanding the Concept

### The Problem

In a microservices architecture, the "Shopping" team and the "Shipping" team 
might manage their own agents independently. They can't just import each 
other's Python classes. They need a standard way to communicate and a shared 
source of truth for business data.

### The Solution

1.  **Communication (A2A)**: The Storefront Agent treats the Shipping Agent as 
    a "remote tool". It uses the A2A protocol to discover the Shipping Agent's 
    capabilities (via its Agent Card) and send requests over HTTP.
2.  **State (Shared Database)**: Instead of passing massive JSON objects back 
    and forth or relying on transient session state, both agents connect to a 
    shared SQL database. The Storefront creates an order in the DB, and the 
    Shipping Agent reads/updates that same record.

### How It Works

**Step 1: The Storefront**
The user talks to the Storefront Agent. When they say "Ship my order", the 
Storefront Agent realizes it can't do that itself. It looks at its list of 
sub-agents and sees the `shipping_agent`.

**Step 2: The Handoff (A2A)**
The Storefront Agent sends an A2A request to the Shipping Agent. This request 
contains the conversation context but effectively hands control over.

**Step 3: Fulfillment**
The Shipping Agent receives the request. It uses the `MCP Database Toolbox` 
to look up the order details from the `orders` table using the user's ID. 
It processes the shipment, updates the database status to 'SHIPPED', and 
returns a summary to the Storefront.

---

## Code Walkthrough

### Repository Structure

```
lesson-06-adk/demo/
├── storefront/       # The primary agent facing the user
│   ├── agent.py      # Configures RemoteA2aAgent
│   └── agent.json    # Agent Card
├── shipping/         # The backend fulfillment service
│   ├── shipping.py   # Database tools and logic
│   ├── agent.json    # Agent Card defining "fulfill_order" skill
│   └── tools.yaml    # Toolbox configuration
└── docs/shipping.sql # Schema for the shared database
```

### Step 1: Defining the Remote Agent

In `storefront/agent.py`, we don't import the shipping class. We define a 
remote connection.

```python
shipping_agent = RemoteA2aAgent(
    name="shipping_agent",
    agent_card="http://localhost:8000/a2a/shipping/.well-known/a2a-agent-card.json"
)
```

**Key points:**
- The `agent_card` URL points to where the Shipping Agent publishes its 
  metadata.
- The Storefront Agent treats this just like any other sub-agent.

### Step 2: The Agent Card

In `shipping/agent.json`, the Shipping Agent advertises what it can do.

```json
{
  "skills": [
    {
      "id": "fulfill_order",
      "name": "Fulfill Order",
      "description": "Complete an order and prepare it for shipping",
      # ...
    }
  ]
}
```

**Key points:**
- This JSON file allows other agents to "discover" the Shipping Agent's 
  skills dynamically.

### Step 3: Shared Database Tools

In `shipping/shipping.py`, we load tools that connect to the database.

```python
db_client = ToolboxSyncClient(toolbox_url)
get_order_tool = db_client.load_tool("get-order")
```

**Key points:**
- The `ToolboxSyncClient` connects to the MCP Database Toolbox server.
- Tools like `get-order` map directly to SQL queries (defined in the Toolbox 
  configuration).

---

## Running the Demo

This demo requires running multiple services.

1.  **Start the Database Toolbox**:
    (Follow instructions in `docs/` or module guides to start the MCP Toolbox 
    pointing to your MySQL instance).

2.  **Start the Agents**:
    You will typically run these in separate terminal windows.
    
    *Window 1 (Shipping Service):*
    ```bash
    cd shipping
    adk run --port 8000
    ```
    
    *Window 2 (Storefront Service):*
    ```bash
    cd storefront
    adk web --port 8080
    ```

3.  **Interact**:
    Open your browser to the Storefront's URL (e.g., `http://localhost:8080`). 
    Ask: "Please ship my open order."

---

## Important Details

### Best Practices

1.  **Loose Coupling**: A2A allows agents to be written in different languages 
    or hosted on different clouds, as long as they speak the protocol.
2.  **Single Source of Truth**: Using a shared database prevents state 
    synchronization issues. If the Shipping Agent updates the status, the 
    Storefront sees it immediately.

### Common Errors

**Error**: `Connection refused`
- **Cause**: The Storefront can't reach the Shipping Agent's URL.
- **Solution**: Ensure the Shipping Agent is running and the URL in 
  `storefront/agent.py` matches the port where `shipping` is hosted.
