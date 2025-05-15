# PocketFlow Visualization

This directory contains tools for visualizing PocketFlow workflow graphs using interactive D3.js visualizations.

## Overview

The visualization tools allow you to:

1. View PocketFlow nodes and flows as an interactive graph
2. See how different flows connect to each other
3. Understand the relationships between nodes within flows

## Features

- **Interactive Graph**: Nodes can be dragged to reorganize the layout
- **Group Visualization**: Flows are displayed as groups with dashed borders
- **Inter-Group Links**: Connections between flows are shown as dashed lines connecting group boundaries
- **Action Labels**: Edge labels show the actions that trigger transitions between nodes

## Requirements

- Python 3.6 or higher
- Modern web browser (Chrome, Firefox, Edge) for viewing the visualizations

## Usage

### 1. Basic Visualization

To visualize a PocketFlow graph, you can use the `visualize_flow` function in `visualize.py`:

```python
from visualize import visualize_flow
from your_flow_module import your_flow

# Generate visualization
visualize_flow(your_flow, "Your Flow Name")
```

This will:
1. Print a Mermaid diagram to the console
2. Generate a D3.js visualization in the `./viz` directory

### 2. Running the Example

The included example shows an order processing pipeline with payment, inventory, and shipping flows:

```bash
# Navigate to the directory
cd cookbook/pocketflow-minimal-flow2flow

# Run the visualization script
python visualize.py
```

This will generate visualization files in the `./viz` directory.

### 3. Viewing the Visualization

After running the script:

1. Host with 
   ```
   cd ./viz/
   ```

2. Interact with the visualization:
   - **Drag nodes** to reorganize
   - **Hover over nodes** to see node names
   - **Observe connections** between nodes and flows

## Customizing the Visualization

### Adjusting Layout Parameters

You can adjust the force simulation parameters in `visualize.py` to change how nodes and groups are positioned:

```javascript
// Create a force simulation
const simulation = d3.forceSimulation(data.nodes)
    // Controls the distance between connected nodes
    .force("link", d3.forceLink(data.links).id(d => d.id).distance(100))
    // Controls how nodes repel each other - lower values bring nodes closer
    .force("charge", d3.forceManyBody().strength(-30))
    // Centers the entire graph in the SVG
    .force("center", d3.forceCenter(width / 2, height / 2))
    // Prevents nodes from overlapping - acts like a minimum distance
    .force("collide", d3.forceCollide().radius(50));
```

### Styling

Adjust the CSS styles in the HTML template inside `create_d3_visualization` function to change colors, shapes, and other visual properties.

## How It Works

The visualization process consists of three main steps:

1. **Flow to JSON Conversion**: The `flow_to_json` function traverses the PocketFlow graph and converts it to a structure with nodes, links, and group information.

2. **D3.js Visualization**: The JSON data is used to create an interactive D3.js visualization with:
   - Nodes represented as circles
   - Flows represented as dashed rectangles containing nodes
   - Links showing connections within and between flows

3. **Group Boundary Connections**: The visualization calculates intersection points with group boundaries to ensure inter-group links connect at the borders rather than centers.

## Extending the Visualization

You can extend the visualization tools by:

1. Adding new node shapes
2. Implementing additional layout algorithms
3. Adding tooltips with more detailed information
4. Creating animation for flow execution

## Troubleshooting

If you encounter any issues:

- Make sure your flow objects are properly constructed with nodes connected correctly
- Check the browser console for any JavaScript errors
- Verify that the generated JSON data structure matches what you expect

## Example Output

The visualization displays:
- Payment processing flow nodes
- Inventory management flow nodes
- Shipping flow nodes
- Group boundaries around each flow
- Connections between flows (Payment → Inventory → Shipping)
