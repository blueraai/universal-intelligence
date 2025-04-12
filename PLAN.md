# Universal Intelligence Documentation Plan

This document outlines the comprehensive plan for the Universal Intelligence documentation and interactive site.

## Part 1: Core Documentation (Completed)

We've completed the foundational documentation that provides detailed explanations of the architecture:

```
docs/
├── 00_system_architecture.md - High-level overview with system diagrams
├── 01_overview.md - Project goals and introduction
├── 02_core_architecture.md - Core interfaces and abstractions
├── 03_plugin_architecture.md - Community component extensibility
├── samples/ - Example implementations inspired by ADK patterns
│   ├── basic_agent.py - Simple model usage
│   ├── tool_using_agent.py - Agent with tools integration
│   ├── multi_agent_system.py - Agents working together
│   ├── rag_agent.py - Retrieval-augmented generation example
│   ├── specialized_agent.py - Domain-specific implementation
│   └── README.md - Sample usage instructions
```

The documentation includes detailed mermaid diagrams, code samples, and thorough explanations of all components.

## Part 2: Interactive 3D Documentation Site

Building on our comprehensive documentation, we're creating an immersive, interactive 3D documentation experience that will revolutionize how users understand the Universal Intelligence framework.

### Conceptual Vision: 3D Universal Intelligence Universe

The site will present Universal Intelligence as an interactive 3D system where users can:
- Explore the architecture visually in an immersive environment
- See components and their connections in a spatial context
- Interact with elements to reveal detailed documentation
- Run live code examples in an integrated playground
- Experience guided tours through the system's functionality

### Technical Architecture

#### Frontend Stack
- **React** (v18+): Component-based UI architecture
- **Three.js** & **React Three Fiber**: 3D visualization framework
- **@react-three/drei**: Higher-level Three.js components
- **Zustand**: Lightweight state management
- **Tailwind CSS**: Utility-first styling
- **MDX**: Enhanced markdown with interactive components
- **Sandpack** (from CodeSandbox): In-browser code execution environment
- **react-markdown**: Documentation rendering
- **Framer Motion**: Animations and transitions

#### Backend Stack (for Code Playground)
- **Node.js**: Runtime environment
- **Express**: Web server framework
- **Socket.io**: Real-time communication
- **Docker**: Containerization for code execution
- **Redis**: Session management and caching

### File Structure

```
ui-docs/
├── public/                    # Static assets
│   ├── models/                # 3D models for components
│   │   ├── agent.glb
│   │   ├── model.glb
│   │   ├── tool.glb
│   │   └── ...
│   ├── textures/              # Visual textures
│   └── fonts/                 # Custom fonts
├── src/
│   ├── components/
│   │   ├── 3d/                # Three.js components
│   │   │   ├── Scene.jsx      # Main 3D scene container
│   │   │   ├── Agent.jsx      # Agent component visualization
│   │   │   ├── Model.jsx      # Model component visualization
│   │   │   ├── Tool.jsx       # Tool component visualization
│   │   │   ├── Connection.jsx # Component connections
│   │   │   └── ...
│   │   ├── ui/                # Interface components
│   │   │   ├── Navbar.jsx
│   │   │   ├── Sidebar.jsx
│   │   │   ├── Modal.jsx
│   │   │   ├── CodePlayground.jsx
│   │   │   └── ...
│   │   └── docs/              # Documentation components
│   │       ├── ContentPanel.jsx
│   │       ├── Diagram.jsx
│   │       ├── CodeBlock.jsx
│   │       └── ...
│   ├── content/               # MDX content from our docs
│   │   ├── overview/
│   │   ├── architecture/
│   │   ├── examples/
│   │   └── tutorials/
│   ├── hooks/                 # Custom React hooks
│   │   ├── use3DNavigation.js
│   │   ├── useCodeExecution.js
│   │   └── ...
│   ├── store/                 # State management
│   │   ├── navigationStore.js
│   │   ├── documentationStore.js
│   │   ├── codeStore.js
│   │   └── ...
│   ├── utils/                 # Helper functions
│   │   ├── animations.js
│   │   ├── threeHelpers.js
│   │   └── ...
│   ├── pages/                 # Page components
│   │   ├── Home.jsx
│   │   ├── Explorer.jsx
│   │   ├── Playground.jsx
│   │   └── ...
│   ├── App.jsx                # Main application component
│   └── index.js               # Entry point
├── server/                    # Backend for code execution
│   ├── index.js               # Server entry point
│   ├── socket.js              # Socket.io configuration
│   ├── sandbox.js             # Sandboxed execution environment
│   ├── docker/                # Docker configuration
│   │   ├── Dockerfile
│   │   └── docker-compose.yml
│   └── ...
├── package.json
└── README.md
```

