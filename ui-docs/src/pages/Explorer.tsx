import React, { useState, Suspense } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, PerspectiveCamera } from '@react-three/drei';
import Scene from '../components/3d/Scene';
import ComponentInfo from '../components/ui/ComponentInfo';

interface ComponentData {
  [key: string]: {
    title: string;
    description: string;
    codeExample: string;
    docsLink: string;
    color: string;
  };
}

const componentData: ComponentData = {
  'Model': {
    title: 'Universal Model',
    description: 'The Universal Model provides a standardized interface for AI language models. It abstracts away hardware-specific optimizations, allowing models to run efficiently across different devices (NVIDIA GPUs, Apple Silicon, CPU).',
    codeExample: `from universal_intelligence import Model

# Initialize a model that works on any hardware
model = Model()

# Get a response from the model
response = model.process("What is machine learning?")
print(response)`,
    docsLink: '/docs/universal-model',
    color: '#4a00e0',
  },
  'Tool': {
    title: 'Universal Tool',
    description: 'The Universal Tool provides a standardized interface for tools that can be used by agents. These range from simple utilities like printing text to complex integrations with external APIs and services.',
    codeExample: `from universal_intelligence import Tool

# Initialize a simple printer tool
printer_tool = Tool()

# Use the tool
result = printer_tool.execute("Hello, Universal Intelligence!")
print(result)`,
    docsLink: '/docs/universal-tool',
    color: '#2dcddf',
  },
  'Agent': {
    title: 'Universal Agent',
    description: 'The Universal Agent provides a standardized system for building AI agents. Agents can use any combination of models and tools, enabling powerful capabilities while maintaining consistent interfaces.',
    codeExample: `from universal_intelligence import Model, Agent

# Initialize a model and create an agent
model = Model()
agent = Agent(universal_model=model)

# Process a request with the agent
result = agent.process("What is machine learning?")
print(result)`,
    docsLink: '/docs/universal-agent',
    color: '#00ff9d',
  },
  'Qwen2.5-7B': {
    title: 'Qwen2.5-7B',
    description: 'Qwen2.5-7B is an implementation of the Universal Model interface for Alibaba\'s Qwen2.5-7B language model. It provides optimized inference for this specific model architecture.',
    codeExample: `from universal_intelligence.community.models.qwen2_5_7b_instruct import Qwen2_5_7B

# Initialize the Qwen model
model = Qwen2_5_7B()

# Process a prompt
response = model.process("Explain quantum computing.")
print(response)`,
    docsLink: '/docs/models/qwen2-5-7b',
    color: '#4a00e0',
  },
  'Llama3': {
    title: 'Llama3',
    description: 'Llama3 is an implementation of the Universal Model interface for Meta\'s Llama3 language model. It supports various sizes of the Llama3 architecture with optimized inference.',
    codeExample: `from universal_intelligence.community.models.llama3_3_70b_instruct import Llama3_3_70B

# Initialize the Llama3 model
model = Llama3_3_70B()

# Process a prompt
response = model.process("Write a poem about AI.")
print(response)`,
    docsLink: '/docs/models/llama3',
    color: '#4a00e0',
  },
  'Other Models': {
    title: 'Other Model Implementations',
    description: 'The Universal Intelligence framework includes implementations for many different language models, such as Gemma, Phi, Falcon, and more. Each implementation provides optimized inference for its specific model architecture.',
    codeExample: `# Using other model implementations
from universal_intelligence.community.models.gemma3_27b_it import Gemma3_27B_IT
from universal_intelligence.community.models.phi4 import Phi4

# Choose the model you want to use
model = Gemma3_27B_IT()  # or Phi4()

# All models use the same interface
response = model.process("Explain how neural networks work.")
print(response)`,
    docsLink: '/docs/models',
    color: '#4a00e0',
  },
};

const Explorer: React.FC = () => {
  const [selectedComponent, setSelectedComponent] = useState<string | null>(null);
  const [viewMode, setViewMode] = useState<'guided' | 'free' | 'map'>('free');

  const handleComponentSelect = (name: string) => {
    setSelectedComponent(name);
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-4xl font-bold mb-6">3D Architecture Explorer</h1>
      <p className="mb-6">
        Explore the Universal Intelligence architecture in an interactive 3D environment.
        Click on components to learn more about them.
      </p>

      <div className="flex mb-4 space-x-4">
        <button
          className={`px-4 py-2 rounded ${viewMode === 'free' ? 'bg-indigo-600 text-white' : 'bg-slate-700 text-slate-300'}`}
          onClick={() => setViewMode('free')}
        >
          Free Exploration
        </button>
        <button
          className={`px-4 py-2 rounded ${viewMode === 'guided' ? 'bg-indigo-600 text-white' : 'bg-slate-700 text-slate-300'}`}
          onClick={() => setViewMode('guided')}
        >
          Guided Tour
        </button>
        <button
          className={`px-4 py-2 rounded ${viewMode === 'map' ? 'bg-indigo-600 text-white' : 'bg-slate-700 text-slate-300'}`}
          onClick={() => setViewMode('map')}
        >
          Concept Map
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 bg-slate-800 rounded-lg overflow-hidden h-[600px]">
          <Suspense fallback={<div className="flex h-full justify-center items-center">Loading 3D scene...</div>}>
            <Canvas>
              <PerspectiveCamera makeDefault position={[0, 0, 10]} />
              <Scene
                viewMode={viewMode}
                selectedComponent={selectedComponent}
                onSelectComponent={handleComponentSelect}
              />
              <OrbitControls
                enableZoom={true}
                enablePan={true}
                enableRotate={true}
                minDistance={5}
                maxDistance={20}
              />
            </Canvas>
          </Suspense>
        </div>

        <div>
          {selectedComponent ? (
            <ComponentInfo
              title={componentData[selectedComponent]?.title || selectedComponent}
              description={componentData[selectedComponent]?.description || "No description available."}
              codeExample={componentData[selectedComponent]?.codeExample || "// No code example available"}
              docsLink={componentData[selectedComponent]?.docsLink || "#"}
              color={componentData[selectedComponent]?.color || "#4a00e0"}
            />
          ) : (
            <div className="bg-slate-800 p-6 rounded-lg h-full">
              <h2 className="text-2xl font-bold mb-4 text-white">
                Select a Component
              </h2>
              <p className="text-slate-300 mb-4">
                Click on any component in the 3D visualization to view detailed information about it.
              </p>
              <p className="text-slate-300">
                The Universal Intelligence framework consists of three main components:
              </p>
              <ul className="list-disc list-inside mt-2 text-slate-300">
                <li>Universal Model - For language models</li>
                <li>Universal Tool - For agent tools</li>
                <li>Universal Agent - For building AI agents</li>
              </ul>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Explorer;
