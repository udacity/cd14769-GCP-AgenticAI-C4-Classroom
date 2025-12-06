### Part 1: The Basic Deposit Account Agent

* Configure and connect the agent to a database.
  * Submission Requirements
    * The `.env` file is **not** submitted
    * The `deposit/tools.yaml` file is configured to use the MCP Database 
      Toolbox library to connect to the database through environment variables
  * Reviewer Tip
    * **Pass the requirement if** the `deposit/tools.yaml` file shows a  
      connection to a MySQL database using environment variables for credentials.
    * **Fail the requirement if** the `deposit/tools.yaml` file is missing 
      or  does not configure a database connection.
    * **Fail the requirement if** credentials or connection information is 
      hardcoded in the `tools.yaml` file.
    * **Fail the requirement if** the student submits their  
      `.env` file. Remind them not to submit secrets.
* Implement tools for querying deposit account information.
  * Submission Requirements
    * A tool is defined in `deposit/tools.yaml` that returns the balance for 
      a specific account. 
    * A tool is defined in `deposit/tools.yaml` that returns recent 
      transactions. 
    * The tools are added to the `tools` list in `deposit/agent.py`.
    * The `deposit/agent-prompt.txt` file is updated to reflect the new tool 
      capabilities. 
  * Reviewer Tip
    * **Pass the requirement if** `deposit/tools.yaml` defines tools for  
      getting account balance and recent transactions.
    * **Pass the requirement if** `deposit/agent.py` loads and uses these tools.
    * **Pass the requirement if** `deposit/agent-prompt.txt` describes how 
      to  use the new tools.
    * **Fail the requirement if** the tools are not defined in `tools.yaml`.
    * **Fail the requirement if** the tools are not added to the agent  in 
      `agent.py`.
    * **Fail the requirement if** the prompt in `agent-prompt.txt` is not  
      updated to reflect the new tools.
    * **Praise the learner's work if** they include a tool to get a list  of 
      accounts to make the agent more robust, as shown in the solution.
    * However... **Pass the requirement with comments if** there are no 
      guardrails or other limits for the customer to use this list to get 
      all balances. (Note that this is tested in the test_scenarios.csv file,
      and it should fail there.)
* Define an agent card for discovery and interaction.
  * Submission Requirements
    * The `deposit/agent.json` file contains a valid agent card.
    * The agent card includes the agent's skills and its URL.
  * Reviewer Tip
    * **Pass the requirement if** `deposit/agent.json` contains a valid 
      agent  card with a name, URL, description, and skills for all public 
      tools.
    * **Fail the requirement if** `deposit/agent.json` is missing or the  
      JSON is invalid.
    * **Fail the requirement if** the agent card is missing the URL or skills.
    * **Praise the learner's work if** the agent card is very descriptive  
      and provides good examples.
* Demonstrate agent functionality through testing.
  * Submission Requirements
    * The agent responds correctly to a balance inquiry through the web 
      interface, demonstrated through screen shots.
    * The agent card is accessible via an A2A request demonstrated by the 
      output of `a2a.py`.
    * The agent responds correctly to a balance inquiry via an A2A request 
      demonstrated by the output of `a2a.py`.
  * Reviewer Tip
    * **Pass the requirement if** the submission includes screenshots of the 
      web interface showing successful balance inquiries.
    * **Pass the requirement if** the submission includes the output of 
      `a2a.py` showing a successful A2A request for the agent card.
    * **Pass the requirement if** the submission includes the output of 
      `a2a.py` showing a successful A2A request for a balance inquiry.
    * **Fail the requirement if** any of the required test evidence is missing.
    * **Fail the requirement if** the test results show the agent is not  
      functioning correctly.
    * **Pass the requirement with comment if** the evidence is provided but 
      is  not clearly labeled or is hard to understand.

### Part 2: The Basic Loan Account Agent

