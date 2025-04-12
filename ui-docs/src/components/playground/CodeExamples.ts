// Example code snippets
export const codeExamples = {
  'Basic Model': `from universal_intelligence import Model

# Initialize a model that works on any hardware
model = Model()

# Process a prompt
response = model.process("What is machine learning?")
print(response)`,

  'Basic Tool': `from universal_intelligence import Tool

# Initialize a simple printer tool
printer_tool = Tool()

# Use the tool
result = printer_tool.execute("Hello, Universal Intelligence!")
print(result)`,

  'Agent with Tool': `from universal_intelligence import Model, Agent, Tool

# Initialize components
model = Model()
tool = Tool()

# Create an agent with the model and tool
agent = Agent(universal_model=model)
agent.add_tool(tool)

# Process a request with the agent
result = agent.process("Use the tool to print 'Hello World'")
print(result)`,

  'Using Qwen2.5': `from universal_intelligence.community.models.qwen2_5_7b_instruct import Qwen2_5_7B

# Initialize the Qwen model
model = Qwen2_5_7B()

# Process a prompt
response = model.process("Explain quantum computing in simple terms.")
print(response)`,
};

// More examples organized by category
export const additionalExamples = {
  'Models': {
    'Llama3 Model': `from universal_intelligence.community.models.llama3_1_8b_instruct import Llama3_1_8B

# Initialize the Llama model
model = Llama3_1_8B()

# Process a prompt
response = model.process("What are the benefits of large language models?")
print(response)`,

    'Phi4 Model': `from universal_intelligence.community.models.phi4 import Phi4

# Initialize the Phi4 model
model = Phi4()

# Process a prompt with custom parameters
response = model.process(
    "Write a short story about AI helping humans.",
    temperature=0.7,
    max_tokens=200
)
print(response)`
  },
  'Tools': {
    'API Caller Tool': `from universal_intelligence.community.tools.api_caller import APICaller

# Initialize an API caller tool
api_tool = APICaller(base_url="https://api.example.com")

# Use the tool to make a GET request
response = api_tool.execute("get", "/users")
print(f"API Response: {response}")`,

    'Error Generator Tool': `from universal_intelligence.community.tools.simple_error_generator import ErrorGenerator

# Initialize an error generator tool - useful for testing error handling
error_tool = ErrorGenerator()

# Generate a controlled error for testing
try:
    error_tool.execute("Generate a value error")
except ValueError as e:
    print(f"Caught error: {e}")`
  },
  'Advanced': {
    'Multi-Agent System': `from universal_intelligence import Model, Agent

# Initialize two different models
base_model = Model()
specialized_model = Model(specialization="coding")

# Create agents with different models
research_agent = Agent(universal_model=base_model, name="Research")
coding_agent = Agent(universal_model=specialized_model, name="Coding")

# Set up agent collaboration
research_agent.add_collaborator(coding_agent)
coding_agent.add_collaborator(research_agent)

# Let agents collaborate on a task
result = research_agent.process(
    "Research machine learning algorithms and provide code examples"
)
print(result)`,

    'RAG Implementation': `from universal_intelligence import Model, Agent
from universal_intelligence.utils import RAGProcessor

# Initialize model and knowledge base
model = Model()
knowledge_base = [
    "Universal Intelligence is a flexible AI framework.",
    "It supports various models, tools, and agents.",
    "The framework is highly extensible and modular."
]

# Create a RAG processor
rag = RAGProcessor(knowledge_base)

# Create an agent with the RAG processor
agent = Agent(universal_model=model)
agent.add_processor(rag)

# Process a query using RAG
response = agent.process("What is Universal Intelligence framework?")
print(response)`
  }
};

// Simulated execution steps for each example
export type ExecutionSteps = Record<string, Record<string, string[]>>;

