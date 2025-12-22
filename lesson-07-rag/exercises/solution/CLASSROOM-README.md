# Lesson 07: Implementing Multi-Agent RAG

In this lesson, we demonstrated how to extend an agent's capabilities using 
Multi-Agent RAG. We enabled the shopping assistant to answer detailed product 
questions by searching unstructured documents in Vertex AI Search and to check 
real-time inventory levels using a SQL database.

---

## Overview

### What We Learned

We learned how to integrate specialized retrieval agents into a larger 
orchestration flow. By separating "Product QA" (unstructured RAG) from 
"Inventory" (structured SQL), we created a system that is both knowledgeable 
about product features and accurate about product availability.

Key Concepts:
- **Vertex AI Search**: Using a vector database to ground LLM answers in 
  technical documentation.
- **Structured Retrieval**: Using SQL tools via the MCP Database Toolbox for 
  precise data lookups.
- **Specialized Agents**: Creating dedicated agents for distinct retrieval tasks 
  to improve reliability and routing.

---

## Code Walkthrough

### Repository Structure

```
lesson-07-rag/exercises/solution/
├── docs/
│   ├── inventory.sql   # Database schema and data
│   ├── tools.yaml      # SQL tool definitions
│   └── P001.pdf...     # Product manuals for RAG
├── shopping/
│   ├── agent.py        # Main orchestrator
│   ├── agents/
│   │   ├── product_info.py # RAG-enabled QA agent
│   │   ├── datastore.py    # Vertex AI Search helper
│   │   ├── inventory.py    # SQL-based inventory agent
│   │   ├── cart.py         # Cart management logic
│   │   └── search.py       # Product search logic
│   ├── prompts/
│   │   ├── agent-prompt.txt      # Orchestrator prompt
│   │   ├── product-qa-prompt.txt # RAG instructions
│   │   ├── inventory-prompt.txt  # Inventory instructions
│   │   └── ... (other prompts)
│   └── __init__.py
```

### Step 1: Product QA Agent (`shopping/agents/product_info.py`)

We created a specialized agent solely for answering questions based on 
documents. This agent uses the `datastore_search_tool` to query Vertex AI 
Search.

```python
# The agent is instructed to ONLY use the search tool
qa_instruction = read_prompt("product-qa-prompt.txt")

product_qa_agent = LlmAgent(
    name="product_qa_agent",
    description="Answers questions about product details, features, and manuals.",
    tools=[datastore_search_tool],
    instruction=qa_instruction,
)
```

**Why this matters**: By isolating this logic, we ensure that general chat or 
inventory questions don't accidentally trigger a document search, and vice 
versa.

### Step 2: Database Inventory (`shopping/agents/inventory.py`)

We migrated the inventory check from a hardcoded dictionary to a live database 
query.

```python
# Connecting to the Toolbox
db_client = ToolboxSyncClient(toolbox_url)
check_inventory_tool = db_client.load_tool("check-inventory")

inventory_agent = Agent(
    # ...
    tools=[check_inventory_tool],
)
```

This ensures that if the warehouse database changes, the agent immediately knows.

### Step 3: Tool Definitions (`docs/tools.yaml`)

We defined the SQL interface for the inventory check and product search.

```yaml
  check-inventory:
    kind: mysql-sql
    source: storefront
    description: Check the inventory quantity for a product.
    parameters:
      - name: product_id
        type: string
    statement: SELECT product_id, (quantity > 0) as in_stock, quantity as count FROM inventory WHERE product_id = ?
  search-products:
    kind: mysql-sql
    source: storefront
    description: Search for products by name or description.
    parameters:
      - name: query
        type: string
        description: The search term.
    statement: SELECT * FROM products WHERE CONCAT(name, ' ', description) LIKE CONCAT('%', ?, '%')
```

### Step 4: Orchestration (`shopping/agent.py`)

The root agent now manages four distinct sub-agents: Search, Inventory, Cart, 
and Product QA.

```python
root_agent = Agent(
    name="shopping_orchestrator",
    sub_agents=[search_agent, inventory_agent, cart_agent, product_qa_agent],
)
```

The orchestrator's prompt (`agent-prompt.txt`) was updated to clearly define 
when to route to `Product QA` (for features/specs) vs. `Inventory` (for stock).

### Complete Example Flow

1.  **User**: "Does the X200 headset support Bluetooth 5.0?"
2.  **Orchestrator**: Routes to `product_qa_agent`.
3.  **Product QA**: Calls `datastore_search_tool("X200 bluetooth version")`.
4.  **Vertex AI Search**: Returns chunks from `P001.pdf`.
5.  **Agent**: "Yes, the X200 supports Bluetooth 5.0."
6.  **User**: "Great, do you have any in stock?"
7.  **Orchestrator**: Routes to `inventory_agent`.
8.  **Inventory**: Calls `check_inventory("P001")`.
9.  **Database**: Returns `{in_stock: true, count: 50}`.
10. **Agent**: "Yes, we have 50 units available."
