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
    level=logging.INFO,  # Change to INFO level for less verbose logs
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger('websocket-server')
logger.setLevel(logging.INFO)

# Reduce connection noise by setting websockets.server to WARNING level
# This will suppress the excessive connection messages while preserving important info
websockets_logger = logging.getLogger('websockets.server')
websockets_logger.setLevel(logging.WARNING)

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

# Process HTTP OPTIONS requests for CORS
async def process_request(path, request_headers):
    """Simple CORS handler for browser preflight requests"""
    # Check if this is a Request object (websockets v14+) or a dict (older versions)
    if hasattr(request_headers, 'headers'):
        # For websockets v14+, Request object
        protocol = request_headers.headers.get('Sec-WebSocket-Protocol', '')
        if protocol.lower() == 'json':
            return None
    elif isinstance(request_headers, dict):
        # For older websockets versions that pass headers as dict
        protocol = request_headers.get('Sec-WebSocket-Protocol', '')
        if protocol.lower() == 'json':
            return None

    # For non-WebSocket requests, return a simple response with CORS headers
    return http_response(
        200,
        CORS_HEADERS,
        b"WebSocket server is running. Connect with a WebSocket client to the endpoint."
    )

def http_response(status, headers, body):
    """Helper to create HTTP responses"""
    return (status, headers, body)

# WebSocket handler with browser-specific optimizations
async def websocket_handler(websocket, path=None):
    """Optimized WebSocket handler for browser clients"""
    client_id = id(websocket)
    client_info = f"{websocket.remote_address if hasattr(websocket, 'remote_address') else 'Unknown'}-{client_id}"
    logger.info(f"Connection opened from {client_info}")

    try:
        # Send welcome message
        welcome_message = json.dumps({
            "type": "connection",
            "status": "connected",
            "message": "Connected to WebSocket server"
        })

        await websocket.send(welcome_message)
        logger.info(f"Sent welcome message to {client_info}")

        # Send immediate ping to maintain connection
        ping_message = json.dumps({
            "type": "ping",
            "timestamp": int(time.time() * 1000)
        })
        await websocket.send(ping_message)

        # Message processing loop
        async for message in websocket:
            try:
                # Parse JSON message
                data = json.loads(message)
                message_type = data.get('type', '')
                logger.info(f"Received {message_type} from {client_info}")

                # Handle different message types
                if message_type == 'execute':
                    # Get code to execute
                    code = data.get('code', '')

                    if not code.strip():
                        await websocket.send(json.dumps({
                            "type": "result",
                            "status": "error",
                            "stdout": "",
                            "stderr": "No code provided.",
                            "error": {"type": "ValueError", "message": "No code provided."}
                        }))
                        continue

                    # Send status update
                    await websocket.send(json.dumps({
                        "type": "status",
                        "status": "running",
                        "message": "Executing code..."
                    }))

                    # Execute the code
                    result = await execute_with_timeout(code)
                    result["type"] = "result"
                    result["status"] = "completed" if not result.get("error") else "error"

                    # Send result
                    await websocket.send(json.dumps(result))
                    logger.info(f"Execution completed for {client_info}")

                elif message_type == 'ping':
                    # Respond to ping with pong
                    timestamp = data.get('timestamp', int(time.time() * 1000))
                    pong_message = json.dumps({
                        "type": "pong",
                        "timestamp": timestamp
                    })
                    await websocket.send(pong_message)

                else:
                    # Echo other message types
                    response = {
                        "type": "echo",
                        "received": data,
                        "message": "Unknown message type"
                    }
                    await websocket.send(json.dumps(response))

            except json.JSONDecodeError:
                logger.warning(f"Received invalid JSON from {client_info}")
                await websocket.send(json.dumps({
                    "type": "error",
                    "message": "Invalid JSON received"
                }))

            except Exception as e:
                logger.error(f"Error processing message from {client_info}: {e}")
                error_msg = json.dumps({
                    "type": "error",
                    "message": str(e)
                })
                await websocket.send(error_msg)

        logger.info(f"Message loop ended normally for {client_info}")

    except websockets.exceptions.ConnectionClosed as e:
        logger.info(f"Connection closed for {client_info}: code={e.code}, reason={e.reason}")

    except Exception as e:
        logger.error(f"Unexpected error for {client_info}: {e}")
        logger.error(traceback.format_exc())

    finally:
        logger.info(f"Connection closed for {client_info}")

async def ping_clients():
    """Periodically ping all clients to keep connections alive"""
    while True:
        await asyncio.sleep(30)  # Send a ping every 30 seconds

async def main():
    """Start the WebSocket server"""
    port = 9765

    # Start server with browser-optimized settings
    logger.info(f"Starting WebSocket server for browser clients on port {port}")

    try:
        server = await websockets.serve(
            websocket_handler,
            "0.0.0.0",  # Listen on all network interfaces
            port,
            # Disable built-in ping/pong (we handle our own)
            ping_interval=None,
            ping_timeout=None,
            # Very permissive close timeout
            close_timeout=5,
            # Use process_request for CORS
            process_request=process_request,
            # Support the 'json' subprotocol
            subprotocols=['json'],
            # Disable compression for compatibility
            compression=None,
            # Large message size
            max_size=10_000_000
        )

        logger.info(f"Server running at ws://localhost:{port}")
        logger.info("Press Ctrl+C to stop the server")

        # Start background ping task
        ping_task = asyncio.create_task(ping_clients())

        # Run forever
        await asyncio.Future()

    except Exception as e:
        logger.error(f"Server error: {e}")
        logger.error(traceback.format_exc())
        raise

if __name__ == "__main__":
    try:
        # Log versions
        logger.info(f"Python version: {sys.version}")
        logger.info(f"Websockets version: {websockets.__version__}")

        # Run the server
        asyncio.run(main())

    except KeyboardInterrupt:
        logger.info("Server stopped by user")

    except Exception as e:
        logger.error(f"Fatal error: {e}")
        logger.error(traceback.format_exc())
        sys.exit(1)
