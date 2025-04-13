import React, { useState, useEffect } from 'react';
import {
  SandpackProvider,
  SandpackLayout,
  SandpackCodeEditor,
  useSandpack
} from '@codesandbox/sandpack-react';
import { useWebSocket } from '../hooks/useWebSocket';
import {
  codeExamples,
  additionalExamples,
} from '../components/playground/CodeExamples';

// Custom theme matching our site
const universalTheme = {
  colors: {
    surface1: '#0a0e17',
    surface2: '#141a24',
    surface3: '#292938',
    clickable: '#4a00e0',
    base: '#f8f8f2',
    disabled: '#999',
    hover: '#6428e0',
    accent: '#00ff9d',
    error: '#ff5757',
    errorSurface: '#2c1616',
  },
  syntax: {
    plain: '#f8f8f2',
    comment: { color: '#6272a4', fontStyle: 'italic' as const },
    keyword: '#ff79c6',
    tag: '#ff79c6',
    punctuation: '#f8f8f2',
    definition: '#50fa7b',
    property: '#66d9ef',
    static: '#bd93f9',
    string: '#f1fa8c',
  },
  font: {
    body: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif',
    mono: 'Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace',
    size: '14px',
    lineHeight: '1.5',
  }
};

// Custom component for WebSocket connection management and running code
const WebSocketRunner: React.FC = () => {
  const { sandpack } = useSandpack();
  const { files, activeFile } = sandpack;
  const [output, setOutput] = useState<string>('');
  const [isRunning, setIsRunning] = useState<boolean>(false);

  // Initialize WebSocket connection
  const {
    sendMessage,
    lastMessage,
    isConnected,
    isConnecting,
    connect,
    resetConnection,
    hasGivenUp
  } = useWebSocket({
    url: 'ws://localhost:8765',
    onOpen: () => {
      console.log('WebSocket connected');
    },
    onClose: () => {
      console.log('WebSocket disconnected');
    },
    onError: (error) => {
      console.error('WebSocket error:', error);
    },
    reconnectAttempts: 3,
    initialReconnectInterval: 1000,
    maxReconnectInterval: 5000
  });

  // Handle messages from the WebSocket server
  useEffect(() => {
    if (lastMessage) {
      if (lastMessage.type === 'result') {
        // Handle execution result
        const result = lastMessage;

        let outputText = '';
        if (result.stdout) {
          outputText += result.stdout;
        }

        if (result.stderr) {
          outputText += `\n${result.stderr}`;
        }

        if (result.error) {
          outputText += `\n${result.error.type}: ${result.error.message}`;
          if (result.error.traceback) {
            outputText += `\n${result.error.traceback}`;
          }
        }

        setOutput(outputText);
        setIsRunning(false);
      } else if (lastMessage.type === 'status') {
        // Handle status updates
        console.log(`Status: ${lastMessage.status} - ${lastMessage.message}`);
      }
    }
  }, [lastMessage]);

  // Execute code
  const handleRunCode = () => {
    if (!isConnected) {
      setOutput('Not connected to execution server. Attempting to reconnect...');
      connect();
      return;
    }

    setIsRunning(true);
    const code = files[activeFile].code;

    // Send code to the WebSocket server
    sendMessage({
      type: 'execute',
      code
    });
  };

  return (
    <div>
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: '0.8rem'
      }}>
        <div style={{ fontWeight: 'bold', color: '#f8f8f2' }}>Code:</div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <div style={{
            fontSize: '0.8rem',
            padding: '0.2rem 0.5rem',
            borderRadius: '4px',
            backgroundColor: isConnected ? '#1e3a1e' : '#3a1e1e',
            color: isConnected ? '#72e472' : '#e47272'
          }}>
            {isConnecting ? 'Connecting...' : (isConnected ? 'Connected ●' : 'Disconnected ○')}
          </div>

          {hasGivenUp && (
            <button
              onClick={resetConnection}
              style={{
                padding: '0.3rem 0.8rem',
                backgroundColor: '#333',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                fontSize: '0.8rem',
                cursor: 'pointer'
              }}
            >
              Retry Connection
            </button>
          )}

          <button
            onClick={handleRunCode}
            disabled={isRunning || !isConnected}
            style={{
              padding: '0.5rem 1.2rem',
              backgroundColor: isRunning || !isConnected ? '#666' : '#00ff9d',
              color: '#111',
              border: 'none',
              borderRadius: '4px',
              fontWeight: 'bold',
              cursor: isRunning || !isConnected ? 'default' : 'pointer',
              transition: 'background-color 0.2s',
            }}
          >
            {isRunning ? 'Running...' : 'Run Code'}
          </button>
        </div>
      </div>

      {/* Custom console output display */}
      <div style={{ marginTop: '1rem' }}>
        <div style={{ fontWeight: 'bold', marginBottom: '0.8rem', color: '#f8f8f2' }}>
          Output:
        </div>
        <div style={{
          backgroundColor: '#141a24',
          padding: '1rem',
          borderRadius: '4px',
          fontFamily: 'monospace',
          color: '#f8f8f2',
          whiteSpace: 'pre-wrap',
          maxHeight: '300px',
          overflowY: 'auto',
          border: '1px solid #333'
        }}>
          {isRunning ? (
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <div style={{
                width: '1rem',
                height: '1rem',
                borderRadius: '50%',
                backgroundColor: '#00ff9d',
                animation: 'blink 1s infinite'
              }}></div>
              <span>Running code...</span>
            </div>
          ) : hasGivenUp ? (
            <div style={{ color: '#e47272' }}>
              Failed to connect to the execution server after multiple attempts.
              Please check if the server is running and click "Retry Connection".
            </div>
          ) : output ? (
            output
          ) : (
            <span style={{ color: '#777' }}>Code execution output will appear here.</span>
          )}
        </div>
      </div>
    </div>
  );
};

