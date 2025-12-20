# Lesson 06: Implementing Multi-Agent State Coordination & Orchestration

In this lesson, we demonstrated how to coordinate state across multiple
independent agents using a shared database and the Agent2Agent (A2A) protocol.
We evolved the shopping assistant to store order data in a MySQL database,
allowing different agents to access the same order information without sharing
memory.

---

## Overview

### What We Learned

We learned how to decouple agent state from the agent instance by persisting
it to an external database. We also learned how to expose an agent as an
A2A service and how to consume that service from another agent.

Key Concepts:

- **Persistent State**: Using a SQL database to store cart and order info.
- **MCP Database Toolbox**: Connecting an LLM to the database safely.
- **A2A Coordination**: Using Agent Cards to define and consume remote services.

---

## Code Walkthrough

### Repository Structure

```
lesson-06-adk/exercises/solution/
├── docs/
│   └── tools.yaml    # Tool definitions for the toolbox
├── shipping/         # Backend fulfillment service
│   ├── agent.py      # Shipping orchestrator
│   ├── agents/
│   │   ├── shipping.py # Database tools and logic
│   │   ├── inquiry.py  # Inquiry logic
│   │   ├── products.py # Product logic
│   │   └── rates.py    # Shipping rates logic
│   ├── prompts/
│   │   ├── agent-prompt.txt         # Shipping orchestrator prompt
│   │   ├── shipping-prompt.txt      # Shipping logic prompt
│   │   ├── inquiry-prompt.txt       # Inquiry logic prompt
│   │   └── ... (other prompts)
│   └── agent.json    # Agent Card defining "fulfill_order" skill
├── shopping/         # Shopping and cart service
│   ├── agent.py      # Shopping orchestrator
│   ├── agents/
│   │   ├── cart.py      # Database cart logic
│   │   ├── inventory.py # Inventory check logic
│   │   ├── search.py    # Product search logic
│   │   ├── products.py  # Product data
│   │   └── order_data.py # Order data logic
│   ├── prompts/
│   │   ├── agent-prompt.txt     # Shopping orchestrator prompt
│   │   ├── search-prompt.txt    # Exact search prompt
│   │   ├── cart-prompt.txt      # Cart management prompt
│   │   └── ... (other prompts)
│   └── agent.json    # Agent Card for shopping service
└── storefront/       # Primary user-facing agent
    ├── agent.py      # Connects to other agents via A2A
    ├── prompts/
    │   └── agent-prompt.txt # Storefront orchestrator prompt
    └── agent.json    # Storefront Agent Card
```

### Step 1: Tool Configuration (`docs/tools.yaml`)

We configured the MCP Database Toolbox to expose specific SQL queries as tools.
This provides a safe interface for the agents to interact with the database.

```yaml
  get-order:
    kind: mysql-sql
    source: storefront
    description: Retrieve an order by its ID.
    parameters:
      - name: order_id
        type: integer
    statement: SELECT * FROM orders WHERE order_id = ?
```

### Step 2: Shopping Agent - Database Connection (`shopping/agents/cart.py`)

The shopping agent connects to the toolbox and loads the tools. We replaced the
in-memory `orders` dictionary with these database tools.

```python
# Connecting to the Toolbox
toolbox_url = os.environ.get("TOOLBOX_URL", "http://127.0.0.1:5000")
db_client = ToolboxSyncClient(toolbox_url)

# Loading tools
get_order_tool = db_client.load_tool("get-order")
add_item_to_cart_tool = db_client.load_tool("add-item-to-cart")
```

The sub-agents were updated to use these tools:

```python
get_order_agent = LlmAgent(
    name="get_order_agent",
    description="Ensures an active order session exists.",
    # ...
    tools=[get_user_id, get_open_order_for_user_tool, create_order_tool],
)
```

### Step 3: Shopping Agent Card (`shopping/agent.json`)

We defined the `agent.json` file to describe the shopping agent's capabilities to
the outside world (specifically, the Storefront agent).

```json
{
  "name": "shopping",
  "url": "http://localhost:8000/a2a/shopping",
  "description": "Agent that manages shopping carts...",
  "skills": [
    {
      "id": "shopping_manager",
      "name": "Shopping Manager",
      "tags": ["Shopping", "Cart"],
      "examples": ["Find headphones", "Add P001 to my cart"]
    }
  ]
}
```

### Step 4: Storefront Orchestration (`storefront/agent.py`)

The Storefront agent acts as the main entry point. It doesn't have the shopping
logic itself; instead, it connects to the `shopping_agent` via A2A.

```python
# Define the remote A2A agent
shopping_agent = RemoteA2aAgent(
    name="shopping_agent",
    agent_card=f"http://localhost:8000/a2a/shopping{AGENT_CARD_WELL_KNOWN_PATH}"
)

root_agent = Agent(
    name="storefront_agent",
    description="Main storefront orchestrator.",
    sub_agents=[shipping_agent, shopping_agent],
)
```

**Key Point**: The `storefront_agent` doesn't need to know *how* the shopping
agent works (database, logic, etc.). It just knows *what* it can do via the
Agent Card.

### complete Example Flow

1.  **User**: "Find me a headset."
2.  **Storefront**: Routes to `shopping_agent` (Remote).
3.  **Shopping**: Receives request, routes to `search_agent`.
4.  **Search**: Returns product info.
5.  **User**: "Add it to my cart."
6.  **Storefront**: Routes to `shopping_agent`.
7.  **Shopping**: Routes to `cart_agent` -> `get_order_agent`.
8.  **Get Order**: Calls `get_open_order_for_user` (SQL: `SELECT ...`). Returns Order ID.
9.  **Add Item**: Calls `add_item_to_cart` (SQL: `UPDATE ...`).
10. **Result**: "Added to cart."

You can verify the result by querying the database:
```sql
SELECT * FROM orders;
```
