#!/usr/bin/env python

import asyncio
import websockets
import json
import sys
import logging

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('websocket-client')

async def test_connection():
    """Simple WebSocket client to test connectivity to our server"""
    uri = "ws://localhost:8765"
    logger.info(f"Attempting to connect to {uri}")

    try:
        async with websockets.connect(uri, ping_interval=None) as websocket:
            logger.info("Connected to WebSocket server")

            # Wait for the initial message
            greeting = await websocket.recv()
            logger.info(f"Received: {greeting}")

            # Send a test message
            test_message = "Hello from test client"
            logger.info(f"Sending: {test_message}")
            await websocket.send(test_message)

            # Wait for the response
            response = await websocket.recv()
            logger.info(f"Received: {response}")

            # Send a JSON message
            json_message = json.dumps({
                "type": "ping",
                "timestamp": 123456789
            })
            logger.info(f"Sending JSON: {json_message}")
            await websocket.send(json_message)

            # Wait for the response
            json_response = await websocket.recv()
            logger.info(f"Received: {json_response}")

            logger.info("Test completed successfully")

    except Exception as e:
        logger.error(f"Error: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False

    return True

async def main():
    """Main entry point"""
    try:
        logger.info("Starting WebSocket connection test")
        success = await test_connection()
        if success:
            logger.info("✅ Test succeeded: WebSocket connection works")
            return 0
        else:
            logger.error("❌ Test failed: Could not establish WebSocket connection")
            return 1
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return 2

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
