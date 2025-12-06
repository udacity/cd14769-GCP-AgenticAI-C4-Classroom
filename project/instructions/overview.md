## Banking on Multiple Agents

You are a Senior Developer at a small financial institution. The senior partners
are interested in AI, but a little nervous about having a single agent with 
access to all a customer’s information. They want you to build a rapid
prototype to demonstrate what agents can do and the feasibility of the idea
without using actual customer data.

**The Challenge**

You will need to implement agents that work together to provide information for
customers, but can also work independently from each other for some tasks. 
Specifically, you’ll need to provide access to three sets of information

- General banking information
- Deposit accounts they have (such as checking or savings accounts)
- Loans they have with the bank

Some of these components need information from the others, but should not have
access to all of them.

- For example, if the customer is trying to open a new loan, the loan agent may
  contact the deposit account agent to ask about their balances.

**Assumptions**

- You won’t need to manage multiple accounts - you can assume authentication has
  been handled for a single account.
- These are not real procedures that the bank follows - your management just
  wants you to do them to prove advanced concepts are feasible before going 
  ahead with real business logic. 

**The Goal**

Build three independent agents that can manage this information and provide it 
to the customer. There may be sub-agents that handle specific tasks. Prove the 
concept is feasible and safe so the bank’s board will approve a full-scale 
project. 

## Project Summary

Using Google’s Agent Development Kit, you will build three prototype customer
support agents, each of which has a very narrow set of data that they have 
access to. There are also only specific tasks that each one can perform with that
data, and this may require creating sub-agents to do these tasks.

You will be running all of them using the same agent runner (adk web), but the
agents should be independent - they will communicate with each other using 
the A2A protocol. 

The three main agents you will build are:

**The Deposit Account Agent**

- Has access to cash deposit accounts only (checking, savings)
- Has several basic tools
    - Current account balances
    - Last three transactions for each account
    - Can report if the total balance for all accounts is greater than a target
      amount. (This will be used by the Loan Agent, described below.)
    - Can provide a list of accounts.
- It should not reveal what the total balance of all accounts are (this is 
  considered a security risk). But it can say if the total is greater or 
  less than some value. 

**The Loan Agent**

- Has access to loan information only
- Has several basic tools
    - Outstanding loan balance
    - Loan payoff date
    - Next loan payment date
- An advanced tool that will determine if they are eligible for a new loan based
  on a number of criteria that are outlined in a policy document provided by 
  the senior loan manager.
    - The main criteria needs to compute the minimum required assets on 
      deposit and check with the deposit account agent if this requirement 
      is met.
    - Another criteria will evaluate a loan officer's assessment of the 
      customer to give them a profile rating.
    - These are all evaluated against the type of loan and how much they are 
      requesting to come up with a conclusion.

**The Manager**

- Can answer questions about the bank.
- Can answer questions from the Loan Agent or the Deposit Account Agent without
  having the customer “transfer to” those agents. This will involve A2A.

All three agents must listen via A2A and be able to present an A2A Agent Card
representing itself.