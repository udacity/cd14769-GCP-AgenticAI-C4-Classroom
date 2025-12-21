# cd14769 - Lesson 01 - demo

Designing Multi-Agent Systems with Agent Cards

- We will learn how to design a robust multi-agent architecture using diagrams
  and define agent interfaces using A2A Agent Cards.
- Setup
    - Open the `lesson-01-design/demo` directory.
    - Note: There is no python code to run in this lesson; we are focusing on
      design artifacts.
- [demo-design-01-photos.svg] High-Level Architecture
    - Open the high-level design diagram.
    - Explain the **Orchestrator Pattern**:
        - The **User** interacts only with the **Photos Agent**.
        - The **Photos Agent** acts as a router/orchestrator.
        - It delegates tasks to specialized workers: **Storage**, **Search**, *
          *Edit**, and **Account**.
    - Discuss why: Decomposing a complex app (like Google Photos) prevents one
      agent from becoming overwhelmed and confused.
- [agent-01-photos.json] The Orchestrator's Contract
    - Open the Agent Card for the Photos agent.
    - Explain **What is an Agent Card?**: It's like a business card or an API
      contract for the A2A protocol. It tells other agents "This is who I am and
      this is what I can do."
    - **Identity**: Name (`photos`), Description (Orchestrator).
    - **Skills**: Highlight `process_request`.
        - This is the entry point. It takes natural language.
        - It maps to the arrows coming *into* the Photos agent in the diagram.
    - **A2A Context**: In a real system, other apps would download this card to
      know how to talk to our Photos app.
- [agent-03-search.json] Specialized Workers
    - Open the Agent Card for the Search agent.
    - Compare with the diagram's "Search Agent" box.
    - **Identity**: Name (`photo_search`).
    - **Skills**: Highlight `search_request`.
        - Description: "Search or browse photos".
        - Examples: "Find photos of cats".
    - Explain the relationship: The Photos Agent (Orchestrator) sees this card
      and knows, "Ah, if the user asks for cats, I should call *this* agent."
- [demo-design-02-storage.svg] & [agent-02-storage.json] Detail View
    - Briefly show the Storage diagram and card.
    - Show how the diagram might imply internal database connections, but the
      Card only exposes the public interface (`upload_photo`).
    - This encapsulates complexity: The Orchestrator doesn't need to know *how*
      storage works, just *how to ask* for it.
- Conclusion
    - Designing before coding helps identify necessary roles.
    - A2A Agent Cards provide a standardized way to define these roles and
      interfaces.
    - This structure allows agents to be built by different teams or run on
      different servers while still working together seamlessly.