* Configure and connect the agent to a database.
  * Submission Requirements
    * The `.env` file is **not** submitted
    * The `loan/tools.yaml` file is configured to use the MCP Database
      Toolbox library to connect to the database through environment
      variables.
  * Reviewer Tip
    * **Pass the requirement if** the `loan/tools.yaml` file shows a
      connection to a MySQL database using environment variables for
      credentials.
    * **Fail the requirement if** the `loan/tools.yaml` file is missing or
      does not configure a database connection.
    * **Fail the requirement if** credentials are hardcoded in the
      `tools.yaml` file.
    * **Fail the requirement if** the student submits their  
      `.env` file. Remind them not to submit secrets.
* Implement tools for querying loan account information.
  * Submission Requirements
    * A tool is defined in `loan/tools.yaml` that returns the balance for a
      specific account.
    * The tool is added to the `tools` list in `loan/agent.py`.
    * The `loan/agent-prompt.txt` file is updated to reflect the new tool
      capabilities.
  * Reviewer Tip
    * **Pass the requirement if** `loan/tools.yaml` defines a tool for
      getting loan account balance.
    * **Pass the requirement if** `loan/agent.py` imports and uses this
      tool.
    * **Pass the requirement if** `loan/agent-prompt.txt` describes how to
      use the new tool.
    * **Fail the requirement if** the tool is not defined in `tools.yaml`.
    * **Fail the requirement if** the tool is not added to the agent in
      `agent.py`.
    * **Fail the requirement if** the prompt in `agent-prompt.txt` is not
      updated to reflect the new tool.
    * **Praise the learner's work if** they include a tool to get a list
      of loan accounts to make the agent more robust.
    * However... **Pass the requirement with comments if** there are no
      guardrails or other limits for the customer to use this list to get
      all balances. (Note that this is tested in the test_scenarios.csv file,
      and it should fail there.)
* Define an agent card for the loan agent.
  * Submission Requirements
    * The `loan/agent.json` file contains a valid agent card.
    * The agent card includes the agent's skills and its URL.
  * Reviewer Tip
    * **Pass the requirement if** `loan/agent.json` contains a valid agent
      card with a name, URL, description, and at least one skill.
    * **Fail the requirement if** `loan/agent.json` is missing or the JSON
      is invalid.
    * **Fail the requirement if** the agent card is missing the URL or
      skills.
    * **Praise the learner's work if** the agent card is very descriptive
      and provides good examples.
* Demonstrate agent functionality through testing.
  * Submission Requirements
    * The agent responds correctly to a balance inquiry through the web
      interface, demonstrated through screen shots.
    * The agent card is accessible via an A2A request demonstrated by the
      output of `a2a.py`.
    * The agent responds correctly to a balance inquiry via an A2A request
      demonstrated by the output of `a2a.py`.
  * Reviewer Tip
    * **Pass the requirement if** the submission includes screenshots of the
      web interface showing successful balance inquiries.
    * **Pass the requirement if** the submission includes the output of
      `a2a.py` showing a successful A2A request for the agent card.
    * **Pass the requirement if** the submission includes the output of
      `a2a.py` showing a successful A2A request for a balance inquiry.
    * **Fail the requirement if** any of the required test evidence is
      missing.
    * **Fail the requirement if** the test results show the agent is not
      functioning correctly.
    * **Pass the requirement with comment if** the evidence is provided but
      is not clearly labeled or is hard to understand.

### Part 3: The Manager Agent

* Implement the manager agent to route requests to sub-agents.
  * Submission Requirements
    * The `manager/agent.py` is updated to add the deposit and loan agents as
      sub-agents via A2A.
  * Reviewer Tip
    * **Pass the requirement if** `manager/agent.py` correctly imports and
      uses `RemoteA2aAgent` to add the deposit and loan agents as
      sub-agents.
    * **Fail the requirement if** `manager/agent.py` does not add the
      sub-agents or does not use `RemoteA2aAgent`.
    * **Pass the requirement with comment if** the student hardcodes the
      URLs to the agent cards instead of using the
      `AGENT_CARD_WELL_KNOWN_PATH` constant or using environment variables 
      to control the base URL.
