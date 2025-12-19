# E-Commerce System Design - Solution

We have designed a robust multi-agent architecture for an e-commerce storefront,
utilizing the "Orchestrator and Workers" pattern to manage complexity.

---

## Overview

### What You'll Learn

You can compare your design to a reference implementation of a multi-agent
e-commerce system. We will examine the choices made in the system architecture
and how Agent Cards are used to define the contracts between agents.

Learning objectives:

- Evaluate a multi-agent system architecture against a reference design.
- Understand how A2A Agent Cards define agent contracts.
- Review specific roles and responsibilities in an e-commerce context.

### Prerequisites

- Understanding of the "Orchestrator and Workers" pattern.
- Knowledge of JSON syntax.

---

## Understanding the Concept

### The Problem

A monolithic approach to e-commerce (one giant prompt or agent) often fails
because the context window becomes cluttered with conflicting instructions (
e.g., shipping rules vs. product return policies). This leads to hallucinations
and poor performance.

### The Solution

This solution implements a **Storefront Agent** as the primary orchestrator. It
delegates specific tasks to four specialized agents: **Inventory** (stock
levels), **Account** (users), **Shopping** (product search and cart), and *
*Shipping** (fulfillment). This separation ensures each agent focuses on a
single domain, making the system more reliable and easier to maintain.

---

## Code Walkthrough

### Repository Structure

```
lesson-01-design/exercises/
├── agent-01-storefront.json       # The Orchestrator
├── agent-02-inventory.json        # Inventory specialist
├── agent-03-account.json          # Account specialist
├── agent-04-shopping.json         # Shopping Cart specialist
├── agent-05-shipping.json         # Shipping specialist
├── exercise-design-01-storefront.svg  # System overview
├── exercise-design-02-inventory.svg   # Data flow for inventory
├── exercise-design-03-account.svg     # Data flow for account
├── exercise-design-04-shopping.svg    # Data flow for shopping
└── exercise-design-05-shipping.svg    # Data flow for shipping
```

### Step 1: System Architecture

**File:** `exercise-design-01-storefront.svg`

Your architecture should resemble the reference diagram, with the **Storefront
Agent** as the single point of entry for the User.

- The **User** communicates *only* with the Storefront.
- The **Storefront** communicates with **Inventory**, **Account**, **Shopping**,
  and **Shipping**.

**Key points:**

- Centralized control via the Storefront.
- Specialized data stores for each agent (implied).

### Step 2: The Orchestrator (Storefront)

**File:** `agent-01-storefront.json`

The Storefront agent's card defines its role as the coordinator. It utilizes "
skills" to delegate tasks rather than accessing databases directly.

```json
{
  "name": "storefront",
  "skills": [
    {
      "id": "handle_customer_request",
      "name": "Handle Request",
      "description": "Process natural language requests from customers.",
      "examples": [
        "I want to buy some headphones",
        "Where is my order?"
      ]
    }
  ]
}
```

**Key points:**

- The `handle_customer_request` skill indicates it accepts open-ended user
  input.
- It acts as a router, classifying the user's intent.

### Step 3: The Specialists

Compare your agent definitions with these specialists. Did you separate concerns
similarly?

**Inventory Agent (`agent-02-inventory.json`)**

- **Responsibility**: Checking and updating stock.
- **Skills**: `check_stock`, `update_stock`

**Account Agent (`agent-03-account.json`)**

- **Responsibility**: User profile and subscription management.
- **Skills**: `get_user_profile`, `update_user_profile`, `manage_subscriptions`,
  `send_notification`

**Shopping Agent (`agent-04-shopping.json`)**

- **Responsibility**: Product search and cart management.
- **Skills**: `search_products`, `check_inventory`, `get_product_info`,
  `manage_cart`

**Shipping Agent (`agent-05-shipping.json`)**

- **Responsibility**: Order tracking and fulfillment.
- **Skills**: `get_order_status`, `fulfill_order`

### Complete Example

In a full interaction:

1. User says "Buy the red shirt".
2. **Storefront** calls **Shopping** to find the product.
3. **Shopping** calls **Inventory** (or checks its own cache) to verify stock.
4. **Storefront** calls **Shopping** to add it to the cart.
5. **Shopping** confirms addition.
6. **Storefront** tells User "Added red shirt to cart."

---

## Important Details

### Best Practices

1. **Strict Boundaries**: The Shipping agent does not know about product
   descriptions, only weights and dimensions. This allows us to change the
   product catalog schema without breaking the shipping logic.
2. **Interface Segregation**: Each agent card exposes only what is necessary for
   other agents to know.

### Common Misconceptions

**Misconception**: "The Orchestrator does all the thinking."
**Reality**: The Orchestrator only handles the *flow*. The specialized agents do
the "thinking" regarding their specific domain (e.g., the Shipping agent "
thinks" about the best carrier route).