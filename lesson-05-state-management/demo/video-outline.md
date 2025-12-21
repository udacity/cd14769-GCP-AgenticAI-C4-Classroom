# cd14769 - Lesson 05 - demo

Implementing Advanced State Management

- We will learn how to move beyond implicit history-based state and implement
  explicit, shared state management in ADK using the `InvocationContext` and
  `ToolContext`.
- Introduction
    - **What**: We are updating a shipping agent to store the order object
      explicitly in session state rather than relying
      on the output produced and stored in the conversation state.
    - **Why**: Implicit state (reading chat history) is brittle. It consumes
      tokens, can be lost in long conversations, and requires complex 
      parsing if you are doing tasks in a custom agent.
      Explicit state is robust, persistent, and easy for code to access.
- Setup
    - **Critical Step**: Explain that for persistent state, we need the Agent
      Engine.
    - Run `python ../notes/create_agent_engine.py` (or explain it if already
      run) to get the resource URI.
    - **Note**: Explain that we need this URI to tell ADK where to save our
      data in the cloud. If you lost it, you can find it in the Google Cloud
      Console under Agent Engine.
- [agents/shipping.py] Saving State with `ToolContext`
    - Focus on the `place_order` tool function.
    - Highlight the new argument: `tool_context: ToolContext`.
    - Show the line: `tool_context.state["order"] = order`.
    - Explain: Instead of just returning data to the chat, we are now saving the
      order object explicitly into the session's "backpack".
- [agents/shipping.py] Accessing State with `InvocationContext`
    - Scroll down to the `ShippingRouter` class.
    - Highlight `_run_async_impl`.
    - **Contrast with Implicit State**:
        - Previously, we might have had to iterate through `context.session.events`
          to find a specific past message and parse JSON to find the subtotal.
        - **New way**: `order = context.session.state.get("order")`.
    - Explain: This is cleaner, safer, and faster. We grab exactly what we
      stored, without digging through chat logs.
- [agents/shipping.py] The `SequentialAgent` Flow
    - Briefly show `fulfillment_workflow_agent`.
    - Explain that the flow is the same, but the data hand-off is now "
      out-of-band" via the session state.
- Running the Code (Persistence Demo)
    - Start `adk web` **with the session service URI**:
      `adk web --session_service_uri agentengine://...`
    - **Emphasis**: If we don't provide this, ADK uses an in-memory service
      that wipes clean if the server restarts. Using the URI saves data to the
      cloud.
    - **Scenario**: Shipping an order to an address.
        - "I want to buy the Wireless Headphones."
        - "Place order for Jane Doe, 456 Elm St..."
    - **Inspect**:
        - Observe the logs or output. The `place_order` tool runs.
        - Internally, it writes to `tool_context.state`.
        - The `ShippingRouter` then immediately reads that state to decide on
          free shipping (since headphones > $100).
- Conclusion
    - Explicit state management allows for robust data sharing between agents.
    - We use `ToolContext` to write data (like our order) into the state.
    - We use `InvocationContext` to read that data back out in our agents.
    - Combined with the Agent Engine, this gives us persistent memory that
      survives across the session.