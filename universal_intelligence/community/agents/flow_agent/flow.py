from typing import Any, Dict, List, Optional, Set, Tuple, Union, Type
import asyncio

from .nodes import Node, BatchNode, AsyncNode, AsyncBatchNode


class Flow:
    """A directed graph of connected nodes.
    
    A Flow manages the execution of a graph of connected nodes,
    starting from a designated start node and following the connections
    between nodes based on the actions returned by each node's post method.
    """
    
    def __init__(self, start: Node) -> None:
        """Initialize a new flow.
        
        Args:
            start: The starting node for the flow
        """
        self.start = start
        self.nodes = self._collect_nodes(start)
        
    def _collect_nodes(self, start: Node) -> Dict[str, Node]:
        """Collect all nodes in the flow starting from the start node.
        
        This performs a depth-first traversal of the node graph to build
        a dictionary of all nodes in the flow, keyed by their names.
        
        Args:
            start: The starting node
            
        Returns:
            Dictionary mapping node names to node instances
        """
        nodes = {}
        visited = set()
        
        def visit(node: Node) -> None:
            if node in visited:
                return
                
            visited.add(node)
            nodes[node.name] = node
            
            for target in node.connections.values():
                visit(target)
                
        visit(start)
        return nodes
        
    def run(self, shared: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Run the flow starting from the start node.
        
        Args:
            shared: Initial shared state dictionary
            
        Returns:
            Final shared state after flow execution
        """
        # Initialize shared state
        state = shared.copy() if shared else {}
        
        # Start with the start node
        current_node = self.start
        
        # Track execution path and prevent infinite loops
        max_steps = state.get("max_steps", 100)
        step_count = 0
        
        # Execute until we reach a node with no connections
        while current_node and step_count < max_steps:
            # Increment step count
            step_count += 1
            
            # Execute the node's lifecycle methods
            try:
                # Prepare data
                prep_data = current_node.prep(state)
                
                # Execute core functionality
                exec_result = current_node.exec(prep_data)
                
                # Process results and get next action
                action = current_node.post(state, prep_data, exec_result)
                
                # Find the next node based on the action
                current_node = current_node.connections.get(action)
                
            except Exception as e:
                # Handle node execution errors
                state["error"] = str(e)
                state["error_node"] = current_node.name
                
                # Try to find an error handler
                current_node = current_node.connections.get("error")
                
                # If no error handler, stop execution
                if not current_node:
                    break
        
        # Add information about execution
        state["_flow_completed"] = current_node is None
        state["_flow_steps"] = step_count
        state["_flow_max_steps_reached"] = step_count >= max_steps
        
        return state
        
    def visualize(self, output_path: Optional[str] = None) -> Dict[str, Any]:
        """Generate a visualization of the flow.
        
        Args:
            output_path: Optional path to save the visualization
            
        Returns:
            Dictionary with visualization data
        """
        # Create nodes data
        nodes_data = []
        for name, node in self.nodes.items():
            nodes_data.append({
                "id": name,
                "label": name,
                "type": node.__class__.__name__
            })
            
        # Create edges data
        edges_data = []
        for name, node in self.nodes.items():
            for action, target in node.connections.items():
                edges_data.append({
                    "from": name,
                    "to": target.name,
                    "label": action
                })
                
        # Create visualization data
        visualization = {
            "nodes": nodes_data,
            "edges": edges_data
        }
        
        # Save visualization if output path is provided
        if output_path:
            import json
            with open(output_path, "w") as f:
                json.dump(visualization, f, indent=2)
                
        return visualization


class BatchFlow(Flow):
    """A flow that processes batches of items.
    
    BatchFlows are specialized flows that process multiple items
    in batch, which can be more efficient than processing them
    one by one in separate flows.
    """
    
    def __init__(self, start: BatchNode) -> None:
        """Initialize a new batch flow.
        
        Args:
            start: The starting batch node
        """
        super().__init__(start)
        
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
        for batch in batches:
            # Create a copy of the shared state
            batch_shared = shared.copy()
            batch_shared["batch_items"] = batch
            
            # Run the flow
            batch_result = self.run(batch_shared)
            results.append(batch_result)
            
        return results


class AsyncFlow(Flow):
    """A flow that supports asynchronous execution.
    
    AsyncFlows enable non-blocking operations, which is useful for
    I/O-bound tasks like API calls, database queries, etc.
    """
    
    def __init__(self, start: AsyncNode) -> None:
        """Initialize a new async flow.
        
        Args:
            start: The starting async node
        """
        super().__init__(start)
        
    async def async_run(self, shared: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Run the flow asynchronously.
        
        Args:
            shared: Initial shared state dictionary
            
        Returns:
            Final shared state after flow execution
        """
        # Initialize shared state
        state = shared.copy() if shared else {}
        
        # Start with the start node
        current_node = self.start
        
        # Track execution path and prevent infinite loops
        max_steps = state.get("max_steps", 100)
        step_count = 0
        
        # Execute until we reach a node with no connections
        while current_node and step_count < max_steps:
            # Increment step count
            step_count += 1
            
            # Execute the node's lifecycle methods
            try:
                # Prepare data
                prep_data = await current_node.async_prep(state)
                
                # Execute core functionality
                exec_result = await current_node.async_exec(prep_data)
                
                # Process results and get next action
                action = await current_node.async_post(state, prep_data, exec_result)
                
                # Find the next node based on the action
                current_node = current_node.connections.get(action)
                
            except Exception as e:
                # Handle node execution errors
                state["error"] = str(e)
                state["error_node"] = current_node.name
                
                # Try to find an error handler
                current_node = current_node.connections.get("error")
                
                # If no error handler, stop execution
                if not current_node:
                    break
        
        # Add information about execution
        state["_flow_completed"] = current_node is None
        state["_flow_steps"] = step_count
        state["_flow_max_steps_reached"] = step_count >= max_steps
        
        return state


class AsyncBatchFlow(BatchFlow, AsyncFlow):
    """A flow that supports both batch processing and asynchronous execution.
    
    AsyncBatchFlows combine the benefits of BatchFlows and AsyncFlows,
    enabling efficient processing of multiple items asynchronously.
    """
    
    def __init__(self, start: AsyncBatchNode) -> None:
        """Initialize a new async batch flow.
        
        Args:
            start: The starting async batch node
        """
        Flow.__init__(self, start)
        
    async def async_batch_run(self, shared: Dict[str, Any], items: List[Any], batch_size: int = 10) -> List[Dict[str, Any]]:
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
        for batch in batches:
            # Create a copy of the shared state
            batch_shared = shared.copy()
            batch_shared["batch_items"] = batch
            
            # Create a task to run the flow
            task = self.async_run(batch_shared)
            tasks.append(task)
            
        # Wait for all tasks to complete
        return await asyncio.gather(*tasks)