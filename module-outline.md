## Module 1: Designing Multi-Agent Architectures with Diagramming Tools and A2A Considerations

### Core Module Primary Learning Objective

Explain the core components of multi-agent systems and how to design their
high-level architecture; including approaches like orchestrator-workers or
primary agent with specialized retrieval agents; and defining roles,
responsibilities, and communication patterns (e.g., synchronous, asynchronous,
use of A2A for inter-application communication).

### Core Topics or Exercises

System architecture design; Roles and responsibilities of each agent;
Communication patterns (ADK internal, A2A for external); System Architecture
Design for Agentic AI; “Orchestrator and workers” approach or “primary agent and
specialized retrieval agents” approach; Introduction to Agent2Agent (A2A)
protocol for interoperability.

### Google Module Primary Learning Objective

Design a high-level architecture for a multi-agent system for a chosen
real-world scenario using diagramming tools, explicitly considering where ADK
internal communication suffices and where A2A protocol would be beneficial for
inter-agent/service communication.

Understand the difference between MCP and A2A and when each should be used.

### Google Additional Learning Objectives

Present agent roles, data flows, and sketch A2A Agent Cards and Skill
definitions for key interaction points if A2A is planned.

### Google Topics or Exercises

Draw a multi-agent architecture diagram for a chosen real-world scenario (e.g.;
a sales pipeline; marketing funnel; or multi-step helpdesk process); Detail ADK
agent interactions; Identify points for A2A communication if agents are separate
services; Define example A2A Agent Cards and Skills.

### Demo:

#### Summary

Let’s take a look at what sort of agents we might be interested in when working
with pictures, similar to how Google Photos does. We’ll explore the different
entry points, handled by different agents, and how the agents may coordinate
with each other. We’ll see why some planning, using a diagramming tool or good
‘ol pencil and paper, helps us focus on good design. We’ll also see; how some of
this translates into remote agents with A2A and how an A2A agent card helps with
design, and how this differs from tool calling with MCP.

#### Features:

* Orchestrating agents
* Peer-to-peer agents

#### Google Specific Features:

* Google Photos design

### Exercise:

#### Summary

Start thinking about a series of agents that are part of an e-commerce website.
Which agents delegate to other agents and which ones have to work together?
Diagram these agents and how they interact with each other \- you can use a
diagramming tool, or even just pencil and paper. The important part is that you
understand how the agents interact and, where possible, how they may run on
different servers.

#### Features:

* Orchestrating agents
* Peer-to-peer agents

#### Google Specific Features:

*

---

## Module 2: Implementing Multi-Agent Architectures with ADK and Introduction to A2A

### Core Module Primary Learning Objective

Understand the process of coding a designed multi-agent architecture using ADK,
connecting agents with well-defined interfaces (ADK method calls), and defining
each agent’s system prompt or specialized toolset. Introduce A2A for cases where
agents are distinct applications needing to interoperate.

### Core Topics or Exercises

Instantiating multiple ADK agents in a codebase; Connecting them with ADK method
calls; Agent Implementation; Defining each agent’s system prompt or specialized
toolset; Using A2A Python SDK for agents that need to communicate across
process/network boundaries via the A2A protocol.

### Google Module Primary Learning Objective

Develop a multi-agent system by coding the designed architecture using ADK for
intra-application agent communication. Introduce the A2A Python SDK for basic
inter-agent communication discovery if agents were separate services.

### Google Additional Learning Objectives

Show ADK agents exchanging messages via method calls; Demonstrate a simple A2A
client discovering an A2A server agent's capabilities (Agent Card).

### Google Topics or Exercises

Write a Python script that spawns multiple ADK agent classes; Show how they
exchange messages (via method calls; queue; or direct method calls within ADK);
Implement a basic A2A server agent (using ADK as a base) and an A2A client that
can retrieve its Agent Card using the A2A Python SDK.

### Demo:

#### Summary

Let’s take a look at just the shipping agent part of e-commerce agents and
explore some of the sub-agents that we will need. Including:

* The agent that ships an order to an address
* A separate agent that can handle shipping inquiries
* An orchestrator that determines which sub-agent is relevant

#### Features:

* Discuss where this may work as a remote agent

#### Google Specific Features:

* ADK agent delegation

### Exercise:

#### Summary

Now think about another part of an e-commerce agent. Adding each item to a cart
might require multiple agents to do tasks:

* An agent to search for items
* An agent to check if the item is still in inventory
* An agent to add an item to a cart
* An orchestrator that determines which sub-agent is relevant

#### Features:

*

#### Google Specific Features:

* ADK agent delegation

---

## Module 3: Implementing Agent Orchestration with ADK (and A2A for External Agents)

### Core Module Primary Learning Objective

