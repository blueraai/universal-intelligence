"""Universal Agents - Map-Reduce Example

This example demonstrates how to create and run a Map-Reduce flow with Universal Agents,
using Universal Intelligence models for text analysis.
"""

import logging
import sys
import os
from typing import List, Dict, Any

# Add root to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from universal_agents.flow import Flow
from universal_agents.node import Node, BatchNode
from universal_agents.patterns import (
    MapNode, ModelMapNode, 
    ReduceNode, ModelReduceNode,
    create_map_reduce_flow
)
from universal_intelligence.core.universal_model import AbstractUniversalModel
from universal_intelligence.community.models.default import get_default_model

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Sample data for demonstration
SAMPLE_DOCUMENTS = [
    "The quick brown fox jumps over the lazy dog. The fox is known for its agility and speed.",
    "Artificial intelligence is transforming industries across the globe. Machine learning models are becoming more sophisticated.",
    "Climate change poses significant challenges for future generations. Renewable energy sources are critical for reducing emissions.",
    "The global economy faces uncertain times ahead. Inflation and supply chain issues continue to affect markets.",
    "Advances in healthcare technology are improving patient outcomes. Personalized medicine is becoming more accessible."
]

# Prompt templates
MAP_PROMPT_TEMPLATE = """
Analyze the following text and extract the main entities and concepts:

TEXT:
"{item}"

Provide a concise analysis with the key entities and concepts from this text.
"""

REDUCE_PROMPT_TEMPLATE = """
I have analyzed several documents and extracted the following key entities and concepts from each:

{items}

Based on these analyses, provide a comprehensive summary of the main themes and entities present across all documents.
Focus on connections between documents and overarching patterns.
"""


def run_map_reduce_example():
    """Run a complete map-reduce example using Universal Agents."""
    logger.info("Starting Map-Reduce example...")
    
    # Initialize the Universal Intelligence model
    model = get_default_model()
    logger.info(f"Using model: {model.__class__.__name__}")
    
    # Create a map-reduce flow
    flow = create_map_reduce_flow(
        map_model=model,
        reduce_model=model,
        map_prompt_template=MAP_PROMPT_TEMPLATE,
        reduce_prompt_template=REDUCE_PROMPT_TEMPLATE,
        name="document_analysis_flow"
    )
    
    # Prepare shared state with input data
    shared_state = {
        "items": SAMPLE_DOCUMENTS
    }
    
    # Run the flow
    logger.info("Running Map-Reduce flow...")
    result = flow.run(shared=shared_state)
    
    # Display results
    logger.info("Map-Reduce flow complete")
    logger.info("Document Analysis Result:")
    print("\n" + "-" * 80)
    print(result["result"])
    print("-" * 80 + "\n")
    
    # Return the result for potential further use
    return result


def run_custom_map_reduce_example():
    """Run a custom map-reduce example with manually created nodes."""
    logger.info("Starting custom Map-Reduce example...")
    
    # Initialize the Universal Intelligence model
    model = get_default_model()
    logger.info(f"Using model: {model.__class__.__name__}")
    
    # Create a custom function for mapping
    def extract_keywords(text: str) -> List[str]:
        """Extract keywords from text using simple heuristics."""
        # This is a simple implementation - in a real app, you might use NLP
        words = text.lower().replace(".", "").replace(",", "").split()
        stopwords = {"the", "a", "an", "is", "are", "for", "and", "or", "in", "of", "to", "with", "on"}
        keywords = [word for word in words if word not in stopwords and len(word) > 3]
        return list(set(keywords))
    
    # Create a custom function for reducing
    def combine_keywords(keyword_lists: List[List[str]]) -> Dict[str, int]:
        """Combine keyword lists and count frequencies."""
        keyword_counts = {}
        for keywords in keyword_lists:
            for keyword in keywords:
                if keyword in keyword_counts:
                    keyword_counts[keyword] += 1
                else:
                    keyword_counts[keyword] = 1
        
        # Sort by frequency
        return dict(sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True))
    
    # Create nodes
    map_node = MapNode(
        map_fn=extract_keywords,
        input_key="documents",
        output_key="keywords",
        name="keyword_extractor"
    )
    
    reduce_node = ReduceNode(
        reduce_fn=combine_keywords,
        input_key="keywords",
        output_key="keyword_counts",
        name="keyword_counter"
    )
    
    summary_node = ModelReduceNode(
        model=model,
        prompt_template="""
        I have analyzed several documents and extracted the following keywords with their frequency counts:
        
        {items}
        
        Based on these keywords, provide a brief summary of the main themes present in the documents.
        Focus on the most frequent keywords and what they might tell us about the content.
        """,
        input_key="keyword_counts",
        output_key="summary",
        items_key="items",
        name="summary_generator"
    )
    
    # Connect nodes
    map_node - "next" >> reduce_node - "next" >> summary_node
    
    # Create flow
    flow = Flow(start=map_node, name="custom_keyword_analysis_flow")
    
    # Prepare shared state with input data
    shared_state = {
        "documents": SAMPLE_DOCUMENTS
    }
    
    # Run the flow
    logger.info("Running custom Map-Reduce flow...")
    result = flow.run(shared=shared_state)
    
    # Display results
    logger.info("Custom Map-Reduce flow complete")
    logger.info("Keyword Analysis:")
    print("\nKeyword frequency counts:")
    for keyword, count in result["keyword_counts"].items():
        if count > 1:  # Only show keywords that appear in multiple documents
            print(f"  {keyword}: {count}")
            
    print("\nSummary:")
    print(result["summary"])
    
    # Return the result for potential further use
    return result


if __name__ == "__main__":
    print("\n=== Running Map-Reduce Example ===\n")
    run_map_reduce_example()
    
    print("\n=== Running Custom Map-Reduce Example ===\n")
    run_custom_map_reduce_example()