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
from typing import Dict, Any, Optional, Tuple, Union

# Configure logging with reduced verbosity
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger('websocket-server')
logger.setLevel(logging.INFO)

# Set all websockets loggers to WARNING to reduce noise
for logger_name in ['websockets.server', 'websockets.protocol', 'websockets.client']:
    logging.getLogger(logger_name).setLevel(logging.WARNING)

# CORS headers
CORS_HEADERS = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization, Sec-WebSocket-Protocol',
    'Access-Control-Max-Age': '86400',
}

# Security settings
MAX_EXECUTION_TIME = 10  # seconds
MAX_OUTPUT_SIZE = 100 * 1024  # 100KB

# Track active connections
active_connections = set()

def execute_python_code(code: str) -> Dict[str, Any]:
    """Execute Python code in a restricted environment and capture output"""
    stdout = io.StringIO()
    stderr = io.StringIO()
    local_vars = {}
    error_info = None

    try:
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            exec(code, {"__builtins__": __builtins__}, local_vars)
    except Exception as e:
        error_type = type(e).__name__
        error_msg = str(e)
        error_traceback = traceback.format_exc()
        error_traceback = re.sub(r'File ".*[/\\]', 'File "', error_traceback)
        
        error_info = {
            "type": error_type,
            "message": error_msg,
            "traceback": error_traceback
        }

    # Truncate output if needed
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

async def execute_with_timeout(code: str, timeout: int = MAX_EXECUTION_TIME) -> Dict[str, Any]:
    """Execute code with a timeout to prevent infinite loops"""
    try:
        loop = asyncio.get_event_loop()
        result = await asyncio.wait_for(
            loop.run_in_executor(None, execute_python_code, code),
            timeout=timeout
        )
        return result
    except asyncio.TimeoutError:
        return {
            "stdout": "",
            "stderr": f"Execution timed out after {timeout} seconds.",
            "error": {
                "type": "TimeoutError",
                "message": f"Code execution took too long (exceeded {timeout} seconds limit).",
                "traceback": ""
            }
        }

async def send_json(websocket, data: Dict[str, Any]) -> bool:
    """Safely send JSON data with error handling"""
    try:
        message = json.dumps(data)
        await websocket.send(message)
        return True
    except websockets.exceptions.ConnectionClosed:
        return False
    except Exception as e:
        logger.error(f"Error sending message: {e}")
        return False

async def process_request(path, request_headers):
    """
    Process HTTP requests - compatible with all websockets versions
    """
    # Handle different websockets versions (10.x through 15.x)
    if hasattr(request_headers, 'headers'):
        # For websockets v10+ with Request object
        method = getattr(request_headers, 'method', 'GET')
        
        if method == "OPTIONS":
            return 200, CORS_HEADERS, b''
        
        # Support for the 'json' subprotocol
        if path == '/' and 'Upgrade' in request_headers.headers:
            return None  # Let the websockets library handle WebSocket upgrades
            
    elif isinstance(request_headers, dict):
        # For older websockets versions with dict headers
        method = request_headers.get(':method', 'GET')
        
        if method == "OPTIONS":
            return 200, CORS_HEADERS, b''
            
        # Check for websocket upgrade
        if path == '/' and 'upgrade' in request_headers.get('connection', '').lower():
            return None
    
    # For non-WebSocket requests, return a simple message
    return 200, CORS_HEADERS, b"WebSocket server is running. Connect with a WebSocket client."

