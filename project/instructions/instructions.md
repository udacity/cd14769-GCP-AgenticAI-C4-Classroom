# Instructions

To demonstrate how multiple agents for the bank can work separately and
together, you’re going to build three independent agents. 
You’ll run all of them using `adk web --a2a`. This will
let you test each individually, but also let them communicate with each other 
via A2A. Each agent should have its own `root_agent` object, but does not need
to handle authentication.

Specifically, the three agents you’ll be building are:

- A loan account agent, which can handle simple questions about the loans that
  the customer has. It will also be able to indicate if you can get a new 
  loan based on criteria specified in a policy document that is stored as a 
  PDF file. This criteria includes:
  - The balance of the customer's loans and deposit accounts. For this, it 
    will need to coordinate with the deposit account agent in some very 
    narrow and specific ways.
  - A summary of the client's history, which is also documented in a PDF file.
- A deposit account agent, which can handle simple questions about your deposit
  accounts, such as a checking or savings account. While it *cannot* give a 
  total account balance (for security reasons), it *can* say if the balance 
  is above a requested value. This is so it can work with the loan account 
  agent. 
- A manager agent that takes all customer questions and either answers them
  itself (if it is a simple question about the bank) or passes it off to one 
  of the other agents to handle. 

We’ll look at the details of what you need to do for each component and what you
need to do to tie them together and test them. You should be able to try 
each agent out individually by running `adk web` in a command prompt and 
then viewing  it via the URL provided. This is a good way to evaluate your 
agents as they evolve.

The bank's board has also given you some test questions and conversations to 
evaluate how well your agents work. You'll need to run this, provide the 
results, and prepare a report examining your agent's performance in light of 
these results. There is a script called `a2a.py` which will help you run 
this evaluation, as well as do some testing and see how the A2A protocol works.

## Project Instructions

Make sure you have completed the setup instructions in the Environment Setup.
This should include
- setting values for your cloud project in the “.env” file 
- activating a virtual environment with venv
- setting up cloud resources
  - a database that stores the account information
  - a Google Cloud Storage bucket to store the loan policy and customer PDF 
    files
- running the MCP Database Toolbox server locally
    1. If you haven't downloaded the MCP Database Toolbox server, [download and install it](https://googleapis.github.io/genai-toolbox/getting-started/introduction/#installing-the-server) for your platform.
    2. From the command line, change directories to where your **`tools.yaml`** file is located.
    3. Make sure the "MYSQL" environment variables are exported in your current command line. If you're using bash, for example, you might do something like `export $(grep -v '^#' .env | xargs)`
    4. Start the server from your command line and add the provided URL to your .env file.
       `/path/to/toolbox --tools-files "tools.yaml"` 
       * If you need to use another port, you can include a `--port` parameter
       * If there are multiple tools files you wish to use, you can specify 
         the --tools-files parameter, and filename, multiple times.
    5. Make sure you update the **`.env`** file to include the "TOOLBOX_URL" that points at the URL that the toolbox is listening to. 

### Part 1: The Basic Deposit Account Agent

The first task is to build an agent that has tools that can answer questions
about deposit accounts. All of this work will be done in files in the 
“deposit” folder. You should **not** import files from elsewhere. The 
“deposit” folder designates it as an independent agent from the others.

There is a basic template provided for you that should yield a running agent,
but not one that does much. Make sure you can run it

1. In a command line, type `adk web --a2a`
2. Using the URL it shows, open that in a browser. It will probably be something
   like `http://localhost:8000` or `http://127.0.0.1:8000`
     * If you need to run it on a different port, because you have something
       else running on port 8000, you can specify
       that with the `--port` parameter, so `--port 8001` would use port
       8001 instead. Adjust all the instructions and the test scenario 
       file below to follow.
3. In the drop-down in the upper left, select “deposit” to make sure you’re
   talking to the agent.

Once you’re sure you can access the agent, you need to build it out:

1. Make sure your database is configured, has a public IP address, has a 
   user that can access it, and has the tables and data defined in the 
   "deposit.sql" file. Make sure your ".env" file has environment variables 
   for this configuration.
2. Begin configuring the "tools.yaml" file to be able to use this database 
   through the MCP Database Toolbox library.
3. Define a tool in the "tools.yaml" file which will return the balance for a
   specifically named account. Then add it to the list of tools in “agent.py” 
   and make sure you update the “agent-prompt.txt” to mention it.
