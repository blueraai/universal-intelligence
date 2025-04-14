#!/usr/bin/env python

import asyncio
import websockets
import json
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('websocket-server')

# Set all websockets loggers to WARNING to reduce noise
logging.getLogger('websockets').setLevel(logging.WARNING)

async def echo(websocket):
    """Simple WebSocket echo server handler"""
    
    # Send welcome message
    welcome = {
        "type": "connection",
        "status": "connected",
        "message": "Connected to WebSocket server"
    }
    await websocket.send(json.dumps(welcome))
    
    try:
        async for message in websocket:
            try:
                data = json.loads(message)
                logger.info(f"Received message: {data.get('type', 'unknown')}")
                
                # Handle ping messages
                if data.get('type') == 'ping':
                    response = {
                        "type": "pong",
                        "timestamp": data.get('timestamp', 0)
                    }
                    await websocket.send(json.dumps(response))
                
                # Echo other messages back
                else:
                    response = {
                        "type": "echo",
                        "received": data
                    }
                    await websocket.send(json.dumps(response))
                    
            except json.JSONDecodeError:
                # Handle non-JSON messages
                response = {
                    "type": "error",
                    "message": "Invalid JSON message"
                }
                await websocket.send(json.dumps(response))
                
    except websockets.exceptions.ConnectionClosed:
        logger.info(f"Connection closed")

async def main():
    # Start the server
    port = 9765
    server = await websockets.serve(
        echo,
        "localhost",
        port,
        # Simple configuration
        ping_timeout=None
    )
    
    logger.info(f"WebSocket echo server started at ws://localhost:{port}")
    
    # Run forever
    await asyncio.Future()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
