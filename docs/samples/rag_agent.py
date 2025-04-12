"""
RAG (Retrieval-Augmented Generation) Agent Example

This example demonstrates how to create a RAG-capable agent:
- Creating a model and tools
- Providing context documents to the model
- Processing a query that utilizes the provided context
"""

from universal_intelligence import Model, Tool, Agent

# Initialize components
model = Model()
api_tool = Tool(configuration={"base_url": "https://api.example.com"})

# Create a RAG-capable agent
# Any Universal Agent can function as a RAG agent by providing context
rag_agent = Agent(
    universal_model=model,
    expand_tools=[api_tool]
)

# Sample documents that might come from a vector database
documents = [
    "AI has revolutionized healthcare with early diagnosis systems. A study by Stanford Medicine showed " +
    "that deep learning models achieved 92% accuracy in detecting pneumonia from chest X-rays, " +
    "outperforming radiologists in some cases.",

    "Machine learning models can predict patient outcomes with increasing accuracy. Recent research " +
    "published in Nature Medicine demonstrated how ML algorithms reduced hospital readmission rates " +
    "by 25% by identifying high-risk patients.",

    "AI-powered surgical robots have improved precision in minimally invasive procedures. The da Vinci " +
    "Surgical System has been used in over 7 million procedures worldwide, with studies showing reduced " +
    "recovery times and decreased post-operative complications."
]

print("=== RAG Agent Configuration ===")
print("Agent is provided with specific context documents about AI in healthcare")
print(f"Number of context documents: {len(documents)}")

# Process a query using the provided context
# The context is passed to the agent's process method
result, logs = rag_agent.process(
    "How has AI impacted healthcare outcomes and what statistics support this?",
    context=documents  # This is the key parameter that enables RAG functionality
)

print("\n=== RAG Agent Response ===")
print(result)

print("\n=== Context Utilization ===")
print("The agent's response is grounded in the specific information provided in the context")
print("Without the context, the response would be more general and might lack the specific statistics")

# Advanced RAG example with dynamic context retrieval
print("\n=== Advanced RAG with Dynamic Context ===")

# In a real application, you might retrieve documents from a database
def retrieve_relevant_documents(query):
    """Simulate retrieving documents from a vector database based on query similarity."""
    print(f"Retrieving documents relevant to: {query}")
    # In a real system, this would query a vector database
    return documents

# Process a query with dynamically retrieved context
query = "What is the impact of AI on surgical procedures?"
retrieved_docs = retrieve_relevant_documents(query)
print(f"Retrieved {len(retrieved_docs)} relevant documents")

result, logs = rag_agent.process(
    query,
    context=retrieved_docs
)

print("\n=== Response with Dynamically Retrieved Context ===")
print(result)

"""
Sample output:

=== RAG Agent Response ===
Based on the provided information, AI has significantly impacted healthcare outcomes in several key areas:

1. Early Diagnosis:
   - Stanford Medicine research showed deep learning models achieved 92% accuracy in detecting pneumonia from chest X-rays
   - These AI systems outperformed radiologists in some cases

2. Patient Outcome Prediction:
   - Machine learning algorithms have demonstrated a 25% reduction in hospital readmission rates
   - This was achieved by identifying high-risk patients, as reported in Nature Medicine

3. Surgical Precision:
   - AI-powered surgical robots like the da Vinci Surgical System have improved precision in minimally invasive procedures
   - The system has been used in over 7 million procedures worldwide
   - Studies show these procedures result in reduced recovery times and decreased post-operative complications

These statistics demonstrate that AI is making measurable improvements in healthcare outcomes across diagnosis, prognosis, and treatment domains.
"""