* Configure the manager agent's prompt for correct routing.
  * Submission Requirements
    * The `manager/agent-prompt.txt` file is updated to instruct the agent
      on how to route requests to the appropriate sub-agent.
  * Reviewer Tip
    * **Pass the requirement if** the `manager/agent-prompt.txt` file
      clearly instructs the agent to route deposit-related questions to
      the deposit agent and loan-related questions to the loan agent.
    * **Fail the requirement if** the prompt does not provide clear
      routing instructions.
    * **Praise the learner's work if** the prompt includes examples of
      different types of questions and which agent to route them to.
* Define an agent card for the manager agent.
  * Submission Requirements
    * The `manager/agent.json` file contains a valid agent card.
    * The agent card includes the agent's skills and its URL.
  * Reviewer Tip
    * **Pass the requirement if** `manager/agent.json` contains a valid
      agent card with a name, URL, description, and at least one skill.
    * **Fail the requirement if** `manager/agent.json` is missing or the
      JSON is invalid.
    * **Fail the requirement if** the agent card is missing the URL or
      skills.
    * **Praise the learner's work if** the agent card is very
      descriptive and provides good examples of the kinds of questions
      the manager agent can handle.
* Demonstrate manager agent functionality through testing.
  * Submission Requirements
    * The agent correctly routes a deposit-related question to the deposit
      agent, demonstrated through screen shots of the web interface.
    * The agent correctly routes a loan-related question to the loan agent,
      demonstrated through screen shots of the web interface.
    * The agent card is accessible via an A2A request demonstrated by the
      output of `a2a.py`.
  * Reviewer Tip
    * **Pass the requirement if** the submission includes screenshots of
      the web interface showing a deposit question being routed to the
      deposit agent.
    * **Pass the requirement if** the submission includes screenshots of
      the web interface showing a loan question being routed to the loan
      agent.
    * **Pass the requirement if** the submission includes the output of
      `a2a.py` showing a successful A2A request for the agent card.
    * **Fail the requirement if** any of the required test evidence is
      missing.
    * **Fail the requirement if** the test results show the agent is not
      routing requests correctly.
    * **Pass the requirement with comment if** the evidence is provided but
      is not clearly labeled or is hard to understand.

### Part 4: Adding a Loan Approval Sub-Agent

* Update the deposit agent with a minimum balance tool.
  * Submission Requirements
    * A new tool added to the deposit agent that takes a number and returns 
      true if the sum of all deposit account balances is greater than this 
      value, and false otherwise. 
    * The tool is added to the `tools` list in `deposit/agent.py`.
    * The `deposit/agent-prompt.txt`, `deposit/agent.json`, and other files 
      as necessary are updated to reflect the new tool.
  * Reviewer Tip
    * **Pass the requirement if** the `deposit/tools.yaml` file defines a
      new tool named `check-minimum-balance` that takes a number and
      returns true or false. There are other ways this could be done, but 
      this is the best. If not done this way, you may want to **Pass with 
      comments**.
    * **Pass the requirement if** the tool is correctly added to the agent
      in `deposit/agent.py` and mentioned in `deposit/agent-prompt.txt`.
    * **Fail the requirement if** the tool is not implemented or not added
      to the agent.
    * **Pass the requirement if** they also update the agent card in
      `deposit/agent.json` to reflect the new tool.
* Implement the `get_requested_value_agent` and
  `outstanding_balance_agent`.
  * Submission Requirements
    * The `get_requested_value_agent` is implemented to determine the loan
      type and amount from the customer's request.
    * The `outstanding_balance_agent` is implemented to get the total
      outstanding balance on all of the customer's loans.
  * Reviewer Tip
    * **Pass the requirement if** the `get_requested_value_agent`
      correctly extracts the loan type and amount from the user's
      request.
    * **Pass the requirement if** the `outstanding_balance_agent`
      correctly calls a tool to get the total outstanding balance.
    * **Fail the requirement if** either agent is not implemented or does
      not function as described.
    * **Praise the learner\'s work if** the agents are well-defined with
      clear prompts and output schemas.
    * **Pass the requirement if** the agents use `output_schema` to define
      the output structure and `output_key` to save the output to the
      state.
