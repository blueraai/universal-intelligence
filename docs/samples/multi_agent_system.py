"""
Multi-Agent System Example

This example demonstrates how to create a system of multiple agents:
- Creating a shared model for efficiency
- Creating specialized agents for specific tasks
- Connecting agents to form a team
- Processing a complex request that requires collaboration
"""

from universal_intelligence import Model, Agent

# Initialize a shared model for efficiency
# By sharing the model, we reduce memory usage and increase performance
shared_model = Model()

# Create specialized agents with different roles
primary_agent = Agent(universal_model=shared_model)
research_agent = Agent(universal_model=shared_model)
fact_checker_agent = Agent(universal_model=shared_model)

# Connect agents to form a team
# This allows the primary agent to delegate tasks to other agents
primary_agent.connect(universal_agents=[research_agent, fact_checker_agent])

print("=== Multi-Agent System Configuration ===")
print("Primary Agent: Coordinates tasks and integrates results")
print("Research Agent: Performs in-depth research on topics")
print("Fact Checker Agent: Verifies information for accuracy")
print("\nNote: All agents share the same model for memory efficiency")

# Process a complex request using the team
# The primary agent will delegate research and fact-checking as needed
result, logs = primary_agent.process(
    "Research the impacts of AI on healthcare and verify the key facts"
)

print("\n=== Multi-Agent Response ===")
print(result)

print("\n=== Agent Collaboration Logs ===")
agent_calls = logs.get('agent_calls', [])
print(f"Number of agent-to-agent calls: {len(agent_calls)}")
for i, call in enumerate(agent_calls):
    print(f"\nCall {i+1}:")
    print(f"  From: {call.get('from', 'Primary')}")
    print(f"  To: {call.get('to', 'Unknown')}")
    print(f"  Task: {call.get('task', 'Unknown')[:50]}...")

"""
Sample output:

=== Agent Collaboration Logs ===
Number of agent-to-agent calls: 2

Call 1:
  From: Primary
  To: Research
  Task: Find detailed information about AI applications in...

Call 2:
  From: Primary
  To: FactChecker
  Task: Verify these key facts about AI in healthcare...
"""

# Dynamic agent connection example
print("\n=== Dynamic Team Formation ===")

# Create a new specialized agent
summarization_agent = Agent(universal_model=shared_model)
print("Created a new Summarization Agent")

# Connect it to the primary agent at runtime
primary_agent.connect(universal_agents=[summarization_agent])
print("Added Summarization Agent to the team")

# The primary agent can now also delegate summarization tasks
print("The primary agent can now delegate summarization tasks")

# Example of using extra_team for one-time collaboration
analysis_agent = Agent(universal_model=shared_model)
print("\n=== Temporary Collaboration ===")
print("Created an Analysis Agent for one-time use")

result, logs = primary_agent.process(
    "Analyze the economic impact of AI in healthcare",
    extra_team=[analysis_agent]
)
print("Temporary collaboration complete")
print("The Analysis Agent is not permanently added to the team")
