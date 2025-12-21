# cd14769 - Lesson 05 - demo

Implementing Advanced State Management

- We will learn how to move beyond implicit history-based state and implement
  explicit, shared state management in ADK using the `InvocationContext` and
  `ToolContext`.
- Setup
    - Open the `lesson-05-state-management/demo` directory.
    - Ensure `.env` is configured (PROJECT_ID, LOCATION).
    - Install dependencies: `pip install -r requirements.txt`.
    - **Critical Step**: Explain that for persistent state, we need the Agent
      Engine.
    - Run `python ../notes/create_agent_engine.py` (or explain it if already
      run) to get the resource URI.
- [agents/shipping.py] Saving State with `ToolContext`
    - Focus on the `place_order` tool function.
    - Highlight the new argument: `tool_context: ToolContext`.
    - Show the line: `tool_context.state["order"] = order`.
    - Explain: Instead of just returning data to the chat, we are now saving the
      order object explicitly into the session's "backpack".
- [agents/shipping.py] Accessing State with `InvocationContext`
    - Scroll down to the `ShippingRouter` class.
    - Highlight `_run_async_impl`.
    - Contrast with Lesson 4:
        - **Old way**: Iterating through `context.session.events` to find a
          specific past message and parsing JSON.
        - **New way**: `order = context.session.state.get("order")`.
    - Explain: This is cleaner, more robust, and doesn't depend on the chat
      history or token limits.
- [agents/shipping.py] The `SequentialAgent` Flow
    - Briefly show `fulfillment_workflow_agent`.
    - Explain that the flow is the same, but the data hand-off is now "
      out-of-band" via the session state.
- Running the Code (Persistence Demo)
    - Start `adk web` **with the session service URI**:
      `adk web --session_service_uri agentengine://...`
    - **Scenario**:
        - "I want to buy the Wireless Headphones."
        - "Place order for Jane Doe, 456 Elm St..."
        - Verify the order is placed and the subtotal is recognized by the
          router (Free Shipping triggers).
        - **Disruption**: Explain that since state is in the cloud, we could
          restart the server or switch devices, and the "cart" and "order" state
          would persist (though we won't fully kill the server here to save
          time, the concept is key).
- Conclusion
    - Explicit state management allows for robust data sharing between agents.
    - `ToolContext` writes the data; `InvocationContext` reads it.
    - The Agent Engine provides the backend to keep this data safe and
      accessible across the session.
