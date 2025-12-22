# cd14769 - Lesson 07 - exercise

Multi-Agent RAG for Shopping

- We've seen how to incorporate search through an agent that can access the PDF
  documents in our library alongside real-time database inventory.
- Setup
    - Ensure `.env` has `DATASTORE_ENGINE_ID` and database credentials.
    - Ensure `toolbox` is running in `docs/` with
      `toolbox --tools-file tools.yaml`.
- [shopping/agents/datastore.py] Implementing the Search Tool
    - Highlighting the code added to call Vertex AI Search.
    - This function (`datastore_search_tool`) allows the agent to "read" the PDF
      manuals we uploaded.
    - This is the "Retrieval" part of RAG for unstructured data.
- [shopping/agents/product_info.py] Creating the RAG Agent
    - We created a dedicated `product_qa_agent`.
    - It is instructed specifically to use the `datastore_search_tool`.
    - This agent acts as the domain expert for technical specs and manual
      details.
- [docs/tools.yaml] Defining SQL Tools
    - We defined `check-inventory` to query the `inventory` table.
    - We also defined `search-products` to find product IDs by name.
    - This represents the "Retrieval" part for structured, transactional data.
- [shopping/agents/inventory.py] Connecting Inventory to SQL
    - Replaced the hardcoded data with `check_inventory_tool`.
    - This ensures the agent always answers with real-time stock levels.
- [shopping/agent.py] Orchestration
    - Added `product_qa_agent` to the `root_agent`'s sub-agents.
    - The orchestrator now has a full team: Search (broad), Inventory (DB),
      Cart (Action), and Product QA (Docs).
- running the code
    - start `adk web --a2a` in the `lesson-07-rag/exercises/solution` directory.
- demonstration
    - Ask: "Does the Home Theater System support Dolby Atmos?"
        - Observe routing to `product_qa_agent`.
        - It searches the PDF manual via Vertex AI.
        - Returns the specific technical answer.
    - Ask: "Do you have any in stock?"
        - Observe routing to `inventory_agent`.
        - It calls the SQL tool `check-inventory`.
        - Returns the exact count from the database.
- Conclusion
    - We successfully built a Multi-Agent RAG system.
    - By specializing agents (one for docs, one for DB), we reduce confusion
      and "hallucinations".
    - The orchestrator seamlessly routes between "Reading the manual" and "
      Checking the warehouse".
