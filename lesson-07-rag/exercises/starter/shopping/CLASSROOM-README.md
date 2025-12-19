# Lesson 07: Implementing Multi-Agent RAG

In this exercise, you will learn how to incorporate multi-agent Retrieval
Augmented Generation (RAG) by extending a shopping assistant. We will enable
it to access unstructured product information (like manuals) from Vertex AI
Search and live inventory data from a SQL database.

---

## Overview

### What You'll Learn

You will learn how to build a sophisticated product expert system that answers
customer questions using both structured and unstructured data.
You are starting with a basic orchestrator and some helper files, and your goal
is to wire up the specialized agents to their respective data sources.

Learning objectives:

- Connect an ADK agent to a Vertex AI Search Data Store for product research.
- Implement a specialized "Product QA" agent to handle technical questions.
- Transition the inventory agent from hardcoded data to a live SQL database
  using the MCP Database Toolbox.
- Update the main orchestrator to route between search, cart, inventory, and
  product knowledge.

### Prerequisites

- A Google Cloud Project with Vertex AI Search (Agent Builder) and Cloud SQL
  enabled.
- A Google Cloud Storage (GCS) bucket.
- The MCP Database Toolbox (`toolbox-core`) installed.
- Basic familiarity of Google Cloud, SQL, and the MCP Agent Toolbox.

---

## Setup

### 1. Environment Variables

Create or update your `.env` file:

```env
GOOGLE_GENAI_USE_VERTEXAI=TRUE
GOOGLE_CLOUD_PROJECT=<your project ID>
GOOGLE_CLOUD_LOCATION=us-central1

TOOLBOX_URL=http://127.0.0.1:5001

MYSQL_HOST=<your mysql server IP address>
MYSQL_USER=<mysql user>
MYSQL_PASSWORD=<mysql password>

DATASTORE_PROJECT_ID=<your project ID>
DATASTORE_ENGINE_ID=<your data store ID>
DATASTORE_LOCATION=global
```

### 2. Vertex AI Search Setup

1. **Create GCS Bucket**: Go to Cloud Storage in the console and create a new
   bucket.
2. **Upload Documents**: Upload the PDF files (`P001.pdf`, `P002.pdf`, etc.)
   found in the `docs` directory to your new
   bucket. These contain the product information your agent will search for.
3. **Create Search App**: Go to **Agent Builder**, create a new App -> **Search
   ** -> **Generic**.
4. **Create Data Store**: Select **Cloud Storage** as the source, pick your
   bucket, and select **Unstructured documents**.
5. **Get ID**: Once created, copy the **Data Store ID** (Engine ID) to your
   `.env` file as `DATASTORE_ENGINE_ID`.

### 3. Database & Toolbox

1. **Load Schema**: Connect to your MySQL instance and load the inventory data:
   ```bash
   mysql -h <ip> -u root -p < ../docs/inventory.sql
   ```
2. **Run Toolbox**: Navigate to the directory with the `tools.yaml` file and 
   start the toolbox:
   ```bash
   export $(grep -v '^#' .env | xargs)
   /path/to/toolbox --tools-file tools.yaml --port 5001
   ```

### 4. Run the Agent

```bash
adk web --a2a
```

---

## Exercise Instructions

### Your Task

Your task is to implement the Product QA functionality and migrate the
inventory check to the database.

### Requirements

Your implementation must:

1. **Configure Tools**: Update `tools.yaml` with the configuration for
   `check-inventory` and `search-products`.
2. **Implement Search Tool**: Complete the `datastore_search_tool` function in
   `datastore.py` to call the Vertex AI Search API.
3. **Inventory Migration**: Update `inventory.py` to use `ToolboxSyncClient` and
   the `check-inventory` tool.
4. **Product QA Agent**: Complete `product_info.py` to define an `LlmAgent` that
   uses your `datastore_search_tool`.
5. **Orchestrator Update**: Update `agent.py` and `agent-prompt.txt` to include
   the new Product QA Agent.

### Repository Structure

```
lesson-07-rag/exercises/starter/shopping/
├── inventory.py      # TODO: Connect to DB
├── datastore.py      # TODO: Implement search tool wrapper
├── product_info.py   # TODO: Define RAG agent
├── agent.py          # TODO: Add RAG agent to orchestrator
├── tools.yaml        # TODO: Define SQL for inventory
└── ...
```

---

## Starter Code & Hints

### 1. Implementing the Search Tool (`datastore.py`)

You need to call the `search` helper function using the environment variables.

```python
def datastore_search_tool(search_query: str):
  """
  Searches store information for the requested information.
  """
  # TODO: Get project_id, engine_id, location from os.environ
  # TODO: Call search(...) and return the result
```

### 2. Defining the RAG Agent (`product_info.py`)

Use the tool you just implemented.

```python
# TODO: Import datastore_search_tool

# TODO: Define product_qa_agent
# It should use the datastore_search_tool
# Its instruction should come from "product-qa-prompt.txt"
```

### 3. Inventory Tool (`tools.yaml`)

Define the SQL to check if a product is in stock.

```yaml
tools:
  check-inventory:
  # ...
  # TODO: Add statement: SELECT ... FROM inventory ...
```

### 4. Updating the Orchestrator (`agent.py`)

Don't forget to import and register your new agent!

```python
# TODO: Import product_qa_agent

root_agent = Agent(
  # ...
  sub_agents=[...],  # TODO: Add it here
)
```

---

## Important Details

### Best Practices

1. **Instruction Quality**: In `product-qa-prompt.txt`, instruct the agent to
   rely *only* on the search tool results. This reduces hallucinations.
2. **Tool Descriptions**: The orchestrator uses agent and tool descriptions to
   route requests. Ensure the "Product QA Agent" description clearly mentions it
   handles features, manuals, and technical specs.

### Common Errors

**Error**: "Discovery Engine API not enabled."

- **Solution**: Enable the "Vertex AI Search and Conversation" API in the Google
  Cloud Console.

**Error**: `check-inventory` returns no results.

- **Solution**: Ensure your SQL query in `tools.yaml` correctly filters by the
  `product_id` parameter (e.g., `WHERE product_id = ?`).
