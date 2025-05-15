from typing import Any, Dict, List, Optional, Union, Callable


class Node:
    """Base class for all nodes in a flow.
    
    A Node is the fundamental processing unit in a flow, with three main lifecycle methods:
    - prep: Prepare data for execution
    - exec: Execute the core functionality
    - post: Process results and determine next action
    """

    def __init__(self, name: Optional[str] = None) -> None:
        """Initialize a new node.
        
        Args:
            name: Optional name for the node (defaults to class name)
        """
        self.name = name or self.__class__.__name__
        self.connections = {}
        
    def __sub__(self, action: str) -> 'NodeConnection':
        """Create a connection from this node with the specified action.
        
        This enables the syntax: node - "action" >> target_node
        
        Args:
            action: The action that triggers the connection
            
        Returns:
            A NodeConnection object for linking to a target node
        """
        return NodeConnection(self, action)
        
    def prep(self, shared: Dict[str, Any]) -> Any:
        """Prepare data for execution.
        
        Args:
            shared: The shared state dictionary
            
        Returns:
            Data to be passed to the exec method
        """
        return None
        
    def exec(self, prep_data: Any) -> Any:
        """Execute the core functionality of the node.
        
        Args:
            prep_data: Data prepared by the prep method
            
        Returns:
            Result of execution
        """
        return prep_data
        
    def post(self, shared: Dict[str, Any], prep_data: Any, exec_result: Any) -> str:
        """Process execution results and determine the next action.
        
        Args:
            shared: The shared state dictionary
            prep_data: Data that was prepared by the prep method
            exec_result: Result from the exec method
            
        Returns:
            Action string indicating the next node to execute
        """
        return "next"


class BatchNode(Node):
    """Node that processes batches of items.
    
    BatchNodes enable processing multiple items in a batch, which can be
    more efficient than processing them one by one in separate nodes.
    """
    
    def __init__(self, name: Optional[str] = None) -> None:
        """Initialize a new batch node.
        
        Args:
            name: Optional name for the node (defaults to class name)
        """
        super().__init__(name)
    
    def batch_prep(self, shared: Dict[str, Any], items: List[Any]) -> List[Any]:
        """Prepare a batch of items for processing.
        
        Args:
            shared: The shared state dictionary
            items: List of items to process
            
        Returns:
            List of prepared data for each item
        """
        return [self.prep(shared) for _ in items]
    
    def batch_exec(self, prep_results: List[Any]) -> List[Any]:
        """Execute on a batch of prepared items.
        
        Args:
            prep_results: List of data prepared by batch_prep
            
        Returns:
            List of execution results
        """
        return [self.exec(prep_data) for prep_data in prep_results]
    
    def batch_post(self, shared: Dict[str, Any], prep_results: List[Any], exec_results: List[Any]) -> str:
        """Process batch execution results.
        
        Args:
            shared: The shared state dictionary
            prep_results: List of prepared data
            exec_results: List of execution results
            
        Returns:
            Action string indicating the next node to execute
        """
        # Default implementation just uses the last item's post result
        if not exec_results:
            return "next"
        return self.post(shared, prep_results[-1], exec_results[-1])
    
    def prep(self, shared: Dict[str, Any]) -> Any:
        """Single-item preparation (implemented by subclasses)."""
        return None
    
    def exec(self, prep_data: Any) -> Any:
        """Single-item execution (implemented by subclasses)."""
        return prep_data
    
    def post(self, shared: Dict[str, Any], prep_data: Any, exec_result: Any) -> str:
        """Single-item post-processing (implemented by subclasses)."""
        return "next"


class AsyncNode(Node):
    """Node that supports asynchronous execution.
    
    AsyncNodes enable non-blocking operations, which is useful for
    I/O-bound tasks like API calls, database queries, etc.
    """
    
    def __init__(self, name: Optional[str] = None) -> None:
        """Initialize a new async node.
        
        Args:
            name: Optional name for the node (defaults to class name)
        """
        super().__init__(name)
    
    async def async_prep(self, shared: Dict[str, Any]) -> Any:
        """Asynchronously prepare data for execution.
        
        Args:
            shared: The shared state dictionary
            
        Returns:
            Data to be passed to async_exec
        """
        return self.prep(shared)
    
    async def async_exec(self, prep_data: Any) -> Any:
        """Asynchronously execute the core functionality.
        
        Args:
            prep_data: Data prepared by async_prep
            
        Returns:
            Result of execution
        """
        return self.exec(prep_data)
    
    async def async_post(self, shared: Dict[str, Any], prep_data: Any, exec_result: Any) -> str:
        """Asynchronously process execution results.
        
        Args:
            shared: The shared state dictionary
            prep_data: Data prepared by async_prep
            exec_result: Result from async_exec
            
        Returns:
            Action string indicating the next node to execute
        """
        return self.post(shared, prep_data, exec_result)


class AsyncBatchNode(BatchNode, AsyncNode):
    """Node that supports both batch processing and asynchronous execution.
    
    AsyncBatchNodes combine the benefits of BatchNodes and AsyncNodes,
    enabling efficient processing of multiple items asynchronously.
    """
    
    def __init__(self, name: Optional[str] = None) -> None:
        """Initialize a new async batch node.
        
        Args:
            name: Optional name for the node (defaults to class name)
        """
        super().__init__(name)
    
    async def async_batch_prep(self, shared: Dict[str, Any], items: List[Any]) -> List[Any]:
        """Asynchronously prepare a batch of items.
        
        Args:
            shared: The shared state dictionary
            items: List of items to process
            
        Returns:
            List of prepared data for each item
        """
        import asyncio
        return await asyncio.gather(*[self.async_prep(shared) for _ in items])
    
    async def async_batch_exec(self, prep_results: List[Any]) -> List[Any]:
        """Asynchronously execute on a batch of prepared items.
        
        Args:
            prep_results: List of data prepared by async_batch_prep
            
        Returns:
            List of execution results
        """
        import asyncio
        return await asyncio.gather(*[self.async_exec(prep_data) for prep_data in prep_results])
    
    async def async_batch_post(self, shared: Dict[str, Any], prep_results: List[Any], exec_results: List[Any]) -> str:
        """Asynchronously process batch execution results.
        
        Args:
            shared: The shared state dictionary
            prep_results: List of prepared data
            exec_results: List of execution results
            
        Returns:
            Action string indicating the next node to execute
        """
        # Default implementation just uses the last item's post result
        if not exec_results:
            return "next"
        return await self.async_post(shared, prep_results[-1], exec_results[-1])


class NodeConnection:
    """Helper class for connecting nodes with actions.
    
    This class enables the syntax: node - "action" >> target_node
    """
    
    def __init__(self, source: Node, action: str) -> None:
        """Initialize a new node connection.
        
        Args:
            source: The source node
            action: The action that triggers the connection
        """
        self.source = source
        self.action = action
    
    def __rshift__(self, target: Node) -> Node:
        """Connect the source node to the target node with the specified action.
        
        This enables the syntax: node - "action" >> target_node
        
        Args:
            target: The target node
            
        Returns:
            The source node (for chaining)
        """
        self.source.connections[self.action] = target
        return self.source