# cd14769 - Lesson 06 - exercise

Implementing Multi-Agent State Coordination & Orchestration

- We've seen how to incorporate persistent state and A2A coordination into our
  shopping agent, allowing it to share order data with the shipping agent through
  a database.
- Setup
    - Ensure the MySQL database is running and populated with
      `docs/shipping.sql`.
    - Verify `.env` file has correct database credentials and `TOOLBOX_URL`.
    - Start the MCP Toolbox: `toolbox --tools-file tools.yaml --port 5001`.
    - Start the ADK web interface with A2A enabled: `adk web --a2a`.
    - Although this will be running all the agents in a single `adk web` 
      instance, these agents could all be running separately.
- [storefront/agent.py] Storefront Orchestration
    - Show the configuration of `shopping_agent` as a `RemoteA2aAgent`, pointing
      to its Agent Card URL.
    - Explain how `root_agent` now orchestrates both `shipping_agent` and
      `shopping_agent` remotely, without importing their code directly.
- [docs/tools.yaml] Tool Configuration
    - Walk through the defined SQL tools: `get-order`,
      `get-open-order-for-user`, `add-item-to-cart`, etc.
    - Explain how `parameters` map to the `?` placeholders in the `statement`.
- [shopping/agents/cart.py] Database Connection & Tools
    - Show the connection to the toolbox:
      `db_client = ToolboxSyncClient(toolbox_url)`.
    - Highlighting the loading of tools: `get_order_tool`,
      `add_item_to_cart_tool`.
    - Show how these tools are passed to `get_order_agent` and `add_item_agent`
      replacing the previous in-memory dictionary.
    - Mention that `get_order_agent` is responsible for ensuring an active order
      session exists
      - It checks for open orders first, then creating if needed.
      - But the creation tool doesn't return any values.
      - We take care of this in the prompt.
- [shopping/prompts/get-order-prompt.txt]
    - The steps here seek to get the user id and locate the currently open 
      order for this user.
    - If there is no order id associated with this user, it needs to create 
      an order.
    - Since that tool doesn't return any values, if it does create an order, 
      it then needs to go look for an open order again.
- [shopping/agent.json] Shopping Agent Card
    - Show the `skills` definition: `shopping_manager`.
    - Explain that this exposes the Shopping Agent's capabilities (Cart
      management, Product search) via A2A so the Storefront can discover them.
- running the code
    - Ensure all services (Database, Toolbox, ADK Web) are running.
- demonstration
    - Open the ADK Web UI and select `storefront`.
    - Ask: "I want to buy some headphones."
        - Observe the Storefront routing the request to the `shopping_agent`
          (via A2A).
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