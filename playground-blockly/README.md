# Universal Intelligence - Blockly Playground 🧩

A visual programming interface for Universal Intelligence using Google's Blockly. Build AI applications by dragging and dropping blocks - runs entirely in your browser!

## Features

- **Visual Programming**: Create AI workflows using drag-and-drop blocks
- **Component Library**: Pre-built blocks for Models, Tools, and Agents
- **Browser-Based**: All code runs in your browser using WebLLM and JavaScript
- **Code Generation**: Automatically generate Python or JavaScript code
- **Live Execution**: Run your visual programs instantly without a backend
- **Multi-Language Support**: View generated code in Python or JavaScript

## Getting Started

### Prerequisites

- Node.js 16+ and npm
- A modern web browser (Chrome, Firefox, Edge, Safari)

### Setup

1. First, build Universal Intelligence for web (from repository root):
   ```bash
   npm install
   npm run build
   ```

2. Install playground dependencies:
   ```bash
   cd playground-blockly
   npm install
   ```

### Running the Playground

#### Development Mode (with Hot Module Replacement)
```bash
cd playground-blockly
npm run dev
```

This will open your browser automatically at `http://localhost:8001/playground-blockly/`

#### Production Preview
```bash
cd playground-blockly
npm run build
npm run preview
```


## Block Categories

### 🧠 Models
- **Local Model**: Create a model that runs on your hardware
- **Remote Model**: Connect to cloud-based models (OpenAI, Anthropic, etc.)
- **Model Process**: Send prompts to models and get responses

### 🔧 Tools
- **Printer Tool**: Output text to console
- **API Tool**: Make HTTP requests
- **MCP Tool**: Connect to Model Context Protocol servers
- **Tool Call**: Execute tool methods

### 🤖 Agents
- **Create Agent**: Build an agent with models and tools
- **Agent Process**: Have agents complete tasks
- **Connect Tools/Agents**: Dynamically add capabilities

## Example Workflows

### Simple Model Chat
1. Drag a "Create Local Model" block
2. Connect it to a "Model Process" block
3. Add a text block with your prompt
4. Run to see the response!

### Agent with Tools
1. Create a Local Model
2. Create a Printer Tool
3. Create an Agent with the model and tool
4. Use Agent Process to give it a task
5. Watch it use the tool to complete the task!

## Tips

- Start with the pre-loaded example to understand the basics
- Use variables to reuse models across multiple agents
- Connect multiple tools to create powerful agents
- Switch between Python/JavaScript to see code in both languages
- Copy generated code to use in your own projects

## How It Works

1. **Blockly Interface**: Visual blocks represent UIN components
2. **Code Generation**: Blocks are converted to JavaScript code
3. **Browser Execution**: Generated code runs directly in the browser
4. **WebLLM Integration**: Local models run using WebGPU in your browser
5. **Remote Models**: Connect to cloud APIs (OpenRouter, OpenAI, etc.)

## Architecture

The playground consists of:
- `index.html`: Main interface with ES modules for UIN
- `custom-blocks.js`: Universal Intelligence block definitions
- `app-web.js`: Browser-based execution logic
- `styles.css`: Visual styling
- `vite.config.js`: Vite development server configuration

## Notes

- **Browser-Only**: All AI processing happens in your browser
- **No Backend**: Everything runs client-side in the browser
- **API Keys**: For remote models, use your own API keys
- **Local Models**: Require WebGPU support in your browser
- **Privacy**: Your code and data never leave your browser