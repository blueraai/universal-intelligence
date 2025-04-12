"""
Tool-Using Agent Example

This example demonstrates how agents can use tools:
- Creating a model
- Creating a printer tool
- Creating an agent with access to the tool
- Processing a request that leverages the tool
"""

from universal_intelligence import Model, Tool, Agent

# Initialize a simple model
model = Model()

# Create a printer tool (the default tool is SimplePrinter)
# This tool will allow the agent to print text to the console
printer_tool = Tool()

# Create an agent with access to the printer tool
agent = Agent(
    universal_model=model,
    expand_tools=[printer_tool]
)

# Process a request that will need to use the tool
result, logs = agent.process("Please print 'Hello, Universal Intelligence!' to the console")

# Print the agent's response
print("\n=== Agent Response ===")
print(result)

# Print the logs to see tool interactions
print("\n=== Processing Logs ===")
print(f"Number of tool calls: {len(logs.get('tool_calls', []))}")

"""
Sample output:

=== Agent Response ===
I've printed 'Hello, Universal Intelligence!' to the console for you.

=== Processing Logs ===
Number of tool calls: 1

(In the console, you would also see:)
Hello, Universal Intelligence!
"""

# Example with multiple tools
from universal_intelligence.community.tools.api_caller import UniversalTool as APICaller

# Create an API caller tool with a configuration
api_tool = APICaller(configuration={
    "base_url": "https://api.example.com",
    "default_headers": {"Content-Type": "application/json"}
})

# Create an agent with multiple tools
multi_tool_agent = Agent(
    universal_model=model,
    expand_tools=[printer_tool, api_tool]
)

# The agent can now use both tools as needed based on the request
print("\n=== Multi-tool Agent ===")
print("Agent now has access to both a printer tool and an API caller tool")
print("It will automatically select the appropriate tool based on the request")
