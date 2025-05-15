"""Universal Agents - Universal Model Integration

This module provides nodes for integrating Universal Intelligence models
into Universal Agents workflows.
"""

import logging
from typing import Any, Dict, List, Optional, Union, Callable

from ..node import Node, AsyncNode
from universal_intelligence.core.universal_model import AbstractUniversalModel

logger = logging.getLogger(__name__)


class UniversalModelNode(Node):
    """Node for executing Universal Intelligence models.
    
    This node enables the use of any Universal Intelligence model within a flow.
    It handles prompt preparation, model execution, and result processing.
    """
    
    def __init__(self, model: AbstractUniversalModel, 
                 prompt_template: str,
                 input_keys: Optional[List[str]] = None,
                 output_key: str = "model_output",
                 name: Optional[str] = None,
                 format_func: Optional[Callable[[Dict[str, Any]], str]] = None,
                 model_parameters: Optional[Dict[str, Any]] = None):
        """Initialize a new Universal Model node.
        
        Args:
            model: A Universal Intelligence model instance
            prompt_template: Template string with {variable} placeholders
            input_keys: Keys from shared state to use in the template
            output_key: Key to store the model output in shared state
            name: Optional name for the node
            format_func: Optional function to format the prompt instead of using template
            model_parameters: Optional parameters to pass to the model
        """
        super().__init__(name or "UniversalModelNode")
        self.model = model
        self.prompt_template = prompt_template
        self.input_keys = input_keys or []
        self.output_key = output_key
        self.format_func = format_func
        self.model_parameters = model_parameters or {}
        
    def prep(self, shared: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare the prompt for the model.
        
        This method extracts data from shared state and formats a prompt
        using either the prompt template or a custom format function.
        
        Args:
            shared: The shared state dictionary
            
        Returns:
            Dictionary with prompt and context data
        """
        # Extract specific keys if provided, otherwise use entire shared state
        if self.input_keys:
            # Only extract keys that exist in the shared state
            context_data = {k: shared.get(k, "") for k in self.input_keys if k in shared}
            
            # Log warning for missing keys
            missing_keys = [k for k in self.input_keys if k not in shared]
            if missing_keys:
                logger.warning(f"Missing keys in shared state: {missing_keys}")
        else:
            context_data = shared
            
        # Format the prompt
        if self.format_func:
            prompt = self.format_func(context_data)
        else:
            try:
                prompt = self.prompt_template.format(**context_data)
            except KeyError as e:
                logger.error(f"Error formatting prompt: {str(e)}")
                prompt = f"Error: Missing key {str(e)} in prompt template"
                
        return {
            "prompt": prompt,
            "context_data": context_data
        }
        
    def exec(self, prep_data: Dict[str, Any]) -> str:
        """Execute the model with the prepared prompt.
        
        This method processes the prepared prompt with the model
        and returns the generated text.
        
        Args:
            prep_data: Dictionary with prompt and context data
            
        Returns:
            Generated text from the model
        """
        prompt = prep_data["prompt"]
        
        try:
            # Process the prompt with the model
            response, _ = self.model.process(prompt, **self.model_parameters)
            return response
        except Exception as e:
            logger.error(f"Error processing prompt with model: {str(e)}")
            return f"Error: {str(e)}"
        
    def post(self, shared: Dict[str, Any], prep_data: Dict[str, Any], exec_result: str) -> str:
        """Store the model output in shared state.
        
        This method updates the shared state with the model output
        and returns the next action.
        
        Args:
            shared: The shared state dictionary
            prep_data: Dictionary with prompt and context data
            exec_result: Generated text from the model
            
        Returns:
            Next action to execute
        """
        # Store the model output in shared state
        shared[self.output_key] = exec_result
        
        # Also store the prompt for reference
        shared[f"{self.output_key}_prompt"] = prep_data["prompt"]
        
        return "next"


class AsyncUniversalModelNode(AsyncNode, UniversalModelNode):
    """Asynchronous node for executing Universal Intelligence models.
    
    This node provides the same functionality as UniversalModelNode,
    but supports asynchronous execution.
    """
    
    def __init__(self, model: AbstractUniversalModel, 
                 prompt_template: str,
                 input_keys: Optional[List[str]] = None,
                 output_key: str = "model_output",
                 name: Optional[str] = None,
                 format_func: Optional[Callable[[Dict[str, Any]], str]] = None,
                 model_parameters: Optional[Dict[str, Any]] = None,
                 streaming: bool = False):
        """Initialize a new Async Universal Model node.
        
        Args:
            model: A Universal Intelligence model instance
            prompt_template: Template string with {variable} placeholders
            input_keys: Keys from shared state to use in the template
            output_key: Key to store the model output in shared state
            name: Optional name for the node
            format_func: Optional function to format the prompt instead of using template
            model_parameters: Optional parameters to pass to the model
            streaming: Whether to use streaming generation
        """
        UniversalModelNode.__init__(
            self, 
            model=model,
            prompt_template=prompt_template,
            input_keys=input_keys,
            output_key=output_key,
            name=name or "AsyncUniversalModelNode",
            format_func=format_func,
            model_parameters=model_parameters
        )
        self.streaming = streaming
        
    async def async_exec(self, prep_data: Dict[str, Any]) -> str:
        """Asynchronously execute the model with the prepared prompt.
        
        This method processes the prepared prompt with the model
        and returns the generated text.
        
        Args:
            prep_data: Dictionary with prompt and context data
            
        Returns:
            Generated text from the model
        """
        prompt = prep_data["prompt"]
        
        try:
            # Process the prompt with the model, with optional streaming
            if self.streaming:
                # For streaming, we need to handle callbacks and accumulate the output
                output_chunks = []
                
                def callback(chunk):
                    output_chunks.append(chunk)
                
                response, _ = self.model.process(
                    prompt, 
                    stream=True, 
                    streaming_callback=callback,
                    **self.model_parameters
                )
                
                # Return the accumulated output or the final response
                return "".join(output_chunks) if output_chunks else response
            else:
                # For non-streaming, just process normally
                response, _ = self.model.process(prompt, **self.model_parameters)
                return response
                
        except Exception as e:
            logger.error(f"Error processing prompt with model: {str(e)}")
            return f"Error: {str(e)}"