Understand orchestration techniques to coordinate multiple agent actions and
achieve complex workflows; including the role of an ADK orchestrator agent that
plans and delegates tasks; and how A2A can be used for orchestrating across
independent agent applications.

### Core Topics or Exercises

Agent orchestration techniques within ADK (e.g., custom orchestrator agent,
LlmAgent for routing); Handling concurrency or sequential chaining in ADK; Role
of an orchestrator agent that plans and delegates tasks; Using A2A for
cross-application orchestration.

### Google Module Primary Learning Objective

Apply orchestration techniques by building an ADK orchestrator that delegates
tasks to other ADK worker agents. Optionally, demonstrate how this orchestrator
could use A2A to delegate tasks to an external A2A-enabled agent/service.

### Google Additional Learning Objectives

Provide scenarios (coding tasks, QA tasks) handled by the ADK multi-agent
system; Show A2A client call from orchestrator if an external agent is involved.

### Google Topics or Exercises

Build an ADK orchestrator that delegates tasks to ADK worker agents; (Optional
Exercise) Extend the orchestrator to make an A2A call (using A2A Python SDK) to
a mock external A2A agent for a specific sub-task.

### Demo:

#### Summary

Let’s build off our existing shipping agent and explore the details of just one
part of it \- sending out an order. This involves some tasks that we need to do
in sequence, and some that we can do in parallel:

* A SeriesAgent that has tools that compute the total price including shipping
  and taxes
* Getting the shipping and taxes through the use of ParallelAgents

#### Features:

*

#### Google Specific Features:

* SeriesAgent
* ParallelAgent

### Exercise:

#### Summary

Think about the agent from your previous exercise that adds an item to a cart.
What other sub-agents does it have? Which can be called in series and which in
parallel?

#### Features:

*

#### Google Specific Features:

* SeriesAgent
* ParallelAgent

---

## Module 4: Implementing Data Routing in ADK Systems and with A2A

### Core Module Primary Learning Objective

Understand how to configure routing mechanisms to manage data flow among ADK
agents and between A2A-connected agents in multi-agent systems; including
different routing strategies and logic design.

### Core Topics or Exercises

