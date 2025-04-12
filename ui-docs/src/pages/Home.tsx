import React from 'react';
import { Link } from 'react-router-dom';

const Home: React.FC = () => {
  return (
    <div className="max-w-5xl mx-auto">
      <section className="mb-12 py-12 text-center">
        <h1 className="text-5xl font-bold mb-6 bg-gradient-to-r from-indigo-600 to-sky-400 bg-clip-text text-transparent">
          Universal Intelligence
        </h1>
        <p className="text-xl mb-8 max-w-3xl mx-auto">
          A standardized, modular framework for creating, distributing, and using
          AI components that work across different hardware setups.
        </p>
        <div className="flex justify-center gap-4">
          <Link to="/explorer" className="bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded">
            Explore in 3D
          </Link>
          <Link to="/playground" className="border border-indigo-600 hover:bg-indigo-800 text-indigo-300 font-bold py-2 px-4 rounded">
            Try the Code Playground
          </Link>
        </div>
      </section>

      <section className="grid md:grid-cols-3 gap-8 mb-12">
        <div className="bg-slate-800 p-6 rounded-lg shadow-lg">
          <h3 className="text-xl font-bold mb-3 text-indigo-400">Universal Model</h3>
          <p>
            A standardized interface for AI models that automatically optimizes for
            your hardware, whether you're using NVIDIA GPUs, Apple Silicon, or CPU.
          </p>
        </div>

        <div className="bg-slate-800 p-6 rounded-lg shadow-lg">
          <h3 className="text-xl font-bold mb-3 text-sky-400">Universal Tool</h3>
          <p>
            A standardized interface for tools that can be used by agents, from
            simple printers to complex API callers and MCP integrations.
          </p>
        </div>

        <div className="bg-slate-800 p-6 rounded-lg shadow-lg">
          <h3 className="text-xl font-bold mb-3 text-green-400">Universal Agent</h3>
          <p>
            A standardized agent system that can use any combination of models and
            tools, with support for agent-to-agent collaboration.
          </p>
        </div>
      </section>

      <section className="mb-12">
        <h2 className="text-3xl font-bold mb-6 text-center">
          Interactive Documentation
        </h2>
        <div className="grid md:grid-cols-2 gap-8">
          <div className="bg-slate-800 p-6 rounded-lg shadow-lg">
            <h3 className="text-xl font-bold mb-3 text-indigo-400">3D Architecture Explorer</h3>
            <p className="mb-4">
              Explore the Universal Intelligence architecture in an interactive 3D
              environment. Visualize components, connections, and data flows.
            </p>
            <Link to="/explorer" className="inline-block bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded">
              Open Explorer
            </Link>
          </div>

          <div className="bg-slate-800 p-6 rounded-lg shadow-lg">
            <h3 className="text-xl font-bold mb-3 text-sky-400">Code Playground</h3>
            <p className="mb-4">
              Try out Universal Intelligence code examples in your browser. Modify
              and run code to see the results in real-time.
            </p>
            <Link to="/playground" className="inline-block bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded">
              Open Playground
            </Link>
          </div>
        </div>
      </section>

      <section className="mb-12">
        <h2 className="text-3xl font-bold mb-6 text-center">
          Get Started
        </h2>
        <div className="bg-slate-800 p-6 rounded-lg shadow-lg">
          <p className="mb-4">
            Install Universal Intelligence with pip:
          </p>
          <div className="bg-slate-900 p-3 rounded-md mb-6 font-mono text-white overflow-x-auto">
            pip install universal-intelligence
          </div>
          <p className="mb-4">
            Or check out the source code on GitHub:
          </p>
          <a
            href="https://github.com/bluera/universal-intelligence"
            className="inline-block bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded"
            target="_blank"
            rel="noopener noreferrer"
          >
            GitHub Repository
          </a>
        </div>
      </section>
    </div>
  );
};

export default Home;
