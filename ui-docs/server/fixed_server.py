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
from typing import Dict, Any, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('websocket-server')

# Set all websockets loggers to WARNING to reduce noise
logging.getLogger('websockets').setLevel(logging.WARNING)

# Security settings
MAX_EXECUTION_TIME = 10  # seconds
MAX_OUTPUT_SIZE = 100 * 1024  # 100KB

# Track active connections
active_connections = set()

# CORS headers
CORS_HEADERS = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization, Sec-WebSocket-Protocol',
    'Access-Control-Max-Age': '86400',
}

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

async def websocket_handler(websocket):
    """WebSocket connection handler with code execution capabilities"""
    # Add to active connections
    active_connections.add(websocket)
    client_id = id(websocket)
    client_info = f"{client_id}"
    
    logger.info(f"New connection from {client_info}")
    
    try:
        # Send welcome message immediately
        welcome = {
            "type": "connection",
            "status": "connected",
            "message": "Connected to WebSocket server"
        }
        await websocket.send(json.dumps(welcome))
        
        # Message handling loop
        async for message in websocket:
            try:
                # Parse as JSON
                data = json.loads(message)
                message_type = data.get('type', '')
                logger.info(f"Received message: {message_type}")
                
                if message_type == 'execute':
                    # Handle code execution
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
                    
                    # Send running status
                    await websocket.send(json.dumps({
                        "type": "status",
                        "status": "running",
                        "message": "Executing code..."
                    }))
                    
                    # Execute code and send result
                    result = await execute_with_timeout(code)
                    result["type"] = "result"
                    result["status"] = "error" if result.get("error") else "completed"
                    
                    await websocket.send(json.dumps(result))
                    
                elif message_type == 'ping':
                    # Handle ping message
                    await websocket.send(json.dumps({
                        "type": "pong",
                        "timestamp": data.get('timestamp', int(time.time() * 1000))
                    }))
                    
                else:
                    # Echo other messages
                    await websocket.send(json.dumps({
                        "type": "echo",
                        "received": data,
                        "message": "Unknown message type"
                    }))
                    
            except json.JSONDecodeError:
                # Handle non-JSON messages
                await websocket.send(json.dumps({
                    "type": "error",
                    "message": "Invalid JSON message"
                }))
                
            except Exception as e:
                # Handle other errors
                logger.error(f"Error processing message: {e}")
                await websocket.send(json.dumps({
                    "type": "error",
                    "message": str(e)
                }))
                
    except websockets.exceptions.ConnectionClosed as e:
        logger.info(f"Connection closed for {client_info}: code={e.code if hasattr(e, 'code') else 'unknown'}")
        
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

async def main():
    """Start the WebSocket server"""
    port = 9765
    host = "localhost"
    
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
            ping_timeout=None,
            # Simpler configuration for better compatibility
            max_size=10_000_000
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
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        logger.error(traceback.format_exc())
        sys.exit(1)
