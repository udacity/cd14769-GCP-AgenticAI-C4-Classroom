# cd14769 - Lesson 04 - demo

Implementing Data Routing with Custom Agents

- We will learn how to implement custom routing logic using `CustomAgent` to
  manage data flow and business rules, bypassing the LLM for deterministic
  decisions.
- [agents/shipping.py] The Problem with Pure LLM Routing
    - Show the standard `shipping_agent` setup.
    - These agents use the LLM to determine what sub-agents or tools should 
      be called.
    - In some cases, particularly when dealing with numbers or other 
      discrete operations, this can be unreliable.
    - In other cases, it may just be more efficient to implement business 
      rules (such as when to apply free shipping) through a discrete algorithm.
- [agents/shipping.py] Introducing `CustomAgent`
    - The solution is a CustomAgent which lets us write python code to 
      implement our business logic. 
    - Show the `ShippingRouter` class inheriting from `BaseAgent`.
    - We pass there parameters to the constructor 
      - the different agents that we want to call
      - The cutoff point for free shipping
    - Explain `_run_async_impl`: This is where the custom python logic lives.
    - It's not prompt-based; it's code-based.
- [agents/shipping.py] Inspecting Event History
    - Walk through the code that iterates through
      `invocation_context.session.events`.
    - Show how it looks for the `place_order_agent` output.
    - Explain why we do this: The `subtotal` was calculated in a previous step,
      and we need to retrieve it to make our routing decision.
    - Highlight the JSON parsing of the event content.
- [agents/shipping.py] Programmatic Routing Logic
    - Show the simple `if/else` block:
        - If `subtotal >= free_threshold`, route to `free_shipping_agent`.
        - Else, route to `shipping_cost_agent`.
    - Explain that this guarantees the business rule is followed 100% of the
      time.
    - Show how we delegate to the chosen agent using
      `subagent.run_async(invocation_context)`.
- [agents/shipping.py and prompts]
  - shipping_cost_agent
  - free_shipping_agent
  - both use the same tool, but have different prompts that call it with 
    different values
    - `shipping-cost-prompt`
    - `free-shipping-prompt`
  - The result are different shipping values based on what the 
    ShippingRouter chose
- Running the Code
    - Run `adk web` in the terminal.
- Demonstration
    - **Scenario 1: Standard Shipping**
        - "Ship order 1002 to John Doe, 123 Main St, Anytown, CA 90210."
        - Point out that the
          `ShippingRouter` saw a low subtotal and selected the standard shipping
          agent.
        - Result: Shipping cost is added.
    - **Scenario 2: Free Shipping**
        - "Ship order 1003 John Doe, 123 Main St, Anytown, CA 90210."
        - Point out in the logs that the `ShippingRouter` saw a high
          subtotal (> $100).
        - Result: "Free Shipping" agent is selected, cost is $0.
- Conclusion
    - We've seen how `CustomAgent` allows us to inject precise python logic into
      our agent workflow.
    - This gives us the best of both worlds: the flexibility of LLMs for
      conversation and the reliability of code for our business rules.
