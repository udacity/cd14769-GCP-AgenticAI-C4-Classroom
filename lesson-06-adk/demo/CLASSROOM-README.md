# Implementing Multi-Agent State Coordination with ADK & A2A

We will learn how to build a distributed multi-agent system where agents 
coordinate to fulfill a user's request as part of a shipping system. We will 
use the Agent-to-Agent (A2A) protocol for communication and a shared 
database for state management.

---

## Overview

### What You'll Learn

We will split the system into two independent agents: a **Storefront Agent** 
(the user interface) and a **Shipping Agent** (the fulfillment backend). You 
will learn how to connect them using A2A and how they share data using a MySQL 
database via the MCP Database Toolbox.

Learning objectives:
- Configuring `RemoteA2aAgent` to connect to external agents.
- Defining an Agent Card (`agent.json`) to publish capabilities.
- Using the MCP Database Toolbox to read/write shared state.
- Running multiple A2A agents within the ADK environment.

### Prerequisites

- Understanding of ADK orchestration.
- Basic familiarity with SQL, Google Cloud SQL, and MCP Database Toolbox
- Access to Google Cloud with Vertex AI enabled.
- A running MySQL instance.

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
    capabilities (via its Agent Card) and send requests.
2.  **State (Shared Database)**: Instead of passing massive JSON objects back 
    and forth or relying on transient session state, agents connect to a 
    shared SQL database.

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
returns a summary to the Storefront. Note that the Storefront Agent *does not* 
create the order; it assumes the order exists in the shared database (likely 
populated by a shopping cart service we aren't building in this specific demo).

---

## Infrastructure Setup

### 1. Google Cloud SQL (MySQL)

You need a MySQL database to act as the shared state.
- Create a MySQL instance in Google Cloud SQL.
- Create a database and user.
- Load the schema from `docs/shipping.sql`.
- Make sure you have added this configuration to your `.env` file.

### 2. Setup MCP Database Toolkit

1. If you have not already done so, download the latest release of the 
   **Google GenAI Toolbox** (MCP server) for your platform from
   the [official documentation](https://googleapis.github.io/genai-toolbox/getting-started/introduction/) or GitHub releases.
2. Make the binary executable (e.g., `chmod +x toolbox`).

### 3. Run the MCP Server

1. Navigate to the directory containing `tools.yaml`.
2. Export your database credentials from your `.env` file so the server can read
   them.
   ```bash
   export $(grep -v '^#' .env | xargs)
   ```
3. Run the toolbox server:
   ```bash
   ./toolbox --tools-file tools.yaml --port 5001
   ```
4. Update `TOOLBOX_URL` in your `.env` file to `http://127.0.0.1:5001`.

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

In `storefront/agent.py`, we define a remote connection.

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
- When we create the `shipping_agent` in the storefront, it will read the 
  agent card.

### Step 3: Shared Database Tools

In `shipping/shipping.py`, we load tools that connect to the database.

```python
db_client = ToolboxSyncClient(toolbox_url)
get_order_tool = db_client.load_tool("get-order")
```

**Key points:**
- The `ToolboxSyncClient` connects to the MCP Database Toolbox server.
- Tools like `get-order` map directly to SQL queries.

---

## Running the Demo

For this demo, we will run both agents within the same `adk web` process 
for simplicity, although A2A allows them to be completely separate services.

1.  **Configure Environment**:
    Ensure your `.env` file has the correct `TOOLBOX_URL` and `MYSQL_*` 
    credentials.

2.  **Start ADK Web**:
    From the `lesson-06-adk/demo` directory:
    ```bash
    adk web --a2a
    ```
    The `--a2a` flag tells ADK to look for `agent.json` files and enable 
    Agent-to-Agent communication features.

3.  **Interact**:
    Open your browser to the provided URL. Ask: "Please ship my open order."

---

## Important Details

### Best Practices

1.  **Loose Coupling**: A2A allows agents to be written in different languages 
    or hosted on different clouds, as long as they speak the protocol.
2.  **Single Source of Truth**: Using a shared database prevents state 
    synchronization issues. If the Shipping Agent updates the status, the 
    Storefront sees it immediately.

### Common Errors

**Error**: `Connection refused` (Toolbox)
- **Cause**: The `TOOLBOX_URL` in `.env` is incorrect or the Toolbox server 
  isn't running.
- **Solution**: Check the port number (default is often 5000 or 5001) and ensure 
  the binary is active.