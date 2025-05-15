"""Universal Agents - Flow Visualization

This module provides utilities for visualizing Universal Agents flows,
helping users understand flow structures and debug execution paths.
"""
import logging
import json
import os
from typing import Any, Dict, List, Optional, Set, Tuple, Union
import html
from datetime import datetime

from .node import Node
from .flow import Flow

logger = logging.getLogger(__name__)

def generate_flow_visualization(
    flow: Flow,
    output_path: Optional[str] = None,
    title: Optional[str] = None,
    include_execution_data: bool = False
) -> str:
    """Generate an HTML visualization for a flow.
    
    Args:
        flow: The flow to visualize
        output_path: Optional path to save the HTML file (if None, returns the HTML)
        title: Optional title for the visualization
        include_execution_data: Whether to include execution data if available
        
    Returns:
        HTML string if output_path is None, otherwise path to generated file
    """
    # Default title if not provided
    if not title:
        title = flow.name or "Flow Visualization"
    
    # Collect nodes and connections
    nodes = []
    edges = []
    node_ids = {}
    
    # Assign IDs to nodes
    for i, node in enumerate(flow.nodes):
        node_id = f"node_{i}"
        node_ids[node] = node_id
        
        # Create node data
        node_data = {
            "id": node_id,
            "label": node.name,
            "type": node.__class__.__name__
        }
        
        # Add execution data if available and requested
        if include_execution_data and hasattr(node, "_execution_data"):
            exec_data = node._execution_data
            if exec_data:
                last_execution = exec_data[-1] if exec_data else {}
                node_data["execution"] = {
                    "count": len(exec_data),
                    "last_action": last_execution.get("action", "unknown"),
                    "last_time": last_execution.get("timestamp", "unknown")
                }
        
        nodes.append(node_data)
    
    # Create edges for connections
    edge_id = 0
    for node in flow.nodes:
        for action, target in node.connections.items():
            if target in node_ids:
                edge_id += 1
                edges.append({
                    "id": f"edge_{edge_id}",
                    "source": node_ids[node],
                    "target": node_ids[target],
                    "label": action
                })
    
    # Create graph data structure
    graph_data = {
        "nodes": nodes,
        "edges": edges,
        "metadata": {
            "title": title,
            "created": datetime.now().isoformat(),
            "flow_name": flow.name,
            "node_count": len(nodes),
            "edge_count": len(edges)
        }
    }
    
    # Generate HTML 
    html_content = _generate_visualization_html(title, graph_data)
    
    # Save to file if path provided
    if output_path:
        # Ensure directory exists
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        
        # Save HTML file
        with open(output_path, "w") as f:
            f.write(html_content)
        
        # Save JSON data for reference
        json_path = output_path.replace(".html", ".json")
        with open(json_path, "w") as f:
            json.dump(graph_data, f, indent=2)
        
        logger.info(f"Flow visualization saved to {output_path}")
        return output_path
    
    # Return HTML string if no path provided
    return html_content


def _generate_visualization_html(title: str, graph_data: Dict[str, Any]) -> str:
    """Generate HTML for flow visualization using D3.js.
    
    Args:
        title: Title for the visualization
        graph_data: Graph data structure with nodes and edges
        
    Returns:
        HTML string with embedded visualization
    """
    # Escape data for safe embedding
    json_data = html.escape(json.dumps(graph_data))
    
    # HTML template with embedded D3.js
    html_template = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{title}</title>
    <script src="https://d3js.org/d3.v7.min.js"></script>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f5f5f5;
        }}
        #container {{
            width: 100%;
            height: 100vh;
            overflow: hidden;
        }}
        svg {{
            width: 100%;
            height: 100%;
        }}
        .node {{
            cursor: pointer;
        }}
        .node rect {{
            stroke: #333;
            stroke-width: 1.5px;
            fill: #fff;
        }}
        .node.start rect {{
            fill: #d4edda;
            stroke: #28a745;
        }}
        .node text {{
            font-size: 14px;
            text-anchor: middle;
            dominant-baseline: middle;
        }}
        .link {{
            fill: none;
            stroke: #999;
            stroke-width: 1.5px;
        }}
        .edgePath path {{
            stroke: #333;
            stroke-width: 1.5px;
            fill: none;
        }}
        .edgeLabel rect {{
            fill: white;
        }}
        .edgeLabel text {{
            font-size: 12px;
            text-anchor: middle;
            dominant-baseline: middle;
        }}
        #info-panel {{
            position: fixed;
            top: 10px;
            right: 10px;
            width: 300px;
            padding: 15px;
            background: white;
            border: 1px solid #ddd;
            border-radius: 5px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}
        #controls {{
            position: fixed;
            bottom: 10px;
            left: 10px;
            padding: 10px;
            background: white;
            border: 1px solid #ddd;
            border-radius: 5px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}
        button {{
            margin: 2px;
            padding: 5px 10px;
        }}
    </style>
