import React from 'react';
import { Link, useLocation } from 'react-router-dom';

interface SidebarProps {
  isOpen: boolean;
  onClose: () => void;
}

const Sidebar: React.FC<SidebarProps> = ({ isOpen, onClose }) => {
  const location = useLocation();

  const isActivePath = (path: string) => {
    return location.pathname === path;
  };

  return (
    <div
      className={`fixed inset-y-0 left-0 z-40 w-64 bg-slate-800 shadow-lg transform transition-transform duration-300 ease-in-out ${
        isOpen ? 'translate-x-0' : '-translate-x-full'
      } lg:translate-x-0 lg:static lg:w-64 lg:min-h-screen overflow-y-auto`}
    >
      <div className="p-4">
        <div className="flex justify-between items-center mb-8">
          <h2 className="text-xl font-bold text-white">Documentation</h2>
          <button
            className="p-2 text-white hover:text-indigo-300 lg:hidden"
            onClick={onClose}
            aria-label="Close sidebar"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <nav>
          <ul className="space-y-2">
            <li>
              <h3 className="text-slate-400 uppercase text-xs font-bold tracking-wider py-2">Getting Started</h3>
              <ul className="pl-2 space-y-1">
                <li>
                  <Link
                    to="/"
                    className={`block px-3 py-2 rounded-md ${isActivePath('/') ? 'bg-indigo-600 text-white' : 'text-slate-300 hover:bg-slate-700'}`}
                  >
                    Introduction
                  </Link>
                </li>
                <li>
                  <Link
                    to="/explorer"
                    className={`block px-3 py-2 rounded-md ${isActivePath('/explorer') ? 'bg-indigo-600 text-white' : 'text-slate-300 hover:bg-slate-700'}`}
                  >
                    3D Explorer
                  </Link>
                </li>
                <li>
                  <Link
                    to="/playground"
                    className={`block px-3 py-2 rounded-md ${isActivePath('/playground') ? 'bg-indigo-600 text-white' : 'text-slate-300 hover:bg-slate-700'}`}
                  >
                    Code Playground
                  </Link>
                </li>
              </ul>
            </li>

            <li>
              <h3 className="text-slate-400 uppercase text-xs font-bold tracking-wider py-2">Core Components</h3>
              <ul className="pl-2 space-y-1">
                <li>
                  <Link
                    to="/explorer?component=Model"
                    className={`block px-3 py-2 rounded-md text-slate-300 hover:bg-slate-700`}
                  >
                    Universal Model
                  </Link>
                </li>
                <li>
                  <Link
                    to="/explorer?component=Tool"
                    className={`block px-3 py-2 rounded-md text-slate-300 hover:bg-slate-700`}
                  >
                    Universal Tool
                  </Link>
                </li>
                <li>
                  <Link
                    to="/explorer?component=Agent"
                    className={`block px-3 py-2 rounded-md text-slate-300 hover:bg-slate-700`}
                  >
                    Universal Agent
                  </Link>
                </li>
              </ul>
            </li>

            <li>
              <h3 className="text-slate-400 uppercase text-xs font-bold tracking-wider py-2">Models</h3>
              <ul className="pl-2 space-y-1">
                <li>
                  <Link
                    to="/explorer?component=Llama3"
                    className={`block px-3 py-2 rounded-md text-slate-300 hover:bg-slate-700`}
                  >
                    Llama3
                  </Link>
                </li>
                <li>
                  <Link
                    to="/explorer?component=Qwen2.5-7B"
                    className={`block px-3 py-2 rounded-md text-slate-300 hover:bg-slate-700`}
                  >
                    Qwen2.5-7B
                  </Link>
                </li>
                <li>
                  <Link
                    to="/explorer?component=Other+Models"
                    className={`block px-3 py-2 rounded-md text-slate-300 hover:bg-slate-700`}
                  >
                    Other Models
                  </Link>
                </li>
              </ul>
            </li>

            <li>
              <h3 className="text-slate-400 uppercase text-xs font-bold tracking-wider py-2">Tools & Agents</h3>
              <ul className="pl-2 space-y-1">
                <li>
                  <a
                    href="https://github.com/bluera/universal-intelligence/tree/main/universal_intelligence/community/tools"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="block px-3 py-2 rounded-md text-slate-300 hover:bg-slate-700"
                  >
                    Community Tools
                  </a>
                </li>
                <li>
                  <a
                    href="https://github.com/bluera/universal-intelligence/tree/main/universal_intelligence/community/agents"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="block px-3 py-2 rounded-md text-slate-300 hover:bg-slate-700"
                  >
                    Community Agents
                  </a>
                </li>
              </ul>
            </li>

            <li>
              <h3 className="text-slate-400 uppercase text-xs font-bold tracking-wider py-2">Resources</h3>
              <ul className="pl-2 space-y-1">
                <li>
                  <a
                    href="https://github.com/bluera/universal-intelligence"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="block px-3 py-2 rounded-md text-slate-300 hover:bg-slate-700"
                  >
                    GitHub Repository
                  </a>
                </li>
              </ul>
            </li>
          </ul>
        </nav>
      </div>
    </div>
  );
};

export default Sidebar;
