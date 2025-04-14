#!/usr/bin/env python

import asyncio
import websockets
import json
import traceback
import logging
import sys
import os
import io
import contextlib
import re
import time
from typing import Dict, Any, Optional, Tuple

# Set up detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger('websocket-server')
logger.setLevel(logging.DEBUG)

# CORS headers for WebSocket connections
CORS_HEADERS = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    'Access-Control-Max-Age': '86400',  # 24 hours
}

# Security settings for code execution
MAX_EXECUTION_TIME = 10  # Maximum execution time in seconds
MAX_OUTPUT_SIZE = 100 * 1024  # Maximum output size in bytes (100KB)

# Execute Python code safely
def execute_python_code(code: str) -> Dict[str, Any]:
    """
    Execute Python code in a restricted environment and capture output

    Returns a dict with:
    - stdout: captured standard output
    - stderr: captured standard error
    - error: error info if an exception occurred
    """
    stdout = io.StringIO()
    stderr = io.StringIO()

    # Create a dictionary for local variables
    local_vars = {}
    error_info = None

    # Wrap execution to catch any exceptions
    try:
        # Capture stdout and stderr
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            # Execute with timeout using asyncio
            exec(code, {"__builtins__": __builtins__}, local_vars)

    except Exception as e:
        error_type = type(e).__name__
        error_msg = str(e)
        error_traceback = traceback.format_exc()

        # Filter out system-specific paths from traceback for security
        error_traceback = re.sub(r'File ".*[/\\]', 'File "', error_traceback)

        error_info = {
            "type": error_type,
            "message": error_msg,
            "traceback": error_traceback
        }

        logger.error(f"Error executing code: {error_type}: {error_msg}")

    # Get output, truncate if too large
    stdout_output = stdout.getvalue()
    stderr_output = stderr.getvalue()

    if len(stdout_output) > MAX_OUTPUT_SIZE:
        stdout_output = stdout_output[:MAX_OUTPUT_SIZE] + "\n... output truncated (too large)"

    if len(stderr_output) > MAX_OUTPUT_SIZE:
        stderr_output = stderr_output[:MAX_OUTPUT_SIZE] + "\n... error output truncated (too large)"

    return {
        "stdout": stdout_output,
        "stderr": stderr_output,
        "error": error_info
    }

# Execute code with timeout
async def execute_with_timeout(code: str, timeout: int = MAX_EXECUTION_TIME) -> Dict[str, Any]:
    """Execute code with a timeout to prevent infinite loops"""
    try:
        # Run the execution in a separate thread
        loop = asyncio.get_event_loop()
        result = await asyncio.wait_for(
            loop.run_in_executor(None, execute_python_code, code),
            timeout=timeout
        )
        return result
    except asyncio.TimeoutError:
        logger.warning(f"Code execution timed out after {timeout} seconds")
        return {
            "stdout": "",
            "stderr": f"Execution timed out after {timeout} seconds.",
            "error": {
                "type": "TimeoutError",
                "message": f"Code execution took too long (exceeded {timeout} seconds limit).",
                "traceback": ""
            }
        }

