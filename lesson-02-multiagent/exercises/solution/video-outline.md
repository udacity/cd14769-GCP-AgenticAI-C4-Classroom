# cd14769 - Lesson 02 - exercise

Implementing Multi-Agent Architectures

- We've seen how to implement a modular multi-agent system where specialized
  agents handle search, inventory, and cart management, all coordinated by a
  central orchestrator.
- Setup
    - Ensure your `.env` file is configured with your Google Cloud project
      details.
    - Install dependencies if needed: `pip install -r requirements.txt`.
- [agent.py] Highlight the `root_agent` and its sub-agents
    - Point out that `root_agent` (the shopping orchestrator) manages three
      sub-agents: `search_agent`, `inventory_agent`, and `cart_agent`.
    - Explain how this hierarchy organizes the shopping flow into discovery,
      availability, and transaction.
- [prompts/agent-prompt.txt] Show the orchestrator's routing logic
    - Review the instructions that tell the orchestrator when to use each
      specialist.
    - For example, delegating "I want to buy X" to search, and "is it in stock?"
      to inventory.
- [agents/search.py] Show the specialized Search Agent
    - Highlight the `search_products` tool and the focused `search-prompt.txt`.
    - This agent's only job is to find products in the catalog.
- [agents/inventory.py] Show the Inventory Agent
    - Point out the `check_inventory` tool.
    - Explain that this agent is the "source of truth" for stock levels,
      separated from search.
- [agents/cart.py] Show the Cart Agent
    - Highlight the `add_to_cart` tool.
    - Note that this agent manages the transactional state, requiring an
      `order_id` and `product_id`.
- running the code
    - Open a terminal above the `solution` directory.
    - Run `adk web`.
    - Open the provided local URL in a browser.
- demonstration
    - Start with: "I'm looking for a laptop."
    - Observe the orchestrator delegating to the `search_agent`.
    - Once it finds the "Premium Laptop (P002)", ask: "Is it in stock?"
    - Show the orchestrator routing to the `inventory_agent`.
    - Finally, say: "Add it to my cart"
    - Show the `cart_agent` successfully adding the item.
- Conclusion
    - We've seen how decomposing a complex workflow into focused agents makes
      the system easier to build, test, and maintain.
    - Each agent can work independently, but is directed by the 
      orchestrator and guided by other parts of the conversation.