### Key Features

#### 1. Interactive 3D Architecture Explorer

```javascript
// src/components/3d/Scene.jsx (Simplified example)
function ArchitectureScene() {
  const { selectedComponent, setSelectedComponent } = useStore();

  return (
    <Canvas camera={{ position: [0, 0, 10], fov: 50 }}>
      <ambientLight intensity={0.5} />
      <pointLight position={[10, 10, 10]} />

      {/* Core Components Group */}
      <group position={[0, 0, 0]}>
        <Model
          position={[0, 2, 0]}
          onClick={() => setSelectedComponent('model')}
          isSelected={selectedComponent === 'model'}
        />
        <Tool
          position={[-2, 0, 0]}
          onClick={() => setSelectedComponent('tool')}
          isSelected={selectedComponent === 'tool'}
        />
        <Agent
          position={[2, 0, 0]}
          onClick={() => setSelectedComponent('agent')}
          isSelected={selectedComponent === 'agent'}
        />

        {/* Connection lines between components */}
        <Connection start={[2, 0, 0]} end={[0, 2, 0]} />
        <Connection start={[2, 0, 0]} end={[-2, 0, 0]} />
      </group>

      {/* Community Implementations */}
      <group position={[0, -4, 0]}>
        {/* Dynamically generated model implementations */}
        {models.map((model, index) => (
          <ModelImplementation
            key={model.id}
            model={model}
            position={[index * 2 - models.length, 0, 0]}
          />
        ))}
      </group>

      <OrbitControls enableZoom={true} enablePan={true} />
    </Canvas>
  );
}
```

The 3D scene will be fully interactive with:
- Orbital camera controls for exploring the architecture
- Clickable components that highlight when selected
- Animated connections between components
- Dynamic loading of community implementations
- Visual effects showing data flow through the system

#### 2. Code Playground with Sandpack Integration

```javascript
// src/components/ui/CodePlayground.jsx (Simplified example)
import { Sandpack } from "@codesandbox/sandpack-react";
import { useCodeStore } from "../../store/codeStore";

function CodePlayground() {
  const { currentExample, output, setOutput, isExecuting, executeCode } = useCodeStore();

  return (
    <div className="code-playground-container">
      <div className="playground-header">
        <h3>Interactive Code Example</h3>
        <select onChange={(e) => loadExample(e.target.value)}>
          {examples.map(ex => (
            <option key={ex.id} value={ex.id}>{ex.name}</option>
          ))}
        </select>
        <button
          onClick={executeCode}
          disabled={isExecuting}
        >
          {isExecuting ? "Running..." : "Run Code"}
        </button>
      </div>

      <div className="editor-output-container">
        <Sandpack
          template="python"
          files={{
            "/main.py": currentExample.code,
          }}
          customSetup={{
            dependencies: {
              "universal-intelligence": "latest"
            }
          }}
          options={{
            showLineNumbers: true,
            showInlineErrors: true,
            editorHeight: 400,
            editorWidthPercentage: 60,
          }}
          theme="dark"
        />

        <div className="output-panel">
          <h4>Output</h4>
          <pre>{output}</pre>
        </div>
      </div>

      <div className="playground-footer">
        <p>Try modifying the code and click "Run Code" to see the results!</p>
      </div>
    </div>
  );
}
```

For more complex execution scenarios, we'll implement a backend service:

