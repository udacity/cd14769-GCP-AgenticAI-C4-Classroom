# Lesson 06: Implementing Multi-Agent State Coordination & Orchestration

In this lesson, we will learn how to coordinate state across multiple
independent agents using a shared database and the Agent2Agent (A2A) protocol.
Starting with a shopping assistant, we will evolve it to store order data 
in a MySQL database, allowing a shipping agent to access the same
order information without sharing memory.

---

## Overview

### What You'll Learn

You will learn how to decouple agent state from the agent instance by persisting
it to an external database. You will also learn how to expose your agent as an
A2A service and how to consume that service from another agent.

Learning objectives:

- Connect an ADK agent to a SQL database using the MCP Database Toolbox.
- Supplement in-memory state management with persistent database storage.
- Define an A2A Agent Card (`agent.json`) to expose agent capabilities.
- Coordinate multiple agents (Storefront, Shopping, Shipping) where state is
  shared via the database.

### Prerequisites

- A running MySQL instance (Cloud SQL or local).
- The MCP Database Toolbox (`toolbox-core`) running and connected to the
  database.
- Basic understanding of ADK agents and tools.

---

## Understanding the Concept

### The Problem

In previous lessons, our agents maintained state (like the shopping cart) in
memory. This works fine for a single conversation, but it fails when:

1. **Scaling**: Multiple instances of the agent can't share the cart.
2. **Handoff**: A different agent (e.g., Shipping) needs to process the order
   but runs in a separate process or server.
3. **Persistence**: If the agent restarts, the cart is lost.

### The Solution

We move the state to a shared database. The **Shopping Agent** writes items to
the database, and the **Shipping Agent** reads the completed order from the same
database. The **Storefront Agent** orchestrates the interaction between the user
and these specialized agents using A2A.

### Key Terms

**MCP Database Toolbox**: A set of tools that allow LLMs to interact with SQL
databases safely.
**A2A (Agent2Agent)**: A protocol for agents to discover and communicate with
each other over a network.
**Agent Card**: A JSON file that describes an agent's capabilities (skills) to
other agents.

---

## Exercise Instructions

### Your Task

You need to update the **Shopping Agent** to use the database instead of memory
and expose it via A2A. Then, you will update the **Storefront Agent** to
communicate with the Shopping Agent.

### Requirements

Your implementation must:

1. **Shopping Agent**:
    * Connect to the MCP Toolbox using `ToolboxSyncClient`.
    * Load tools (`get-order`, `create-order`, `add-item-to-cart`,
      `get-open-order-for-user`) from the toolbox.
    * Update `get_order_agent` and `add_item_agent` to use these database tools.
    * Complete `agent.json` to define the "Shopping Manager" skill.
2. **Storefront Agent**:
    * Define the `shopping_agent` as a `RemoteA2aAgent`.
    * Add the `shopping_agent` to the orchestrator's sub-agents.

### Repository Structure

```
lesson-06-adk/exercises/starter/
├── shopping/
│   ├── cart.py       # TODO: Connect to DB and update tools
│   ├── agent.json    # TODO: Define Agent Card
│   ├── agent.py      # The shopping agent root
│   └── ...
└── storefront/
    ├── agent.py      # TODO: Connect to Shopping Agent via A2A
    └── ...
```

Make sure you copy `.env-sample` to `.env` in both directories (or the parent
directory if shared) and configure your `TOOLBOX_URL` and MySQL credentials.

**Note**: You need to have the MCP Database Toolbox running and pointing to your
MySQL database.

### Starter Code

#### 1. Shopping Agent (`shopping/cart.py`)

You need to establish the connection to the toolbox and load the necessary
tools.

```python
# ... imports

# --- Database Connection ---
toolbox_url = os.environ.get("TOOLBOX_URL", "http://127.0.0.1:5000")

# TODO: Connect to the Toolbox
# db_client = ToolboxSyncClient(toolbox_url)

# TODO: Load the tools from the toolbox
# get_order_tool = ...
# create_order_tool = ...
# ...

# --- Sub-Agents ---

get_order_agent = LlmAgent(
  # ...
  # TODO: Update tools to use the database tools and get_user_id
  tools=[],
)
```

#### 2. Shopping Agent Card (`shopping/agent.json`)

Define the skill that the shopping agent provides.

```json
{
  "name": "shopping",
  "url": "http://localhost:8000/a2a/shopping",
  ...
  "skills": [
    {
      "id": "shopping_manager",
      "name": "Shopping Manager",
      "description": "Manage shopping cart and find products",
      "tags": [
        "Shopping",
        "Cart",
        "Search"
      ],
      "examples": [
        "Find headphones",
        "Add P001 to my cart",
        "What is in my cart?"
      ]
    }
  ]
}
```

#### 3. Storefront Agent (`storefront/agent.py`)

Connect the storefront to the remote shopping agent.

```python
# ... imports

# TODO: create shopping agent
# shopping_agent = RemoteA2aAgent(
#    name="shopping_agent",
#    agent_card=f"http://localhost:8000/a2a/shopping{AGENT_CARD_WELL_KNOWN_PATH}"
# )

root_agent = Agent(
  name="storefront_agent",
  # ...
  # TODO: Add shopping and shipping sub-agents
  sub_agents=[shopping_agent, shipping_agent],
)
```

### Expected Behavior

**Running the System:**

1. Start the **Database** (MySQL).
2. Start the **MCP Toolbox** connected to the database.
3. Start the **ADK Web** server from the directory where all the agents are 
   listed:
   ```bash
   adk web --a2a
   ```

**Example Usage:**

In the ADK Web interface, select the **Storefront Agent**.

User: "I want to buy some headphones."
Agent: (Routes to Shopping Agent -> Search) "I found these headphones..."
User: "Add the first one to my cart."
Agent: (Routes to Shopping Agent -> Cart -> Add Item) "Added to cart."

**Behind the Scenes:**

- The Shopping Agent uses the `add-item-to-cart` tool which executes a SQL
  `INSERT` into the `order_items` table.
- You can verify this by querying the database directly.

### Implementation Hints

1. **Toolbox Connection**: The `ToolboxSyncClient` simplifies loading tools. You
   don't need to define the tool functions manually; the toolbox provides them
   based on the SQL configuration.
2. **Tool Context**: The `get_user_id` tool is a helper to extract the user ID
   from the `ToolContext`. The database tools often require `user_id` to fetch
   the correct order.
3. **A2A URLs**: Ensure the `url` in `agent.json` matches where the ADK Web
   server is hosting the agent (usually
   `http://localhost:8000/a2a/<agent-name>`).

---

## Important Details

### Common Misconceptions

**Misconception**: "I need to pass the cart items between agents in the prompt."
**Reality**: With a shared database, you only need to pass the `order_id` or
`user_id`. The agents look up the current state from the database.

**Misconception**: "A2A is just for remote servers."
**Reality**: A2A is useful even for local development to decouple agents. It
forces you to define clear interfaces (Agent Cards) and makes future deployment
to separate services easier.

### Common Errors

**Error**: "Connection refused" when connecting to Toolbox.

- **Cause**: The Toolbox server isn't running or the `TOOLBOX_URL` is incorrect.
- **Solution**: Check the terminal where you started the Toolbox and verify the
  port.

**Error**: "Table 'orders' doesn't exist."

- **Cause**: The database schema hasn't been loaded.
- **Solution**: Run the `docs/shipping.sql` script (from the demo or solution)to
  create the tables.
