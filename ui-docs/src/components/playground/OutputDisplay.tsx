import React from 'react';

interface OutputDisplayProps {
  output: string;
  isRunning: boolean;
}

// A styled output display with ANSI color support
const OutputDisplay: React.FC<OutputDisplayProps> = ({ output, isRunning }) => {
  // Convert simple ANSI color codes to styled spans
  const formatOutput = (text: string) => {
    if (!text) return <span>Run your code to see the output here.</span>;

    // Handle newlines
    const lines = text.split('\n');

    return (
      <>
        {lines.map((line, i) => {
          // Output types with colors
          if (line.startsWith("Agent:")) {
            return <div key={i} style={{ color: "#00ff9d" }}>{line}</div>;
          } else if (line.startsWith("Tool executed:")) {
            return <div key={i} style={{ color: "#15e6ff" }}>{line}</div>;
          } else if (line.startsWith("Error:")) {
            return <div key={i} style={{ color: "#ff5555" }}>{line}</div>;
          } else if (line.startsWith("Warning:")) {
            return <div key={i} style={{ color: "#ffb86c" }}>{line}</div>;
          } else if (line.startsWith("API Response:")) {
            return <div key={i} style={{ color: "#bd93f9" }}>{line}</div>;
          }

          // Default styling
          return <div key={i}>{line}</div>;
        })}
      </>
    );
  };

  // Blinking cursor for running state
  const cursor = isRunning ? (
    <span className="blinking-cursor" style={{ animation: "blink 1s step-end infinite" }}>▋</span>
  ) : null;

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
        overflowY: 'auto',
        maxHeight: '300px',
        whiteSpace: 'pre-wrap',
      }}
    >
      {formatOutput(output)}
      {cursor}
    </div>
  );
};

export default OutputDisplay;
