"""Universal Agents - Map-Reduce Pattern Implementation

This module provides a ready-to-use implementation of the Map-Reduce pattern
using Universal Agents. Map-Reduce is a powerful pattern for processing large
datasets by splitting them into smaller chunks, processing each chunk independently,
and then combining the results.
"""
import logging
from typing import Any, Dict, List, Optional, Union, Callable, TypeVar, Generic, Tuple
from ..node import Node, BatchNode, Flow
from ..universal_integration import UniversalModelNode, UniversalToolNode
from universal_intelligence.core.universal_model import AbstractUniversalModel
from universal_intelligence.core.universal_tool import AbstractUniversalTool

logger = logging.getLogger(__name__)
T = TypeVar('T')

class MapNode(BatchNode, Generic[T]):
    """Node that applies a mapping function to each item in a batch.
    
    The MapNode takes a list of items, applies a mapping function to each item,
    and outputs the mapped results.
    """
    
    def __init__(self, 
                 map_fn: Callable[[Any], T],
                 input_key: str = "items",
                 output_key: str = "mapped_items",
                 name: Optional[str] = None):
        """Initialize a MapNode.
        
        Args:
            map_fn: Function to apply to each item
            input_key: Key in shared state for input items
            output_key: Key in shared state to store mapped items
            name: Optional name for the node
        """
        super().__init__(name=name)
        self.map_fn = map_fn
        self.input_key = input_key
        self.output_key = output_key
    
    def prep(self, shared: Dict[str, Any]) -> List[Any]:
        """Prepare the items for mapping.
        
        Args:
            shared: Shared state dictionary
            
        Returns:
            List of items to process
        """
        if self.input_key not in shared:
            raise KeyError(f"Input key '{self.input_key}' not found in shared state")
        
        items = shared[self.input_key]
        if not isinstance(items, list):
            raise TypeError(f"Expected list for key '{self.input_key}', got {type(items)}")
        
        return items
    
    def process_batch_item(self, item: Any) -> T:
        """Process a single item in the batch.
        
        Args:
            item: Item to process
            
        Returns:
            Processed item
        """
        return self.map_fn(item)
    
    def post(self, shared: Dict[str, Any], prep_data: List[Any], exec_result: List[T]) -> str:
        """Store the mapped results in shared state.
        
        Args:
            shared: Shared state dictionary
            prep_data: Original items
            exec_result: Mapped items
            
        Returns:
            Next action to take
        """
        shared[self.output_key] = exec_result
        return "next"


class ModelMapNode(BatchNode):
    """Node that applies an LLM to each item in a batch.
    
    The ModelMapNode uses a Universal Intelligence model to process each item
    in a batch, applying the same prompt template to each item.
    """
    
    def __init__(self, 
                 model: AbstractUniversalModel,
                 prompt_template: str,
                 input_key: str = "items",
                 output_key: str = "mapped_items",
                 item_key: str = "item",
                 model_parameters: Optional[Dict[str, Any]] = None,
                 name: Optional[str] = None):
        """Initialize a ModelMapNode.
        
        Args:
            model: Universal Intelligence model to use
            prompt_template: Prompt template to apply to each item
            input_key: Key in shared state for input items
            output_key: Key in shared state to store mapped items
            item_key: Key to use for the item in prompt formatting
            model_parameters: Optional parameters for the model
            name: Optional name for the node
        """
        super().__init__(name=name)
        self.model = model
        self.prompt_template = prompt_template
        self.input_key = input_key
        self.output_key = output_key
        self.item_key = item_key
        self.model_parameters = model_parameters or {}
    
    def prep(self, shared: Dict[str, Any]) -> List[Any]:
        """Prepare the items for mapping.
        
        Args:
            shared: Shared state dictionary
            
        Returns:
            List of items to process
        """
        if self.input_key not in shared:
            raise KeyError(f"Input key '{self.input_key}' not found in shared state")
        
        items = shared[self.input_key]
        if not isinstance(items, list):
            raise TypeError(f"Expected list for key '{self.input_key}', got {type(items)}")
        
        return items
    
    def process_batch_item(self, item: Any) -> str:
        """Process a single item with the model.
        
        Args:
            item: Item to process
            
        Returns:
            Model output for the item
        """
        # Format the prompt with the item
        prompt_data = {self.item_key: item}
        prompt = self.prompt_template.format(**prompt_data)
        
        # Execute the model
        return self.model.generate(prompt, **self.model_parameters)
    
    def post(self, shared: Dict[str, Any], prep_data: List[Any], exec_result: List[str]) -> str:
        """Store the mapped results in shared state.
        
        Args:
            shared: Shared state dictionary
            prep_data: Original items
            exec_result: Model outputs for each item
            
        Returns:
            Next action to take
        """
        shared[self.output_key] = exec_result
        return "next"


