"""Universal Agents - RAG Pattern Implementation

This module provides a ready-to-use implementation of the Retrieval Augmented
Generation (RAG) pattern using Universal Agents.
"""

import logging
from typing import Any, Dict, List, Optional, Union, Callable

from ..node import Node, Flow
from ..universal_integration import UniversalModelNode, UniversalToolNode
from universal_intelligence.core.universal_model import AbstractUniversalModel
from universal_intelligence.core.universal_tool import AbstractUniversalTool

logger = logging.getLogger(__name__)


class QueryNode(Node):
    """Node for processing a query in a RAG flow.
    
    This node extracts the query from shared state and performs
    any pre-processing before retrieval.
    """
    
    def __init__(self, 
                 input_key: str = "query",
                 output_key: str = "processed_query",
                 name: Optional[str] = None):
        """Initialize a new Query node.
        
        Args:
            input_key: Key in shared state for the query
            output_key: Key to store the processed query
            name: Optional name for the node
        """
        super().__init__(name or "QueryNode")
        self.input_key = input_key
        self.output_key = output_key
        
    def prep(self, shared: Dict[str, Any]) -> str:
        """Extract the query from shared state.
        
        Args:
            shared: The shared state dictionary
            
        Returns:
            The extracted query
        """
        if self.input_key not in shared:
            logger.warning(f"Query key '{self.input_key}' not found in shared state")
            return ""
            
        return shared[self.input_key]
        
    def exec(self, prep_data: str) -> str:
        """Process the query before retrieval.
        
        This method can be overridden to implement query expansion,
        reformulation, or other pre-processing.
        
        Args:
            prep_data: The extracted query
            
        Returns:
            The processed query
        """
        # By default, just return the query as-is
        # Override this method to implement query preprocessing
        return prep_data
        
    def post(self, shared: Dict[str, Any], prep_data: str, exec_result: str) -> str:
        """Store the processed query in shared state.
        
        Args:
            shared: The shared state dictionary
            prep_data: The extracted query
            exec_result: The processed query
            
        Returns:
            The next action to execute
        """
        # Store the processed query
        shared[self.output_key] = exec_result
        
        return "retrieve"