# WebSocket handler for both testing and UI integration
async def websocket_handler(websocket, path=None):
    """WebSocket handler to communicate with both Python test clients and browser clients"""
    try:
        # Log connection info
        addr = websocket.remote_address if hasattr(websocket, 'remote_address') else 'Unknown'
        path_info = path if path else getattr(websocket, 'path', 'unknown')

        # Safer way to get headers that works in both websockets 14.x and 15.x
        origin = "unknown"
        try:
            if hasattr(websocket, 'request_headers'):
                origin = websocket.request_headers.get('Origin', 'unknown')
            elif hasattr(websocket, 'origin'):
                origin = websocket.origin
        except Exception as e:
            logger.debug(f"Error getting origin: {e}")

        logger.info(f"Connection opened from {addr} with path {path_info}, origin: {origin}")

        try:
            # Send welcome message as JSON for the UI client
            welcome_message = json.dumps({
                "type": "connection",
                "status": "connected",
                "message": "Connected to WebSocket server"
            })

            # Use wait_for to handle potential timeouts
            await asyncio.wait_for(websocket.send(welcome_message), timeout=2.0)
            logger.info(f"Sent welcome message: {welcome_message}")

            # Small delay before sending ping to ensure connection is stable
            await asyncio.sleep(0.1)

            # Send an immediate ping to help keep the connection open
            ping_message = json.dumps({
                "type": "ping",
                "timestamp": int(time.time() * 1000)
            })
            await asyncio.wait_for(websocket.send(ping_message), timeout=2.0)
            logger.info("Sent initial ping to keep connection alive")
        except (asyncio.TimeoutError, websockets.exceptions.ConnectionClosed) as e:
            logger.error(f"Connection unstable during handshake: {e}")
            # Continue to message handling loop, let the normal error handlers manage the situation
        except Exception as e:
            logger.error(f"Error during connection setup: {e}")

        # Wait for messages
        async for message in websocket:
            logger.info(f"Received message: {message[:200]}...")

            try:
                # Try to parse as JSON
                parsed = json.loads(message)
                message_type = parsed.get('type', '')

                # Handle different message types
                if message_type == 'execute':
                    # Handle code execution request
                    logger.info("Processing code execution request")
                    code = parsed.get('code', '')

                    if not code.strip():
                        await websocket.send(json.dumps({
                            "type": "result",
                            "status": "error",
                            "stdout": "",
                            "stderr": "No code provided.",
                            "error": {"type": "ValueError", "message": "No code provided."}
                        }))
                        continue

                    # Send running status
                    await websocket.send(json.dumps({
                        "type": "status",
                        "status": "running",
                        "message": "Executing code..."
                    }))

                    # Actually execute the code
                    result = await execute_with_timeout(code)

                    # Add completion status
                    result["type"] = "result"
                    result["status"] = "error" if result.get("error") else "completed"

                    # Send result to client
                    await websocket.send(json.dumps(result))
                    logger.info("Sent execution result")

                elif message_type == 'ping':
                    # Respond to ping with pong
                    await websocket.send(json.dumps({
                        "type": "pong",
                        "timestamp": parsed.get('timestamp', 0)
                    }))
                    logger.info("Sent pong response")

                else:
                    # Echo other JSON messages
                    response = {
                        "type": "echo",
                        "original": parsed,
                        "message": "Echo from server"
                    }
                    await websocket.send(json.dumps(response))
                    logger.info(f"Echoed JSON message: {json.dumps(response)[:100]}...")

            except json.JSONDecodeError:
                # Handle plain text messages
                if message.strip().lower() == 'ping':
                    await websocket.send('pong')
                    logger.info("Sent pong to text ping")
                else:
                    # Echo non-JSON messages with simple wrapper
                    echo_msg = json.dumps({
                        "type": "echo",
                        "text": message,
                        "format": "plain"
                    })
                    await websocket.send(echo_msg)
                    logger.info(f"Echoed text message: {echo_msg[:100]}...")
            except Exception as e:
                # Log any other errors during message processing
                logger.error(f"Error processing message: {e}")
                error_msg = json.dumps({
                    "type": "error",
                    "message": str(e),
                    "traceback": traceback.format_exc()
                })
                await websocket.send(error_msg)
                logger.error(traceback.format_exc())

    except websockets.exceptions.ConnectionClosed as e:
        logger.info(f"Connection closed: code={e.code}, reason={e.reason}")
    except Exception as e:
        logger.error(f"Handler error: {e}")
        logger.error(traceback.format_exc())

# Process HTTP OPTIONS requests for CORS - Updated for compatibility with different websockets versions
async def process_request(path, request):
    """
    Process HTTP requests to handle CORS preflight requests from browsers.

    Parameters:
    - path: The request path
    - request: The websockets Request object (different structure in different versions)

    Returns:
    - A tuple (status, headers, body) for non-WebSocket requests
    - None for WebSocket upgrade requests (to let websockets library handle it)
    """
    logger.info(f"Processing request for path: {path}")

    # Check if request has a headers attribute (for newer websockets versions)
    if not hasattr(request, 'headers'):
        # For older websockets versions (like 14.x), the request might be the headers dictionary itself
        return None

    # Get request method - different ways depending on websockets version
    method = getattr(request, 'method', None)
    if method is None:
        # Try to get it from headers
        method = request.headers.get(':method', 'GET')

    # For OPTIONS requests (CORS preflight)
    if method == "OPTIONS":
        logger.info(f"Handling CORS preflight request")
        # Return 200 OK with CORS headers
        return 200, CORS_HEADERS, b''

    # Check for Upgrade header
    headers = getattr(request, 'headers', {})

    # For WebSocket upgrade, return None to let websockets library handle it
    if 'Upgrade' in headers and headers['Upgrade'].lower() == 'websocket':
        logger.info("WebSocket upgrade request")
        return None

    # For other HTTP requests, return a simple response with CORS headers
    return 200, CORS_HEADERS, b"This server handles WebSocket connections only."

async def main():
    # Start the WebSocket server
    logger.info("Starting WebSocket server for code execution")
    logger.info(f"CORS headers configured: {CORS_HEADERS}")

    try:
        # Create server with minimal configuration for maximum compatibility
        PORT = 9765  # Changed port to avoid conflicts
        # Configuration optimized for browser compatibility
        server = await websockets.serve(
            websocket_handler,
            "0.0.0.0",  # Listen on all interfaces for better compatibility
            PORT,        # Port number
            ping_interval=None,  # Disable built-in pings, we'll handle manually in code
            ping_timeout=None,   # Disable ping timeouts
            close_timeout=5,     # Shorter timeout for closing
            max_size=10_000_000, # 10MB max message size
            process_request=process_request,  # Add CORS handling
            subprotocols=['json'],  # Accept 'json' subprotocol to match client
            # Compression options
            compression=None,  # Disable compression for better compatibility
        )

        logger.info(f"WebSocket server started at ws://localhost:{PORT}")
        logger.info(f"Environment: {os.environ.get('PYTHONPATH', 'Not set')}")

        # Run forever
        await asyncio.Future()
    except Exception as e:
        logger.error(f"Error starting server: {e}")
        logger.error(traceback.format_exc())
        raise

if __name__ == "__main__":
    try:
        # Print version information
        logger.info(f"Python version: {sys.version}")
        logger.info(f"Websockets version: {websockets.__version__}")

        # Run the server
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
        logger.error(traceback.format_exc())