class ReduceNode(Node, Generic[T]):
    """Node that reduces a list of items to a single result.
    
    The ReduceNode takes a list of items and applies a reduction function to combine
    them into a single result.
    """
    
    def __init__(self, 
                 reduce_fn: Callable[[List[Any]], T],
                 input_key: str = "mapped_items",
                 output_key: str = "reduced_result",
                 name: Optional[str] = None):
        """Initialize a ReduceNode.
        
        Args:
            reduce_fn: Function to reduce items to a single result
            input_key: Key in shared state for input items
            output_key: Key in shared state to store reduced result
            name: Optional name for the node
        """
        super().__init__(name=name)
        self.reduce_fn = reduce_fn
        self.input_key = input_key
        self.output_key = output_key
    
    def prep(self, shared: Dict[str, Any]) -> List[Any]:
        """Prepare the items for reduction.
        
        Args:
            shared: Shared state dictionary
            
        Returns:
            List of items to reduce
        """
        if self.input_key not in shared:
            raise KeyError(f"Input key '{self.input_key}' not found in shared state")
        
        items = shared[self.input_key]
        if not isinstance(items, list):
            raise TypeError(f"Expected list for key '{self.input_key}', got {type(items)}")
        
        return items
    
    def exec(self, prep_data: List[Any]) -> T:
        """Reduce the items to a single result.
        
        Args:
            prep_data: Items to reduce
            
        Returns:
            Reduced result
        """
        return self.reduce_fn(prep_data)
    
    def post(self, shared: Dict[str, Any], prep_data: List[Any], exec_result: T) -> str:
        """Store the reduced result in shared state.
        
        Args:
            shared: Shared state dictionary
            prep_data: Original items
            exec_result: Reduced result
            
        Returns:
            Next action to take
        """
        shared[self.output_key] = exec_result
        return "next"


class ModelReduceNode(Node):
    """Node that reduces a list of items using an LLM.
    
    The ModelReduceNode uses a Universal Intelligence model to combine multiple items
    into a single result, useful for summarization and synthesis tasks.
    """
    
    def __init__(self, 
                 model: AbstractUniversalModel,
                 prompt_template: str,
                 input_key: str = "mapped_items",
                 output_key: str = "reduced_result",
                 items_key: str = "items",
                 model_parameters: Optional[Dict[str, Any]] = None,
                 name: Optional[str] = None):
        """Initialize a ModelReduceNode.
        
        Args:
            model: Universal Intelligence model to use
            prompt_template: Prompt template for reduction
            input_key: Key in shared state for input items
            output_key: Key in shared state to store reduced result
            items_key: Key to use for the items in prompt formatting
            model_parameters: Optional parameters for the model
            name: Optional name for the node
        """
        super().__init__(name=name)
        self.model = model
        self.prompt_template = prompt_template
        self.input_key = input_key
        self.output_key = output_key
        self.items_key = items_key
        self.model_parameters = model_parameters or {}
    
    def prep(self, shared: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare data for model execution.
        
        Args:
            shared: Shared state dictionary
            
        Returns:
            Data for model execution
        """
        if self.input_key not in shared:
            raise KeyError(f"Input key '{self.input_key}' not found in shared state")
        
        items = shared[self.input_key]
        if not isinstance(items, list):
            raise TypeError(f"Expected list for key '{self.input_key}', got {type(items)}")
        
        # Format the prompt with the items
        prompt_data = {self.items_key: items}
        prompt = self.prompt_template.format(**prompt_data)
        
        return {"prompt": prompt}
    
    def exec(self, prep_data: Dict[str, Any]) -> str:
        """Execute the model with the prepared prompt.
        
        Args:
            prep_data: Prepared data
            
        Returns:
            Model output
        """
        return self.model.generate(prep_data["prompt"], **self.model_parameters)
    
    def post(self, shared: Dict[str, Any], prep_data: Dict[str, Any], exec_result: str) -> str:
        """Store the reduced result in shared state.
        
        Args:
            shared: Shared state dictionary
            prep_data: Prepared data
            exec_result: Model output
            
        Returns:
            Next action to take
        """
        shared[self.output_key] = exec_result
        return "next"


def create_map_reduce_flow(
    map_model: AbstractUniversalModel,
    reduce_model: AbstractUniversalModel,
    map_prompt_template: str,
    reduce_prompt_template: str,
    input_key: str = "items",
    output_key: str = "result",
    map_model_parameters: Optional[Dict[str, Any]] = None,
    reduce_model_parameters: Optional[Dict[str, Any]] = None,
    name: Optional[str] = None
) -> Flow:
    """Create a Map-Reduce flow with models for both mapping and reducing.
    
    Args:
        map_model: Model to use for mapping items
        reduce_model: Model to use for reducing results
        map_prompt_template: Prompt template for mapping
        reduce_prompt_template: Prompt template for reducing
        input_key: Key in shared state for input items
        output_key: Key in shared state to store final result
        map_model_parameters: Optional parameters for the map model
        reduce_model_parameters: Optional parameters for the reduce model
        name: Optional name for the flow
        
    Returns:
        Configured Map-Reduce flow
    """
    # Create the mapping node
    map_node = ModelMapNode(
        model=map_model,
        prompt_template=map_prompt_template,
        input_key=input_key,
        output_key="mapped_items",
        item_key="item",
        model_parameters=map_model_parameters,
        name="map_node"
    )
    
    # Create the reduce node
    reduce_node = ModelReduceNode(
        model=reduce_model,
        prompt_template=reduce_prompt_template,
        input_key="mapped_items",
        output_key=output_key,
        items_key="items",
        model_parameters=reduce_model_parameters,
        name="reduce_node"
    )
    
    # Connect the nodes
    map_node - "next" >> reduce_node
    
    # Create and return the flow
    return Flow(start=map_node, name=name or "map_reduce_flow")