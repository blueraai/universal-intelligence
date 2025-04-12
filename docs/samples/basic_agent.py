"""
Basic Agent Example

This example demonstrates the simplest usage of Universal Intelligence:
- Creating a model
- Creating an agent powered by the model
- Processing a simple request
"""

from universal_intelligence import Model, Agent

# Initialize a simple model
# Universal Intelligence automatically selects the optimal configuration for your hardware
model = Model()

# Create an agent powered by the model
agent = Agent(universal_model=model)

# Process a simple request
result, logs = agent.process("What is machine learning?")

# Print the model's response
print("\n=== Model Response ===")
print(result)

# The logs contain metadata about the processing
print("\n=== Processing Logs ===")
print(f"Engine used: {logs.get('engine')}")
print(f"Quantization: {logs.get('quantization')}")

"""
Sample output:

=== Model Response ===
Machine learning is a branch of artificial intelligence that focuses on developing systems
that can learn from and make decisions based on data. Instead of being explicitly programmed
to perform a task, these systems are trained using large amounts of data and algorithms that
give them the ability to learn how to perform tasks on their own.

The process involves feeding the system data, allowing it to identify patterns, and then
enabling it to make decisions with minimal human intervention. Common applications include
image recognition, speech recognition, recommendation systems, and predictive analytics.

=== Processing Logs ===
Engine used: transformers
Quantization: BNB_4
"""
