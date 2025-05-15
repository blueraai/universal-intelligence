"""Universal Agents - Basic Example

This example demonstrates how to create and run a simple flow with Universal Agents,
using a Universal Intelligence model.
"""

import logging
import sys
import os

# Add the repository root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from universal_agents.node import Node, Flow
from universal_agents.universal_integration import UniversalModelNode
from universal_intelligence.community.models.default import UniversalModel

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class InputNode(Node):
    """Node for processing user input."""
    
    def __init__(self, name=None):
        super().__init__(name or "InputNode")
        
    def prep(self, shared):
        """Get input from user or shared state."""
        if "input" in shared:
            return shared["input"]
        else:
            user_input = input("Enter your question: ")
            shared["input"] = user_input
            return user_input
            
    def post(self, shared, prep_data, exec_result):
        """Store input and proceed to next node."""
        shared["user_question"] = exec_result
        return "process"


class ProcessingNode(Node):
    """Node for enhancing or modifying the user input."""
    
    def __init__(self, name=None):
        super().__init__(name or "ProcessingNode")
        
    def prep(self, shared):
        """Get the user question from shared state."""
        return shared.get("user_question", "")
        
    def exec(self, prep_data):
        """Enhance the question with additional context."""
        # In a real application, this could rewrite the question,
        # add context, classify it, etc.
        if not prep_data.endswith("?"):
            return f"{prep_data}?"
        return prep_data
        
    def post(self, shared, prep_data, exec_result):
        """Store enhanced question and proceed to model."""
        shared["enhanced_question"] = exec_result
        return "generate"


class OutputNode(Node):
    """Node for formatting and displaying the model's output."""
    
    def __init__(self, name=None):
        super().__init__(name or "OutputNode")
        
    def prep(self, shared):
        """Get the model output from shared state."""
        return shared.get("model_output", "No response generated.")
        
    def exec(self, prep_data):
        """Format the output."""
        return f"\nAnswer: {prep_data}\n"
        
    def post(self, shared, prep_data, exec_result):
        """Display the output and store the final result."""
        print(exec_result)
        shared["result"] = exec_result
        
        if input("\nDo you want to ask another question? (y/n): ").lower() == 'y':
            shared.pop("input", None)
            shared.pop("user_question", None)
            shared.pop("enhanced_question", None)
            shared.pop("model_output", None)
            return "restart"
        
        return "complete"


def main():
    """Main function to run the example."""
    print("\nWelcome to Universal Agents Basic Example!\n")
    print("This example demonstrates a simple flow with an input node, processing node,")
    print("model node, and output node. The flow processes user questions and generates")
    print("answers using a Universal Intelligence model.\n")
    
    try:
        # Initialize a Universal Intelligence model
        model = UniversalModel()
        
        # Create nodes
        input_node = InputNode()
        processing_node = ProcessingNode()
        
        model_node = UniversalModelNode(
            model=model,
            prompt_template="""Please answer the following question concisely:
            
Question: {enhanced_question}

Answer:""",
            input_keys=["enhanced_question"],
            output_key="model_output"
        )
        
        output_node = OutputNode()
        
        # Connect nodes
        input_node - "process" >> processing_node
        processing_node - "generate" >> model_node
        model_node - "next" >> output_node
        output_node - "restart" >> input_node
        
        # Create flow
        flow = Flow(start=input_node, name="BasicQuestionAnswerFlow")
        
        # Initialize shared state
        shared = {}
        
        # Run the flow
        final_state = flow.run(shared)
        
        print("\nFlow completed successfully!")
        
    except Exception as e:
        logger.error(f"Error running example: {str(e)}")
        raise
        
    print("\nThank you for using Universal Agents!\n")


if __name__ == "__main__":
    main()