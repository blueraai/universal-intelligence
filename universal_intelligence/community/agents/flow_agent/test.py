import argparse
import os
import sys

# Add parent directories to the path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, parent_dir)

from universal_intelligence.community.models.default import UniversalModel
from .agent import FlowUniversalAgent
from .nodes import Node
from .flow import Flow


class TextInput(Node):
    def prep(self, shared):
        """Get text input from shared state or request it."""
        if "text" not in shared:
            if "input" in shared:
                shared["text"] = shared["input"]
            else:
                shared["text"] = input("\nEnter text to convert: ")
        return shared["text"]

    def post(self, shared, prep_res, exec_res):
        print("\nChoose transformation:")
        print("1. Convert to UPPERCASE")
        print("2. Convert to lowercase")
        print("3. Reverse text")
        print("4. Remove extra spaces")
        print("5. Exit")
        
        choice = input("\nYour choice (1-5): ")
        
        if choice == "5":
            return "exit"
        
        shared["choice"] = choice
        return "transform"


class TextTransform(Node):
    def prep(self, shared):
        return shared["text"], shared["choice"]
    
    def exec(self, inputs):
        text, choice = inputs
        
        if choice == "1":
            return text.upper()
        elif choice == "2":
            return text.lower()
        elif choice == "3":
            return text[::-1]
        elif choice == "4":
            return " ".join(text.split())
        else:
            return "Invalid option!"
    
    def post(self, shared, prep_res, exec_res):
        print("\nResult:", exec_res)
        shared["result"] = exec_res
        
        if input("\nConvert another text? (y/n): ").lower() == 'y':
            shared.pop("text", None)  # Remove previous text
            return "input"
        return "exit"


class EndNode(Node):
    def post(self, shared, prep_res, exec_res):
        print("\nThank you for using Text Converter!")
        return None


def main():
    # Parse arguments
    parser = argparse.ArgumentParser(description='Test the Flow-based Universal Agent')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose output')
    args = parser.parse_args()
    
    # Create the agent with a model
    model = UniversalModel()
    agent = FlowUniversalAgent(model=model, verbose=args.verbose)
    
    # Create nodes
    text_input = TextInput(name="input")
    text_transform = TextTransform(name="transform")
    end_node = EndNode(name="end")
    
    # Connect nodes
    text_input - "transform" >> text_transform
    text_transform - "input" >> text_input
    text_transform - "exit" >> end_node
    
    # Create flow
    flow = agent.create_flow(start=text_input)
    
    print("\nWelcome to Text Converter!")
    print("=========================")
    
    # Initialize shared store and run the flow
    shared = {}
    
    # Process with the flow
    result, logs = agent.process(
        input="Hello, world!",
        flow=flow,
        shared_state=shared
    )
    
    print("\nFinal result:", result)
    return 0


if __name__ == "__main__":
    sys.exit(main())