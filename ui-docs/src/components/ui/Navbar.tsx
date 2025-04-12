import React, { useState } from 'react';
import { Link } from 'react-router-dom';

interface NavbarProps {
  toggleSidebar: () => void;
}

const Navbar: React.FC<NavbarProps> = ({ toggleSidebar }) => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  return (
    <header className="bg-slate-800 shadow-lg sticky top-0 z-50">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center h-16">
          {/* Logo and Mobile Menu Button */}
          <div className="flex items-center">
            <button
              className="p-2 mr-3 lg:hidden text-white hover:text-indigo-300"
              onClick={toggleSidebar}
              aria-label="Toggle sidebar"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>

            <Link to="/" className="flex items-center">
              <span className="text-2xl font-bold bg-gradient-to-r from-indigo-600 to-sky-400 bg-clip-text text-transparent">
                Universal Intelligence
              </span>
            </Link>
          </div>

          {/* Desktop Navigation */}
          <nav className="hidden lg:flex space-x-8">
            <Link to="/" className="text-white hover:text-indigo-300 py-2">Home</Link>
            <Link to="/explorer" className="text-white hover:text-indigo-300 py-2">3D Explorer</Link>
            <Link to="/playground" className="text-white hover:text-indigo-300 py-2">Playground</Link>
            <a
              href="https://github.com/bluera/universal-intelligence"
              target="_blank"
              rel="noopener noreferrer"
              className="text-white hover:text-indigo-300 py-2"
            >
              GitHub
            </a>
          </nav>

          {/* Mobile Menu Button */}
          <div className="lg:hidden">
            <button
              className="p-2 text-white hover:text-indigo-300"
              onClick={toggleMenu}
              aria-label="Toggle menu"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h8m-8 6h16" />
              </svg>
            </button>
          </div>
        </div>

        {/* Mobile Menu */}
        {isMenuOpen && (
          <div className="lg:hidden py-4 space-y-4">
            <Link to="/" className="block text-white hover:text-indigo-300 py-2">Home</Link>
            <Link to="/explorer" className="block text-white hover:text-indigo-300 py-2">3D Explorer</Link>
            <Link to="/playground" className="block text-white hover:text-indigo-300 py-2">Playground</Link>
            <a
              href="https://github.com/bluera/universal-intelligence"
              target="_blank"
              rel="noopener noreferrer"
              className="block text-white hover:text-indigo-300 py-2"
            >
              GitHub
            </a>
          </div>
        )}
      </div>
    </header>
  );
};

export default Navbar;
