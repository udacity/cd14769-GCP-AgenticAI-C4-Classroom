# cd14769 - Lesson 05 - exercise solution

Explicit State in Shopping Cart

- We have updated the shopping agent to use advanced state management,
  specifically using `ToolContext` to maintain a sticky `order_id`.
- Setup
    - Open the `lesson-05-state-management/exercises/solution` directory.
    - Ensure `.env` is configured.
    - Install dependencies: `pip install -r requirements.txt`.
    - Ensure the Agent Engine is ready (resource URI).
- [agents/cart.py] Sticky Order ID with `ToolContext`
    - Focus on `get_order` tool.
    - **Change**: Explain that it now checks
      `tool_context.state.get("order_id")` first.
    - If missing, it generates a new ID and saves it:
      `tool_context.state["order_id"] = order_id`.
    - This effectively "starts a session" for that specific order.
- [agents/cart.py] Simplified `add_to_cart`
    - Focus on `add_to_cart` tool.
    - **Change**: Notice the function signature no longer requires `order_id`.
    - It retrieves the ID directly:
      `order_id = tool_context.state.get("order_id")`.
    - Explain: This simplifies the LLM's job. It doesn't need to memorize or
      extract the ID from the conversation history. It just knows "add X to
      cart", and the code handles the "which cart" part.
- Running the Code (Persistence Demo)
    - Start `adk web` with the session service URI.
    - **Scenario**: Adding items to a cart.
        - "Start a new order." (Triggers `get_order`, saves ID).
        - "Add the USB Hub to my cart." (Triggers `add_to_cart`, reads ID from
          state).
        - "Add the HDMI Cable." (Again, reads ID from state).
    - **Persistence Check**:
        - Stop the `adk web` server.
        - Restart it with the same URI.
        - Ask "What is in my cart?".
        - The agent should successfully retrieve the cart because the `order_id`
          was persisted in the Agent Engine session state, allowing it to look
          up the correct order data.
- Conclusion
    - By using `ToolContext` for explicit state, we decoupled the tool's
      dependencies from the conversation text.
    - The agent is now more robust and user-friendly, as the user doesn't need
      to track their order number.
    - Backed by Agent Engine, this state survives interruptions, mimicking a
      real-world logged-in experience.
