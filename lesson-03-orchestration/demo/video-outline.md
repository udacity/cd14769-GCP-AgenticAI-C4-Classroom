# cd14769 - Lesson 03 - demo
Implementing Agent Orchestration with ADK

- We will learn how to implement advanced orchestration patterns using ADK, specifically "Sequential" (Series) and "Parallel" execution, to build a robust order fulfillment system.
- Setup
  - Open the `lesson-03-orchestration/demo` folder in your IDE.
  - Ensure your `.env` file is configured with your Google Cloud project details.
  - Install dependencies: `pip install -r requirements.txt`.
- [agent.py] Top-Down: The Root Agent
  - Show `root_agent` definition.
  - Explain it acts as the main dispatcher, routing to `shipping_agent` or `inquiry_agent` based on high-level intent.
- [agents/shipping.py] Top-Down: The Shipping Agent
  - Show `shipping_agent`. It manages the domain of shipping but delegates the heavy lifting.
  - Point out its sub-agents: `fulfillment_workflow_agent` (for doing the work) and `approve_order_agent` (for the final confirmation).
- [agents/shipping.py] Deep Dive: Sequential Orchestration
  - Highlight `fulfillment_workflow_agent` defined as a `SequentialAgent`.
  - **Concept**: Explain that standard `LlmAgent`s decide their own steps, which is great for flexibility but can be unpredictable for strict business processes.
  - **Why Sequential?**: We *must* have an address before we calculate tax. We *must* have costs before we sum the total. `SequentialAgent` enforces this strict order: `place_order` -> `costs` -> `compute` -> `summary`.
- [agents/shipping.py] Deep Dive: Parallel Execution
  - Highlight `costs_agent` defined as a `ParallelAgent`.
  - **Why Parallel?**: Calculating shipping and calculating tax are independent tasks. Waiting for one to finish before starting the other is inefficient.
  - Show how it groups `shipping_cost_agent` and `taxes_cost_agent`. ADK runs them simultaneously and gathers results.
- [agents/shipping.py] The Worker Agents (LlmAgents)
  - Briefly show the leaf agents like `place_order_agent` or `taxes_cost_agent`.
  - Note they are standard `LlmAgent`s focused on a single tool. This granularity allows them to be orchestrated by the parent agents.
- running the code
  - Open a terminal in the `lesson-03-orchestration/demo` directory.
  - Run `adk web`.
  - Open the provided local URL in a browser.
- demonstration
  - Type: "Ship order 1001 to John Doe at 123 Main St, New York, NY 10001."
  - **Trace the flow**:
    1. `root_agent` -> `shipping_agent` -> `fulfillment_workflow_agent`.
    2. **Sequential Step 1**: `place_order_agent` extracts the address.
    3. **Sequential Step 2**: `costs_agent` (Parallel). Watch logs to see shipping and tax logic firing together.
    4. **Sequential Step 3**: `compute_order_agent` aggregates the parallel outputs.
    5. **Sequential Step 4**: `order_summary_agent` presents the result.
  - Finally, type "Yes, approve it." to show the `shipping_agent` switching to the `approve_order_agent` path.
- Conclusion
  - We've moved from simple delegation to defining explicit workflows.
  - Use `SequentialAgent` when order matters.
  - Use `ParallelAgent` for efficiency when tasks are independent.