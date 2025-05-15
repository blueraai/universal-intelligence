"""Universal Agents - RAG Example

This example demonstrates how to create and run a RAG flow with Universal Agents,
using Universal Intelligence models and tools.
"""

import logging
import sys
import os
from typing import List, Dict, Any

# Add the repository root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from universal_agents.patterns import create_rag_flow
from universal_agents.node import Node, Flow
from universal_intelligence.community.models.default import UniversalModel

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class SimpleTool:
    """A simple mock tool for retrieval in this example."""
    
    def __init__(self):
        # Example documents about Universal Agents
        self.documents = [
            {
                "content": "Universal Agents is a port of PocketFlow's functionality utilizing Universal Intelligence (UIN). It enables you to build complex AI workflows using connected processing nodes while leveraging UIN's standardized components.",
                "source": "docs/guides/guide-universal-agents-usage-v1.0.0.md",
                "relevance": 0.95
            },
            {
                "content": "Nodes are the fundamental building blocks of a flow. Each node has three main methods: prep (prepares data for execution), exec (executes the core functionality), and post (processes results and determines the next action).",
                "source": "docs/specs/spec-universal-agents-v1.0.0.md",
                "relevance": 0.88
            },
            {
                "content": "Flows are directed graphs of connected nodes with shared state management. A Flow manages the execution of a graph of connected nodes, starting from a designated start node and following the connections between nodes based on the actions returned by each node's post method.",
                "source": "docs/specs/spec-universal-agents-v1.0.0.md",
                "relevance": 0.85
            },
            {
                "content": "Universal Agents integrates with UIN by providing specialized nodes: UniversalModelNode for using UIN models, UniversalToolNode for using UIN tools, and UniversalAgentNode for using UIN agents.",
                "source": "docs/analysis/analysis-universal-agents-implementation-v1.0.0.md",
                "relevance": 0.82
            },
            {
                "content": "Common design patterns implemented in Universal Agents include: RAG (Retrieval Augmented Generation), Map-Reduce, Multi-Agent Collaboration, and Workflow Orchestration.",
                "source": "docs/guides/guide-universal-agents-usage-v1.0.0.md",
                "relevance": 0.78
            }
        ]
    
    def contract(self):
        """Return the tool contract."""
        return {
            "name": "SimpleRetrievalTool",
            "description": "A simple tool for retrieving documents",
            "methods": [
                {
                    "name": "retrieve",
                    "description": "Retrieve documents based on a query",
                    "asynchronous": False,
                    "arguments": [
                        {
                            "name": "query",
                            "type": "str",
                            "description": "The search query",
                            "required": True
                        },
                        {
                            "name": "top_k",
                            "type": "int",
                            "description": "Number of results to return",
                            "required": False
                        }
                    ]
                }
            ]
        }
    
    def retrieve(self, query: str, top_k: int = 3) -> tuple[List[Dict[str, Any]], Dict[str, Any]]:
        """Retrieve documents based on a query.
        
        Args:
            query: The search query
            top_k: Number of results to return
            
        Returns:
            Tuple of (results, logs)
        """
        logger.info(f"Retrieving documents for query: {query}")
        
        # In a real implementation, this would search for documents
        # For this example, we'll just return some of our sample documents
        results = sorted(self.documents, key=lambda x: x["relevance"], reverse=True)[:top_k]
        
        return results, {"retrieved": len(results), "query": query}


class InputNode(Node):
    """Node for getting user input."""
    
    def __init__(self, name=None):
        super().__init__(name or "InputNode")
        
    def prep(self, shared):
        """Get input from user or shared state."""
        if "input" in shared:
            return shared["input"]
        else:
            user_input = input("\nEnter your question about Universal Agents: ")
            shared["input"] = user_input
            return user_input
            
    def post(self, shared, prep_data, exec_result):
        """Store input and proceed to RAG flow."""
        shared["query"] = exec_result
        shared["top_k"] = 3  # Set number of documents to retrieve
        return "rag"


class OutputNode(Node):
    """Node for displaying the final answer."""
    
    def __init__(self, name=None):
        super().__init__(name or "OutputNode")
        
    def prep(self, shared):
        """Get the answer from shared state."""
        return {
            "answer": shared.get("answer", "No answer generated."),
            "context": shared.get("context", ""),
            "document_count": shared.get("context_document_count", 0)
        }
        
    def post(self, shared, prep_data, exec_result):
        """Display the answer and prompt for another question."""
        result = exec_result
        
        print(f"\nAnswer: {result['answer']}")
        print(f"\n(Based on {result['document_count']} documents)")
        
        if input("\nDo you want to see the retrieved context? (y/n): ").lower() == 'y':
            print("\n--- Retrieved Context ---\n")
            print(result["context"])
            print("\n------------------------\n")
        
        if input("Do you want to ask another question? (y/n): ").lower() == 'y':
            # Clear relevant state for next question
            shared.pop("input", None)
            shared.pop("query", None)
            shared.pop("answer", None)
            shared.pop("context", None)
            return "restart"
        
        return "complete"


def main():
    """Main function to run the example."""
    print("\nWelcome to Universal Agents RAG Example!\n")
    print("This example demonstrates a RAG (Retrieval Augmented Generation) flow")
    print("that retrieves information about Universal Agents and generates answers")
    print("based on the retrieved context.\n")
    
    try:
        # Initialize a Universal Intelligence model
        model = UniversalModel()
        
        # Create a simple retrieval tool
        retrieval_tool = SimpleTool()
        
        # Create the input and output nodes
        input_node = InputNode()
        output_node = OutputNode()
        
        # Create the RAG flow
        rag_flow = create_rag_flow(
            retrieval_tool=retrieval_tool,
            retrieval_method="retrieve",
            generation_model=model,
            prompt_template="""Answer the following question about Universal Agents based on the provided context.
            
Context:
{context}

Question:
{query}

Answer:"""
        )
        
        # Create the main flow
        input_node - "rag" >> rag_flow.start
        
        # Connect the last node of the RAG flow to the output node
        # Find the output node of the RAG flow (the one with no outgoing connections)
        rag_output_node = None
        for node in rag_flow.nodes.values():
            if "complete" in node.connections:
                node.connections["complete"] = output_node
                rag_output_node = node
                break
                
        if not rag_output_node:
            # If no node with "complete" action, connect the last node in the path
            # This is a simplification; in a real application, you'd need a more robust approach
            for node_name in rag_flow.nodes:
                if node_name == "OutputNode":
                    rag_flow.nodes[node_name].connections["complete"] = output_node
                    break
        
        # Connect the output node back to the input node for multiple questions
        output_node - "restart" >> input_node
        
        # Create the main flow
        main_flow = Flow(start=input_node, name="RAGQuestionAnswerFlow")
        
        # Initialize shared state
        shared = {}
        
        # Run the flow
        final_state = main_flow.run(shared)
        
        print("\nFlow completed successfully!")
        
    except Exception as e:
        logger.error(f"Error running example: {str(e)}")
        raise
        
    print("\nThank you for using Universal Agents!\n")


if __name__ == "__main__":
    main()