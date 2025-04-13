#!/usr/bin/env python

import asyncio
import websockets
import json
import traceback
import logging
import sys
import os

# Set up detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout  # Ensure logs go to stdout for Docker to capture them
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

        # Send welcome message as JSON for the UI client
        welcome_message = json.dumps({
            "type": "connection",
            "status": "connected",
            "message": "Connected to WebSocket server"
        })
        await websocket.send(welcome_message)
        logger.info(f"Sent welcome message: {welcome_message}")

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

                    # Send running status
                    await websocket.send(json.dumps({
                        "type": "status",
                        "status": "running",
                        "message": "Executing code..."
                    }))

                    # Simulate code execution and send result
                    await asyncio.sleep(0.5)  # Simulate processing time

                    await websocket.send(json.dumps({
                        "type": "result",
                        "status": "completed",
                        "stdout": "Hello from WebSocket Server!\nYour code executed successfully.",
                        "stderr": "",
                        "error": None
                    }))
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

# Process HTTP OPTIONS requests for CORS
async def process_request(path, request):
    """
    Process HTTP requests to handle CORS preflight requests from browsers.

    Parameters:
    - path: The request path
    - request: The websockets.http11.Request object

    Returns:
    - A tuple (status, headers, body) for non-WebSocket requests
    - None for WebSocket upgrade requests (to let websockets library handle it)
    """
    logger.info(f"Processing request for path: {path}")

    # Get the headers
    headers = {}

    # For OPTIONS requests (CORS preflight)
    if request.method == "OPTIONS":
        logger.info(f"Handling CORS preflight request for {path}")
        # Return 200 OK with CORS headers
        return 200, CORS_HEADERS, b''

    # For WebSocket upgrade, add CORS headers to the response
    if "Upgrade" in request.headers and request.headers["Upgrade"].lower() == "websocket":
        logger.info(f"WebSocket upgrade request, adding CORS headers")
        # For WebSocket connections, we'll manually add headers to the response
        # But let the websockets library handle the actual upgrade
        return None

    # For other HTTP requests, we'll return a simple response with CORS headers
    return 200, CORS_HEADERS, b"This server handles WebSocket connections only."

async def main():
    # Start the WebSocket server
    logger.info("Starting WebSocket server for code execution")
    logger.info(f"CORS headers configured: {CORS_HEADERS}")

    try:
        # Create server with minimal configuration for maximum compatibility
        server = await websockets.serve(
            websocket_handler,
            "0.0.0.0",   # Listen on all interfaces
            8765,        # Port number
            ping_interval=20,     # Send pings to keep connection alive
            ping_timeout=30,      # Timeout for pings
            close_timeout=10,     # Timeout for closing
            max_size=10_000_000,  # 10MB max message size
            process_request=process_request,  # Add CORS handling
        )

        logger.info("WebSocket server started at ws://0.0.0.0:8765")
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
