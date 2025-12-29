# cd14769 - Lesson 01 - demo

Designing Multi-Agent Systems with Agent Cards

- We will learn how to design a robust multi-agent architecture using diagrams
  and define agent interfaces using A2A Agent Cards through a hypothetical 
  photo agent that might have mobile, web, and chat-based interfaces.
    - We're not going to be doing any coding in this demo
    - It is important that, first, we think about the design and how multiple 
      agents may need to communicate with each other.
    - Although I'm showing you a graphic of the design, you can start with 
      something as simple as pencil and paper.
    - The design is the important part.
- [demo-design-01-photos.svg] High-Level Architecture
    - Open the high-level design diagram.
      - This examines how we humans will interact with this agent
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
    - **URL**: Possibly the most important since it lets agents know where 
      this agent receives messages.
    - **Skills**: Highlight `process_request`.
        - This is the entry point. It takes natural language.
        - It shows the other agents or tools that are available.
        - There does not need to be a 1:1 mapping with other components, but 
          if there are too many variations, you should think about why.
    - **A2A Context**: Other apps would download this card to
      know how to talk to our Photos app and what features or skills are 
      available
- Review other agents
- Conclusion
    - Designing before coding helps identify necessary roles.
    - A2A Agent Cards provide a standardized way to define these roles and
      interfaces, which lead to the sub-agents that support them.
    - From here, we can start building these sub-agents and then tie them 
      together where our 
