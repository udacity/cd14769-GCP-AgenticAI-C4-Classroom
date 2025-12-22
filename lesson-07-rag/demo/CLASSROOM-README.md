# Lesson 07: Implementing Multi-Agent RAG

We will learn how to extend RAG capabilities to multiple cooperating agents by
creating a shipping inquiry agent that can retrieve information from both
unstructured policy documents in Vertex AI Search and structured order data
in a SQL database.

---

## Overview

### What You'll Learn

You will learn how to build a sophisticated inquiry system that combines the
power of vector search for natural language documents with precise database
lookups for transactional data. We will use a shipping inquiry agent to
demonstrate how an agent can answer policy questions from PDFs while
simultaneously tracking live orders from a MySQL database.

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

- A Google Cloud Project with Vertex AI Search (Agent Builder) and Cloud SQL
  enabled.
- A Google Cloud Storage (GCS) bucket for storing documents.
- The MCP Database Toolbox (`toolbox-core`) configured to point to your MySQL
  instance.
- Authentication configured for Google Cloud (Application Default Credentials).

---

## Setup

### 1. Environment Variables

Create or update your `.env` file in `lesson-07-rag/demo/shipping/` (and
`storefront/` if needed):

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

To enable the agent to search through documents, we need to upload them to Cloud
Storage and index them with Vertex AI Search (Agent Builder).

**A. Create a GCS Bucket & Upload Documents**

1. Go to **Cloud Storage** in the Google Cloud Console.
2. Create a new bucket (standard settings, enforce public access prevention).
3. Upload the files from `docs/policies` to this bucket.

**B. Create the Search App & Data Store**

1. Go to **Agent Builder** (Vertex AI Search and Conversation).
2. Create a new App -> **Search** -> **Generic**.
3. **Create a Data Store**:
    * Select **Cloud Storage**.
    * Select the bucket you created above.
    * Select **Unstructured documents**.
4. Link the Data Store to your App and create it.
5. Once created, copy the **Data Store ID** (Engine ID) from the Data Stores
   list and update `DATASTORE_ENGINE_ID` in your `.env`.

### 3. Database Setup

Ensure your MySQL database has the `shipping` schema loaded.

```bash
mysql -h <ip_address> -u root -p < docs/shipping.sql
```

### 4. Run MCP Toolbox

1. Open a **new terminal window**.
2. Navigate to the `docs` directory where `tools.yaml` is located.
   ```bash
   cd docs
   ```
3. Export your database credentials from your `.env` file (located in the parent
   directory) so the server can read them.
   ```bash
   export $(grep -v '^#' ../.env | xargs)
   ```
4. Run the toolbox server (assuming the `toolbox` binary is in your path or
   copied here):
   ```bash
   toolbox --tools-file tools.yaml --port 5001
   ```
   *Note: You may need to adjust the path to your `toolbox` binary.*
5. Update `TOOLBOX_URL` in your `.env` file to `http://127.0.0.1:5001`.

### 5. Run ADK Web

In the directory where all the agent directories are:

```bash
adk web --a2a
```

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
│   ├── tools.yaml    # SQL tool definitions
│   └── policies/     # Policy documents to be indexed
├── shipping/         # The backend fulfillment service
│   ├── agent.py      # Shipping orchestrator
│   ├── agents/
│   │   ├── inquiry.py   # RAG-enabled inquiry agent
│   │   ├── datastore.py # Helper for Vertex AI Search
│   │   ├── shipping.py  # fulfillment logic
│   │   ├── products.py  # Product data
│   │   └── rates.py     # Shipping rates
│   ├── prompts/
│   │   ├── agent-prompt.txt   # Shipping orchestrator prompt
│   │   ├── inquiry-prompt.txt # Inquiry logic prompt
│   │   └── ... (other prompts)
│   └── agent.json    # Agent Card
└── storefront/       # Primary user-facing agent
    ├── agent.py      # Connects to other agents via A2A
    ├── prompts/
    │   └── agent-prompt.txt # Storefront orchestrator prompt
    └── agent.json    # Storefront Agent Card
```

### Step 1: Configuring Database Tools (`docs/tools.yaml`)

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

### Step 2: Implementing the Search Tool (`shipping/agents/datastore.py`)

We use the Google Cloud Discovery Engine SDK to query our indexed documents.

```python
def datastore_search_tool(search_query: str):
  """Searches store information for the requested information."""
  return search(
    project_id=os.environ.get("DATASTORE_PROJECT_ID"),
    engine_id=os.environ.get("DATASTORE_ENGINE_ID"),
    location=os.environ.get("DATASTORE_LOCATION", "global"),
    search_query=search_query,
  )
```

**Key points:**

- This tool takes a natural language query and returns relevant "chunks" of text
  from our PDFs.
- It uses environment variables to keep the code portable across different
  projects.

### Step 3: The Inquiry Agent (`shipping/agents/inquiry.py`)

This is where the RAG logic comes together. The agent delegates specific
questions to specialized sub-agents.

```python
# inquiry.py
get_order_agent = Agent(
  name="get_order_agent",
  description="Handles questions about the status of orders",
  model=model,
  instruction=read_prompt("inquiry-order-prompt.txt"),
  tools=[get_order_tool],
)

policy_search_agent = Agent(
  name="datastore_search_agent",
  description="Handles questions about corporate store policies, including shipping policies",
  model=model,
  instruction=read_prompt("inquiry-policy-prompt.txt"),
  tools=[datastore_search_tool],
)

inquiry_agent = Agent(
  name="shipping_inquiry_agent",
  description="Handles questions about shipping policies and tracking.",
  model=model,
  instruction=read_prompt("inquiry-prompt.txt"),
  sub_agents=[get_order_agent, policy_search_agent],
)
```

**How it works:**

1. When a customer asks a question, the agent reviews the available sub-agents.
2. If the question is about a policy, it delegates to `policy_search_agent`,
   which uses `datastore_search_tool`.
3. If the question is about an order, it delegates to `get_order_agent`, which
   uses `get_order_tool`.
4. The sub-agents return their findings, and the inquiry agent synthesizes the
   answer.

### Complete Example

The **Shipping Orchestrator** connects these specialized agents.

```python
# agent.py
from .agents.shipping import shipping_agent
from .agents.inquiry import inquiry_agent

root_agent = Agent(
  name="shipping_orchestrator",
  description="Main orchestrator for shipping tasks.",
  model=model,
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