const Playground: React.FC = () => {
  const [selectedCategory, setSelectedCategory] = useState<string>('Examples');
  const [selectedExample, setSelectedExample] = useState<string>('Basic Model');
  const [code, setCode] = useState<string>(codeExamples['Basic Model']);

  // Get all examples combined
  const getAllExamples = () => {
    const examples: Record<string, Record<string, string>> = {
      'Examples': Object.fromEntries(
        Object.entries(codeExamples).map(([key, value]) => [key, value])
      )
    };

    // Add additional examples by category
    Object.entries(additionalExamples).forEach(([category, categoryExamples]) => {
      examples[category] = categoryExamples;
    });

    return examples;
  };

  const allExamples = getAllExamples();

  const handleExampleChange = (category: string, example: string) => {
    setSelectedCategory(category);
    setSelectedExample(example);

    // Get the code for this example
    const exampleCode = allExamples[category][example];
    setCode(exampleCode);
  };

  // Add CSS for blinking cursor
  useEffect(() => {
    const style = document.createElement('style');
    style.textContent = `
      @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0; }
      }
    `;
    document.head.appendChild(style);

    return () => {
      document.head.removeChild(style);
    };
  }, []);

  return (
    <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '2rem' }}>
      <h1 style={{ fontSize: '2rem', fontWeight: 'bold', marginBottom: '1rem', color: '#f8f8f2' }}>
        Code Playground
      </h1>

      <p style={{ marginBottom: '2rem', color: '#f8f8f2' }}>
        Try out Universal Intelligence code examples in this interactive playground.
        Select an example below or modify the code to experiment with the framework.
      </p>

      {/* Example category tabs */}
      <div style={{ display: 'flex', borderBottom: '1px solid #333', marginBottom: '1rem' }}>
        {Object.keys(allExamples).map((category) => (
          <div
            key={category}
            onClick={() => setSelectedCategory(category)}
            style={{
              padding: '0.5rem 1rem',
              cursor: 'pointer',
              backgroundColor: selectedCategory === category ? '#4a00e0' : 'transparent',
              color: selectedCategory === category ? 'white' : '#ccc',
              borderTopLeftRadius: '4px',
              borderTopRightRadius: '4px',
              marginRight: '0.5rem',
              fontWeight: selectedCategory === category ? 'bold' : 'normal',
            }}
          >
            {category}
          </div>
        ))}
      </div>

      {/* Example selection buttons */}
      <div style={{ marginBottom: '1.5rem' }}>
        <div style={{ marginBottom: '0.7rem', fontWeight: 'bold', color: '#f8f8f2' }}>
          Select an example:
        </div>
        <div style={{ display: 'flex', gap: '0.7rem', flexWrap: 'wrap' }}>
          {Object.keys(allExamples[selectedCategory] || {}).map((example) => (
            <button
              key={example}
              onClick={() => handleExampleChange(selectedCategory, example)}
              style={{
                padding: '0.5rem 1rem',
                backgroundColor: selectedExample === example ? '#4a00e0' : '#292938',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer',
                transition: 'background-color 0.2s',
              }}
            >
              {example}
            </button>
          ))}
        </div>
      </div>

      {/* SandPack editor */}
      <SandpackProvider
        template="vanilla"
        customSetup={{
          entry: '/main.py',
        }}
        theme={universalTheme}
        files={{
          '/main.py': {
            code: code,
            active: true
          }
        }}
        options={{
          externalResources: [],
          recompileMode: "delayed",
          recompileDelay: 500,
        }}
      >
        <SandpackLayout>
          <SandpackCodeEditor
            showLineNumbers={true}
            showInlineErrors={true}
            showRunButton={false}
            style={{ height: '400px' }}
          />
          <WebSocketRunner />
        </SandpackLayout>
      </SandpackProvider>

      {/* Information section */}
      <div style={{
        marginTop: '2rem',
        padding: '1.2rem',
        backgroundColor: '#141a24',
        borderRadius: '4px',
        color: '#f8f8f2'
      }}>
        <h3 style={{ color: '#2dcddf', marginBottom: '0.8rem', fontWeight: 'bold' }}>
          About this Playground
        </h3>
        <p>
          This playground executes Universal Intelligence code on a back-end Python server.
          The code you write runs in a sandboxed environment with the Universal Intelligence
          framework installed. You can try out different examples or create your own code
          to experiment with the framework's capabilities.
        </p>
      </div>
    </div>
  );
};

export default Playground;