* Implement the `policy_agent` and `user_profile_agent` to analyze PDF
  documents from Google Cloud Storage.
  * Submission Requirements
    * The `policy_agent` is implemented to load the policy guidelines PDF
      from a Google Cloud Storage bucket and extract the evaluation
      criteria.
    * The `user_profile_agent` is implemented to load the customer profile
      PDF document from a Google Cloud Storage bucket and determine their
      customer rating.
    * The Google Cloud Storage bucket to use is specified through an 
      environment variable.
  * Reviewer Tip
    * **Pass the requirement if** the `policy_agent` and `user_profile_agent`
      use `static_instruction` to load the policy and customer profile
      PDFs from GCS.
    * **Pass the requirement if** the GCS bucket is configured using an
      environment variable.
    * **Fail the requirement if** the agents do not load the PDFs from GCS
      or fail to extract the required information.
    * **Fail the requirement if** the student loads the PDF using another
      method and converts it to text directly, instead of using
      `static_instruction`.
    * **Pass the requirement with comments if** the GCS bucket is
      hardcoded.
    * **Pass the requirement if** the agents use `output_schema` to define
      the output structure and `output_key` to save the output to the
      state.
* Implement the custom `total_value_agent` and the A2A-enabled
  `check_equity_agent`.
  * Submission Requirements
    * The `total_value_agent` is implemented as a custom agent to compute
      the minimum required deposit account balance. The values necessary to 
      do this calculation come from state values.
    * The `check_equity_agent` is implemented to communicate with the
      deposit agent via A2A to check if the total deposit balance is
      above the minimum required level.
  * Reviewer Tip
    * **Pass the requirement if** the `total_value_agent` is implemented
      as a custom agent that
      * gets the total outstanding balance, the value requested, 
        and the debt-to-equity ratio from the state
      * correctly calculates the minimum required equity
      * saves the minimum required equity to the state
    * **Pass the requirement if** the `check_equity_agent` uses A2A to
      call the deposit agent's `check-minimum-balance` tool.
    * **Fail the requirement if** the `total_value_agent` 
      * is not a custom agent, 
      * the calculation is incorrect, 
      * values are not read from state,
      * or values are not saved to state
    * **Fail the requirement if** the `check_equity_agent` does not use
      A2A to communicate with the deposit agent.
    * **Pass the requirement if** the `check_equity_agent` uses
      `output_schema` to define the output structure and `output_key` to
      save the output to the state.
* Implement an agent to make a final loan decision and generate a
  response.
  * Submission Requirements
    * An agent is implemented to make a final loan decision based on the
      information gathered by the other sub-agents.
    * The agent generates a friendly response to the customer.
    * If the loan is approved, the response informs the customer that a
      loan officer will contact them.
    * If the loan is rejected, the response is polite and does not give
      specific details about the rejection.
  * Reviewer Tip
    * **Pass the requirement if** the agent makes a decision based on the
      gathered information (equity and customer rating).
    * **Pass the requirement if** the agent generates a polite response
      that does not reveal sensitive information if the loan is
      rejected.
    * **Fail the requirement if** the agent's decision logic is flawed or
      if it reveals sensitive information upon rejection.
    * **Praise the learner's work if** they use the "gemini-2.5-pro" or 
      other top-level reasoning model to write this portion.
    * **Pass the requirement with comments if** they use "gemini-2.5-flash" 
      or "gemini-2.5-flash-lite" as a model for this portion. You may wish 
      to question them if these models are sufficient at generating a reply 
      that meets the requirements.