Data flow management within ADK (passing data between agent calls); Routing
logic design (ADK's LlmAgent, custom logic); Overview of routing strategies in a
multi-agent environment; Data exchange patterns in A2A (e.g., passing parameters
in Skill calls, handling different content types).

### Google Module Primary Learning Objective

Configure routing mechanisms within an ADK multi-agent system and demonstrate
basic data exchange using A2A protocol between two simple agents/services.

### Google Additional Learning Objectives

Implement data passing between ADK agents; Use A2A Python SDK to send data as
part of a Skill invocation and receive a response.

### Google Topics or Exercises

Write Python code within ADK that decides which ADK agent receives which chunk
of data (e.g., using LlmAgent or custom conditions); Implement a simple A2A
client-server interaction where data is passed with a Skill call and a result is
returned.

### Demo:

#### Summary

We will explore how to implement our business logic, including priority routing,
using CustomAgents by extending our shipping agent to allow for free shipping
for some customers or in some cases. We will also see why routing using the LLM
is not always good practice.

#### Features:

* Custom routing

#### Google Specific Features:

* CustomAgent

### Exercise:

#### Summary

One common use for round-robin routing between different sub-agents is because
you are introducing a new agent in production and want to gradually shift from
the old agent to the new one. This could actually be a weighted round-robin,
since you may favor one agent over another initially, and gradually shift more
and more of the load to the other as you gain confidence in it. You’ll be using
a CustomAgent to make the determination of which sub-agent to use for this
request and will build two different sub agents (generally an LLMAgent, but with
different tools and/or instructions) so you can evaluate how each performs.

#### Features:

* A/B testing
* Round-robin routing
* Custom routing

#### Google Specific Features:

* CustomAgent

---

## Module 5: Implementing Advanced State Management with ADK

### Core Module Primary Learning Objective

Understand advanced methods for tracking and updating agent state (
conversation-level vs. system-level) across multi-turn interactions in
multi-agent systems built with ADK. Consider how state might be implicitly
managed or explicitly shared when interacting with external A2A agents.

### Core Topics or Exercises

Implementing conversation-level state vs. system-level state in ADK (using
Session, State, persistent storage); Handling partial errors or re-requests;
Distinctions between ephemeral and persistent data using Google Cloud databases;
Challenges of state consistency when A2A agents are involved (A2A agents are
opaque).

### Google Module Primary Learning Objective

Evaluate and apply methods for tracking and updating shared or coordinated state
across multiple ADK agents using Google Cloud Databases (e.g., Firestore, Cloud
SQL, Spanner) for persistence.

### Google Additional Learning Objectives

Simulate system recovery from partial failures by restoring state from a
database.

### Google Topics or Exercises

Experiment with storing conversation info or shared task status in Firestore or
Cloud SQL, accessible by multiple ADK agents; Simulate partial failure and test
how the system recovers or resumes based on persisted state.

### Demo:

#### Summary

Previous examples rely on implicit state as the output of each agent is
incorporated into the conversation. Let’s see how to implement this using
explicit state and the ADK state management system. We’ll discuss when each is
appropriate to use.

#### Features:

*

#### Google Specific Features:

* InvocationContext which includes session and state information
* Session state using the Vertex AI Agent Engine

### Exercise:

#### Summary

Adjust your shopping agent so it maintains the order through session state.

#### Features:

*

#### Google Specific Features:

* InvocationContext which includes session and state information

---

## Module 6: Implementing Multi-Agent State Coordination & Orchestration with ADK

### Core Module Primary Learning Objective

Understand how to develop a coordinated multi-agent system (primarily within
ADK) that synchronizes states for coherent task execution; including conflict
resolution strategies. Discuss challenges when coordinating with external A2A
agents where state is not directly shared.

### Core Topics or Exercises

State synchronization protocols within a single ADK application; Conflict
resolution strategies if multiple ADK agents produce contradictory data;
Ensuring agent progress consistency before proceeding to the next step; A2A
interaction patterns for task handoff and result aggregation that imply state
coordination without direct sharing.

### Google Module Primary Learning Objective

Develop a coordinated multi-agent ADK system that uses A2A and state that is
shared using a database.

### Google Additional Learning Objectives

Use shared database with MCP Database Toolbox for ADK agents to read/write
intermediate states for coordination.

### Google Topics or Exercises

Build a multi-agent ADK system with a central orchestrator that collects partial
states from worker ADK agents (e.g., stored in Firestore); Implement simple
logic to address conflicts if two agents produce contradictory data for a shared
sub-task.

### Demo:

#### Summary

We’ve been building two different primary agents over these demos and exercises.
Let’s put them together with the caveat that each needs to run independently.
We’ll see how A2A let’s them be independent, but still hand off to each other or
from an orchestrator, and how they can share state using a MySQL database we
access through MCP Database Toolbox.

#### Features:

*

#### Google Specific Features:

* A2aAgent
* MCP Database Toolbox
* Google Cloud SQL for MySQL

### Exercise:

#### Summary

Save order data in the database so the shipping agent can handle the order via
A2A. Create the agent card for the shopping cart agent and update it to save the
order in a database for the shipping agent to access it.

#### Features:

*

#### Google Specific Features:

* A2aAgent
* MCP Database Toolbox
* Google Cloud SQL for MySQL

---

## Module 7: Implementing Multi-Agent RAG with ADK and Vertex AI Search/RAG Engine

### Core Module Primary Learning Objective

Understand how to extend RAG to multiple cooperating ADK agents; each
specialized in certain retrieval tasks from sources like Vertex AI RAG
Engine/Search; including multi-agent tool usage and orchestration for multi-step
retrieval.

### Core Topics or Exercises

Multi-agent tool usage within ADK for RAG; Orchestration of ADK agents for
multi-step retrieval (e.g., one agent queries different sources, another
synthesizes); Discussion on dividing retrieval tasks among specialized ADK
sub-agents using Vertex AI RAG Engine/Search.

### Google Module Primary Learning Objective

Extend RAG to multiple cooperating ADK agents, each specialized in certain
retrieval tasks from Vertex AI RAG Engine/Search, by implementing a system that
integrates retrieval, chaining, and final answer generation.

### Google Additional Learning Objectives

Debug and validate queries that require data from multiple document sets or
sources managed by different ADK agents but using a central RAG setup.

### Google Topics or Exercises

Step-by-step ADK code example integrating retrieval by multiple ADK agents (
e.g., one for product docs, one for troubleshooting guides, both using Vertex AI
RAG Engine), chaining results, and final answer generation by a synthesizer ADK
agent using Gemini; Show how to identify missing info and trigger re-retrieval
by the appropriate agent.

### Demo:

#### Summary

If a user has a question about their order, or perhaps about returning their
order, the agent may need to consult both policy documents (stored in Vertex AI
Search) and order information (stored in the order database and accessed through
MCP Database Toolbox) to answer the question. We’ll see how to build a
multi-agent RAG that can use data from all these sources.

#### Features:

* Multi-agent RAG

#### Google Specific Features:

* Agent Builder RAG Engine
* MCP Database Toolbox
* Google Cloud SQL for MySQL

### Exercise:

#### Summary

Extend the shopping cart so it can answer questions about a product, including
product information (From Vertex AI Search) and quantity available (from the
database through MCP Database Toolbox).

#### Features:

* Multi-agent RAG

#### Google Specific Features:

* Agent Builder RAG Engine
* MCP Database Toolbox
* Google Cloud SQL for MySQL

---

