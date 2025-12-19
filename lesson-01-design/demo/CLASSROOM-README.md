# Google Photos Design

We will learn how to design a multi-agent system for a photo management
application, similar to Google Photos, and how to define the agents using A2A
Agent Cards.

---

## Overview

### What You'll Learn

You will explore how to decompose a complex application into a system of
cooperating agents. You will learn to visualize the architecture using diagrams
and formally define each agent's interface and capabilities using Agent Cards,
which facilitate Agent-to-Agent (A2A) communication.

Learning objectives:

- Design a high-level architecture for a multi-agent system.
- Understand the "Orchestrator and Workers" pattern.
- Define A2A Agent Cards to specify agent capabilities and interfaces.

### Prerequisites

- Basic understanding of what an AI agent is.
- Familiarity with JSON format.

---

## Understanding the Concept

### The Problem

Building a complex application like a photo library involves handling diverse
tasks: managing large file storage, performing semantic search on images,
editing photos, and managing user accounts. Trying to handle all of this in a
single monolithic agent can lead to a confusing system prompt, context window
limits, and difficulty in maintaining the code.

### The Solution

We decompose the application into specialized agents. A primary "Orchestrator"
agent interacts with the user and delegates tasks to specialized "Worker"
agents (Storage, Search, Edit, Account). This separation of concerns makes each
agent simpler, more robust, and easier to maintain.

### How It Works

**Step 1: Architecture Design**
We visualize how agents connect. The user talks to the main Photos agent, which
then routes requests to the appropriate sub-agent.

**Step 2: A2A Agent Cards**
To let agents "know" about each other, especially if they run on different
servers, we use **Agent Cards**. These are JSON files that describe an agent's
name, description, and the "Skills" (functions) it provides.

### Key Terms

**Orchestrator**: An agent that acts as a central coordinator, receiving tasks
and delegating them to other agents.
**A2A (Agent-to-Agent)**: A protocol or pattern allowing independent agents to
communicate and collaborate.
**Agent Card**: A JSON definition of an agent's identity and capabilities, used
for discovery in an A2A system.

---

## Design Walkthrough

### Repository Structure

```
lesson-01-design/demo/
├── agent-01-photos.json       # Agent Card for the main Orchestrator
├── agent-02-storage.json      # Agent Card for the Storage agent
├── agent-03-search.json       # Agent Card for the Search agent
├── agent-04-edit.json         # Agent Card for the Edit agent
├── agent-05-account.json      # Agent Card for the Account agent
├── demo-design-01-photos.svg  # High-level system architecture diagram
├── demo-design-02-storage.svg # Detail view of the Storage agent
├── demo-design-03-search.svg  # Detail view of the Search agent
├── demo-design-04-edit.svg    # Detail view of the Edit agent
└── demo-design-05-account.svg # Detail view of the Account agent
```

### Step 1: System Overview

The first design artifact is the high-level architecture.

**File:** `demo-design-01-photos.svg`

This diagram illustrates the entry point of the application. The User interacts
solely with the **Photos Agent**. This agent acts as the interface, interpreting
user intent (e.g., "Find photos of my cat" or "Free up space") and deciding
which downstream agent can fulfill that request. It encapsulates the system's
complexity from the user.

**Key points:**

- Single entry point for the user.
- Modular design with specialized back-end agents.

### Step 2: The Orchestrator Agent Card

The **Photos Agent** needs to be defined so other systems (or a registry) know
what it does.

**File:** `agent-01-photos.json`

```json
{
  "name": "photos",
  "url": "http://localhost:8001/a2a/photos",
  "description": "Main orchestrator agent for the Photos application. Manages user interactions and delegates to specialized agents for storage, search, editing, and account management.",
  "skills": [
    {
      "id": "process_request",
      "name": "Process Request",
      "description": "Handle a natural language request from the user regarding their photo library.",
      "tags": [
        "Photos",
        "Orchestrator"
      ],
      "examples": [
        "Find all my photos of cats",
        "Edit the last photo to be black and white",
        "How much storage do I have left?"
      ]
    }
  ]
}
```

**Key points:**

- **`name` & `description`**: Clearly state the agent's role.
- **`skills`**: The `process_request` skill shows that this agent accepts
  natural language instructions.

### Step 3: Specialized Capabilities (Storage Agent)

The **Storage Agent** is a worker that handles specific technical tasks.

**File:** `agent-02-storage.json`

```json
{
  "name": "photo_storage",
  "url": "http://localhost:8002/a2a/storage",
  "description": "Manages the storage of photo files and metadata.",
  "skills": [
    {
      "id": "upload_photo",
      "name": "Upload Photo",
      "description": "Save a new photo to storage.",
      "tags": [
        "Storage"
      ],
      "examples": [
        "Upload this image file"
      ]
    }
  ]
}
```

**Key points:**

- **Specific Responsibility**: It only handles storage, not searching or
  editing.
- **Defined Interface**: The `upload_photo` skill is a discrete action other
  agents can call.

### Complete Example

By defining cards for all agents (`search`, `edit`, `account`), we create a "
directory" of services. The Orchestrator (Photos Agent) can theoretically look
up these cards to understand which agent handles "finding cats" (Search Agent)
vs "freeing up space" (Account/Storage Agent).

---

## Important Details

### Best Practices

1. **Single Responsibility Principle**: Each agent should do one thing well. The
   Storage agent shouldn't try to edit photos.
2. **Clear Interfaces**: Your Agent Cards are the contract between agents.
   Descriptions should be unambiguous so an LLM can decide which agent to call.

### Common Misconceptions

**Misconception**: "More agents are always better."
**Reality**: Every agent adds latency and complexity. Only split agents when the
complexity of a single prompt becomes unmanageable or when capabilities (like
access to specific databases) need to be isolated.