```javascript
// server/sandbox.js (Simplified example)
const { exec } = require('child_process');
const Docker = require('dockerode');
const docker = new Docker();

async function executeCodeInContainer(code, socketId) {
  const container = await docker.createContainer({
    Image: 'universal-intelligence-sandbox',
    Cmd: ['python', '-c', code],
    HostConfig: {
      Memory: 512 * 1024 * 1024, // 512MB limit
      MemorySwap: 512 * 1024 * 1024,
      CpuPeriod: 100000,
      CpuQuota: 50000, // 50% CPU limit
      NetworkMode: 'none', // No network access
    },
  });

  await container.start();

  // Stream output to client
  const stream = await container.logs({
    follow: true,
    stdout: true,
    stderr: true,
  });

  stream.on('data', (chunk) => {
    io.to(socketId).emit('code-output', chunk.toString());
  });

  // Set timeout for long-running code
  setTimeout(async () => {
    try {
      await container.stop();
      io.to(socketId).emit('code-output', '\n[Execution timed out]');
    } catch (e) {
      // Container might have already completed
    }
  }, 30000); // 30 second timeout

  // Clean up when container finishes
  container.wait(async () => {
    io.to(socketId).emit('code-execution-complete');
    await container.remove();
  });
}
```

The code playground will support:
- Full Python execution environment
- Universal Intelligence package pre-installed
- Real-time output streaming
- Error handling with helpful contextual messages
- Secure execution in isolated containers
- Example library with all the sample code
- Connection to the 3D visualization (highlighting relevant components)

#### 3. Visual Learning Modes

The UI will include multiple ways to learn the system:

```javascript
// src/pages/Explorer.jsx (Simplified example)
function Explorer() {
  const { viewMode, setViewMode } = useNavigationStore();

  return (
    <div className="explorer-container">
      <div className="view-mode-selector">
        <button
          className={viewMode === 'guided' ? 'active' : ''}
          onClick={() => setViewMode('guided')}
        >
          Guided Tour
        </button>
        <button
          className={viewMode === 'free' ? 'active' : ''}
          onClick={() => setViewMode('free')}
        >
          Free Exploration
        </button>
        <button
          className={viewMode === 'map' ? 'active' : ''}
          onClick={() => setViewMode('map')}
        >
          Concept Map
        </button>
      </div>

      {viewMode === 'guided' && <GuidedTour />}
      {viewMode === 'free' && <FreeExploration />}
      {viewMode === 'map' && <ConceptMap />}
    </div>
  );
}
```

#### 4. Dynamic Sequence Visualizer

```javascript
// src/components/docs/SequenceVisualizer.jsx (Simplified example)
function SequenceVisualizer({ steps }) {
  const [currentStep, setCurrentStep] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);

  useEffect(() => {
    if (isPlaying) {
      const timer = setInterval(() => {
        setCurrentStep(prev => (prev < steps.length - 1 ? prev + 1 : 0));
      }, 1500);
      return () => clearInterval(timer);
    }
  }, [isPlaying, steps.length]);

  return (
    <div className="sequence-visualizer">
      <div className="sequence-controls">
        <button onClick={() => setIsPlaying(!isPlaying)}>
          {isPlaying ? 'Pause' : 'Play'}
        </button>
        <input
          type="range"
          min={0}
          max={steps.length - 1}
          value={currentStep}
          onChange={(e) => {
            setCurrentStep(parseInt(e.target.value));
            setIsPlaying(false);
          }}
        />
        <span>{currentStep + 1} / {steps.length}</span>
      </div>

      <div className="sequence-diagram">
        {steps[currentStep].participants.map((participant, i) => (
          <div key={i} className="participant">
            <div className="participant-label">{participant}</div>
            <div className="participant-line" />
          </div>
        ))}

        {steps[currentStep].messages.map((msg, i) => (
          <div
            key={i}
            className="message"
            style={{
              left: `${msg.from * 150}px`,
              width: `${(msg.to - msg.from) * 150}px`,
              top: `${100 + i * 50}px`,
            }}
          >
            <div className="message-line" />
            <div className="message-label">{msg.label}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
```

