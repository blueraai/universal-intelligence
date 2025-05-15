"""Universal Agents - Workflow Pattern Implementation

This module provides a ready-to-use implementation of the Workflow pattern
using Universal Agents. The Workflow pattern enables complex, conditional flows
with decision points, parallel execution paths, and dynamic routing.
"""
import logging
from typing import Any, Dict, List, Optional, Union, Callable, TypeVar, Generic, Tuple, Set
from ..node import Node, Flow
from ..universal_integration import UniversalModelNode, UniversalToolNode, UniversalAgentNode
from universal_intelligence.core.universal_model import AbstractUniversalModel
from universal_intelligence.core.universal_tool import AbstractUniversalTool

logger = logging.getLogger(__name__)
T = TypeVar('T')

class DecisionNode(Node):
    """Node that makes decisions about workflow branching.
    
    The DecisionNode evaluates conditions to determine which path in a workflow
    should be taken, enabling conditional branching and complex flows.
    """
    
    def __init__(self, 
                 decision_fn: Callable[[Dict[str, Any]], str],
                 conditions: Dict[str, str],
                 default_action: str = "default",
                 name: Optional[str] = None):
        """Initialize a DecisionNode.
        
        Args:
            decision_fn: Function that evaluates shared state and returns a condition key
            conditions: Mapping from condition keys to actions
            default_action: Action to take if condition is not found in mapping
            name: Optional name for the node
        """
        super().__init__(name=name)
        self.decision_fn = decision_fn
        self.conditions = conditions
        self.default_action = default_action
    
    def prep(self, shared: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare data for decision making.
        
        Args:
            shared: Shared state dictionary
            
        Returns:
            Shared state for decision making
        """
        return shared
    
    def exec(self, prep_data: Dict[str, Any]) -> str:
        """Execute the decision function.
        
        Args:
            prep_data: Shared state
            
        Returns:
            Decision condition key
        """
        return self.decision_fn(prep_data)
    
    def post(self, shared: Dict[str, Any], prep_data: Dict[str, Any], exec_result: str) -> str:
        """Determine the next action based on the decision result.
        
        Args:
            shared: Shared state dictionary
            prep_data: Original shared state
            exec_result: Decision result
            
        Returns:
            Next action to take
        """
        # Map the decision result to an action
        action = self.conditions.get(exec_result, self.default_action)
        logger.info(f"Decision node '{self.name}' chose action '{action}' based on condition '{exec_result}'")
        return action


class ModelDecisionNode(Node):
    """Node that uses an LLM to make decisions about workflow branching.
    
    The ModelDecisionNode uses a Universal Intelligence model to evaluate
    a prompt and determine which path in a workflow should be taken.
    """
    
    def __init__(self, 
                 model: AbstractUniversalModel,
                 prompt_template: str,
                 options: List[str],
                 input_keys: Optional[List[str]] = None,
                 output_key: Optional[str] = None,
                 model_parameters: Optional[Dict[str, Any]] = None,
                 name: Optional[str] = None):
        """Initialize a ModelDecisionNode.
        
        Args:
            model: Universal Intelligence model to use
            prompt_template: Template for decision prompt
            options: List of valid decision options
            input_keys: Keys in shared state to include in prompt
            output_key: Optional key to store decision in shared state
            model_parameters: Optional parameters for the model
            name: Optional name for the node
        """
        super().__init__(name=name)
        self.model = model
        self.prompt_template = prompt_template
        self.options = options
        self.input_keys = input_keys or []
        self.output_key = output_key
        self.model_parameters = model_parameters or {}
    
    def prep(self, shared: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare the prompt for the model.
        
        Args:
            shared: Shared state dictionary
            
        Returns:
            Prepared prompt and context
        """
        # Extract the values for the input keys
        context = {}
        for key in self.input_keys:
            if key in shared:
                context[key] = shared[key]
            else:
                logger.warning(f"Input key '{key}' not found in shared state")
                context[key] = None
        
        # Format the options for the prompt
        options_text = "\n".join([f"- {option}" for option in self.options])
        context["options"] = options_text
        
        # Format the prompt
        prompt = self.prompt_template.format(**context)
        
        return {
            "prompt": prompt,
            "context": context
        }
    
    def exec(self, prep_data: Dict[str, Any]) -> str:
        """Execute the model to make a decision.
        
        Args:
            prep_data: Prepared data
            
        Returns:
            Model decision
        """
        # Generate a response from the model
        response = self.model.generate(prep_data["prompt"], **self.model_parameters)
        
        # Extract the decision from the response
        # This is a simple implementation - in a real app, you would want
        # more robust parsing or structured output
        for option in self.options:
            if option.lower() in response.lower():
                return option
        
        # If no option was found, log a warning and return the first option
        logger.warning(f"Model decision did not match any option. Response: {response[:100]}...")
        return self.options[0]
    
    def post(self, shared: Dict[str, Any], prep_data: Dict[str, Any], exec_result: str) -> str:
        """Store the decision and determine the next action.
        
        Args:
            shared: Shared state dictionary
            prep_data: Prepared data
            exec_result: Model decision
            
        Returns:
            Next action to take
        """
        # Store the decision in shared state if output_key is specified
        if self.output_key:
            shared[self.output_key] = exec_result
        
        # Return the decision as the action
        logger.info(f"Model decision node '{self.name}' chose action '{exec_result}'")
        return exec_result


class ParallelNode(Node):
    """Node that executes multiple flows in parallel and aggregates results.
    
    The ParallelNode allows for concurrent execution of different paths in a workflow,
    gathering results from all paths before proceeding.
    """
    
    def __init__(self, 
                 flows: Dict[str, Flow],
                 aggregator_fn: Optional[Callable[[Dict[str, Dict[str, Any]]], Dict[str, Any]]] = None,
                 input_key: Optional[str] = None,
                 output_key: str = "parallel_results",
                 name: Optional[str] = None):
        """Initialize a ParallelNode.
        
        Args:
            flows: Dictionary mapping names to flows
            aggregator_fn: Optional function to aggregate results
            input_key: Optional key for input to copy to all flows
            output_key: Key to store aggregated results
            name: Optional name for the node
        """
        super().__init__(name=name)
        self.flows = flows
        self.aggregator_fn = aggregator_fn
        self.input_key = input_key
        self.output_key = output_key
    
    def prep(self, shared: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare data for parallel execution.
        
        Args:
            shared: Shared state dictionary
            
        Returns:
            Prepared data for each flow
        """
        # Create a copy of the shared state for each flow
        flow_data = {}
        for flow_name in self.flows:
            # If input_key is specified, only copy that value
            if self.input_key and self.input_key in shared:
                flow_data[flow_name] = {"input": shared[self.input_key]}
            else:
                # Otherwise copy the entire shared state
                flow_data[flow_name] = shared.copy()
        
        return flow_data
    
    def exec(self, prep_data: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        """Execute all flows in parallel.
        
        Args:
            prep_data: Prepared data for each flow
            
        Returns:
            Results from each flow
        """
        # Execute each flow with its prepared data
        results = {}
        for flow_name, flow_shared in prep_data.items():
            flow = self.flows[flow_name]
            logger.info(f"Executing parallel flow '{flow_name}'")
            try:
                results[flow_name] = flow.run(shared=flow_shared)
            except Exception as e:
                logger.error(f"Error executing flow '{flow_name}': {str(e)}")
                results[flow_name] = {"error": str(e)}
        
        return results
    
    def post(self, shared: Dict[str, Any], prep_data: Dict[str, Dict[str, Any]], 
             exec_result: Dict[str, Dict[str, Any]]) -> str:
        """Aggregate results and store in shared state.
        
        Args:
            shared: Shared state dictionary
            prep_data: Prepared data
            exec_result: Results from each flow
            
        Returns:
            Next action to take
        """
        # Aggregate results if aggregator function is provided
        if self.aggregator_fn:
            aggregated = self.aggregator_fn(exec_result)
            shared[self.output_key] = aggregated
        else:
            # Otherwise store the raw results
            shared[self.output_key] = exec_result
        
        return "next"


class SequentialWorkflowNode(Node):
    """Node that executes a sequence of nodes before continuing.
    
    The SequentialWorkflowNode allows for defining a linear sub-workflow
    that executes completely before continuing to the next node.
    """
    
    def __init__(self, 
                 nodes: List[Node],
                 input_key: Optional[str] = None,
                 output_key: Optional[str] = None,
                 name: Optional[str] = None):
        """Initialize a SequentialWorkflowNode.
        
        Args:
            nodes: List of nodes to execute in sequence
            input_key: Optional key for input to pass to first node
            output_key: Optional key to store result from last node
            name: Optional name for the node
        """
        super().__init__(name=name)
        self.nodes = nodes
        self.input_key = input_key
        self.output_key = output_key
        
        # Connect the nodes in sequence
        for i in range(len(nodes) - 1):
            nodes[i] - "next" >> nodes[i + 1]
    
    def prep(self, shared: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare data for sequential execution.
        
        Args:
            shared: Shared state dictionary
            
        Returns:
            Prepared data
        """
        # Create a copy of shared state for the sequential workflow
        workflow_shared = shared.copy()
        
        # If input_key is specified, store the value separately
        if self.input_key and self.input_key in shared:
            return {
                "shared": workflow_shared,
                "input": shared[self.input_key]
            }
        
        return {"shared": workflow_shared}
    
    def exec(self, prep_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute nodes in sequence.
        
        Args:
            prep_data: Prepared data
            
        Returns:
            Result of sequential execution
        """
        workflow_shared = prep_data["shared"]
        
        # Start with the first node
        current_node = self.nodes[0]
        result = None
        
        # Execute each node in sequence
        while current_node:
            # Prepare the node
            node_prep_data = current_node.prep(workflow_shared)
            
            # Execute the node
            node_exec_result = current_node.exec(node_prep_data)
            
            # Post-process and get next action
            action = current_node.post(workflow_shared, node_prep_data, node_exec_result)
            
            # Store the result of the last node
            if current_node == self.nodes[-1]:
                result = node_exec_result
            
            # Find the next node based on the action
            next_node = None
            if action == "next" and current_node != self.nodes[-1]:
                # Move to the next node in the sequence
                next_index = self.nodes.index(current_node) + 1
                if next_index < len(self.nodes):
                    next_node = self.nodes[next_index]
            else:
                # If action isn't "next" or we're at the end, stop
                break
            
            current_node = next_node
        
        return {
            "shared": workflow_shared,
            "result": result
        }
    
    def post(self, shared: Dict[str, Any], prep_data: Dict[str, Any], 
             exec_result: Dict[str, Any]) -> str:
        """Update shared state with results from sequence.
        
        Args:
            shared: Shared state dictionary
            prep_data: Prepared data
            exec_result: Result of sequential execution
            
        Returns:
            Next action to take
        """
        # Copy any new or changed values from the workflow's shared state
        workflow_shared = exec_result["shared"]
        for key, value in workflow_shared.items():
            shared[key] = value
        
        # Store the final result if output_key is specified
        if self.output_key and "result" in exec_result:
            shared[self.output_key] = exec_result["result"]
        
        return "next"


class LoopNode(Node):
    """Node that executes a flow repeatedly until a condition is met.
    
    The LoopNode allows for iterative execution of a flow, checking
    a condition after each iteration to determine whether to continue.
    """
    
    def __init__(self, 
                 flow: Flow,
                 condition_fn: Callable[[Dict[str, Any], int], bool],
                 max_iterations: int = 10,
                 iteration_key: str = "iteration",
                 result_key: str = "loop_results",
                 name: Optional[str] = None):
        """Initialize a LoopNode.
        
        Args:
            flow: Flow to execute repeatedly
            condition_fn: Function that determines when to stop looping
            max_iterations: Maximum number of iterations
            iteration_key: Key to store current iteration number
            result_key: Key to store results from all iterations
            name: Optional name for the node
        """
        super().__init__(name=name)
        self.flow = flow
        self.condition_fn = condition_fn
        self.max_iterations = max_iterations
        self.iteration_key = iteration_key
        self.result_key = result_key
    
    def prep(self, shared: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare data for loop execution.
        
        Args:
            shared: Shared state dictionary
            
        Returns:
            Prepared data for loop
        """
        # Create a copy of shared state for the loop
        loop_shared = shared.copy()
        
        return {
            "shared": loop_shared,
            "original_shared": shared
        }
    
    def exec(self, prep_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the flow in a loop.
        
        Args:
            prep_data: Prepared data
            
        Returns:
            Results from loop execution
        """
        loop_shared = prep_data["shared"]
        results = []
        
        # Initialize iteration counter
        iteration = 0
        loop_shared[self.iteration_key] = iteration
        
        # Execute the flow until the condition is met or max iterations reached
        while True:
            logger.info(f"Loop iteration {iteration}")
            
            # Execute the flow
            try:
                result = self.flow.run(shared=loop_shared)
                results.append(result)
                
                # Update iteration counter for next iteration
                iteration += 1
                loop_shared[self.iteration_key] = iteration
                
                # Check if we should continue
                if iteration >= self.max_iterations:
                    logger.info(f"Loop reached maximum iterations ({self.max_iterations})")
                    break
                
                if self.condition_fn(loop_shared, iteration):
                    logger.info("Loop condition satisfied, exiting loop")
                    break
                
            except Exception as e:
                logger.error(f"Error in loop iteration {iteration}: {str(e)}")
                break
        
        return {
            "shared": loop_shared,
            "results": results,
            "iterations": iteration
        }
    
    def post(self, shared: Dict[str, Any], prep_data: Dict[str, Any], 
             exec_result: Dict[str, Any]) -> str:
        """Update shared state with results from loop.
        
        Args:
            shared: Shared state dictionary
            prep_data: Prepared data
            exec_result: Results from loop
            
        Returns:
            Next action to take
        """
        # Copy any new or changed values from the loop's shared state
        loop_shared = exec_result["shared"]
        for key, value in loop_shared.items():
            shared[key] = value
        
        # Store the results
        shared[self.result_key] = exec_result["results"]
        shared[f"{self.iteration_key}_count"] = exec_result["iterations"]
        
        return "next"


def create_conditional_workflow(
    model: AbstractUniversalModel,
    decision_prompt: str,
    options: Dict[str, Tuple[List[Node], str]],
    input_keys: List[str],
    output_key: str = "workflow_result",
    name: Optional[str] = None
) -> Flow:
    """Create a workflow with a model-based decision point and conditional branches.
    
    Args:
        model: Universal Intelligence model for decision making
        decision_prompt: Prompt template for decision
        options: Dictionary mapping option names to (nodes, description) tuples
        input_keys: Keys in shared state to include in decision prompt
        output_key: Key to store final result
        name: Optional name for the flow
        
    Returns:
        Configured conditional workflow
    """
    # Build the options list and descriptions
    option_list = list(options.keys())
    option_descriptions = []
    for option, (_, description) in options.items():
        option_descriptions.append(f"{option}: {description}")
    
    # Create the decision node
    decision_node = ModelDecisionNode(
        model=model,
        prompt_template=decision_prompt + "\n\nOptions:\n" + "\n".join(option_descriptions),
        options=option_list,
        input_keys=input_keys,
        output_key="decision",
        name="decision_node"
    )
    
    # Create the workflow nodes and connect them to the decision node
    for option, (nodes, _) in options.items():
        if not nodes:
            continue
            
        # Connect the nodes in sequence
        for i in range(len(nodes) - 1):
            nodes[i] - "next" >> nodes[i + 1]
            
        # Connect the decision node to the first node in this branch
        decision_node - option >> nodes[0]
        
        # Have the last node in the branch set the workflow result
        last_node = nodes[-1]
        
        # Create a simple Result Node to store the output
        result_node = Node(name=f"result_node_{option}")
        
        def result_node_post(shared, prep_data, exec_result):
            shared[output_key] = exec_result
            return "complete"
            
        result_node.post = result_node_post
        
        # Connect the last node to the result node
        last_node - "next" >> result_node
    
    # Create and return the flow
    return Flow(start=decision_node, name=name or "conditional_workflow")