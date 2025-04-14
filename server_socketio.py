#!/usr/bin/env python

import asyncio
import socketio
import aiohttp
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
logger = logging.getLogger('socketio-server')
logger.setLevel(logging.DEBUG)

# Create a Socket.IO server
sio = socketio.AsyncServer(
    async_mode='aiohttp',
    cors_allowed_origins=['http://localhost:5173'],  # Allow connections from the frontend
    ping_interval=25,
    ping_timeout=60,
    max_http_buffer_size=10_000_000,  # 10MB max message size
)

# Create an application instance for the server
app = aiohttp.web.Application()
sio.attach(app)

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

# Socket.IO event handlers
@sio.event
async def connect(sid, environ):
    """Handle client connection"""
    logger.info(f"Client connected: {sid}")
    # Send welcome message
    await sio.emit('connection', {
        "type": "connection",
        "status": "connected",
        "message": "Connected to Socket.IO server"
    }, room=sid)

@sio.event
async def disconnect(sid):
    """Handle client disconnection"""
    logger.info(f"Client disconnected: {sid}")

@sio.event
async def ping(sid, data):
    """Respond to ping messages"""
    logger.info(f"Received ping from {sid}")
    await sio.emit('pong', {
        "type": "pong",
        "timestamp": int(time.time() * 1000)
    }, room=sid)

@sio.event
async def execute(sid, data):
    """Execute Python code"""
    logger.info(f"Received code execution request from {sid}")

    try:
        code = data.get('code', '')

        if not code.strip():
            await sio.emit('result', {
                "type": "result",
                "status": "error",
                "stdout": "",
                "stderr": "No code provided.",
                "error": {"type": "ValueError", "message": "No code provided."}
            }, room=sid)
            return

        # Send running status
        await sio.emit('status', {
            "type": "status",
            "status": "running",
            "message": "Executing code..."
        }, room=sid)

        # Actually execute the code
        result = await execute_with_timeout(code)

        # Add completion status
        result["type"] = "result"
        result["status"] = "error" if result.get("error") else "completed"

        # Send result to client
        await sio.emit('result', result, room=sid)
        logger.info("Sent execution result")

    except Exception as e:
        logger.error(f"Error processing execution request: {e}")
        logger.error(traceback.format_exc())
        await sio.emit('error', {
            "type": "error",
            "message": str(e),
            "traceback": traceback.format_exc()
        }, room=sid)

# This is a generic event handler that logs any events not specifically handled
@sio.event
async def message(sid, data):
    """Handle generic messages"""
    logger.info(f"Received message from {sid}: {data}")
    try:
        # Echo the message back with an echo type
        await sio.emit('echo', {
            "type": "echo",
            "original": data,
            "message": "Echo from server"
        }, room=sid)
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        logger.error(traceback.format_exc())
        await sio.emit('error', {
            "type": "error",
            "message": str(e),
            "traceback": traceback.format_exc()
        }, room=sid)

# Main function to run the server
async def main():
    """Run the Socket.IO server"""
    logger.info("Starting Socket.IO server for code execution")

    PORT = 9765

    # Configure the server
    runner = aiohttp.web.AppRunner(app)
    await runner.setup()
    site = aiohttp.web.TCPSite(runner, '0.0.0.0', PORT)

    # Start the server
    await site.start()
    logger.info(f"Socket.IO server started at http://localhost:{PORT}")

    # Keep the server running
    try:
        # Keep the server running indefinitely
        await asyncio.Future()
    except asyncio.CancelledError:
        # Cleanup when the task is cancelled
        await runner.cleanup()

if __name__ == "__main__":
    try:
        # Print version information
        logger.info(f"Python version: {sys.version}")
        logger.info(f"SocketIO version: {socketio.__version__}")
        logger.info(f"aiohttp version: {aiohttp.__version__}")

        # Run the server
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
        logger.error(traceback.format_exc())