### Visual Theme and Style Guide

```css
/* src/styles/theme.css (Simplified example) */
:root {
  /* Color Palette */
  --primary: #4a00e0;
  --primary-light: #7028e4;
  --secondary: #2dcddf;
  --accent: #00ff9d;
  --background-dark: #0a0e17;
  --background-light: #141a24;
  --text-primary: #ffffff;
  --text-secondary: #b8c7e0;

  /* Typography */
  --font-main: 'Inter', sans-serif;
  --font-code: 'Fira Code', monospace;
  --font-heading: 'Space Grotesk', sans-serif;

  /* Spacing */
  --space-xs: 0.25rem;
  --space-sm: 0.5rem;
  --space-md: 1rem;
  --space-lg: 2rem;
  --space-xl: 4rem;

  /* Effects */
  --glow-primary: 0 0 15px rgba(74, 0, 224, 0.6);
  --glow-secondary: 0 0 15px rgba(45, 205, 223, 0.6);
  --glow-accent: 0 0 15px rgba(0, 255, 157, 0.6);
}

/* Component Examples */
.component-node {
  background: var(--background-light);
  border: 1px solid var(--primary);
  border-radius: 8px;
  box-shadow: var(--glow-primary);
  padding: var(--space-md);
  transition: all 0.3s ease;
}

.component-node:hover,
.component-node.active {
  box-shadow: var(--glow-primary), 0 0 30px rgba(74, 0, 224, 0.4);
  transform: scale(1.05);
}

/* Data flow effects */
.data-particle {
  background: var(--accent);
  height: 4px;
  width: 4px;
  border-radius: 50%;
  position: absolute;
  animation: flow 2s linear infinite;
}

@keyframes flow {
  0% {
    opacity: 0;
    transform: translateX(0) scale(0.5);
  }
  50% {
    opacity: 1;
    transform: translateX(50%) scale(1);
  }
  100% {
    opacity: 0;
    transform: translateX(100%) scale(0.5);
  }
}
```

### Development and Deployment Infrastructure

```yaml
# docker-compose.yml
version: '3.8'

services:
  frontend:
    build:
      context: ./ui-docs
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    volumes:
      - ./ui-docs:/app
      - /app/node_modules
    environment:
      - NODE_ENV=development
      - REACT_APP_API_URL=http://localhost:4000

  backend:
    build:
      context: ./server
      dockerfile: Dockerfile
    ports:
      - "4000:4000"
    volumes:
      - ./server:/app
      - /app/node_modules
    environment:
      - NODE_ENV=development
    depends_on:
      - redis

  sandbox:
    build:
      context: ./sandbox
      dockerfile: Dockerfile
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    environment:
      - MAX_CONTAINERS=10
      - CONTAINER_TIMEOUT=30
    restart: always

  redis:
    image: redis:alpine
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data

volumes:
  redis-data:
```

## Implementation Plan

### Phase 1: Foundation (1-2 weeks)
- Set up React + Three.js project structure
- Convert existing documentation to MDX format
- Create basic 3D models for core components
- Implement Sandpack code playground integration

### Phase 2: Core Experience (2-3 weeks)
- Develop the 3D architecture explorer with basic interactions
- Implement camera controls and interactive elements
- Create documentation panels with proper content linking
- Set up the code execution environment with Docker

### Phase 3: Enhanced Features (2-3 weeks)
- Build advanced code playground features
- Implement guided tours and exploration modes
- Develop sequence visualizer with animation
- Create concept map views

### Phase 4: Polish and Launch (1-2 weeks)
- Add animations and transitions
- Optimize performance
- Implement responsive design
- Conduct user testing and refinement
- Deploy to production

## Conclusion

This enhanced documentation plan combines traditional technical documentation with cutting-edge interactive visualization to create an unparalleled learning experience for Universal Intelligence. By leveraging 3D visualization, interactive code execution, and intuitive navigation, users will gain a deeper understanding of the architecture and capabilities of the framework.