* Design and implement the loan approval sub-agent with orchestration agents 
  that integrate all of the above sub-agents.
  * Submission Requirements
    * This sub-agent uses the above sub-agents to perform the steps of
      the loan approval process.
    * Orchestration agents are used to coordinate the flow of information
      between the sub-agents.
    * The state is used to pass information between the sub-agents.
  * Reviewer Tip
    * **Pass the requirement if** a loan approval sub-agent is created
      that contains the other sub-agents.
    * **Pass the requirement if** orchestration agents (like
      `SequentialAgent` and `ParallelAgent`) are used to control the
      flow. At least one instance of both are required.
    * **Pass the requirement if** the state is used to pass information
      between the agents.
    * **Fail the requirement if** the sub-agents are not integrated into a
      single workflow.
    * **Fail the requirement if** either `SequentialAgent` or 
      `ParallelAgent` aren't used. In this case, evaluate how they are doing 
      the orchestration and suggest that they may wish to reconsider, but 
      try to avoid leading them to using these two classes specifically. 
      They should be able to get it from the module.
    * **Praise the learner's work if** they use a diagram to explain
      their orchestration strategy.
* Integrate and test the complete loan approval workflow.
  * Submission Requirements
    * The loan approval sub-agent is added to the `sub_agents` list in
      `loan/agent.py`.
    * The `loan/agent-prompt.txt` and `loan/agent.json` files are
      updated to reflect the new capabilities.
    * The submission includes screenshots of the web interface using the 
      "loan" agent specifically showing a successful loan approval request.
    * The submission includes screenshots of the web interface using 
      the "loan" agent specifically showing a rejected loan approval request.
  * Reviewer Tip
    * **Pass the requirement if** the loan approval sub-agent is added to
      the main loan agent.
    * **Pass the requirement if** the loan agent's prompt and card are
      updated.
    * **Pass the requirement if** screenshots are provided for both a
      successful and a rejected loan approval, showing the final state.
    * **Fail the requirement if** the integration is not done or if the
      test evidence is missing or incomplete.

### Part 5: Testing, Evaluating, and Preparing Your Report

* Test the multi-agent system using the provided test scenarios.
  * Submission Requirements
    * The `test_results.csv` file is submitted.
    * The file contains the results of running the `a2a.py` script with
      the provided `test_scenarios.csv` file.
  * Reviewer Tip
    * **Pass the requirement if** the `test_results.csv` file is submitted
      and contains the results of running the test scenarios.
    * **Fail the requirement if** the `test_results.csv` file is not
      submitted or is empty.
* Prepare a report explaining the multi-agent system.
  * Submission Requirements
    * A report is submitted that explains the architecture of the
      multi-agent system.
    * The report optionally includes a diagram of the multi-agent
      interactions.
    * The explanation of the loan approval agent is particularly
      detailed.
  * Reviewer Tip
    * **Pass the requirement if** the report clearly explains the
      architecture of the multi-agent system, including the roles of
      each agent and how they interact.
    * **Pass the requirement if** the explanation of the loan approval
      agent is detailed and easy to understand.
    * **Fail the requirement if** the report does not explain the system
      architecture or the explanation is unclear.
    * **Praise the learner's work if** they include a clear and helpful
      diagram of the multi-agent interactions.
* In your report, evaluate the test results and identify strengths and 
  weaknesses.
  * Submission Requirements
    * The report evaluates the results from the `test_results.csv` file.
    * The report identifies specific strengths of the implemented system.
    * The report identifies specific areas for improvement.
  * Reviewer Tip
    * **Pass the requirement if** the report discusses the test results and
      identifies at least one strength and one weakness of the system.
    * **Fail the requirement if** the report does not evaluate the test
      results or does not identify any strengths or weaknesses.
    * **Fail the requirement if** the test results include responses that 
      the project requirements explicitly forbid. Some examples of tests 
      that should be caught by guardrails:
      * msg-003-1 attempts to get the total of all deposits, but this is not 
        allowed by the requirements.
      * msg-007-1 and 2 and msg-008-1 and 2 attempt to get a loan with 
        incomplete information that the second message in the thread asks for.
      * msg-006-1 attempts bank fraud, and there shouldn't be a tool that 
        allows it.
    * **Praise the learner's work if** the evaluation is insightful and
      well-supported by the test results.
