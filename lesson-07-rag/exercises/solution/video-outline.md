# cd14769 - Lesson 07 - exercise

Multi-Agent RAG for Shopping

- We've seen how to incorporate search through an agent that allows shoppers 
  to ask additional questions about the products they are looking for by 
  providing information from both product summary sheets in PDF and our 
  real-time database inventory.
- Setup
    - Docs have been loaded into the bucket and then the data store 
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
    - I'm looking for a new smart watch.
    - Is it water resistant, and do you have any in stock?
    - Show that it transfers to the two agents to get information and 
      summarizes the results.
- Conclusion
    - We successfully built a Multi-Agent RAG system that provides customers 
      the information they want from the most accurate sources available.
    - We've seen how the orchestrator seamlessly routes between "Reading the 
      manual" and "Checking the warehouse" and summarizes that information 
      for our customer.