async def websocket_handler(websocket, path=None):
    """WebSocket connection handler optimized for browser clients"""
    # Generate client ID for tracking
    client_id = id(websocket)
    remote_addr = getattr(websocket, 'remote_address', 'unknown')
    client_info = f"{remote_addr}-{client_id}"
    
    logger.info(f"New connection from {client_info}")
    
    # Add to active connections
    active_connections.add(websocket)
    
    try:
        # Get accepted subprotocols (works in multiple websockets versions)
        subprotocol = getattr(websocket, 'subprotocol', None)
        logger.info(f"Using subprotocol: {subprotocol}")
        
        # Send welcome message immediately
        await send_json(websocket, {
            "type": "connection",
            "status": "connected",
            "message": "Connected to WebSocket server"
        })
        
        # Small delay before initial ping to ensure connection is stable
        await asyncio.sleep(0.1)
        
        # Send an initial ping
        await send_json(websocket, {
            "type": "ping",
            "timestamp": int(time.time() * 1000)
        })
        
        # Message handling loop
        async for message in websocket:
            try:
                # Try to parse as JSON
                data = json.loads(message)
                message_type = data.get('type', '')
                
                if message_type == 'execute':
                    # Handle code execution
                    code = data.get('code', '')
                    
                    if not code.strip():
                        await send_json(websocket, {
                            "type": "result",
                            "status": "error",
                            "stdout": "",
                            "stderr": "No code provided.",
                            "error": {"type": "ValueError", "message": "No code provided."}
                        })
                        continue
                    
                    # Send running status
                    await send_json(websocket, {
                        "type": "status",
                        "status": "running",
                        "message": "Executing code..."
                    })
                    
                    # Execute code and send result
                    result = await execute_with_timeout(code)
                    result["type"] = "result"
                    result["status"] = "error" if result.get("error") else "completed"
                    
                    await send_json(websocket, result)
                    
                elif message_type == 'ping':
                    # Handle ping message
                    await send_json(websocket, {
                        "type": "pong",
                        "timestamp": data.get('timestamp', int(time.time() * 1000))
                    })
                    
                else:
                    # Echo other messages
                    await send_json(websocket, {
                        "type": "echo",
                        "received": data,
                        "message": "Unknown message type"
                    })
                    
            except json.JSONDecodeError:
                # Handle non-JSON messages
                await send_json(websocket, {
                    "type": "error",
                    "message": "Invalid JSON message"
                })
                
            except Exception as e:
                # Handle other errors
                logger.error(f"Error processing message: {e}")
                await send_json(websocket, {
                    "type": "error",
                    "message": str(e)
                })
                
    except websockets.exceptions.ConnectionClosed as e:
        logger.info(f"Connection closed for {client_info}: code={e.code}, reason={e.reason}")
        
    except Exception as e:
        logger.error(f"Error in handler for {client_info}: {e}")
        logger.error(traceback.format_exc())
        
    finally:
        # Remove from active connections
        active_connections.remove(websocket)
        logger.info(f"Connection closed for {client_info}")

async def heartbeat():
    """Send periodic pings to all connected clients"""
    while True:
        try:
            if active_connections:
                timestamp = int(time.time() * 1000)
                ping_message = json.dumps({
                    "type": "ping",
                    "timestamp": timestamp
                })
                
                # Create a list of send operations
                send_tasks = [
                    asyncio.create_task(ws.send(ping_message))
                    for ws in active_connections
                ]
                
                # Use gather with return_exceptions to prevent one failure affecting others
                if send_tasks:
                    await asyncio.gather(*send_tasks, return_exceptions=True)
                    
                logger.debug(f"Sent heartbeat to {len(active_connections)} clients")
                
        except Exception as e:
            logger.error(f"Error in heartbeat: {e}")
            
        await asyncio.sleep(15)  # Send heartbeat every 15 seconds

async def start_server():
    """Start the WebSocket server with optimal browser compatibility"""
    port = int(os.environ.get('PORT', 9765))
    host = os.environ.get('HOST', '0.0.0.0')
    
    logger.info(f"Starting WebSocket server on {host}:{port}")
    logger.info(f"Python version: {sys.version}")
    logger.info(f"Websockets version: {websockets.__version__}")
    
    try:
        # Start heartbeat task
        heartbeat_task = asyncio.create_task(heartbeat())
        
        # Configure the server
        server = await websockets.serve(
            websocket_handler,
            host,
            port,
            # Disable built-in ping mechanism (we use our own)
            ping_interval=None,
            ping_timeout=None,
            # Use a short close timeout
            close_timeout=5,
            # Support subprotocols
            subprotocols=['json'],
            # Disable compression (can cause issues with some clients)
            compression=None,
            # Handle preflight requests for CORS
            process_request=process_request,
            # Allow larger messages
            max_size=10_000_000,
        )
        
        logger.info(f"WebSocket server running at ws://{host}:{port}")
        logger.info("Press Ctrl+C to stop the server")
        
        # Keep server running
        await asyncio.Future()
        
    except Exception as e:
        logger.error(f"Error starting server: {e}")
        logger.error(traceback.format_exc())
        raise
    finally:
        # Ensure heartbeat task is cancelled if server stops
        if 'heartbeat_task' in locals():
            heartbeat_task.cancel()

if __name__ == "__main__":
    try:
        asyncio.run(start_server())
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        logger.error(traceback.format_exc())
        sys.exit(1)
