# cd14769 - Lesson 02 - demo

Implementing Multi-Agent Architectures

- We will learn how to implement a basic multi-agent system using the ADK
  toolkit by creating a shipping orchestrator that delegates tasks to
  specialized sub-agents.
- Setup
    - Open the `lesson-02-multiagent/demo` folder in your IDE.
    - Ensure your `.env` file is configured with your Google Cloud project
      details.
    - Install dependencies if you haven't already:
      `pip install -r requirements.txt`.
- [agent.py] Highlight the `root_agent` definition
    - Point out the `sub_agents=[shipping_agent, inquiry_agent]` parameter.
    - Explain that this defines the hierarchy: `root_agent` is the
      orchestrator (parent) and knows about these two specific children.
    - This is the core mechanism for connecting agents in ADK.
- [prompts/agent-prompt.txt] Show the orchestrator's system prompt
  - Highlight the instructions: "You have access to two specialized
    sub-agents..."
  - Explain that the orchestrator's job is *routing*, not *doing*. It analyzes
    intent and delegates.
- [agents/inquiry.py] Show the `inquiry_agent` definition
    - Point out that this agent is self-contained with its own `instruction` and
      `tools` (specifically `get_order_info`).
    - Note the `name` "shipping_inquiry_agent" - this name is how the
      orchestrator refers to it in logs and reasoning.
- [agents/shipping.py] Show the `shipping_agent` definition
    - Briefly show this is another specialized agent for a different task (
      placing orders).
- running the code
    - Open a terminal above the `demo` directory.
    - Run `adk web`.
    - Open the provided local URL in a browser.
- demonstration
    - Inquiry
      - Type "Where is my order 1001?"
      - Observe the thought process in the debug panel (or logs).
      - Highlight that the orchestrator (shipping_orchestrator) receives the
        message first.
      - Show it deciding to call the `shipping_inquiry_agent`.
      - Show the inquiry agent executing `get_order_info` and responding.
    - Shipping
      - Next, type "I want to ship order 1002 to John Doe at 123 Main St,
        Springfield, IL 62704".
      - Show the orchestrator routing this to the `shipping_agent`.
      - Show the shipping agent calling `place_order`.
    - Emphasize that these are still agents
      - Reset the session
      - Ask "Where is my order?"
      - Agent will prompt you for the information
- Conclusion
    - Summarize that we've broken a complex problem into three manageable
      pieces: an orchestrator and two specialists.
    - This keeps prompts small and responsibilities clear.