</head>
<body>
    <div id="container"></div>
    <div id="info-panel">
        <h2>{title}</h2>
        <p><strong>Nodes:</strong> <span id="node-count">{len(graph_data["nodes"])}</span></p>
        <p><strong>Connections:</strong> <span id="edge-count">{len(graph_data["edges"])}</span></p>
        <div id="node-details">
            <h3>Node Details</h3>
            <p>Click on a node to see details</p>
        </div>
    </div>
    <div id="controls">
        <button id="reset-zoom">Reset Zoom</button>
        <button id="toggle-physics">Toggle Physics</button>
        <button id="toggle-labels">Toggle Labels</button>
    </div>
    
    <script>
    // Graph data
    const graphData = JSON.parse('{json_data}');
    
    // D3.js force directed graph
    const width = window.innerWidth;
    const height = window.innerHeight;
    
    // Setup SVG
    const svg = d3.select('#container')
        .append('svg')
        .attr('width', width)
        .attr('height', height);
    
    // Add zoom capability
    const g = svg.append('g');
    
    const zoom = d3.zoom()
        .scaleExtent([0.1, 4])
        .on('zoom', (event) => {{
            g.attr('transform', event.transform);
        }});
    
    svg.call(zoom);
    
    // Force simulation
    let physicsEnabled = true;
    const simulation = d3.forceSimulation(graphData.nodes)
        .force('link', d3.forceLink(graphData.edges).id(d => d.id).distance(150))
        .force('charge', d3.forceManyBody().strength(-300))
        .force('center', d3.forceCenter(width / 2, height / 2))
        .force('collision', d3.forceCollide().radius(80));
    
    // Draw links
    const link = g.append('g')
        .selectAll('path')
        .data(graphData.edges)
        .enter().append('path')
        .attr('class', 'link')
        .attr('marker-end', 'url(#arrowhead)');
    
    // Arrowhead marker
    svg.append('defs').append('marker')
        .attr('id', 'arrowhead')
        .attr('viewBox', '0 -5 10 10')
        .attr('refX', 25)
        .attr('refY', 0)
        .attr('markerWidth', 6)
        .attr('markerHeight', 6)
        .attr('orient', 'auto')
        .append('path')
        .attr('d', 'M0,-5L10,0L0,5')
        .attr('fill', '#999');
    
    // Draw nodes
    const node = g.append('g')
        .selectAll('.node')
        .data(graphData.nodes)
        .enter().append('g')
        .attr('class', d => 'node ' + (d.id === 'node_0' ? 'start' : ''))
        .call(d3.drag()
            .on('start', dragstarted)
            .on('drag', dragged)
            .on('end', dragended));
    
    // Node rectangles
    node.append('rect')
        .attr('width', d => Math.max(d.label.length * 10, 100))
        .attr('height', 50)
        .attr('x', d => -Math.max(d.label.length * 10, 100) / 2)
        .attr('y', -25)
        .attr('rx', 5)
        .attr('ry', 5);
    
    // Node labels
    node.append('text')
        .text(d => d.label)
        .attr('class', 'node-label');
    
    // Edge labels
    const edgeLabels = g.append('g')
        .selectAll('.edgeLabel')
        .data(graphData.edges)
        .enter().append('g')
        .attr('class', 'edgeLabel');
    
    edgeLabels.append('rect')
        .attr('width', d => Math.max(d.label.length * 8, 30))
        .attr('height', 20)
        .attr('x', d => -Math.max(d.label.length * 8, 30) / 2)
        .attr('y', -10)
        .attr('rx', 3)
        .attr('ry', 3);
    
    edgeLabels.append('text')
        .text(d => d.label);
    
    // Update positions on simulation tick
    simulation.on('tick', () => {{
        link.attr('d', d => {{
            const sourceX = d.source.x;
            const sourceY = d.source.y;
            const targetX = d.target.x;
            const targetY = d.target.y;
            
            return `M${{sourceX}},${{sourceY}} L${{targetX}},${{targetY}}`;
        }});
        
        node.attr('transform', d => `translate(${{d.x}},${{d.y}})`);
        
        edgeLabels.attr('transform', d => {{
            const midX = (d.source.x + d.target.x) / 2;
            const midY = (d.source.y + d.target.y) / 2;
            return `translate(${{midX}},${{midY}})`;
        }});
    }});
    
    // Drag functions
    function dragstarted(event, d) {{
        if (!event.active && physicsEnabled) simulation.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
    }}
    
    function dragged(event, d) {{
        d.fx = event.x;
        d.fy = event.y;
    }}
    
    function dragended(event, d) {{
        if (!event.active && physicsEnabled) simulation.alphaTarget(0);
        if (physicsEnabled) {{
            d.fx = null;
            d.fy = null;
        }}
    }}
    
    // Node click handler for details
    node.on('click', (event, d) => {{
        const nodeDetails = document.getElementById('node-details');
        let html = `<h3>Node: ${{d.label}}</h3>`;
        html += `<p><strong>Type:</strong> ${{d.type}}</p>`;
        
        if (d.execution) {{
            html += `<p><strong>Executions:</strong> ${{d.execution.count}}</p>`;
            html += `<p><strong>Last Action:</strong> ${{d.execution.last_action}}</p>`;
            html += `<p><strong>Last Time:</strong> ${{d.execution.last_time}}</p>`;
        }}
        
        // Show connections
        html += `<p><strong>Connections:</strong></p>`;
        const connections = graphData.edges.filter(e => e.source.id === d.id || e.target.id === d.id);
        if (connections.length > 0) {{
            html += `<ul>`;
            connections.forEach(conn => {{
                if (conn.source.id === d.id) {{
                    html += `<li>→ ${{conn.label}} → ${{conn.target.label}}</li>`;
                }} else {{
                    html += `<li>← ${{conn.label}} ← ${{conn.source.label}}</li>`;
                }}
            }});
            html += `</ul>`;
        }} else {{
            html += `<p>No connections</p>`;
        }}
        
        nodeDetails.innerHTML = html;
    }});
    
    // Control buttons
    document.getElementById('reset-zoom').addEventListener('click', () => {{
        svg.transition().duration(750).call(
            zoom.transform,
            d3.zoomIdentity,
            d3.zoomTransform(svg.node()).invert([width / 2, height / 2])
        );
    }});
    
    document.getElementById('toggle-physics').addEventListener('click', () => {{
        physicsEnabled = !physicsEnabled;
        if (physicsEnabled) {{
            simulation.restart();
            node.each(d => {{
                d.fx = null;
                d.fy = null;
            }});
        }} else {{
            simulation.stop();
            node.each(d => {{
                d.fx = d.x;
                d.fy = d.y;
            }});
        }}
    }});
    
    document.getElementById('toggle-labels').addEventListener('click', () => {{
        const edgeLabelsVisible = edgeLabels.style('display') !== 'none';
        edgeLabels.style('display', edgeLabelsVisible ? 'none' : 'block');
    }});
    </script>