4. Do something similar to create a tool that will return the most transactions.
5. You can create other tools if you feel they are necessary, but keep in 
   mind the other requirements and restrictions.  
6. Create an agent card in “agent.json” that reflects the skills that are
   available and the URL where the agent should be available.

Test the agent:

1. Test it using the web page “http://localhost:8000/” and selecting the
   “deposit” agent as you did above.
2. Make sure you can access the agent card by using the a2a.py program with 
   a command such as 
   `python a2a.py --url http://localhost:8080/a2a/deposit` --card`
3. Send an A2A formatted HTTP POST request to the agent using the a2a.py 
   program with a command such as
   `python a2a.py --url http://localhost:8080/a2a/deposit` --prompt "How 
   much is in my vacation account?"`

### Part 2: The Basic Loan Account Agent

The next task is to build an agent that has tools that can answer questions
about loans. All of this work will be done in files in the “loan” folder. 
You should **not** import files from elsewhere. The “loan” folder designates 
it as an independent agent from the others.

There is a basic template provided for you that should yield a running agent,
but not one that does much. Make sure you  can run it as above, but with the 
“loan” agent.

Once you’re sure you can access the agent, you need to build it out:

1. As above, make sure the database is configured (you can use the same 
   database) and that it is loaded with the data from "loan.sql".
2. Also as above, update the "tools.yaml" file with this information.
3. Define a tool in the "tools.yaml" file which will return the balance for a
   specifically named account. Then add it to the list of tools in 
   “agent.py” and make sure you update the “agent-prompt.txt” to mention it.
3. Create an agent card in “agent.json” that reflects the skills that are
   available and the URL where the agent should be available.

Test the agent:

1. Test it using the web page “http://localhost:8000/” and selecting the “loan”
   agent as you did above.
2. Make sure you can access the agent card as you did above, but the URL 
   will now be "http://localhost:8000/a2a/loan".
3. Similar to what you did above, send an A2A formatted HTTP POST request to 
   the agent with a prompt asking about the balance on the personal account.

### Part 3: The Manager Agent

Once you have the two department agents, you’ll create a manager agent that
forwards requests to both of them in the “manager” folder:

1. Add a `RemoteA2aAgent` for both the deposit agent and the loan agent,
   referencing their agent cards by URL and add them as sub-agents for the 
   `root_agent` in “agent.py”.
2. Update the “agent-prompt.txt” to make sure requests get routed to the correct
   sub-agent.
3. Create an agent card in “agent.json” that reflects the skills that are
   available and the URL where the agent should be available.

Test this agent:

1. Test it using the web page “http://localhost:8000/” and selecting the
   “manager” agent. Ask questions that you know will be directed to either 
   the loan or deposit account agent and see how the web test tool indicates 
   it gets routed to those agents.
2. Make sure you can access the agent card and send an A2A formatted HTTP 
   POST request using the `a2a.py` tool with the  URL 
   “http://localhost:8000/a2a/manager”.

### Part 4: Adding a Loan Approval Sub-Agent

Once you have all the agents working independently and with the manager agent,
you’ll get the loan agent working to ask questions of the deposit account agent.

Start by updating the deposit agent:

1. Add a new tool through "tools.yaml" named `check-minimum-balance` that 
   takes a number and returns true if the sum of all the deposit account 
   balances is greater than this value, or false otherwise.
2. Add this to the tools in “deposit/agent.py” and make sure you update 
   "agent-prompt.txt" and "agent.json".
3. Test this to make sure it works as you expect.

Create the loan approval sub-agent. This will be an agent that calls several 
other agents that you will need to design and create. These agents will 
communicate with each other by storing their results in the state in an 
appropriate way.

You will need to create the following sub-agents (of the loan approval 
sub-agent) with these requirements and specifications. You may wish to 
diagram how each of these agents will interact with each other and what 
orchestration agents will be necessary to coordinate them. For consistency, 
names for these agents are also provided:
- Take the request from the customer and determine what type of loan they 
  want and how much they are asking for. (get_requested_value_agent)
- The total outstanding balance on all of the customer's loans. 
  (outstanding_balance_agent)
- Load the policy guidelines PDF from a Google Cloud Storage bucket to extract 
  the evaluation criteria you will be enforcing based on the type and the 
  amount requested. (policy_agent)
