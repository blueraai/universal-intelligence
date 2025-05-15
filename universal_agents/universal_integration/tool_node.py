"""Universal Agents - Universal Tool Integration

This module provides nodes for integrating Universal Intelligence tools
into Universal Agents workflows.
"""

import logging
from typing import Any, Dict, List, Optional, Union, Callable

from ..node import Node, AsyncNode
from universal_intelligence.core.universal_tool import AbstractUniversalTool

logger = logging.getLogger(__name__)


class UniversalToolNode(Node):
    """Node for executing Universal Intelligence tools.
    
    This node enables the use of any Universal Intelligence tool within a flow.
    It handles parameter mapping, tool execution, and result processing.
    """
    
    def __init__(self, tool: AbstractUniversalTool, 
                 method_name: str,
                 arg_mapping: Dict[str, str],
                 result_key: str = "tool_result",
                 name: Optional[str] = None,
                 error_handling: str = "continue"):
        """Initialize a new Universal Tool node.
        
        Args:
            tool: A Universal Intelligence tool instance
            method_name: Name of the tool method to call
            arg_mapping: Mapping from method parameters to shared state keys
            result_key: Key to store the tool result in shared state
            name: Optional name for the node
            error_handling: How to handle errors ('continue', 'raise', or 'return')
        """
        super().__init__(name or f"{tool.contract()['name']}_{method_name}")
        self.tool = tool
        self.method_name = method_name
        self.arg_mapping = arg_mapping
        self.result_key = result_key
        self.error_handling = error_handling
        
        # Validate method exists
        if not hasattr(self.tool, self.method_name):
            raise ValueError(f"Method '{self.method_name}' not found in tool {self.tool.contract()['name']}")
            
        # Get the method contract from the tool contract
        self.method_contract = None
        for method in self.tool.contract().get("methods", []):
            if method["name"] == self.method_name:
                self.method_contract = method
                break
                
        if not self.method_contract:
            logger.warning(f"Method '{self.method_name}' not found in tool contract")
        
    def prep(self, shared: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare arguments for the tool method.
        
        This method extracts data from shared state based on the arg_mapping
        and prepares a dictionary of arguments for the tool method.
        
        Args:
            shared: The shared state dictionary
            
        Returns:
            Dictionary of method arguments
        """
        # Extract arguments from shared state based on mapping
        args = {}
        missing_keys = []
        
        for param, key in self.arg_mapping.items():
            if key in shared:
                args[param] = shared[key]
            else:
                missing_keys.append(key)
                
        # Log warning for missing keys
        if missing_keys:
            logger.warning(f"Missing keys in shared state: {missing_keys}")
            
        return {
            "args": args,
            "missing_keys": missing_keys
        }
        
    def exec(self, prep_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the tool method with the prepared arguments.
        
        This method calls the specified tool method with the prepared arguments
        and returns the result.
        
        Args:
            prep_data: Dictionary of method arguments
            
        Returns:
            Dictionary with result and metadata
        """
        args = prep_data["args"]
        
        try:
            # Get the method from the tool
            method = getattr(self.tool, self.method_name)
            
            # Call the method with prepared arguments
            result, logs = method(**args)
            
            return {
                "result": result,
                "logs": logs,
                "success": True,
                "error": None
            }
            
        except Exception as e:
            logger.error(f"Error executing tool method: {str(e)}")
            
            if self.error_handling == "raise":
                raise
            
            return {
                "result": None,
                "logs": {},
                "success": False,
                "error": str(e)
            }
        
    def post(self, shared: Dict[str, Any], prep_data: Dict[str, Any], exec_result: Dict[str, Any]) -> str:
        """Store the tool result in shared state.
        
        This method updates the shared state with the tool result
        and returns the next action based on success or failure.
        
        Args:
            shared: The shared state dictionary
            prep_data: Dictionary of method arguments
            exec_result: Dictionary with result and metadata
            
        Returns:
            Next action to execute
        """
        # Store the complete result in shared state
        shared[self.result_key] = exec_result["result"]
        
        # Also store logs and status
        shared[f"{self.result_key}_logs"] = exec_result["logs"]
        shared[f"{self.result_key}_success"] = exec_result["success"]
        
        if exec_result["error"]:
            shared[f"{self.result_key}_error"] = exec_result["error"]
            return "error" if "error" in self.connections else "next"
        
        return "success" if "success" in self.connections else "next"


class AsyncUniversalToolNode(AsyncNode, UniversalToolNode):
    """Asynchronous node for executing Universal Intelligence tools.
    
    This node provides the same functionality as UniversalToolNode,
    but supports asynchronous execution for tools with async methods.
    """
    
    def __init__(self, tool: AbstractUniversalTool, 
                 method_name: str,
                 arg_mapping: Dict[str, str],
                 result_key: str = "tool_result",
                 name: Optional[str] = None,
                 error_handling: str = "continue"):
        """Initialize a new Async Universal Tool node.
        
        Args:
            tool: A Universal Intelligence tool instance
            method_name: Name of the tool method to call
            arg_mapping: Mapping from method parameters to shared state keys
            result_key: Key to store the tool result in shared state
            name: Optional name for the node
            error_handling: How to handle errors ('continue', 'raise', or 'return')
        """
        UniversalToolNode.__init__(
            self,
            tool=tool,
            method_name=method_name,
            arg_mapping=arg_mapping,
            result_key=result_key,
            name=name or f"Async{tool.contract()['name']}_{method_name}",
            error_handling=error_handling
        )
        
        # Check if the method is marked as asynchronous in the contract
        self.is_async_method = False
        if self.method_contract:
            self.is_async_method = self.method_contract.get("asynchronous", False)
            
    async def async_exec(self, prep_data: Dict[str, Any]) -> Dict[str, Any]:
        """Asynchronously execute the tool method with the prepared arguments.
        
        This method calls the specified tool method with the prepared arguments
        and returns the result. It handles both async and non-async methods.
        
        Args:
            prep_data: Dictionary of method arguments
            
        Returns:
            Dictionary with result and metadata
        """
        args = prep_data["args"]
        
        try:
            # Get the method from the tool
            method = getattr(self.tool, self.method_name)
            
            # Call the method with prepared arguments
            if self.is_async_method:
                # For async methods, await the result
                result, logs = await method(**args)
            else:
                # For non-async methods, just call normally
                result, logs = method(**args)
            
            return {
                "result": result,
                "logs": logs,
                "success": True,
                "error": None
            }
            
        except Exception as e:
            logger.error(f"Error executing tool method: {str(e)}")
            
            if self.error_handling == "raise":
                raise
            
            return {
                "result": None,
                "logs": {},
                "success": False,
                "error": str(e)
            }