* As part of your analysis, address the risks of using agents in this scenario 
  and suggest mitigations.
  * Submission Requirements
    * The report addresses the risks of using agents for this banking
      application, particularly loan approvals.
    * The report suggests possible ways to mitigate these risks.
  * Reviewer Tip
    * **Pass the requirement if** the report identifies at least two risks
      of using agents in this banking scenario and suggests a plausible
      mitigation for each. The biggest risks of this include 
      * LLM hallucinations not based on the state
      * Taking a human out of the decision making loop
      * Insufficient guardrails to prevent security issues
      * The non-deterministic nature of LLMs and the agents that are based 
        on them
    * **Fail the requirement if** the report does not address risks or the
      suggested mitigations are not well-thought-out. At least one of the 
      above risks should be included or the requirement fails.
    * **Praise the learner's work if** the risk analysis is thorough and
      the suggested mitigations are creative and practical.
    * **Praise the learner's work if** they identify the use of "thinking" 
      or "reasoning" models as potentially risky operations and point out 
      that this is why the custom agent is used to make the mathematical 
      calculation.
* Suggest further improvements to the system.
  * Submission Requirements
    * The report includes at least two distinct suggestions for further
      improvements to the system.
    * The suggestions are based on the evaluation of the system and the
      identified areas for improvement.
  * Reviewer Tip
    * **Pass the requirement if** the report includes at least two
      distinct and well-reasoned suggestions for improving the system.
    * **Fail the requirement if** the report does not include any
      suggestions for improvement.
    * **Praise the learner's work if** the suggestions are creative and
      show a deep understanding of the system and its potential.

### Suggestions To Make Your Project Stand Out

* Run the agents on different ports or machines.
  * Submission Requirements
    * The agent cards for the deposit, loan, and manager agents are
      updated to reflect the new locations.
    * The submission includes evidence that the agents are running on
      different ports or machines and can still communicate with each
      other.
  * Reviewer Tip
    * **Do not fail the project if** the student has not implemented any
      of these suggestions. These are optional enhancements.
    * **Praise the learner's work if** they have successfully deployed the
      agents to different ports or machines and demonstrated that they
      can still communicate with each other.
* Save loan applications to a database.
  * Submission Requirements
    * A new tool is created to save the loan application and the agent's
      decision to a database.
    * The loan approval sub-agent is updated to use this new tool.
    * The submission includes evidence that the loan applications are
      being saved to the database.
  * Reviewer Tip
    * **Praise the learner's work if** they have implemented a tool to
      save loan applications and can show evidence of this working
      correctly.
    * **Comment if** they do not use the MCP Database Toolbox to insert data 
      into the database in a controlled way.
* Create a loan manager agent to review applications.
  * Submission Requirements
    * A new agent is created for loan managers.
    * The agent has tools to review the loan applications saved in the
      database.
    * The submission includes evidence of the loan manager agent
      functioning correctly.
  * Reviewer Tip
    * **Praise the learner's work if** they have created a new agent for
      loan managers and can demonstrate its functionality. This shows a
      great understanding of how to extend the system.
* Expand test coverage.
  * Submission Requirements
    * Additional tests for other loan types and amounts are added to 
      `test_scenarios.csv`.
    * The report and analysis includes the results of these additional 
      tests.
    * Additional customer profiles are created and used for testing.
  * Reviewer Tip
    * **Praise the learner's work if** they have expanded the test 
      coverage with more test cases and/or customer profiles.
    * **Do not fail the project if** the student has not implemented any
      of these suggestions. These are optional enhancements.
