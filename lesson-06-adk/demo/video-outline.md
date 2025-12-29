# cd14769 - Lesson 06 - demo

Implementing Multi-Agent State Coordination with ADK & A2A

- We will learn how to build a distributed multi-agent system where a Storefront
  Agent and a Shipping Agent coordinate using the Agent-to-Agent (A2A) protocol
  and manage state via a shared MySQL database.
- Why Shared State?
    - When agents are independent services (as they are with A2A), they cannot
      share memory variables.
    - We can't pass the entire business state (inventory, all orders, etc.) back
      and forth in the chat context.
    - A shared SQL database acts as the "Single Source of Truth," allowing
      agents to coordinate asynchronously without tight coupling.
- A2A vs. MCP: Understanding the Difference
    - In this lesson, we use both. It is important to distinguish them:
    - **A2A (Agent-to-Agent):** Used for *delegation* and *coordination* between
      high-level agents. "I need you to handle this shipping request." (
      Storefront -> Shipping).
    - **MCP (Model Context Protocol):** Used for *grounding* and *tool
      access*. "I need to execute this specific SQL query." (Shipping Agent ->
      Database).
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
    - **A2A Deep Dive:** This allows the Storefront to be completely agnostic of
      how Shipping is implemented. It could be Python, Java, or Go. It just
      needs to speak A2A.
- [shipping/agent.json] The Agent Card
    - Defines the "skills" this agent exposes to the world (e.g.,
      `fulfill_order`).
    - **A2A Deep Dive:** This file acts as the "API Contract" or "Service
      Definition." It allows the Storefront agent to "discover" the Shipping
      agent's capabilities dynamically.
- [shipping/agents/shipping.py] Shared Database Access via MCP
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
    - Ask: "Ship order 1002 to Jane Doe, 12 Third St, Forth, tx, 56789."
    - Observe: The Storefront agent receives the request, recognizes it can't
      handle it, and delegates to the `shipping_agent` via A2A.
    - *Behind the Scenes:* Note that the Storefront didn't send the *order
      object*. It sent the *intent*. The Shipping agent looked up the order in
      the DB.
    - But we don't see any of that. We just see the reply.
    - If we want to see it, we can access the agent directly, or we can use 
      something like Cloud Trace to view it.
    - Switch to the `shipping` agent in the dropdown.
    - Ask: "What is the status of order 1001?"
    - Observe: The Shipping agent queries the database directly to answer
    - We see the activity in the debugger, proving it works as a standalone 
      service. 
- conclusion and summary
    - We've moved from monolithic agents that may contain sub-agents to 
      distributed systems, where a sub-agent may run remotely.
    - This is similar to how we may use MCP to run a tool remotely, on an 
      MCP server, but requires a more elaborate contract and handoff.
    - **A2A** enabled our agents to collaborate like separate microservices.
    - **MCP** enabled our agents to securely access external data (SQL) 
      through a tool.
    - **Shared Database** provided the coordination layer so agents stayed in
      sync.
    - This pattern allows us to build much more complicated and richer 
      agents that can run on separate servers, yet still delegate to each 
      other where it makes the most sense. We explore this even more in the 
      exercise.
