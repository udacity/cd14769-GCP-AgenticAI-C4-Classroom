# cd14769 - Lesson 03 - exercise

Implementing Agent Orchestration with ADK

- We've seen how to implement advanced orchestration patterns (Sequential and
  Parallel agents) as part of a robust and optimized shopping cart workflow.
- Setup
    - Open the `lesson-03-orchestration/exercises/solution` folder in your IDE.
    - Ensure your `.env` file is configured with your Google Cloud project
      details.
    - Install dependencies: `pip install -r requirements.txt`.
- [agent.py] Show the Orchestrator
    - Briefly show `root_agent` delegating to `cart_agent`.
- [agents/cart.py] Top-Down: The Cart Workflow
    - Highlight `cart_agent` as a `SequentialAgent`.
    - Explain the logic: First, we *must* prepare (get order, check stock),
      *then* we can add the item.
    - This ensures `add_item_agent` always has valid data.
- [agents/cart.py] Deep Dive: Parallel Preparation
    - Highlight `cart_prep_agent` as a `ParallelAgent`.
    - It runs `get_order_agent` and `inventory_data_agent` together.
    - **Why Parallel?**: Fetching the order session and checking inventory are
      independent network operations. Doing them in parallel saves time.
- [agents/cart.py] The Worker Agents
    - Briefly show `get_order_agent`, `add_item_agent`, and import of
      `inventory_data_agent`.
    - Show `prompts/add-item-prompt.txt` to illustrate how the leaf agent is
      instructed.
- running the code
- demonstration
    - Type: "Add product P001 to my cart."
    - **Trace the flow**:
        1. `root_agent` -> `cart_agent`.
        2. **Sequential Step 1**: `cart_prep_agent` (Parallel).
            - `get_order_agent` ensures an order ID exists.
            - `inventory_data_agent` checks if P001 is in stock.
        3. **Sequential Step 2**: `add_item_agent` runs.
            - It sees the order ID and the "In Stock" status from the previous
              step.
            - It successfully adds the item.
    - Try one that is out of stock: "Add product P003 to my cart."
- Conclusion
    - By combining Sequential and Parallel patterns, we created a "Cart
      Pipeline": Prepare -> Commit.
    - This structure is safer (checks inventory first) and faster (checks in
      parallel).
