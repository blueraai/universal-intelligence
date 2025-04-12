import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import './index.css';
import PlaygroundPage from './pages/Playground';

// Simplified placeholder page
const Home = () => (
  <div style={{ maxWidth: '800px', margin: '0 auto', padding: '20px' }}>
    <h1 style={{ fontSize: '2.5rem', fontWeight: 'bold', marginBottom: '1rem' }}>
      Universal Intelligence
    </h1>
    <p style={{ fontSize: '1.2rem', marginBottom: '2rem' }}>
      A standardized, modular framework for creating, distributing, and using
      AI components that work across different hardware setups.
    </p>

    <div style={{ display: 'flex', justifyContent: 'center', gap: '1rem', marginBottom: '2rem' }}>
      <Link to="/explorer" style={{
        backgroundColor: '#4a00e0',
        color: 'white',
        padding: '0.5rem 1rem',
        borderRadius: '0.25rem',
        textDecoration: 'none'
      }}>
        Explore in 3D
      </Link>
      <Link to="/playground" style={{
        border: '1px solid #4a00e0',
        color: '#b8c7e0',
        padding: '0.5rem 1rem',
        borderRadius: '0.25rem',
        textDecoration: 'none'
      }}>
        Try the Code Playground
      </Link>
    </div>

    <div style={{
      display: 'grid',
      gridTemplateColumns: '1fr 1fr 1fr',
      gap: '1rem',
      marginBottom: '2rem'
    }}>
      <div style={{ backgroundColor: '#141a24', padding: '1rem', borderRadius: '0.5rem' }}>
        <h3 style={{ fontSize: '1.2rem', fontWeight: 'bold', marginBottom: '0.5rem', color: '#4a00e0' }}>
          Universal Model
        </h3>
        <p>
          A standardized interface for AI models that automatically optimizes for
          your hardware, whether you're using NVIDIA GPUs, Apple Silicon, or CPU.
        </p>
      </div>

      <div style={{ backgroundColor: '#141a24', padding: '1rem', borderRadius: '0.5rem' }}>
        <h3 style={{ fontSize: '1.2rem', fontWeight: 'bold', marginBottom: '0.5rem', color: '#2dcddf' }}>
          Universal Tool
        </h3>
        <p>
          A standardized interface for tools that can be used by agents, from
          simple printers to complex API callers and MCP integrations.
        </p>
      </div>

      <div style={{ backgroundColor: '#141a24', padding: '1rem', borderRadius: '0.5rem' }}>
        <h3 style={{ fontSize: '1.2rem', fontWeight: 'bold', marginBottom: '0.5rem', color: '#00ff9d' }}>
          Universal Agent
        </h3>
        <p>
          A standardized agent system that can use any combination of models and
          tools, with support for agent-to-agent collaboration.
        </p>
      </div>
    </div>
  </div>
);

// Placeholder Explorer page
const Explorer = () => (
  <div style={{ maxWidth: '800px', margin: '0 auto', padding: '20px' }}>
    <h1 style={{ fontSize: '2rem', fontWeight: 'bold', marginBottom: '1rem' }}>
      3D Architecture Explorer
    </h1>
    <p style={{ marginBottom: '1rem' }}>
      This feature is coming soon. The 3D explorer will allow you to interact with
      the Universal Intelligence architecture in a spatial environment.
    </p>
    <div style={{
      backgroundColor: '#141a24',
      padding: '2rem',
      borderRadius: '0.5rem',
      textAlign: 'center'
    }}>
      <h2 style={{ fontSize: '1.5rem', fontWeight: 'bold', marginBottom: '0.5rem', color: '#4a00e0' }}>
        3D Explorer Under Development
      </h2>
      <p>
        We're building an immersive 3D experience to help you understand the
        Universal Intelligence architecture.
      </p>
    </div>
  </div>
);

// Main App Component
function App() {
  return (
    <Router>
      <div style={{
        backgroundColor: '#0a0e17',
        minHeight: '100vh',
        color: 'white',
        display: 'flex',
        flexDirection: 'column'
      }}>
        <header style={{
          backgroundColor: '#141a24',
          padding: '1rem',
          marginBottom: '2rem',
          boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)'
        }}>
          <div style={{
            maxWidth: '1200px',
            margin: '0 auto',
            display: 'flex',
            justifyContent: 'space-between'
          }}>
            <Link to="/" style={{
              fontSize: '1.5rem',
              fontWeight: 'bold',
              color: 'white',
              textDecoration: 'none'
            }}>
              <span style={{ color: '#4a00e0' }}>Universal</span> Intelligence
            </Link>
            <nav style={{ display: 'flex', gap: '1.5rem' }}>
              <Link to="/" style={{ color: 'white', textDecoration: 'none' }}>Home</Link>
              <Link to="/explorer" style={{ color: 'white', textDecoration: 'none' }}>Explorer</Link>
              <Link to="/playground" style={{ color: 'white', textDecoration: 'none' }}>Playground</Link>
              <a
                href="https://github.com/bluera/universal-intelligence"
                style={{ color: 'white', textDecoration: 'none' }}
                target="_blank"
                rel="noopener noreferrer"
              >
                GitHub
              </a>
            </nav>
          </div>
        </header>

        <main style={{ flex: 1 }}>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/explorer" element={<Explorer />} />
            <Route path="/playground" element={<PlaygroundPage />} />
          </Routes>
        </main>

        <footer style={{
          backgroundColor: '#141a24',
          padding: '1.5rem',
          marginTop: '3rem',
          textAlign: 'center'
        }}>
          <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
            <p>Universal Intelligence Documentation © 2025</p>
          </div>
        </footer>
      </div>
    </Router>
  );
}

export default App;