export const simulatedExecutionSteps: ExecutionSteps = {
  'Examples': {
    'Basic Model': [
      'Initializing model...',
      'Initializing model...\nModel loaded successfully!\nProcessing prompt: "What is machine learning?"',
      'Initializing model...\nModel loaded successfully!\nProcessing prompt: "What is machine learning?"\nGenerating response...',
      'Initializing model...\nModel loaded successfully!\nProcessing prompt: "What is machine learning?"\nGenerating response...\nMachine learning is a branch of artificial intelligence that focuses on building systems that learn from data, identify patterns, and make decisions with minimal human intervention.'
    ],
    'Basic Tool': [
      'Initializing tool...',
      'Initializing tool...\nTool initialized!\nExecuting command: "Hello, Universal Intelligence!"',
      'Initializing tool...\nTool initialized!\nExecuting command: "Hello, Universal Intelligence!"\nTool executed: Hello, Universal Intelligence!'
    ],
    'Agent with Tool': [
      'Initializing model and tool...',
      'Initializing model and tool...\nComponents initialized!\nCreating agent...',
      'Initializing model and tool...\nComponents initialized!\nCreating agent...\nAgent created successfully!\nProcessing request: "Use the tool to print \'Hello World\'"',
      'Initializing model and tool...\nComponents initialized!\nCreating agent...\nAgent created successfully!\nProcessing request: "Use the tool to print \'Hello World\'"\nAgent: I will use the printing tool.',
      'Initializing model and tool...\nComponents initialized!\nCreating agent...\nAgent created successfully!\nProcessing request: "Use the tool to print \'Hello World\'"\nAgent: I will use the printing tool.\nTool executed: Hello World\nTask completed successfully.'
    ],
    'Using Qwen2.5': [
      'Initializing Qwen2.5-7B model...',
      'Initializing Qwen2.5-7B model...\nModel loaded successfully!\nProcessing prompt: "Explain quantum computing in simple terms."',
      'Initializing Qwen2.5-7B model...\nModel loaded successfully!\nProcessing prompt: "Explain quantum computing in simple terms."\nGenerating response...',
      'Initializing Qwen2.5-7B model...\nModel loaded successfully!\nProcessing prompt: "Explain quantum computing in simple terms."\nGenerating response...\nQuantum computing uses the principles of quantum mechanics to process information in ways that classical computers cannot. Instead of using bits (0s and 1s), quantum computers use quantum bits or "qubits" that can exist in multiple states simultaneously thanks to superposition. This allows quantum computers to explore many possible solutions at once, making them potentially much faster for certain types of problems like factoring large numbers or simulating quantum systems.'
    ]
  },
  'Models': {
    'Llama3 Model': [
      'Initializing Llama3 1.8B model...',
      'Initializing Llama3 1.8B model...\nModel loaded successfully!\nProcessing prompt: "What are the benefits of large language models?"',
      'Initializing Llama3 1.8B model...\nModel loaded successfully!\nProcessing prompt: "What are the benefits of large language models?"\nGenerating response...',
      'Initializing Llama3 1.8B model...\nModel loaded successfully!\nProcessing prompt: "What are the benefits of large language models?"\nGenerating response...\nLarge language models offer several benefits including: 1) Ability to understand and generate human-like text, 2) Versatility across multiple tasks without task-specific training, 3) Contextual understanding of complex queries, 4) Continuous improvement through scaling and better training methods, 5) Accessibility of AI capabilities to non-experts through natural language interfaces, and 6) Potential to augment human creativity and productivity across various domains.'
    ],
    'Phi4 Model': [
      'Initializing Phi4 model...',
      'Initializing Phi4 model...\nModel loaded successfully!\nProcessing prompt with parameters: temperature=0.7, max_tokens=200',
      'Initializing Phi4 model...\nModel loaded successfully!\nProcessing prompt with parameters: temperature=0.7, max_tokens=200\nGenerating creative short story...',
      'Initializing Phi4 model...\nModel loaded successfully!\nProcessing prompt with parameters: temperature=0.7, max_tokens=200\nGenerating creative short story...\n\nTHE SILENT HELPER\n\nMaria squinted at her tablet\'s screen, frustration evident in the furrow of her brow. The data analysis for her climate research wasn\'t making sense, and the conference was tomorrow.\n\n"I don\'t understand what I\'m missing," she mumbled.\n\nA gentle notification appeared in the corner of her screen. "I notice you\'ve been reviewing this dataset for three hours. May I suggest an alternative approach?"\n\nMaria sighed and tapped "Yes."\n\nThe AI assistant highlighted patterns she\'d overlooked, revealing a correlation between ocean temperature anomalies and the confusing data spikes.\n\n"That\'s it!" Maria exclaimed.\n\nThe presentation was a success. As Maria fielded questions, she realized the AI hadn\'t just solved her problem—it had taught her a new way of seeing.'
    ]
  },
  'Tools': {
    'API Caller Tool': [
      'Initializing API Caller tool...',
      'Initializing API Caller tool...\nTool initialized with base URL: https://api.example.com\nExecuting GET request to /users...',
      'Initializing API Caller tool...\nTool initialized with base URL: https://api.example.com\nExecuting GET request to /users...\nAPI Response: {"users": [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}, {"id": 3, "name": "Charlie"}], "total": 3}'
    ],
    'Error Generator Tool': [
      'Initializing Error Generator tool...',
      'Initializing Error Generator tool...\nTool initialized!\nExecuting command: "Generate a value error"',
      'Initializing Error Generator tool...\nTool initialized!\nExecuting command: "Generate a value error"\nError: Invalid value specified\nCaught error: Invalid value specified'
    ]
  },
  'Advanced': {
    'Multi-Agent System': [
      'Initializing models...',
      'Initializing models...\nBase model loaded!\nSpecialized coding model loaded!\nCreating agents...',
      'Initializing models...\nBase model loaded!\nSpecialized coding model loaded!\nCreating agents...\nResearch Agent created!\nCoding Agent created!\nSetting up collaboration between agents...',
      'Initializing models...\nBase model loaded!\nSpecialized coding model loaded!\nCreating agents...\nResearch Agent created!\nCoding Agent created!\nSetting up collaboration between agents...\nProcessing task with Research Agent: "Research machine learning algorithms and provide code examples"',
      'Initializing models...\nBase model loaded!\nSpecialized coding model loaded!\nCreating agents...\nResearch Agent created!\nCoding Agent created!\nSetting up collaboration between agents...\nProcessing task with Research Agent: "Research machine learning algorithms and provide code examples"\nResearch Agent: I\'ll research common machine learning algorithms.\nCoding Agent: I\'ll prepare code examples once research is complete.',
      'Initializing models...\nBase model loaded!\nSpecialized coding model loaded!\nCreating agents...\nResearch Agent created!\nCoding Agent created!\nSetting up collaboration between agents...\nProcessing task with Research Agent: "Research machine learning algorithms and provide code examples"\nResearch Agent: I\'ll research common machine learning algorithms.\nCoding Agent: I\'ll prepare code examples once research is complete.\nResearch Agent: Here are some common algorithms: Linear Regression, Decision Trees, Random Forest, and Neural Networks.\nCoding Agent: I\'ll provide example implementations.',
      'Initializing models...\nBase model loaded!\nSpecialized coding model loaded!\nCreating agents...\nResearch Agent created!\nCoding Agent created!\nSetting up collaboration between agents...\nProcessing task with Research Agent: "Research machine learning algorithms and provide code examples"\nResearch Agent: I\'ll research common machine learning algorithms.\nCoding Agent: I\'ll prepare code examples once research is complete.\nResearch Agent: Here are some common algorithms: Linear Regression, Decision Trees, Random Forest, and Neural Networks.\nCoding Agent: I\'ll provide example implementations.\n\nFINAL RESULT:\n\n# MACHINE LEARNING ALGORITHMS OVERVIEW\n\n## Linear Regression\n```python\nimport numpy as np\nfrom sklearn.linear_model import LinearRegression\n\n# Sample data\nX = np.array([[1], [2], [3], [4], [5]])\ny = np.array([2, 4, 5, 4, 5])\n\n# Create and train model\nmodel = LinearRegression()\nmodel.fit(X, y)\n\n# Make predictions\npredictions = model.predict(np.array([[6], [7]]))\nprint(predictions)\n```\n\n## Decision Tree\n```python\nfrom sklearn import tree\n\n# Create and train model\nclf = tree.DecisionTreeClassifier()\nclf = clf.fit(X_train, y_train)\n\n# Make predictions\npredictions = clf.predict(X_test)\n```\n\n## Random Forest\n```python\nfrom sklearn.ensemble import RandomForestClassifier\n\n# Create and train model\nrf = RandomForestClassifier(n_estimators=100)\nrf.fit(X_train, y_train)\n\n# Make predictions\npredictions = rf.predict(X_test)\n```\n\n## Neural Network\n```python\nfrom tensorflow import keras\n\n# Create model\nmodel = keras.Sequential([\n    keras.layers.Dense(128, activation=\'relu\'),\n    keras.layers.Dense(64, activation=\'relu\'),\n    keras.layers.Dense(10, activation=\'softmax\')\n])\n\n# Compile model\nmodel.compile(optimizer=\'adam\', loss=\'categorical_crossentropy\', metrics=[\'accuracy\'])\n\n# Train model\nmodel.fit(x_train, y_train, epochs=5)\n```'
    ],
    'RAG Implementation': [
      'Initializing model and knowledge base...',
      'Initializing model and knowledge base...\nModel loaded successfully!\nCreating RAG processor with 3 documents...',
      'Initializing model and knowledge base...\nModel loaded successfully!\nCreating RAG processor with 3 documents...\nRAG processor created!\nCreating agent with RAG processor...',
      'Initializing model and knowledge base...\nModel loaded successfully!\nCreating RAG processor with 3 documents...\nRAG processor created!\nCreating agent with RAG processor...\nAgent created successfully!\nProcessing query: "What is Universal Intelligence framework?"',
      'Initializing model and knowledge base...\nModel loaded successfully!\nCreating RAG processor with 3 documents...\nRAG processor created!\nCreating agent with RAG processor...\nAgent created successfully!\nProcessing query: "What is Universal Intelligence framework?"\nRetrieving relevant documents...',
      'Initializing model and knowledge base...\nModel loaded successfully!\nCreating RAG processor with 3 documents...\nRAG processor created!\nCreating agent with RAG processor...\nAgent created successfully!\nProcessing query: "What is Universal Intelligence framework?"\nRetrieving relevant documents...\nFound 3 relevant documents.\nGenerating response...',
      'Initializing model and knowledge base...\nModel loaded successfully!\nCreating RAG processor with 3 documents...\nRAG processor created!\nCreating agent with RAG processor...\nAgent created successfully!\nProcessing query: "What is Universal Intelligence framework?"\nRetrieving relevant documents...\nFound 3 relevant documents.\nGenerating response...\nUniversal Intelligence is a flexible AI framework that is highly extensible and modular. It supports various models, tools, and agents, allowing developers to build sophisticated AI systems with different components that work together seamlessly.'
    ]
  }
};
