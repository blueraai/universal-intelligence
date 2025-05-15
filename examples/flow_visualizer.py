"""Universal Agents - Flow Visualizer Demo

This script demonstrates the visualization capabilities of Universal Agents
by creating a flow and generating a visualization of its execution.
"""

import os
import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

# Import from the fully standalone demo
from fully_standalone_demo import Node, Flow, NodeConnection

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class VisualizableFlow(Flow):
    """Extended Flow class with visualization capabilities."""
    
    def __init__(self, start: Node, name: Optional[str] = None, 
                 visualization_path: Optional[str] = None):
        """Initialize a flow with visualization support."""
        super().__init__(start, name)
        self.visualization_path = visualization_path or "visualizations"
    
    def run(self, shared: Optional[Dict[str, Any]] = None, max_steps: int = 100) -> Dict[str, Any]:
        """Run the flow and generate visualization."""
        result = super().run(shared, max_steps)
        
        # Generate visualization
        self._generate_visualization(result.get("_flow_execution_path", []), result)
        
        return result
    
    def _generate_visualization(self, execution_path: List[str], state: Dict[str, Any]) -> None:
        """Generate a visualization of the flow execution."""
        try:
            # Create nodes data
            nodes_data = []
            for node in self.nodes:
                nodes_data.append({
                    "id": node.name,
                    "label": node.name,
                    "type": node.__class__.__name__,
                    "executed": node.name in execution_path
                })
            
            # Create edges data
            edges_data = []
            for node in self.nodes:
                for action, target in node.connections.items():
                    # Check if this edge was traversed during execution
                    was_traversed = False
                    for i in range(len(execution_path) - 1):
                        if execution_path[i] == node.name and execution_path[i+1] == target.name:
                            was_traversed = True
                            break
                    
                    edges_data.append({
                        "from": node.name,
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
            
            # Generate a simple HTML viewer
            self._generate_html_viewer(filepath)
            
        except Exception as e:
            logger.error(f"Error generating visualization: {str(e)}")
    
    def _generate_html_viewer(self, json_filepath: str) -> None:
        """Generate a simple HTML viewer for the visualization."""
        html_filepath = json_filepath.replace('.json', '.html')
        
        # Get the JSON filename only (not the full path)
        json_filename = os.path.basename(json_filepath)
        
        # Create the data directly in the HTML to avoid CORS issues
        with open(json_filepath, 'r') as f:
            json_data = f.read()
        
        html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Universal Agents Flow Visualization</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; }
        #flow-info { margin-bottom: 20px; }
        #flow-info h1 { margin-bottom: 5px; }
        #flow-info p { margin: 5px 0; }
        #flow-graph { width: 100%; height: 500px; border: 1px solid #ccc; }
        .node { padding: 10px; border-radius: 5px; }
        .node.executed { background-color: #b3e0ff; }
        .node:not(.executed) { background-color: #f0f0f0; }
        .edge { stroke-width: 2px; }
        .edge.traversed { stroke: #0066cc; }
        .edge:not(.traversed) { stroke: #cccccc; }
    </style>
    <script src="https://d3js.org/d3.v5.min.js"></script>
</head>
<body>
    <div id="flow-info">
        <h1 id="flow-name"></h1>
        <p>Execution Time: <span id="execution-time"></span></p>
        <p>Steps: <span id="steps"></span></p>
        <p>Execution Path: <span id="execution-path"></span></p>
    </div>
    
    <div id="flow-graph"></div>
    
    <script>
        // Load the JSON data directly to avoid CORS issues
        const data = JSON_DATA_PLACEHOLDER;
        
        // Display flow information
        document.getElementById('flow-name').textContent = data.flow_name;
        document.getElementById('execution-time').textContent = new Date(data.execution_time).toLocaleString();
        document.getElementById('steps').textContent = data.steps;
        document.getElementById('execution-path').textContent = data.execution_path.join(' → ');
        
        // Create a force-directed graph
        const width = document.getElementById('flow-graph').clientWidth;
        const height = document.getElementById('flow-graph').clientHeight;
        
        const svg = d3.select('#flow-graph')
            .append('svg')
            .attr('width', width)
            .attr('height', height);
        
        // Create a simulation for positioning nodes
        const simulation = d3.forceSimulation(data.nodes)
            .force('link', d3.forceLink(data.edges).id(d => d.id).distance(100))
            .force('charge', d3.forceManyBody().strength(-300))
            .force('center', d3.forceCenter(width / 2, height / 2));
        
        // Create the edges
        const edges = svg.append('g')
            .selectAll('line')
            .data(data.edges)
            .enter()
            .append('line')
            .attr('class', d => 'edge' + (d.traversed ? ' traversed' : ''))
            .style('stroke', d => d.traversed ? '#0066cc' : '#cccccc')
            .style('stroke-width', 2);
        
        // Add edge labels
        const edgeLabels = svg.append('g')
            .selectAll('text')
            .data(data.edges)
            .enter()
            .append('text')
            .text(d => d.label)
            .attr('font-size', 10)
            .attr('text-anchor', 'middle')
            .attr('dy', -5);
        
        // Create the nodes
        const nodes = svg.append('g')
            .selectAll('g')
            .data(data.nodes)
            .enter()
            .append('g')
            .call(d3.drag()
                .on('start', dragstarted)
                .on('drag', dragged)
                .on('end', dragended));
        
        // Add node rectangles
        nodes.append('rect')
            .attr('class', d => 'node' + (d.executed ? ' executed' : ''))
            .attr('width', 120)
            .attr('height', 40)
            .attr('rx', 5)
            .attr('ry', 5)
            .style('fill', d => d.executed ? '#b3e0ff' : '#f0f0f0')
            .style('stroke', '#666')
            .style('stroke-width', 1);
        
        // Add node labels
        nodes.append('text')
            .text(d => d.label)
            .attr('text-anchor', 'middle')
            .attr('dominant-baseline', 'middle')
            .attr('font-size', 12)
            .attr('x', 60)
            .attr('y', 20);
        
        // Update positions during simulation
        simulation.on('tick', () => {
            edges
                .attr('x1', d => d.source.x)
                .attr('y1', d => d.source.y)
                .attr('x2', d => d.target.x)
                .attr('y2', d => d.target.y);
            
            edgeLabels
                .attr('x', d => (d.source.x + d.target.x) / 2)
                .attr('y', d => (d.source.y + d.target.y) / 2);
            
            nodes.attr('transform', d => `translate(${d.x - 60}, ${d.y - 20})`);
        });
        
        // Drag functions
        function dragstarted(d) {
            if (!d3.event.active) simulation.alphaTarget(0.3).restart();
            d.fx = d.x;
            d.fy = d.y;
        }
        
        function dragged(d) {
            d.fx = d3.event.x;
            d.fy = d3.event.y;
        }
        
        function dragended(d) {
            if (!d3.event.active) simulation.alphaTarget(0);
            d.fx = null;
            d.fy = null;
        }
    </script>
</body>
</html>
"""
        
        # Replace placeholder with actual JSON data
        html_content = html_template.replace('JSON_DATA_PLACEHOLDER', json_data)
        
        # Write HTML file
        with open(html_filepath, 'w') as f:
            f.write(html_content)
        
        logger.info(f"HTML viewer saved to {html_filepath}")


# Demo Nodes (from fully_standalone_demo.py)
class InputNode(Node):
    """Node for handling user input."""
    
    def __init__(self, name: Optional[str] = None):
        super().__init__(name or "InputNode")
    
    def prep(self, shared: Dict[str, Any]) -> str:
        """Get input from shared state."""
        return shared.get("input", "Default input")
    
    def post(self, shared: Dict[str, Any], prep_data: str, exec_result: str) -> str:
        """Store the input and proceed to processing."""
        shared["user_input"] = exec_result
        return "process"


class ProcessingNode(Node):
    """Node for processing input."""
    
    def __init__(self, name: Optional[str] = None):
        super().__init__(name or "ProcessingNode")
    
    def prep(self, shared: Dict[str, Any]) -> str:
        """Get user input from shared state."""
        return shared.get("user_input", "")
    
    def exec(self, prep_data: str) -> str:
        """Transform the input."""
        return prep_data.upper()
    
    def post(self, shared: Dict[str, Any], prep_data: str, exec_result: str) -> str:
        """Store the processed input."""
        shared["processed_input"] = exec_result
        
        # Choose next action based on input content
        if "weather" in prep_data.lower():
            return "weather"
        elif "hello" in prep_data.lower():
            return "greeting"
        else:
            return "generate"


class WeatherNode(Node):
    """Node for handling weather queries."""
    
    def __init__(self, name: Optional[str] = None):
        super().__init__(name or "WeatherNode")
    
    def prep(self, shared: Dict[str, Any]) -> str:
        """Get the processed input."""
        return shared.get("processed_input", "")
    
    def exec(self, prep_data: str) -> Dict[str, Any]:
        """Generate weather information."""
        return {
            "condition": "sunny",
            "temperature": 75,
            "humidity": 45
        }
    
    def post(self, shared: Dict[str, Any], prep_data: str, exec_result: Dict[str, Any]) -> str:
        """Format weather information and store it."""
        weather_info = f"Weather is {exec_result['condition']} with a temperature of {exec_result['temperature']}°F and {exec_result['humidity']}% humidity."
        shared["response"] = weather_info
        return "output"


class GreetingNode(Node):
    """Node for generating greetings."""
    
    def __init__(self, name: Optional[str] = None):
        super().__init__(name or "GreetingNode")
    
    def exec(self, prep_data: str) -> str:
        """Generate a greeting."""
        return "Hello! How can I assist you today?"
    
    def post(self, shared: Dict[str, Any], prep_data: str, exec_result: str) -> str:
        """Store the greeting."""
        shared["response"] = exec_result
        return "output"


class GenerationNode(Node):
    """Node for generating responses."""
    
    def __init__(self, name: Optional[str] = None):
        super().__init__(name or "GenerationNode")
    
    def prep(self, shared: Dict[str, Any]) -> str:
        """Get the processed input."""
        return shared.get("processed_input", "")
    
    def exec(self, prep_data: str) -> str:
        """Generate a response based on the input."""
        return f"You said: {prep_data}. This is a demonstration of response generation based on your input."
    
    def post(self, shared: Dict[str, Any], prep_data: str, exec_result: str) -> str:
        """Store the generated response."""
        shared["response"] = exec_result
        return "output"


class OutputNode(Node):
    """Node for displaying the final output."""
    
    def __init__(self, name: Optional[str] = None):
        super().__init__(name or "OutputNode")
    
    def prep(self, shared: Dict[str, Any]) -> Dict[str, Any]:
        """Collect data for output."""
        return {
            "input": shared.get("user_input", ""),
            "response": shared.get("response", "No response generated.")
        }
    
    def exec(self, prep_data: Dict[str, Any]) -> Dict[str, Any]:
        """Format the output."""
        return prep_data
    
    def post(self, shared: Dict[str, Any], prep_data: Dict[str, Any], exec_result: Dict[str, Any]) -> str:
        """Display the output."""
        print(f"\nUser Input: {exec_result['input']}")
        print(f"Response: {exec_result['response']}")
        return "complete"


def main():
    """Main function that runs the visualizer demo."""
    print("\n=== Universal Agents Flow Visualizer Demo ===\n")
    print("This demo shows how to visualize the execution of a flow.")
    print("It will generate JSON and HTML files for visualization.\n")
    
    # Create nodes
    input_node = InputNode()
    processing_node = ProcessingNode()
    weather_node = WeatherNode()
    greeting_node = GreetingNode()
    generation_node = GenerationNode()
    output_node = OutputNode()
    
    # Connect nodes
    input_node - "process" >> processing_node
    processing_node - "weather" >> weather_node
    processing_node - "greeting" >> greeting_node
    processing_node - "generate" >> generation_node
    weather_node - "output" >> output_node
    greeting_node - "output" >> output_node
    generation_node - "output" >> output_node
    
    # Create visualizable flow
    flow = VisualizableFlow(
        start=input_node, 
        name="VisualizableFlow", 
        visualization_path="visualizations"
    )
    
    # Run the flow with different inputs to create visualizations
    inputs = [
        "Hello, how are you?",
        "What's the weather like today?",
        "Tell me something interesting"
    ]
    
    for i, input_text in enumerate(inputs):
        print(f"\n--- Running with input: '{input_text}' ---")
        
        # Initialize shared state
        shared = {"input": input_text}
        
        # Run the flow
        result = flow.run(shared)
        
        # Display execution information
        print(f"Flow completed in {result.get('_flow_steps')} steps")
        print(f"Execution path: {' -> '.join(result.get('_flow_execution_path'))}")
        print(f"Visualization saved to visualizations/ directory")
        print("-" * 50)
    
    print("\nDemo completed successfully!")
    print("You can find the visualization files in the 'visualizations' directory.")
    print("Open the HTML files in a web browser to see the interactive visualizations.")


if __name__ == "__main__":
    main()