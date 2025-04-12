import React, { useState } from 'react';

// A simple code editor with syntax highlighting
const CodeEditor: React.FC<{ code: string; onChange: (value: string) => void }> = ({ code, onChange }) => {
  return (
    <div className="code-editor">
      <textarea
        value={code}
        onChange={(e) => onChange(e.target.value)}
        style={{
          width: '100%',
          height: '300px',
          backgroundColor: '#1e1e2e',
          color: '#f8f8f2',
          padding: '1rem',
          fontFamily: 'Fira Code, monospace',
          fontSize: '14px',
          border: '1px solid #333',
          borderRadius: '4px',
          resize: 'none',
        }}
      />
    </div>
  );
};

// A simple output display
const OutputDisplay: React.FC<{ output: string }> = ({ output }) => {
  return (
    <div
      style={{
        backgroundColor: '#0f0f17',
        color: '#f8f8f2',
        padding: '1rem',
        fontFamily: 'Fira Code, monospace',
        fontSize: '14px',
        minHeight: '150px',
        borderRadius: '4px',
        border: '1px solid #333',
      }}
    >
      {output || 'Run your code to see the output here.'}
    </div>
  );
};

// Example code snippets
const codeExamples = {
  'Basic Model': `from universal_intelligence import Model

# Initialize a model that works on any hardware
model = Model()

# Process a prompt
response = model.process("What is machine learning?")
print(response)`,

  'Basic Tool': `from universal_intelligence import Tool

# Initialize a simple printer tool
printer_tool = Tool()

# Use the tool
result = printer_tool.execute("Hello, Universal Intelligence!")
print(result)`,

  'Agent with Tool': `from universal_intelligence import Model, Agent, Tool

# Initialize components
model = Model()
tool = Tool()

# Create an agent with the model and tool
agent = Agent(universal_model=model)
agent.add_tool(tool)

# Process a request with the agent
result = agent.process("Use the tool to print 'Hello World'")
print(result)`,

  'Using Qwen2.5': `from universal_intelligence.community.models.qwen2_5_7b_instruct import Qwen2_5_7B

# Initialize the Qwen model
model = Qwen2_5_7B()

# Process a prompt
response = model.process("Explain quantum computing in simple terms.")
print(response)`,
};

const Playground: React.FC = () => {
  const [selectedExample, setSelectedExample] = useState<string>('Basic Model');
  const [code, setCode] = useState<string>(codeExamples['Basic Model']);
  const [output, setOutput] = useState<string>('');
  const [isRunning, setIsRunning] = useState<boolean>(false);

  const handleExampleChange = (example: string) => {
    setSelectedExample(example);
    setCode(codeExamples[example as keyof typeof codeExamples]);
  };

  const handleRunCode = () => {
    setIsRunning(true);

    // Simulate code execution
    setTimeout(() => {
      let simulatedOutput = '';

      if (selectedExample === 'Basic Model') {
        simulatedOutput = 'Machine learning is a branch of artificial intelligence that focuses on building systems that learn from data, identify patterns, and make decisions with minimal human intervention.';
      } else if (selectedExample === 'Basic Tool') {
        simulatedOutput = 'Hello, Universal Intelligence!';
      } else if (selectedExample === 'Agent with Tool') {
        simulatedOutput = 'Agent: I will use the printing tool.\nTool executed: Hello World\nTask completed successfully.';
      } else if (selectedExample === 'Using Qwen2.5') {
        simulatedOutput = 'Quantum computing uses the principles of quantum mechanics to process information in ways that classical computers cannot. Instead of using bits (0s and 1s), quantum computers use quantum bits or "qubits" that can exist in multiple states simultaneously thanks to superposition. This allows quantum computers to explore many possible solutions at once, making them potentially much faster for certain types of problems like factoring large numbers or simulating quantum systems.';
      }

      setOutput(simulatedOutput);
      setIsRunning(false);
    }, 1500);
  };

  return (
    <div style={{ maxWidth: '1000px', margin: '0 auto', padding: '2rem' }}>
      <h1 style={{ fontSize: '2rem', fontWeight: 'bold', marginBottom: '1rem' }}>
        Code Playground
      </h1>

      <p style={{ marginBottom: '2rem' }}>
        Try out Universal Intelligence code examples in this interactive playground.
        Select an example below or modify the code to experiment with the framework.
      </p>

      <div style={{ marginBottom: '1rem' }}>
        <div style={{ marginBottom: '0.5rem', fontWeight: 'bold' }}>Select an example:</div>

        <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap', marginBottom: '1rem' }}>
          {Object.keys(codeExamples).map((example) => (
            <button
              key={example}
              onClick={() => handleExampleChange(example)}
              style={{
                padding: '0.5rem 1rem',
                backgroundColor: selectedExample === example ? '#4a00e0' : '#292938',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer',
              }}
            >
              {example}
            </button>
          ))}
        </div>
      </div>

      <div style={{ marginBottom: '1rem' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
          <div style={{ fontWeight: 'bold' }}>Code:</div>
          <button
            onClick={handleRunCode}
            disabled={isRunning}
            style={{
              padding: '0.5rem 1rem',
              backgroundColor: isRunning ? '#666' : '#00ff9d',
              color: '#111',
              border: 'none',
              borderRadius: '4px',
              fontWeight: 'bold',
              cursor: isRunning ? 'default' : 'pointer',
            }}
          >
            {isRunning ? 'Running...' : 'Run Code'}
          </button>
        </div>

        <CodeEditor code={code} onChange={setCode} />
      </div>

      <div>
        <div style={{ fontWeight: 'bold', marginBottom: '0.5rem' }}>Output:</div>
        <OutputDisplay output={output} />
      </div>

      <div style={{ marginTop: '2rem', padding: '1rem', backgroundColor: '#141a24', borderRadius: '4px' }}>
        <h3 style={{ color: '#2dcddf', marginBottom: '0.5rem', fontWeight: 'bold' }}>Note:</h3>
        <p>
          This is a demonstration playground. The code is not actually executed on the server.
          To run Universal Intelligence code on your own machine, please install the framework
          using pip: <code>pip install universal-intelligence</code>
        </p>
      </div>
    </div>
  );
};

export default Playground;
