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
- Configure MCP Toolbox tools using a YAML configuration.

### Prerequisites

- A running MySQL instance such as in Cloud SQL.
- The MCP Database Toolbox (`toolbox-core`) installed.
- Basic understanding of SQL and the MCP Database Toolbox.
- Basic understanding of ADK agents and tools.

---

## Setup

### 1. Environment Variables

Make sure you have a `.env` file in the `lesson-06-adk/exercises/starter/`
directory (or in both `shopping/` and `storefront/` if you prefer). It should
contain:

```env
GOOGLE_GENAI_USE_VERTEXAI=TRUE
GOOGLE_CLOUD_PROJECT=<your project ID>
GOOGLE_CLOUD_LOCATION=us-central1
TOOLBOX_URL=http://127.0.0.1:5001
MYSQL_HOST=<your mysql server IP address>
MYSQL_USER=<mysql user>
MYSQL_PASSWORD=<mysql password>
```

### 2. Setup Google Cloud SQL (or Local MySQL)

If you do not already have an SQL instance to use:

1. In the Google Cloud Console, go to **Cloud SQL**.
2. Select **Create Instance** -> **MySQL**.
3. Select **Enterprise** edition -> **Sandbox** preset.
4. Choose **MySQL 8.0**.
5. Set your Instance ID and root password.
6. Choose the **us-central1** region (Single zone).
7. Set Machine configuration to **1 vCPU**.
8. Create the instance.

Once created, get the **Public IP address** and set it as `MYSQL_HOST` in your
`.env`.

Connect to your database and create the schema:

```bash
mysql -h <ip_address> -u root -p < docs/shipping.sql
```

(You may need to grant permissions to your user as well).

### 3. Setup and Run MCP Toolbox

1. Open a **new terminal window**.
2. Navigate to the `docs` directory where `tools.yaml` is located.
   ```bash
   cd docs
   ```
3. Export your database credentials from your `.env` file (located in the parent directory) so the server can read them.
   ```bash
   export $(grep -v '^#' ../.env | xargs)
   ```
4. Run the toolbox server (assuming the `toolbox` binary is in your path or copied here):
   ```bash
   toolbox --tools-file tools.yaml --port 5001
   ```
   *Note: You may need to adjust the path to your `toolbox` binary.*
5. Update `TOOLBOX_URL` in your `.env` file to `http://127.0.0.1:5001`.

### 4. Run ADK Web

In the directory whith all the agent directories, start `adk web`:

```bash
adk web --a2a
```

---

## Exercise Instructions

### Your Task

You need to update the **Shopping Agent** to use the database instead of memory
and expose it via A2A. Then, you will update the **Storefront Agent** to
communicate with the Shopping Agent. The **Shipping Agent** is already provided
and needs no changes.

### Requirements

1. **Configure Tools (`docs/tools.yaml`)**:
    * Open `docs/tools.yaml`.
    * Replace the `TODO` placeholders with the correct tool configuration.

2. **Shopping Agent (`shopping/`)**:
    * **`agents/cart.py`**: Connect to the MCP Toolbox using `ToolboxSyncClient`.
    * **`agents/cart.py`**: Load tools (`get-order`, `create-order`,`add-item-to-cart`,
      `get-open-order-for-user`) from the toolbox.
    * **`agents/cart.py`**: Update `get_order_agent` and `add_item_agent` to use these
      database tools.
    * **`agent.json`**: Create this file to define the "Shopping Manager" skill
      and agent capabilities.

3. **Storefront Agent (`storefront/`)**:
    * **`agent.py`**: Define the `shopping_agent` as a `RemoteA2aAgent`.
    * **`agent.py`**: Add the `shopping_agent` to the orchestrator's sub-agents.

### Repository Structure

```
lesson-06-adk/exercises/starter/
├── docs/
│   ├── shipping.sql  # Database schema
│   └── tools.yaml    # TODO: Configure database tools
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
│   │   └── ... (other prompts)
│   └── agent.json    # Agent Card defining "fulfill_order" skill
├── shopping/         # Shopping and cart service
│   ├── agent.py      # Shopping orchestrator
│   ├── agents/
│   │   ├── cart.py      # TODO: Implement database cart logic
│   │   ├── inventory.py # Inventory check logic
│   │   ├── search.py    # Product search logic
│   │   ├── products.py  # Product data
│   │   └── order_data.py # Order data logic
│   ├── prompts/
│   │   ├── agent-prompt.txt     # Shopping orchestrator prompt
│   │   ├── search-prompt.txt    # Exact search prompt
│   │   └── ... (other prompts)
│   └── agent.json    # TODO: Create Agent Card
└── storefront/       # Primary user-facing agent
    ├── agent.py      # TODO: Connect to other agents via A2A
    ├── prompts/
    │   └── agent-prompt.txt # Storefront orchestrator prompt
    └── agent.json    # Storefront Agent Card
```

### Starter Code & Hints

#### 1. Configuring Tools (`docs/tools.yaml`)

You need to configure the tools, particularly with the SQL that the 
toolbox will execute and a definition of the parameters (in order) that will 
be given to the SQL.

```yaml
tools:
  get-order:
    kind: mysql-sql
    source: storefront
    description: Retrieve an order by its ID.
    parameters:
      - name: order_id
        type: integer
        description: The ID of the order to retrieve.
    statement: # TODO: Add the SQL here to execute this
```

#### 2. Shopping Agent (`shopping/cart.py`)

Establish the connection and load tools.

```python
# ... imports
from toolbox_core import ToolboxSyncClient

# ...

# TODO: Load the tools from the toolbox
# get_order_tool = db_client.load_tool("get-order")
# ...
```

#### 3. Shopping Agent Card (`shopping/agent.json`)

You must create this file. It defines how other agents see your shopping agent.

```json
{
  "name": "shopping",
  "url": "http://localhost:8000/a2a/shopping",
  "description": "Agent that manages shopping carts...",
  "skills": [
    {
      "id": "shopping_manager",
      "name": "Shopping Manager",
      "description": "Manage shopping cart and find products",
      "tags": [
        "Shopping",
        "Cart"
      ],
      "examples": [
        "Find headphones",
        "Add P001 to my cart"
      ]
    }
  ]
}
```

#### 4. Storefront Agent (`storefront/agent.py`)

Connect the storefront to the remote shopping agent.

```python
# ... imports
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent,
  AGENT_CARD_WELL_KNOWN_PATH

# TODO: create shopping agent
# shopping_agent = RemoteA2aAgent(
#    name="shopping_agent",
#    agent_card=f"http://localhost:8000/a2a/shopping{AGENT_CARD_WELL_KNOWN_PATH}"
# )
```

### Expected Behavior

**Example Usage:**

In the ADK Web interface, select the **Storefront Agent**.

User: "I want to buy some headphones."
Agent: (Routes to Shopping Agent -> Search) "I found these headphones..."
User: "Add the first one to my cart."
Agent: (Routes to Shopping Agent -> Cart -> Add Item) "Added to cart."

**Verification:**
After adding an item, query your MySQL database:

```sql
SELECT *
FROM orders;
```

You should see the item added to the table.

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
  port matches your `.env` and code (default is often 5000 or 5001, be
  consistent).

**Error**: "Table 'orders' doesn't exist."

- **Cause**: The database schema hasn't been loaded.
- **Solution**: Run the `docs/shipping.sql` script into your database.