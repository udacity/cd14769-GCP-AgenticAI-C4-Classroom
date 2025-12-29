# E-Commerce System Design

We will apply the design principles we've learned to architecture a new
multi-agent system for an e-commerce storefront.

---

## Overview

### What You'll Learn

You will practice decomposing a business domain into distinct agent roles. You
will determine the relationships and communication paths between these agents
and formally define their capabilities.

Learning objectives:

- Analyze a set of business requirements to identify necessary agents.
- Create a system architecture diagram showing agent delegation.
- Author A2A Agent Cards to specify the interface for each agent.

### Prerequisites

- Understanding of the "Orchestrator and Workers" pattern.
- Knowledge of JSON syntax.

---

## Understanding the Concept

### The Problem

An online store is a complex ecosystem. It needs to track products (Inventory),
manage users (Account), handle transactions (Shopping Cart), and arrange
logistics (Shipping). A single agent trying to manage all these rules would be
overwhelmed and prone to errors (e.g., hallucinating inventory that doesn't
exist).

### The Solution

By splitting the domain into specialized agents, we ensure that the "Inventory
Agent" always has accurate stock data, while the "Shipping Agent" focuses solely
on logistics. A central "Storefront Agent" coordinates these specialists to
provide a seamless customer experience.

---

## Exercise Instructions

### Your Task

You need to design the architecture for this e-commerce system and define the
agents that comprise it. Think about how each component may need to talk to 
other components and how they work with databases.

### Requirements

Your design must include the following agents:

1. **Storefront Agent (Orchestrator)**: The main interface for the customer. It
   understands what the user wants to buy or check and routes them to the right
   place.
2. **Inventory Agent**: Can search for products and check stock levels.
3. **Account Agent**: Manages user profiles, addresses, and payment methods.
4. **Shopping Agent**: Manages the current shopping cart (adding/removing
   items).
5. **Shipping Agent**: Calculates shipping costs and tracks deliveries.

Your implementation must:

1. Produce a **System Diagram** showing how the User connects to the Storefront,
   how the Storefront connects to the sub-agents, how the various agents 
   talk to each other, and what data stores are necessary for each.
2. Produce 5 **Agent Card JSON files**, one for each agent, defining their
   `name`, `description`, and `skills`.

### Repository Structure

Since this is a design exercise, you are starting with a blank slate. You will
create the files.

```
exercises/starter/
├── CLASSROOM-README.md  # This file
├── system-design.svg    # Your resulting diagram in any format
├── agent-storefront.json
├── agent-inventory.json
├── agent-account.json
├── agent-shopping.json
└── agent-shipping.json
```

### Starter Code

There is no Python code for this exercise. You can use any diagramming tool you
prefer (Lucidchart, Draw.io, Excalidraw) or even pencil and paper.

### Expected Behavior

**1. The Diagram**
Your diagram should clearly show the **Storefront Agent** as the central hub.
The User should not talk directly to the Inventory or Shipping agents; they
should go through the Storefront.

**2. The Agent Cards**
Each JSON file should look valid and describe the agent.

*Example: agent-inventory.json*

```json
{
  "name": "inventory",
  "description": "Manages product catalog and stock levels.",
  "skills": [
    {
      "id": "search_products",
      "name": "Search Products",
      "description": "Find products by name or category."
    }
  ]
}
```

### Implementation Hints

1. **Think about the "User Flow"**: If a user says "I want to buy a red shirt,"
   which agent needs to be called first? (Inventory). Who needs to be called
   next? (Shopping Cart). Who coordinates this? (Storefront).
2. **Isolate Responsibilities**: Does the Shipping agent need to know *who*
   bought the item? Or just *where* it is going and *how heavy* it is? Keeping
   agents decoupled makes them more reusable.
3. **Naming Matters**: Use clear, descriptive names for your skills (e.g.,
   `add_to_cart` vs `do_thing`) so the Orchestrator (and the LLM driving it)
   knows when to use them.

---

## Important Details

### Best Practices

1. **Orchestrator Pattern**: Keep the Storefront agent "thin". Its job is to
   understand the user and call the right expert, not to do the math or look up
   database records itself.
2. **Context separation**: By using different agents, we ensure the "Shipping"
   prompt doesn't get confused by "Account" rules.

### Common Errors

**Error**: Giving the Orchestrator too many direct tools.

- **Cause**: Trying to make the main agent do everything (e.g., giving the
  Storefront direct SQL access to the inventory).
- **Solution**: Delegate! The Storefront should ask the Inventory Agent, "Do we
  have this?", not run a query itself.
