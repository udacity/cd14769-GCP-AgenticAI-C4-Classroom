# cd14769 - Lesson 06 - demo

Implementing Multi-Agent State Coordination with ADK & A2A

- We will learn how to build a distributed multi-agent system where a Storefront
  Agent and a Shipping Agent coordinate using the Agent-to-Agent (A2A) protocol
  and manage state via a shared MySQL database.
- Setup
    - Ensure you have a MySQL database instance (e.g., Google Cloud SQL) running
      and populated with `docs/shipping.sql`.
    - Configure the `.env` file with your database credentials (`MYSQL_HOST`,
      `MYSQL_USER`, etc.) and `TOOLBOX_URL`.
    - Download and install the Google GenAI Toolbox (MCP server).
    - Open a terminal in `lesson-06-adk/demo/docs`.
    - Export environment variables: `export $(grep -v '^#' ../.env | xargs)`
    - Run the MCP Toolbox: `toolbox --tools-file tools.yaml --port 5001` (adjust
      command based on your binary location/name and the port you want to use).
- [storefront/agent.py] `RemoteA2aAgent` configuration
    - Shows how the Storefront agent treats the Shipping agent as a remote
      dependency.
    - Points to the `agent_card` URL (e.g.,
      `http://localhost:8000/a2a/shipping/.well-known/a2a-agent-card.json`).
    - This is the key difference from standard sub-agents; we aren't importing
      Python code directly.
- [shipping/agent.json] The Agent Card
    - Defines the "skills" this agent exposes to the world (e.g.,
      `fulfill_order`).
    - Allows the Storefront agent to "discover" what the Shipping agent can do
      without knowing its internal implementation.
- [shipping/agents/shipping.py] Shared Database Access
    - Uses `ToolboxSyncClient` to connect to the running MCP Toolbox.
    - Loads tools like `get-order` which map directly to SQL queries defined in
      `docs/tools.yaml`.
    - Demonstrates state management: the Shipping agent reads/writes to the DB,
      which acts as the single source of truth.
- running the code
    - Ensure the MCP Toolbox is running in its own terminal window.
    - In a new terminal, navigate to `lesson-06-adk/demo`.
    - Start the ADK web interface with A2A enabled: `adk web --a2a`
- demonstration
    - Open the web UI (e.g., `http://localhost:8080`).
    - Select the `storefront` agent.
    - Ask: "Please ship my open order."
    - Observe: The Storefront agent receives the request, recognizes it can't
      handle it, and delegates to the `shipping_agent` via A2A. The Shipping
      agent then updates the database.
    - Switch to the `shipping` agent in the dropdown.
    - Ask: "What is the status of order 1001?"
    - Observe: The Shipping agent queries the database directly to answer,
      proving it works as a standalone service and that state is persisted in
      the database, not just in memory.
- conclusion and summary
