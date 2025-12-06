# Module 07 Exercise Starter

This exercise builds upon the concepts of state management and introduces Multi-Agent RAG with Vertex AI Search and MCP Database Toolbox.

Your goal is to extend the existing shopping cart agent to answer questions about products and check their available quantity.

## Exercise Description

Extend the shopping cart so it can answer questions about a product, including product information (from Vertex AI Search) and quantity available (from the database through MCP Database Toolbox).

### Tasks:

1.  **Integrate Vertex AI Search for Product Information:**
    *   Create a new Python file (e.g., `rag_tools.py`) to house a function that queries Vertex AI Search for product information.
    *   This function should take a `query` (e.g., product name, feature, question) and return relevant information from your configured Vertex AI Search Data Store.
    *   Add this new function as a tool to a new or existing agent (e.g., `product_qa_agent`).
    *   Update the main `shopping_orchestrator` in `agent.py` to route product-related questions to this new agent.

2.  **Integrate MCP Database Toolbox for Product Quantity:**
    *   Modify the `inventory_agent` (in `inventory.py`) to use `toolbox_core.ToolboxSyncClient` to connect to a MySQL database.
    *   Assume a tool named `check-inventory` is exposed by the MCP Toolbox, which can query product quantities from the `inventory` table in your database.
    *   Update the `inventory_agent` to use this `check-inventory` tool instead of the hardcoded product data.

3.  **Update `requirements.txt`:**
    *   Add `google-cloud-discoveryengine` and `toolbox-core` to `requirements.txt`.

4.  **Update Environment and Setup:**
    *   Ensure your `.env` file (or environment variables) includes `PROJECT_ID`, `LOCATION`, `DATA_STORE_ID` for Vertex AI Search, and `TOOLBOX_URL`, `MYSQL_HOST`, `MYSQL_USER`, `MYSQL_PASSWORD` for the MCP Toolbox and MySQL database.
    *   Set up your Vertex AI Search Data Store with product information.
    *   Set up your MySQL database with an `inventory` table and populate it with product quantities. An `inventory.sql` file is provided in the `docs/` folder to help with this.

## Environment Setup

```bash
# .env file example
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

Make sure you replace <your project ID> with the ID for your project.

Using a LOCATION of us-central1 is usually the best bet in the United States,
but consider other cloud data center locations for elsewhere.

See below for the values that are needed for the TOOLBOX_URL and the
various MYSQL environment variables

## Additional Setup

### Vertex AI Search Setup

1.  Enable the Vertex AI Search and Conversation API in your Google Cloud Project.
2.  Go to the [Agent Builder console](https://console.cloud.google.com/gen-app-builder/engines).
3.  Create a new App of type "Search".
4.  Select "Generic" as the content type.
5.  Create a new Data Store (Cloud Storage or Upload).
6.  Upload product information (e.g., product descriptions, manuals, FAQs) to the Data Store.
    For example, you can create text files for each product and upload them.
7.  Once created and the app is linked to the data store, get the **Data Store ID** from the Data Stores tab.
8.  Set the `DATA_STORE_ID`, `PROJECT_ID`, and `LOCATION` in your environment variables (or .env file).

### Setup Google Cloud SQL

If you do not already have an SQL instance to use:

1. In the Google Cloud Console, go to the "Cloud SQL" configuration. (Hint:
   You can search for it in the search bar.)
2. Select "Create Instance"
3. Choose MySQL
4. Select the Enterprise edition. **Not** the "Enterprise Plus" edition
5. Select Edition preset: Sandbox
6. Choose Database version: MySQL 8.0
7. Set the Instance ID
8. Set the root password
9. Choose the "us-central1" region with a Single zone. (You can choose
   another region, but it should be the one that most of your project runs in.)
10. Select Customize your instance
11. Change the Machine configuration to 1 vCPU
12. You can leave other settings alone and select the "Create instance" button.

Once the instance is created / updated, you can get the Public IP address
from the list of instances and enter it as the value for MYSQL_HOST in your
.env file.

You can then connect to the database server using the local mysql command
with something like:

```
mysql -h <ip_address> -u root -p 
```

You can then load in the database and files with a MySQL command
`\s ../docs/inventory.sql`.

You then need to permit your user to the database with a MySQL commands such as
```mysql
GRANT SELECT ON `db_name`.* TO `user_name`@`%`;
```

### Setup and run MCP Toolbox

See [here](https://googleapis.github.io/genai-toolbox/getting-started/introduction/)
for how to download the toolbox server for your platform.

To run the MCP server:
1. From the command line, change directories to where your tools.yaml file is
2. Make sure the MYSQL environment variables are exported in your current
   command line
    - If this is using bash, for example, you might do this as something like
      `export $(grep -v '^#' .env | xargs)`
3. Run `/path/to/toolbox --tools-file tools.yaml`
    - If you need to use another port, you can include a --port parameter

Update the TOOLBOX_URL in the .env file to specify the hostname (usually
localhost) and port the MCP Server is listening to.
