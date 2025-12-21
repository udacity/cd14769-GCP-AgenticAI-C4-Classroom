# cd14769 - Lesson 06 - exercise

Implementing Multi-Agent State Coordination & Orchestration

- We've seen how to incorporate search through an agent that can access the PDF
  documents in our library.
- Setup
    - Ensure the MySQL database is running and populated with
      `docs/shipping.sql`.
    - Verify `.env` file has correct database credentials and `TOOLBOX_URL`.
    - Start the MCP Toolbox: `toolbox --tools-file tools.yaml --port 5001`.
    - Start the ADK web interface with A2A enabled: `adk web --a2a`.
- [docs/tools.yaml] Tool Configuration
    - Walk through the defined SQL tools: `get-order`,
      `get-open-order-for-user`, `add-item-to-cart`, etc.
    - Explain how `parameters` map to the `?` placeholders in the `statement`.
- [shopping/agents/cart.py] Database Connection & Tools
    - Show the connection to the toolbox:
      `db_client = ToolboxSyncClient(toolbox_url)`.
    - Highlighting the loading of tools: `get_order_tool`,
      `add_item_to_cart_tool`.
    - Show how these tools are passed to `get_order_agent` and `add_item_agent`.
    - Mention that `get_order_agent` is responsible for ensuring an active order
      session exists (checking for open orders first, then creating if needed).
- [shopping/agent.json] Shopping Agent Card
    - Show the `skills` definition: `shopping_manager`.
    - Explain that this exposes the Shopping Agent's capabilities (Cart
      management, Product search) via A2A.
- [storefront/agent.py] Storefront Orchestration
    - Show the configuration of `shopping_agent` as a `RemoteA2aAgent`, pointing
      to its Agent Card URL.
    - Explain how `root_agent` now orchestrates both `shipping_agent` and
      `shopping_agent` remotely.
- running the code
    - Ensure all services (Database, Toolbox, ADK Web) are running.
- demonstration
    - Open the ADK Web UI and select `storefront`.
    - Ask: "I want to buy some headphones."
        - Observe the Storefront routing the request to the `shopping_agent` (
          via A2A).
        - The Shopping Agent then routes to its internal `search_agent` to find
          products.
    - Ask: "Add the first one to my cart."
        - Observe the Storefront routing to `shopping_agent`.
        - The Shopping Agent routes to `cart_agent`.
        - `cart_agent` uses `get_order_agent` (calling `get-open-order-for-user`
          SQL tool) to get the Order ID.
        - `cart_agent` then uses `add_item_agent` (calling `add-item-to-cart`
          SQL tool) to update the database.
    - Verify the state persistence by querying the database directly (e.g.,
      `SELECT * FROM orders;`) or by asking the agent "What is in my cart?".
- conclusion and summary
