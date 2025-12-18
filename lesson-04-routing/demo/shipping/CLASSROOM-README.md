# Implementing Data Routing in ADK Systems

We will learn how to implement custom routing logic using `CustomAgent` to
manage data flow and business rules, such as offering free shipping for
high-value orders.

---

## Overview

### What You'll Learn

Learners will understand how to bypass LLM-based decision making for routing
when fixed business rules apply. You will see how to extend `BaseAgent` to
create a `CustomAgent` that inspects the conversation history (Events) and
routes requests based on programmatic logic.

Learning objectives:

- Implement a `CustomAgent` by extending `BaseAgent`.
- Access and inspect session `Events` to extract data.
- Implement programmatic routing logic (e.g., if-then rules).

### Prerequisites

- Understanding of ADK agents, including Sequential and Parallel agents.
- Basic understanding of Python classes and inheritance.
- Access to Google Cloud with Vertex AI enabled.

---

## Understanding the Concept

### The Problem

While LLMs are great at identifying intent, they can be unreliable for strict
business logic, like determining if an order qualifies for a discount. Relying
on an LLM to "check the subtotal and pick the right agent" might lead to
inconsistent results.

### The Solution

A `CustomAgent` allows you to write Python code to handle the routing. Instead
of asking the LLM "Should this order get free shipping?", we write a simple
`if subtotal >= 100` statement in code. This ensures 100% accuracy and follows
strict business rules.

### How It Works

**Step 1: The Context**
The `place_order_agent` runs first and outputs the order `subtotal`. This output
is recorded as an `Event` in the session history.

**Step 2: The Router**
The `shipping_router_agent` (our CustomAgent) is triggered. It doesn't use an
LLM. Instead, it:

1. Iterates through the session events.
2. Finds the output from `place_order_agent`.
3. Parses the JSON to find the `subtotal`.

**Step 3: The Logic**

- If `subtotal >= 100`, it delegates to the `free_shipping_agent`.
- Otherwise, it delegates to the standard `shipping_cost_agent`.

---

## Code Walkthrough

### Repository Structure

```
shipping/
├── shipping.py       # Implementation of the ShippingRouter class
├── agent.py          # Root orchestrator
├── rates.py          # Shipping rates (including 'free')
└── ...
```

### Step 1: Defining the Custom Router

In `shipping.py`, we define the `ShippingRouter` class.

```python
class ShippingRouter(BaseAgent):
  def __init__(self, name: str, free_agent: Agent, standard_agent: Agent,
               free_threshold: float):
    super().__init__(name=name, ...)
    self.free_threshold = free_threshold
    # ... agents stored ...

  async def _run_async_impl(self, invocation_context: InvocationContext) ->
  AsyncGenerator[Event, None]:
    # Logic to find the subtotal from previous events
    subtotal = 0
    events = invocation_context.session.events
    for event in reversed(events):
      if event.author == "place_order_agent":
        # Parse JSON content to get subtotal
        data = json.loads(event.content.parts[0].text)
        subtotal = data.get("subtotal", 0)
        break

    # Programmatic routing
    if subtotal >= self.free_threshold:
      subagent = self.free_agent
    else:
      subagent = self.standard_agent

    # Delegate to the chosen subagent
    async for event in subagent.run_async(invocation_context):
      yield event
```

**Key points:**

- Inherits from `BaseAgent`.
- Implements `_run_async_impl` to define the custom behavior.
  - This is the important component when creating a `CustomAgent`
  - You'll be putting your business logic in this method
- Uses `invocation_context.session.events` to look back at what happened
  previously.
- You can choose what subagent to run and then call 
  `run_async (invocation_context)` on that subagent, yielding to the events 
  that it returns. This is a standard pattern you should follow when 
  choosing the next agent to invoke

### Step 2: Instantiating the Router

The router is created with the necessary threshold and sub-agents.

```python
shipping_router_agent = ShippingRouter(
  name="shipping_router_agent",
  free_agent=free_shipping_agent,
  standard_agent=shipping_cost_agent,
  free_threshold=100.00,
)
```

---

## Important Details

### Best Practices

1. **Reliability**: Use CustomAgents for any routing that follows a strict,
   non-negotiable business rule.
2. **Clean Data**: Ensure that the agents providing data to the router (like
   `place_order_agent`) use an `output_schema` to produce consistent JSON that
   is easy to parse.

### Common Errors

**Error**: `json.JSONDecodeError`

- **Cause**: The router tried to parse an event that wasn't valid JSON (perhaps
  a text message from the customer or an LLM's conversational filler).
- **Solution**: Always check the `event.author` to ensure you are only parsing
  data from the specific agent you expect.
