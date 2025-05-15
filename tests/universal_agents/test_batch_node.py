"""
Tests for the BatchNode functionality in Universal Agents.
"""
import unittest
import sys
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from universal_agents.node import Node, BatchNode
from universal_agents.flow import Flow


class ArrayChunkNode(BatchNode):
    """A node that splits an array into chunks and processes each chunk."""
    
    def __init__(self, chunk_size=10, name=None):
        super().__init__(name=name)
        self.chunk_size = chunk_size
    
    def prep(self, shared):
        # Get array from shared state and split into chunks
        array = shared.get('input_array', [])
        chunks = []
        for start in range(0, len(array), self.chunk_size):
            end = min(start + self.chunk_size, len(array))
            chunks.append(array[start:end])
        return chunks
    
    def process_batch_item(self, chunk):
        # Process a single chunk (sum the elements)
        return sum(chunk)
    
    def post(self, shared, prep_data, exec_result):
        # Store chunk results in shared state
        shared['chunk_results'] = exec_result
        return "next"


class SumReduceNode(Node):
    """A node that sums up all chunk results."""
    
    def prep(self, shared):
        # Get chunk results from shared state
        return shared.get('chunk_results', [])
    
    def exec(self, prep_data):
        # Sum all chunk results
        return sum(prep_data)
    
    def post(self, shared, prep_data, exec_result):
        # Store the total sum in shared state
        shared['total'] = exec_result
        return "next"


class TestBatchNode(unittest.TestCase):
    
    def test_batch_processing(self):
        """Test basic batch processing functionality."""
        # Create a batch node
        batch_node = ArrayChunkNode(chunk_size=10, name="batch_node")
        
        # Prepare shared state with input array
        shared = {
            'input_array': list(range(30))  # [0,1,2,...,29]
        }
        
        # Run the node
        batch_node.run(shared)
        
        # Verify results
        results = shared['chunk_results']
        self.assertEqual(len(results), 3)  # 3 chunks
        self.assertEqual(results, [45, 145, 245])
        # First chunk: 0+1+2+...+9 = 45
        # Second chunk: 10+11+12+...+19 = 145
        # Third chunk: 20+21+22+...+29 = 245
    
    def test_map_reduce_flow(self):
        """Test a complete map-reduce flow with batch processing."""
        # Create nodes
        batch_node = ArrayChunkNode(chunk_size=10, name="batch_node")
        reduce_node = SumReduceNode(name="reduce_node")
        
        # Connect nodes
        batch_node - "next" >> reduce_node
        
        # Create flow
        flow = Flow(start=batch_node, name="map_reduce_flow")
        
        # Prepare shared state with input array
        shared = {
            'input_array': list(range(100))  # [0,1,2,...,99]
        }
        
        # Run the flow
        flow.run(shared)
        
        # Verify results
        expected_sum = sum(range(100))  # 4950
        self.assertEqual(shared['total'], expected_sum)
    
    def test_empty_batch(self):
        """Test batch processing with an empty input array."""
        # Create nodes
        batch_node = ArrayChunkNode(chunk_size=10, name="batch_node")
        reduce_node = SumReduceNode(name="reduce_node")
        
        # Connect nodes
        batch_node - "next" >> reduce_node
        
        # Create flow
        flow = Flow(start=batch_node, name="empty_batch_flow")
        
        # Prepare shared state with empty input array
        shared = {
            'input_array': []
        }
        
        # Run the flow
        flow.run(shared)
        
        # Verify results
        self.assertEqual(shared.get('chunk_results', None), [])
        self.assertEqual(shared.get('total', None), 0)
    
    def test_custom_chunk_size(self):
        """Test batch processing with different chunk sizes."""
        # Create a batch node with custom chunk size
        batch_node = ArrayChunkNode(chunk_size=7, name="custom_batch_node")
        
        # Prepare shared state with input array
        shared = {
            'input_array': list(range(20))  # [0,1,2,...,19]
        }
        
        # Run the node
        batch_node.run(shared)
        
        # Verify results
        results = shared['chunk_results']
        self.assertEqual(len(results), 3)  # 3 chunks with size 7,7,6
        self.assertEqual(results, [21, 84, 105])
        # First chunk: 0+1+2+3+4+5+6 = 21
        # Second chunk: 7+8+9+10+11+12+13 = 84
        # Third chunk: 14+15+16+17+18+19 = 105
    
    def test_single_item_chunks(self):
        """Test batch processing with chunk_size=1 (extreme case)."""
        # Create a batch node with chunk size 1
        batch_node = ArrayChunkNode(chunk_size=1, name="single_item_batch_node")
        
        # Prepare shared state with input array
        shared = {
            'input_array': list(range(5))  # [0,1,2,3,4]
        }
        
        # Run the node
        batch_node.run(shared)
        
        # Verify results
        results = shared['chunk_results']
        self.assertEqual(len(results), 5)  # 5 chunks with size 1 each
        self.assertEqual(results, [0, 1, 2, 3, 4])
    
    def test_batch_with_parallel_flag(self):
        """Test batch processing with parallel execution flag."""
        # Create a batch node with parallel execution
        batch_node = ArrayChunkNode(chunk_size=10, name="parallel_batch_node")
        batch_node.parallel = True  # Enable parallel execution
        
        # Prepare shared state with input array
        shared = {
            'input_array': list(range(30))  # [0,1,2,...,29]
        }
        
        # Run the node
        batch_node.run(shared)
        
        # Verify results (should be the same as sequential execution)
        results = shared['chunk_results']
        self.assertEqual(len(results), 3)  # 3 chunks
        self.assertEqual(results, [45, 145, 245])


if __name__ == '__main__':
    unittest.main()