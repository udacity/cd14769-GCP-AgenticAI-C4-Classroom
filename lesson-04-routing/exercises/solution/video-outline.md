# cd14769 - Lesson 04 - exercise solution

Implementing Custom Routing and Conditional Logic

- In this exercise, you were asked to implement advanced routing logic using 
  `CustomAgent`. This let us do two different tasks
  - The first was to allow us to do A/B testing of a new feature. We needed 
    careful control of this, so we wrote code that routed between two 
    different agents based on a random number
  - The second was conditional execution based on data from previous steps. 
    Depending on how many items were in stock, we could have another agent 
    take action, or skip that agent completely.
- [agents/search.py] A/B Testing with `SearchRouter`
    - Highlight `search_products_broad`: The new tool logic that matches any
      word.
    - Show `search_agent_broad`: The new agent configuration using the broad
      search tool.
    - **Key Change**: The `SearchRouter` class.
        - Walk through `_run_async_impl`.
        - Explain the `random.random()` check for A/B testing.
        - Show how it delegates to either `agent_a` (exact) or `agent_b` (
          broad).
        - An important step is executing the sub-agent and yielding all the 
          event results that it returns. This is how we route to the next 
          agent in the chain.
    - Show the instantiation of `search_agent` as the router, hiding the
      complexity from the rest of the system.
- [agents/inventory.py] Conditional Logic in Inventory
    - **Key Change**: `PossiblyReorderAgent`.
        - Walk through the logic of inspecting `context.session.events`.
        - Explain finding the output from `check_inventory_agent` (the previous
          step).
        - Show the conditional check: `if inventory_data.count < 5`.
        - If true, it runs `reorder_agent`. If false, it does nothing (pass).
    - **Key Change**: `inventory_data_agent` as a `SequentialAgent`.
        - Show the list: `[check_inventory_agent, possibly_reorder_agent]`.
        - Explain that `possibly_reorder_agent` acts as a smart filter or
          "middleware" that conditionally adds more info.
- Running the Code
    - Run `adk web` in the terminal.
- Demonstration
    - **Scenario 1: Search A/B Test**
        - Search for "blue headphones".
        - Explain that you might get exact matches or broad matches depending on
          the random roll.
        - (Optional) Try a few times to see if the behavior changes (or check
          logs).
    - **Scenario 2: Inventory Conditional Check**
        - "Add P001 to my cart."
          - Gets the order and checks the inventory (in parallel)
          - Check inventory will set the model response so it is structured
          - Then it is added to the cart
        - "Add P012 to my cart".
          - Gets the order and checks the inventory (in parallel)
          - check inventory will set the model response since it is structured
          - Since the count is less than 5, the possibly reorder agent calls 
            check reorder status
          - This sets the internal data structure so we are ordering this 
            product, and returns structured data saying so
          - But the product is still added to the cart.
- Conclusion
    - We successfully implemented a `SearchRouter` for controlled A/B testing.
    - We built a `PossiblyReorderAgent` that intelligently reacts to the output
      of a previous agent in a sequence.
    - This pattern allows for efficient, logic-driven workflows that save tokens
      and time by using the LLM when it is needed, but applying our business 
      rules where that makes sense.
