#!/usr/bin/env python

import asyncio
import websockets
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('websocket-test-client')

async def test_websocket():
    """Test WebSocket connection to the server."""
    try:
        logger.info("Connecting to WebSocket server...")

        # Connect with same protocols as the browser uses
        async with websockets.connect(
            'ws://localhost:9765',
            subprotocols=['json'],
            max_size=10_000_000,
            ping_interval=None  # Disable automatic pings
        ) as websocket:
            logger.info("Connected to WebSocket server")

            # Handle welcome message
            response = await websocket.recv()
            logger.info(f"Received welcome message: {response}")

            # Handle initial ping
            try:
                ping_response = await asyncio.wait_for(websocket.recv(), timeout=2.0)
                logger.info(f"Received initial ping: {ping_response}")
            except asyncio.TimeoutError:
                logger.warning("No initial ping received")

            # Send a ping
            ping_message = json.dumps({
                "type": "ping",
                "timestamp": 123456789
            })
            await websocket.send(ping_message)
            logger.info(f"Sent ping message: {ping_message}")

            # Wait for pong response
            try:
                pong_response = await asyncio.wait_for(websocket.recv(), timeout=2.0)
                logger.info(f"Received pong response: {pong_response}")
            except asyncio.TimeoutError:
                logger.warning("No pong response received")

            # Send a simple code execution request
            code = "print('Hello from the test client')"
            execute_message = json.dumps({
                "type": "execute",
                "code": code
            })
            await websocket.send(execute_message)
            logger.info(f"Sent code execution request: {execute_message}")

            # Wait for status message
            try:
                status_response = await asyncio.wait_for(websocket.recv(), timeout=2.0)
                logger.info(f"Received status message: {status_response}")
            except asyncio.TimeoutError:
                logger.warning("No status message received")

            # Wait for result
            try:
                result_response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                logger.info(f"Received result: {result_response}")
            except asyncio.TimeoutError:
                logger.warning("No result received")

            # Keep the connection open for a moment to test stability
            logger.info("Keeping connection open for a short time...")
            await asyncio.sleep(2.0)
            logger.info("Test completed successfully!")

    except websockets.exceptions.ConnectionClosed as e:
        logger.error(f"Connection closed prematurely: code={e.code}, reason={e.reason}")
    except Exception as e:
        logger.error(f"Error during test: {e}")

# Run the test
if __name__ == "__main__":
    asyncio.run(test_websocket())
