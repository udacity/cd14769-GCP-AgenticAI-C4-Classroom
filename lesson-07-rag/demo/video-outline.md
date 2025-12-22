# cd14769 - Lesson 07 - demo

Multi-Agent RAG with Vertex AI Search and SQL

- We will learn how to implement Multi-Agent Retrieval Augmented Generation (
  RAG) by combining an agent that searches unstructured policy documents (using
  Vertex AI Search) with an agent that queries structured order data (using the
  MCP Database Toolbox and SQL).
- Setup
    - Vertex AI Search Setup:
        - Go to Google Cloud Console -> Cloud Storage. Create a bucket.
        - Upload the PDF manuals from `demo/docs/manuals/` to this bucket.
        - Go to "Agent Builder" (Vertex AI Search and Conversation).
        - Create a new App -> Search -> Generic.
        - Create a Data Store -> Cloud Storage -> Select your bucket ->
          Unstructured documents.
        - Link the Data Store to the App.
        - Copy the "Data Store ID" (Engine ID) and set `DATASTORE_ENGINE_ID` in
          `demo/shipping/.env`.
    - Database Setup:
        - Ensure your MySQL instance is running.
        - Load the shipping data:
          `mysql -h <host> -u <user> -p < demo/docs/shipping.sql`.
    - MCP Database Toolbox:
        - Open a terminal and navigate to `demo/docs/`.
        - Export environment variables:
          `export $(grep -v '^#' ../shipping/.env | xargs)`.
        - Start the toolbox: `toolbox --tools-file tools.yaml --port 5001`.
- [shipping/agents/datastore.py] The Vertex AI Search Tool
    - Show `datastore_search_tool` and the `search` function.
    - Explain how it uses `discoveryengine` client to retrieve chunks from PDF
      documents.
    - This connects our agent to the "knowledge base".
- [docs/tools.yaml] The SQL Tool Definition
    - Show the `get-order` tool.
    - Explain the SQL statement: `SELECT * FROM orders WHERE order_id = ?`.
    - This gives our agent access to "live business data".
- [shipping/agents/inquiry.py] The Inquiry Agent Structure
    - Show `get_order_agent`: dedicated to using `get_order_tool`.
    - Show `policy_search_agent`: dedicated to using `datastore_search_tool`.
    - Show `inquiry_agent`: the orchestrator that manages these two sub-agents.
    - Explain the strategy: Divide and Conquer. One agent for facts (DB), one
      for knowledge (Docs).
- [shipping/prompts/inquiry-prompt.txt] The Synthesis Instructions
    - detailed instructions on how to use the sub-agents.
    - "If a customer references their order... you must call the
      `get_order_agent`".
    - "Use `policy_search_agent` to search the knowledge base".
- Running the code
    - Start the agent: `adk web --a2a` in the `lesson-07-rag/demo` directory.
    - Open the web interface.
- Demonstration
    - Enter the prompt: "I just got order 1001 and I don't like it. How long do
      I have to return it?"
    - Watch the `shipping_orchestrator` route to `shipping_inquiry_agent`.
    - Observe `shipping_inquiry_agent` delegating to `get_order_agent`.
        - `get_order_agent` calls `get-order` tool (SQL).
        - Returns order details (e.g., "Order 1001, Shipped, Date: ...").
    - Observe `shipping_inquiry_agent` delegating to `policy_search_agent`.
        - `policy_search_agent` calls `datastore_search_tool` (Vertex AI).
        - Returns policy chunks (e.g., "Returns accepted within 30 days...").
    - Observe the final synthesis: The agent combines the order date with the
      30-day policy to give a specific answer (e.g., "Since your order was
      shipped on [Date], you have until [Date + 30] to return it.").
- Conclusion
    - We've demonstrated Multi-Agent RAG.
    - We didn't just "search": we combined specific structured data (Order ID)
      with general unstructured knowledge (Policy).
    - This allows for highly personalized and accurate support responses that
      neither source could provide alone.