class ContextBuilderNode(Node):
    """Node for building context from retrieved documents.
    
    This node takes retrieved documents and formats them into
    a context string for the generation step.
    """
    
    def __init__(self,
                 retrieval_key: str = "retrieved_documents",
                 output_key: str = "context",
                 max_tokens: Optional[int] = None,
                 name: Optional[str] = None):
        """Initialize a new Context Builder node.
        
        Args:
            retrieval_key: Key in shared state for retrieved documents
            output_key: Key to store the built context
            max_tokens: Optional maximum tokens for context
            name: Optional name for the node
        """
        super().__init__(name or "ContextBuilderNode")
        self.retrieval_key = retrieval_key
        self.output_key = output_key
        self.max_tokens = max_tokens
        
    def prep(self, shared: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract retrieved documents from shared state.
        
        Args:
            shared: The shared state dictionary
            
        Returns:
            List of retrieved documents
        """
        if self.retrieval_key not in shared:
            logger.warning(f"Retrieval key '{self.retrieval_key}' not found in shared state")
            return []
            
        documents = shared[self.retrieval_key]
        
        # Handle different formats of retrieved documents
        if not isinstance(documents, list):
            logger.warning(f"Retrieved documents not in list format")
            return [documents] if documents else []
            
        return documents
        
    def exec(self, prep_data: List[Dict[str, Any]]) -> str:
        """Build a context string from retrieved documents.
        
        Args:
            prep_data: List of retrieved documents
            
        Returns:
            Formatted context string
        """
        if not prep_data:
            return "No relevant information found."
            
        # Format documents into a context string
        context_parts = []
        
        for i, doc in enumerate(prep_data):
            # Handle different document formats
            if isinstance(doc, str):
                # Simple string format
                content = doc
                metadata = {}
            elif isinstance(doc, dict):
                # Dictionary format with content and metadata
                content = doc.get("content", doc.get("text", ""))
                metadata = {k: v for k, v in doc.items() if k not in ["content", "text"]}
            else:
                logger.warning(f"Unknown document format: {type(doc)}")
                continue
                
            # Format document with metadata
            doc_header = f"Document {i+1}"
            if metadata:
                # Include metadata in the header
                meta_str = ", ".join(f"{k}: {v}" for k, v in metadata.items())
                doc_header += f" ({meta_str})"
                
            context_parts.append(f"{doc_header}:\n{content}\n")
            
        # Join all document parts
        context = "\n".join(context_parts)
        
        # Truncate if max_tokens is specified
        if self.max_tokens and len(context.split()) > self.max_tokens:
            # Simple truncation by word count (not perfect, but a reasonable approximation)
            words = context.split()
            context = " ".join(words[:self.max_tokens])
            context += "... [content truncated]"
            
        return context
        
    def post(self, shared: Dict[str, Any], prep_data: List[Dict[str, Any]], exec_result: str) -> str:
        """Store the context in shared state.
        
        Args:
            shared: The shared state dictionary
            prep_data: List of retrieved documents
            exec_result: Formatted context string
            
        Returns:
            The next action to execute
        """
        # Store the context
        shared[self.output_key] = exec_result
        
        # Also store the document count
        shared[f"{self.output_key}_document_count"] = len(prep_data)
        
        return "generate"


def create_rag_flow(
    retrieval_tool: AbstractUniversalTool,
    retrieval_method: str,
    generation_model: AbstractUniversalModel,
    retrieval_arg_mapping: Optional[Dict[str, str]] = None,
    prompt_template: Optional[str] = None,
    name: Optional[str] = None
) -> Flow:
    """Create a RAG flow with the specified components.
    
    This function creates a complete RAG flow with query processing,
    retrieval, context building, and generation nodes.
    
    Args:
        retrieval_tool: Universal Tool for document retrieval
        retrieval_method: Method name to call on the retrieval tool
        generation_model: Universal Model for text generation
        retrieval_arg_mapping: Optional mapping from tool parameters to shared state keys
        prompt_template: Optional template for generation prompt
        name: Optional name for the flow
        
    Returns:
        A configured RAG flow
    """
    # Default retrieval argument mapping
    if retrieval_arg_mapping is None:
        retrieval_arg_mapping = {"query": "processed_query", "top_k": "top_k"}
        
    # Default prompt template
    if prompt_template is None:
        prompt_template = """Answer the following question based on the provided context.

Context:
{context}

Question:
{query}

Answer:"""
        
    # Create nodes
    query_node = QueryNode(input_key="query", output_key="processed_query")
    
    retrieval_node = UniversalToolNode(
        tool=retrieval_tool,
        method_name=retrieval_method,
        arg_mapping=retrieval_arg_mapping,
        result_key="retrieved_documents"
    )
    
    context_node = ContextBuilderNode(
        retrieval_key="retrieved_documents",
        output_key="context"
    )
    
    generation_node = UniversalModelNode(
        model=generation_model,
        prompt_template=prompt_template,
        input_keys=["context", "query"],
        output_key="answer"
    )
    
    # Create output node
    class OutputNode(Node):
        def prep(self, shared):
            return shared.get("answer", "No answer generated.")
            
        def post(self, shared, prep_data, exec_result):
            shared["result"] = exec_result
            return "complete"
            
    output_node = OutputNode(name="OutputNode")
    
    # Connect nodes
    query_node - "retrieve" >> retrieval_node
    retrieval_node - "success" >> context_node
    context_node - "generate" >> generation_node
    generation_node - "next" >> output_node
    
    # Create fallbacks for error handling
    retrieval_node - "error" >> output_node
    
    # Create flow
    flow = Flow(start=query_node, name=name or "RAGFlow")
    
    return flow