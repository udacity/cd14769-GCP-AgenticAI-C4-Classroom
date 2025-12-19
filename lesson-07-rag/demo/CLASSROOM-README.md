# Lesson 07: Implementing Multi-Agent RAG

In this lesson, we will learn how to incorporate multi-agent Retrieval Augmented
Generation (RAG) by creating an agent that can access both unstructured policy
documents in Vertex AI Search and structured order data in a SQL database.

---

## Overview

### What You'll Learn

You will learn how to build a sophisticated inquiry system that combines the
power of vector search for natural language documents with precise database
lookups for transactional data.

Learning objectives:

- Connect an ADK agent to a Vertex AI Search Data Store for unstructured data
  retrieval.
- Use the MCP Database Toolbox to retrieve structured session data (like order
  status) from a SQL database.
- Orchestrate multiple retrieval tools within a single specialized inquiry
  agent.
- Seamlessly hand off between a storefront entry point and a remote shipping
  agent using A2A.

### Prerequisites

- A Google Cloud Project with Vertex AI Search and Cloud SQL enabled.
- The MCP Database Toolbox (`toolbox-core`) configured to point to your MySQL
  instance.
- Authentication configured for Google Cloud (Application Default Credentials).

---

## Understanding the Concept

### The Problem

Customer support often involves two distinct types of information retrieval. A
customer might ask, "What is your return policy?" (which requires searching
through a PDF manual) and then immediately ask, "Where is my order #1005?" (
which requires querying a database). Managing these two data sources manually in
a single prompt is complex and prone to errors.

### The Solution

We implement a **Multi-Agent RAG** system. We create a specialized **Inquiry
Agent** that is equipped with two tools: one for searching the document
knowledge base and one for querying the live order database. The orchestrator
routes customer questions to this expert agent, which then decides which tool is
appropriate for the specific question.

### How It Works

**Step 1: Unstructured Retrieval (Vertex AI Search)**
The agent uses a "Search" tool to query a vector index of documents (like
shipping policies). This allows the LLM to provide answers "grounded" in company
policy rather than making them up.

**Step 2: Structured Retrieval (MCP Toolbox)**
The agent uses a SQL tool to look up the `order_status` in a MySQL table. This
provides real-time, accurate data about the customer's specific transaction.

**Step 3: Synthesis**
The agent combines the information from both sources (if necessary) to provide a
single, coherent response to the customer.

### Key Terms

**RAG (Retrieval Augmented Generation)**: A technique that grants an LLM access
to external data to improve the accuracy and relevance of its responses.
**Vertex AI Search**: A Google Cloud service that provides enterprise-grade
search and RAG capabilities over your own data.
**Structured vs. Unstructured Data**: Structured data lives in tables (SQL),
while unstructured data lives in documents (PDFs, text files).

---

## Code Walkthrough

### Repository Structure

```
lesson-07-rag/demo/
├── docs/
│   ├── shipping.sql  # Database schema
│   └── manuals/      # Policy documents to be indexed in Vertex AI Search
├── shipping/
│   ├── inquiry.py    # The RAG-enabled inquiry agent
│   ├── datastore.py  # Helper function for Vertex AI Search
│   ├── tools.yaml    # SQL tool definitions
│   └── agent.py      # Shipping orchestrator
└── storefront/
    └── agent.py      # Main entry point (A2A Client)
```

### Step 1: Configuring Database Tools (`tools.yaml`)

We define the SQL interface in a YAML file. The MCP Toolbox uses this to
generate tools that the agent can call.

```yaml
tools:
  get-order:
    kind: mysql-sql
    source: storefront
    description: Retrieve an order by its ID.
    parameters:
      - name: order_id
        type: integer
    statement: SELECT * FROM orders WHERE order_id = ?
```

**Key points:**

- The `description` helps the LLM understand *when* to use this tool.
- The `statement` ensures the LLM doesn't have to write raw SQL, preventing
  injection attacks.

### Step 2: Implementing the Search Tool (`datastore.py`)

We use the Google Cloud Discovery Engine SDK to query our indexed documents.

```python
def datastore_search_tool(search_query: str):
  """Searches store information for the requested information."""
  return search(
    project_id=os.environ.get("DATASTORE_PROJECT_ID"),
    engine_id=os.environ.get("DATASTORE_ENGINE_ID"),
    search_query=search_query,
  )
```

**Key points:**

- This tool takes a natural language query and returns relevant "chunks" of text
  from our PDFs.
- It uses environment variables to keep the code portable across different
  projects.

### Step 3: The Inquiry Agent (`inquiry.py`)

This is where the RAG logic comes together. The agent is given both the database
tool and the search tool.

```python
# inquiry.py
inquiry_agent = Agent(
  name="shipping_inquiry_agent",
  description="Handles questions about shipping policies and tracking.",
  model=model,
  instruction=read_prompt("inquiry-prompt.txt"),
  tools=[get_order_tool, datastore_search_tool],
)
```

**How it works:**

1. When a customer asks a question, the agent reviews the available tools.
2. If the question is about a policy, it calls `datastore_search_tool`.
3. If the question is about an order, it calls `get_order_tool`.
4. It then uses the results to answer the customer.

### Complete Example

The **Shipping Orchestrator** connects these specialized agents.

```python
# agent.py
shipping_agent = Agent(
  name="shipping_agent",
  instruction=shipping_instruction,
  sub_agents=[fulfillment_workflow_agent, approve_order_agent],
)

root_agent = Agent(
  name="shipping_orchestrator",
  instruction=orchestrator_instruction,
  sub_agents=[shipping_agent, inquiry_agent],
)
```

**Expected output:**

```
Customer: "What is your return policy, and where is my order #1?"
Agent: "Our return policy allows returns within 30 days of delivery. 
Regarding your order #1, its current status is 'shipped'."
```

---

## Important Details

### Best Practices

1. **Groundedness**: Always instruct your RAG agents to only answer based on the
   retrieved information. If the tool returns nothing, the agent should say it
   doesn't know rather than guessing.
2. **Clear Tool Descriptions**: The orchestrator relies on descriptions to route
   requests correctly. Ensure the description for the Search tool and the
   Database tool are distinct and descriptive.

### Common Errors

**Error**: "403 Permission Denied" when calling Vertex AI Search.

- **Cause**: The service account running the agent doesn't have the
  `Discovery Engine Viewer` role.
- **Solution**: Grant the necessary IAM permissions in the Google Cloud Console.

**Error**: "Database connection timeout."

- **Cause**: The MCP Toolbox is not running or the `TOOLBOX_URL` in `.env` is
  incorrect.
- **Solution**: Verify the Toolbox is running on the expected port and matches
  the `.env` configuration.