</body>
</html>
"""
    
    return html_template


def visualize_execution_path(
    flow: Flow, 
    execution_trace: List[Dict[str, Any]],
    output_path: Optional[str] = None,
    title: Optional[str] = None
) -> str:
    """Generate a visualization of a specific execution path through a flow.
    
    Args:
        flow: The flow that was executed
        execution_trace: Trace of nodes visited during execution
        output_path: Optional path to save the HTML file
        title: Optional title for the visualization
        
    Returns:
        HTML string if output_path is None, otherwise path to generated file
    """
    # Default title
    if not title:
        title = f"{flow.name} Execution Path" if flow.name else "Flow Execution Path"
    
    # Attach execution data to nodes
    for node in flow.nodes:
        node._execution_data = []
    
    # Process execution trace
    for step in execution_trace:
        node = step.get("node")
        if node in flow.nodes:
            if not hasattr(node, "_execution_data"):
                node._execution_data = []
            
            node._execution_data.append({
                "action": step.get("action", "unknown"),
                "timestamp": step.get("timestamp", datetime.now().isoformat()),
                "data": step.get("data", {})
            })
    
    # Generate visualization with execution data
    return generate_flow_visualization(
        flow=flow,
        output_path=output_path,
        title=title,
        include_execution_data=True
    )