- A custom agent that, based on the total outstanding balance and the 
  debt-to-equity ratio determined by the above agents, computes what the 
  minimum deposit account balance needs to be. (total_value_agent)
- Communicates, via A2A, with the deposit sub-agent you created above to 
  determine if the total deposit balances are above this minimum required 
  level. (check_equity_agent)
- Load the customer profile PDF document from a Google Cloud Storage bucket 
  and determine their customer rating. (user_profile_agent)
- Based on all of the above information you've collected, make a 
  determination if they should receive the loan and give them an answer in a 
  friendly format. If they should receive the loan, let them know a loan 
  officer will be contacting them shortly. If they should not, you should be 
  polite, but you should not give them specific details about why the loan 
  application was rejected. Specifically, you should not give them any 
  information that was contained in, or derived from, the policy or user 
  profile.

Don't forget to add this agent to the loan `root_agent`, update its prompt, 
and update the agent card.

Test this agent by asking the manager for a loans of different values and 
different types. Using the web console is a great way to try it out and see 
how the state changes

### Part 5: Testing, Evaluating, and Preparing Your Report

You'll be testing your agents against a data set provided in the 
"test_scenarios.csv" file. If you look at the file (and you should), you'll 
see that it provides prompts, some of them as parts of sessions, that will 
be sent to the manager endpoint. As you analyse the results, make sure you 
pay attention to which parts are part of a single session and which are from 
different sessions. If you run the tests more than once, you will need to 
restart the A2A servers to make sure they are not retaining the old sessions.

You can run this using 
`python a2a.py --in test_scenarios.csv --out test_results`

This will produce three files:
* "test_results.csv" contains a CSV file with the message ID and response. 
  This directly matches the entries in the "test_scenarios.csv" file.
* "test_results.json" contains a list of JSON events, one per line. Each 
  event contains the JSON results from the corresponding prompt, which are 
  far more extensive than the text response and can be useful for debugging.
* "test_results.txt" is a human-readable form for each thread and prompt. It 
  shows the thread ID, and each request and response for that thread.

You should then prepare a report for the bank's board. This should include:
- A comprehensive explanation of your multi-agent system.
  - You may wish to include a diagram of the multi-agent interactions.
  - This is especially important when documenting the loan approval agent.
- Evaluating the results from running the test scenarios and highlighting 
  strengths and areas for improvement.
- Addressing the risks of using agents and possible ways to mitigate these 
  risks.
- Suggestions for further improvements to the system based on all of the above.

## Assessment Instructions

See the rubric for details about each of the following things that you will 
submit for review:
* Well documented source code, including prompt files and tools.yaml files
* Screen shots of several tests of the loan approval sub-agent while using 
  the web tool for the loan agent. 
  * These screen shots should illustrate all the steps involved in the 
    sub-agent and the final state of your agent.
  * Note that this should be tested against the "loan" agent directly, **not** 
    the "manager" agent, so you can see the full interaction and final state.
  * You may also submit screen shots of individual requests and responses at 
    various stages if you feel it will help illustrate how your code works.
* Your test_results.txt, test_results.json, and test_results.csv file.
  * You do **not** need to submit your test_scenarios.csv file unless you 
    have made significant additions or changes.
* Your final report and analysis, which may (but does not have to) include 
  diagrams or illustrations of the multi-agent interactions.

## Next Steps: Further Enhancements

The bank managers will certainly be impressed by this prototype. But perhaps
there are a few other things you can do
that might really wow them and convince them to back the project:

- If you’re not convinced that these are really separate servers - go ahead and
  run each on a different port or on different machines completely. Just 
  remember to change your agent cards to reflect their new locations.
- In this prototype, the loan application and decision only go to the 
  customer. Can you add tools that will also save the application (and the 
  agent's suggestion) to a database? Perhaps even an agent for loan managers 
  that will help them review new items on this list? 
- The tests, particularly for the loan approval, are somewhat narrow since 
  they only cover a few cases and only for one set of customer information. 
  You may wish to expand your test coverage with:
  - Additional tests to test for other types of loans and amounts to 
    borrow. 
  - More customer profiles that you'll run all the tests against. (Remember 
    that this may require other data stored in your database as well as 
    additional client documents in GCS.)
  - Including all of these as part of your report and analysis.
