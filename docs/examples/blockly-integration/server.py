#!/usr/bin/env python3
"""
Simple HTTP server for running the Universal Agents Blockly demo.
This server handles CORS issues and serves files from the current directory.
"""

import http.server
import socketserver
import os
import sys
import webbrowser
from urllib.parse import urlparse, unquote
import threading
import time

PORT = 8000
DEBUG = True

def debug_log(message):
    """Print debug message if DEBUG is enabled."""
    if DEBUG:
        print(f"[DEBUG] {message}")

class CORSHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Handler that adds CORS headers to responses."""
    
    def log_message(self, format, *args):
        """Override to provide more detailed logging."""
        if DEBUG:
            sys.stderr.write(f"[{self.log_date_time_string()}] {self.address_string()} - {format % args}\n")
    
    def end_headers(self):
        """Add CORS headers to all responses."""
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With, Content-Type, Authorization")
        super().end_headers()
        
    def do_OPTIONS(self):
        """Handle OPTIONS requests by adding CORS headers."""
        self.send_response(200)
        self.end_headers()
        
    def do_GET(self):
        """Handle GET requests, logging them for debugging."""
        path = self.path
        debug_log(f"GET request: {path}")
        
        # Normalize path to serve files from the correct directory
        parsed_path = urlparse(path)
        clean_path = unquote(parsed_path.path)
        
        # Check if path exists relative to current directory
        if clean_path == "/":
            clean_path = "/index.html"
            self.path = "/index.html"
            
        file_path = os.path.join(os.getcwd(), clean_path.lstrip("/"))
        
        if os.path.exists(file_path) and os.path.isfile(file_path):
            debug_log(f"Serving file: {file_path}")
            
            # Set correct content type for JavaScript files
            if file_path.endswith('.js'):
                self.send_response(200)
                self.send_header('Content-type', 'application/javascript')
                self.end_headers()
                with open(file_path, 'rb') as f:
                    self.wfile.write(f.read())
                return
            # Handle HTML files
            elif file_path.endswith('.html'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                with open(file_path, 'rb') as f:
                    self.wfile.write(f.read())
                return
            # Let SimpleHTTPRequestHandler handle other file types
            else:
                return super().do_GET()
        else:
            debug_log(f"File not found: {file_path}")
            return super().do_GET()

def check_files():
    """Check if all required files exist."""
    required_files = [
        "index.html",
        "test.js",
        "basic_node_block_definition.js",
        "flow_block_definition.js",
        "model_node_block_definition.js",
        "toolbox_configuration.js"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("WARNING: The following required files are missing:")
        for file in missing_files:
            print(f"  - {file}")
        print("The demo may not work correctly without these files.")
    else:
        print("All required files are present.")

def open_browser():
    """Open browser after a short delay."""
    def _open_browser():
        time.sleep(1.0)
        url = f"http://localhost:{PORT}/index.html"
        print(f"Opening browser at {url}")
        webbrowser.open(url)
    
    thread = threading.Thread(target=_open_browser)
    thread.daemon = True
    thread.start()

def run_server():
    """Run the server."""
    handler = CORSHTTPRequestHandler
    
    try:
        with socketserver.TCPServer(("", PORT), handler) as httpd:
            print("\n" + "="*50)
            print(" Universal Agents Blockly Integration Demo Server")
            print("="*50 + "\n")
            
            print(f"Server running at http://localhost:{PORT}")
            print(f"Open your browser to http://localhost:{PORT}/index.html")
            print("\nTest the integration by:")
            print("1. Drag blocks from the toolbox to the workspace")
            print("2. View the generated code in the right panel")
            print("3. Click 'Run Tests' to verify the integration")
            print("\nCheck browser console (F12 -> Console) for detailed logs\n")
            print("Press Ctrl+C to stop the server\n")
            
            # Open browser automatically
            open_browser()
            
            # Start the server
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped")
    except Exception as e:
        print(f"\nError starting server: {e}")
        print(f"Port {PORT} might be in use. Try changing the PORT value.")

if __name__ == "__main__":
    # Change to the directory containing this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    print(f"Working directory: {os.getcwd()}")
    
    # Check files
    check_files()
    
    # Run server
    run_server()