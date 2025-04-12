import React, { useState, useRef, useEffect } from 'react';
import CodeEditor from '../components/playground/CodeEditor';
import OutputDisplay from '../components/playground/OutputDisplay';
import {
  codeExamples,
  additionalExamples,
  simulatedExecutionSteps
} from '../components/playground/CodeExamples';

const Playground: React.FC = () => {
  const [selectedCategory, setSelectedCategory] = useState<string>('Examples');
  const [selectedExample, setSelectedExample] = useState<string>('Basic Model');
  const [code, setCode] = useState<string>(codeExamples['Basic Model']);
  const [output, setOutput] = useState<string>('');
  const [isRunning, setIsRunning] = useState<boolean>(false);
  const [executionStep, setExecutionStep] = useState<number>(0);
  const executionTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

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

    // Reset output and execution state
    setOutput('');
    setIsRunning(false);
    setExecutionStep(0);

    if (executionTimerRef.current) {
      clearTimeout(executionTimerRef.current);
    }
  };

  // Enhanced simulation with step-by-step execution
  const handleRunCode = () => {
    setIsRunning(true);
    setExecutionStep(0);
    setOutput('');

    // Clear any existing execution timer
    if (executionTimerRef.current) {
      clearTimeout(executionTimerRef.current);
    }

    // This will simulate a step-by-step execution
    executeNextStep();
  };

  const executeNextStep = () => {
    // Get the appropriate simulated output based on the category, example and step
    if (simulatedExecutionSteps[selectedCategory]?.[selectedExample]) {
      const steps = simulatedExecutionSteps[selectedCategory][selectedExample];

      if (executionStep < steps.length) {
        // Use the pre-defined step output
        setOutput(steps[executionStep]);
        setExecutionStep(prev => prev + 1);

        // If we have more steps, schedule the next one
        if (executionStep + 1 < steps.length) {
          executionTimerRef.current = setTimeout(executeNextStep, 800);
        } else {
          // Execution complete
          setIsRunning(false);
        }
      } else {
        // No more steps, execution complete
        setIsRunning(false);
      }
    } else {
      // No steps defined for this example, just show a default message
      setOutput('Example execution complete.');
      setIsRunning(false);
    }
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

  // Clean up any timers when component unmounts
  useEffect(() => {
    return () => {
      if (executionTimerRef.current) {
        clearTimeout(executionTimerRef.current);
      }
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

      {/* Code editor section */}
      <div style={{ marginBottom: '1rem' }}>
        <div style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          marginBottom: '0.8rem'
        }}>
          <div style={{ fontWeight: 'bold', color: '#f8f8f2' }}>Code:</div>
          <button
            onClick={handleRunCode}
            disabled={isRunning}
            style={{
              padding: '0.5rem 1.2rem',
              backgroundColor: isRunning ? '#666' : '#00ff9d',
              color: '#111',
              border: 'none',
              borderRadius: '4px',
              fontWeight: 'bold',
              cursor: isRunning ? 'default' : 'pointer',
              transition: 'background-color 0.2s',
            }}
          >
            {isRunning ? 'Running...' : 'Run Code'}
          </button>
        </div>

        <CodeEditor code={code} onChange={setCode} />
      </div>

      {/* Output section */}
      <div style={{ marginBottom: '2rem' }}>
        <div style={{ fontWeight: 'bold', marginBottom: '0.8rem', color: '#f8f8f2' }}>
          Output:
        </div>
        <OutputDisplay output={output} isRunning={isRunning} />
      </div>

      {/* Information section */}
      <div style={{
        marginTop: '2rem',
        padding: '1.2rem',
        backgroundColor: '#141a24',
        borderRadius: '4px',
        color: '#f8f8f2'
      }}>
        <h3 style={{ color: '#2dcddf', marginBottom: '0.8rem', fontWeight: 'bold' }}>
          Note:
        </h3>
        <p>
          This is a demonstration playground. The code is not actually executed on the server.
          To run Universal Intelligence code on your own machine, please install the framework
          using pip: <code style={{ backgroundColor: '#292938', padding: '0.1rem 0.3rem', borderRadius: '3px' }}>
            pip install universal-intelligence
          </code>
        </p>
      </div>
    </div>
  );
};

export default Playground;
