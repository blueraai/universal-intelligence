"""Universal Agents - Flow Abstractions

This module defines the Flow classes that orchestrate the execution of nodes in a workflow.
Flows are directed graphs of connected nodes with shared state management.
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional, Set, Tuple, Union, Type, Callable
from copy import deepcopy

from .node import Node, BatchNode, AsyncNode, AsyncBatchNode

logger = logging.getLogger(__name__)


class Flow:
    """A directed graph of connected nodes.
    
    A Flow manages the execution of a graph of connected nodes,
    starting from a designated start node and following the connections
    between nodes based on the actions returned by each node's post method.
    """
    
    def __init__(self, start: Node, name: Optional[str] = None, visualization: bool = False, 
                 visualization_path: Optional[str] = None):
        """Initialize a new flow.
        
        Args:
            start: The starting node for the flow
            name: Optional name for the flow
            visualization: Whether to enable flow visualization
            visualization_path: Path to save visualization files
        """
        self.start = start
        self.name = name or f"flow_{id(self)}"
        self.nodes = self._collect_nodes(start)
        self.visualization = visualization
        self.visualization_path = visualization_path
        
    def _collect_nodes(self, start: Node) -> List[Node]:
        """Collect all nodes in the flow starting from the start node.
        
        This performs a depth-first traversal of the node graph to build
        a list of all nodes in the flow.
        
        Args:
            start: The starting node
            
        Returns:
            List of all node instances in the flow
        """
        nodes = []
        visited = set()
        
        def visit(node: Node) -> None:
            if node in visited:
                return
                
            visited.add(node)
            nodes.append(node)
            
            for target in node.connections.values():
                visit(target)
                
        visit(start)
        return nodes
        
    def run(self, shared: Optional[Dict[str, Any]] = None, step_by_step: bool = False,
           max_steps: Optional[int] = None) -> Dict[str, Any]:
        """Run the flow starting from the start node.
        
        Args:
            shared: Initial shared state dictionary
            step_by_step: Whether to pause after each node for debugging
            max_steps: Maximum number of steps to execute (to prevent infinite loops)
            
        Returns:
            Final shared state after flow execution
        """
        # Initialize shared state
        state = shared.copy() if shared else {}
        
        # Set default max_steps if not provided
        if max_steps is None:
            max_steps = state.get("max_steps", 100)
        
        # Start with the start node
        current_node = self.start
        
        # Track execution path and prevent infinite loops
        step_count = 0
        execution_path = []
        
        # Execute until we reach a node with no connections or hit max_steps
        while current_node and step_count < max_steps:
            # Increment step count
            step_count += 1
            
            # Record execution path
            execution_path.append(current_node.name)
            
            # Log current node execution
            logger.info(f"Executing node: {current_node.name} (step {step_count})")
            
            # Execute the node's lifecycle methods
            try:
                # Prepare data
                prep_data = current_node.prep(state)
                
                # Execute core functionality
                exec_result = current_node.exec(prep_data)
                
                # Process results and get next action
                action = current_node.post(state, prep_data, exec_result)
                
                # Log the action
                logger.info(f"Node {current_node.name} returned action: {action}")
                
                # Find the next node based on the action
                next_node = current_node.connections.get(action)
                
                # If step_by_step is enabled, wait for input before continuing
                if step_by_step and next_node:
                    input(f"Press Enter to continue to node {next_node.name}...")
                
                # Update current node
                current_node = next_node
                
            except Exception as e:
                # Handle node execution errors
                logger.error(f"Error in node {current_node.name}: {str(e)}")
                state["error"] = str(e)
                state["error_node"] = current_node.name
                
                # Try to find an error handler
                current_node = current_node.connections.get("error")
                
                # If no error handler, stop execution
                if not current_node:
                    logger.error("No error handler found, stopping flow execution")
                    break
        
        # Add information about execution
        state["_flow_completed"] = current_node is None
        state["_flow_steps"] = step_count
        state["_flow_execution_path"] = execution_path
        state["_flow_max_steps_reached"] = step_count >= max_steps
        
        # Log completion
        logger.info(f"Flow {self.name} completed in {step_count} steps")
        
        # Generate visualization if enabled
        if self.visualization:
            self._generate_visualization(execution_path, state)
        
        return state
    
    def _generate_visualization(self, execution_path: List[str], state: Dict[str, Any]) -> None:
        """Generate a visualization of the flow execution.
        
        Args:
            execution_path: List of node names in execution order
            state: Final state after execution
        """
        if not self.visualization_path:
            logger.warning("Visualization path not provided, skipping visualization")
            return
            
        try:
            import json
            import os
            from datetime import datetime
            
            # Create nodes data
            nodes_data = []
            for name, node in self.nodes.items():
                nodes_data.append({
                    "id": name,
                    "label": name,
                    "type": node.__class__.__name__,
                    "executed": name in execution_path
                })
                
            # Create edges data
            edges_data = []
            for name, node in self.nodes.items():
                for action, target in node.connections.items():
                    # Check if this edge was traversed during execution
                    was_traversed = False
                    for i in range(len(execution_path) - 1):
                        if execution_path[i] == name and execution_path[i+1] == target.name:
                            was_traversed = True
                            break
                            
                    edges_data.append({
                        "from": name,
                        "to": target.name,
                        "label": action,
                        "traversed": was_traversed
                    })
                    
            # Create visualization data
            visualization = {
                "flow_name": self.name,
                "execution_time": datetime.now().isoformat(),
                "steps": len(execution_path),
                "execution_path": execution_path,
                "nodes": nodes_data,
                "edges": edges_data
            }
            
            # Create visualization directory if it doesn't exist
            os.makedirs(self.visualization_path, exist_ok=True)
            
            # Save visualization to file
            filename = f"{self.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            filepath = os.path.join(self.visualization_path, filename)
            
            with open(filepath, "w") as f:
                json.dump(visualization, f, indent=2)
                
            logger.info(f"Flow visualization saved to {filepath}")
            
        except Exception as e:
            logger.error(f"Error generating visualization: {str(e)}")
            
        
class BatchFlow(Flow):
    """A flow that processes batches of items.
    
    BatchFlows are specialized flows that process multiple items
    in batch, which can be more efficient than processing them
    one by one in separate flows.
    """
    
    def __init__(self, start: BatchNode, name: Optional[str] = None, visualization: bool = False,
                visualization_path: Optional[str] = None):
        """Initialize a new batch flow.
        
        Args:
            start: The starting batch node
            name: Optional name for the flow
            visualization: Whether to enable flow visualization
            visualization_path: Path to save visualization files
        """
        super().__init__(start, name, visualization, visualization_path)
        
    def batch_run(self, shared: Dict[str, Any], items: List[Any], batch_size: int = 10) -> List[Dict[str, Any]]:
        """Run the flow on a batch of items.
        
        Args:
            shared: Initial shared state dictionary
            items: List of items to process
            batch_size: Number of items to process in each batch
            
        Returns:
            List of final shared states for each batch
        """
        # Create batches
        batches = [items[i:i+batch_size] for i in range(0, len(items), batch_size)]
        
        # Process each batch
        results = []
        for i, batch in enumerate(batches):
            logger.info(f"Processing batch {i+1}/{len(batches)} with {len(batch)} items")
            
            # Create a copy of the shared state
            batch_shared = shared.copy()
            batch_shared["batch_items"] = batch
            batch_shared["batch_index"] = i
            batch_shared["total_batches"] = len(batches)
            
            # Run the flow
            batch_result = self.run(batch_shared)
            results.append(batch_result)
            
        return results


class AsyncFlow(Flow):
    """A flow that supports asynchronous execution.
    
    AsyncFlows enable non-blocking operations, which is useful for
    I/O-bound tasks like API calls, database queries, etc.
    """
    
    def __init__(self, start: AsyncNode, name: Optional[str] = None, visualization: bool = False,
                visualization_path: Optional[str] = None):
        """Initialize a new async flow.
        
        Args:
            start: The starting async node
            name: Optional name for the flow
            visualization: Whether to enable flow visualization
            visualization_path: Path to save visualization files
        """
        super().__init__(start, name, visualization, visualization_path)
        
    async def async_run(self, shared: Optional[Dict[str, Any]] = None, 
                      max_steps: Optional[int] = None) -> Dict[str, Any]:
        """Run the flow asynchronously.
        
        Args:
            shared: Initial shared state dictionary
            max_steps: Maximum number of steps to execute (to prevent infinite loops)
            
        Returns:
            Final shared state after flow execution
        """
        # Initialize shared state
        state = shared.copy() if shared else {}
        
        # Set default max_steps if not provided
        if max_steps is None:
            max_steps = state.get("max_steps", 100)
        
        # Start with the start node
        current_node = self.start
        
        # Track execution path and prevent infinite loops
        step_count = 0
        execution_path = []
        
        # Execute until we reach a node with no connections
        while current_node and step_count < max_steps:
            # Increment step count
            step_count += 1
            
            # Record execution path
            execution_path.append(current_node.name)
            
            # Log current node execution
            logger.info(f"Executing node: {current_node.name} (step {step_count})")
            
            # Execute the node's lifecycle methods
            try:
                # Prepare data
                prep_data = await current_node.async_prep(state)
                
                # Execute core functionality
                exec_result = await current_node.async_exec(prep_data)
                
                # Process results and get next action
                action = await current_node.async_post(state, prep_data, exec_result)
                
                # Log the action
                logger.info(f"Node {current_node.name} returned action: {action}")
                
                # Find the next node based on the action
                current_node = current_node.connections.get(action)
                
            except Exception as e:
                # Handle node execution errors
                logger.error(f"Error in node {current_node.name}: {str(e)}")
                state["error"] = str(e)
                state["error_node"] = current_node.name
                
                # Try to find an error handler
                current_node = current_node.connections.get("error")
                
                # If no error handler, stop execution
                if not current_node:
                    logger.error("No error handler found, stopping flow execution")
                    break
        
        # Add information about execution
        state["_flow_completed"] = current_node is None
        state["_flow_steps"] = step_count
        state["_flow_execution_path"] = execution_path
        state["_flow_max_steps_reached"] = step_count >= max_steps
        
        # Log completion
        logger.info(f"Flow {self.name} completed in {step_count} steps")
        
        # Generate visualization if enabled
        if self.visualization:
            self._generate_visualization(execution_path, state)
        
        return state


class AsyncBatchFlow(BatchFlow, AsyncFlow):
    """A flow that supports both batch processing and asynchronous execution.
    
    AsyncBatchFlows combine the benefits of BatchFlows and AsyncFlows,
    enabling efficient processing of multiple items asynchronously.
    """
    
    def __init__(self, start: AsyncBatchNode, name: Optional[str] = None, visualization: bool = False,
                visualization_path: Optional[str] = None):
        """Initialize a new async batch flow.
        
        Args:
            start: The starting async batch node
            name: Optional name for the flow
            visualization: Whether to enable flow visualization
            visualization_path: Path to save visualization files
        """
        Flow.__init__(self, start, name, visualization, visualization_path)
        
    async def async_batch_run(self, shared: Dict[str, Any], items: List[Any], 
                            batch_size: int = 10) -> List[Dict[str, Any]]:
        """Run the flow asynchronously on a batch of items.
        
        Args:
            shared: Initial shared state dictionary
            items: List of items to process
            batch_size: Number of items to process in each batch
            
        Returns:
            List of final shared states for each batch
        """
        # Create batches
        batches = [items[i:i+batch_size] for i in range(0, len(items), batch_size)]
        
        # Process each batch
        tasks = []
        for i, batch in enumerate(batches):
            logger.info(f"Processing batch {i+1}/{len(batches)} with {len(batch)} items")
            
            # Create a copy of the shared state
            batch_shared = shared.copy()
            batch_shared["batch_items"] = batch
            batch_shared["batch_index"] = i
            batch_shared["total_batches"] = len(batches)
            
            # Create a task to run the flow
            task = self.async_run(batch_shared)
            tasks.append(task)
            
        # Wait for all tasks to complete
        return await asyncio.gather(*tasks)