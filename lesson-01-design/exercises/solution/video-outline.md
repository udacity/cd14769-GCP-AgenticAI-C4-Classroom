# cd14769 - Lesson 01 - exercise solution

E-Commerce System Design

- We have completed the design for a multi-agent e-commerce system, defining the
  architecture and agent interfaces using A2A Agent Cards.
- Setup
    - There is no code to run; we are reviewing design artifacts.
- [exercise-design-01-storefront.svg] The Storefront Architecture
    - Open the high-level design diagram.
    - Explain the **Storefront Agent** (Orchestrator):
        - It is the primary point of entry for the Customer.
        - It routes requests to **Shopping**, **Shipping**, **Account**, and *
          *Inventory**.
- [agent-01-storefront.json] The Storefront Contract
    - Open the Storefront Agent Card.
    - **Identity**: Name (`storefront`), Description (Orchestrator).
    - **Skills**: Highlight `handle_customer_request`.
        - This corresponds to the user input arrow in the diagram.
        - Also note skills like `shopping_agent` and `shipping_agent`. These
          represent the connections to the downstream agents.
- [agent-02-inventory.json] & [agent-03-account.json] Backend Services
  - Briefly mention Inventory (`check_stock`) and Account (
    `manage_subscriptions`).
  - These are backend utilities that support the main user flows.
- [agent-04-shopping.json] & [agent-05-shipping.json] Specialized Workers
    - Open the Shopping and Shipping cards.
    - **Shopping**:
        - Focus on skills like `manage_cart`, `search_products`.
        - This agent "owns" the shopping experience.
        - Can transfer to the shipping agent from the cart
    - **Shipping**:
        - Focus on skills like `fulfill_order`, `get_order_status`.
        - This agent encapsulates logistics.
    - **Key Concept**: Separation of Concerns. The Storefront doesn't know how
      to ship a box; it just knows the Shipping Agent *can* ship a box.
- Conclusion
    - By defining these Agent Cards, we have created a blueprint for our system.
    - Each card represents a clear boundary and a specific set of
      responsibilities.
    - This design prepares us to implement these agents independently while 
      also defining the boundaries how these agents may need to work together.
