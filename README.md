# Universal Intelligence WebSocket Server

A simple WebSocket server for the Universal Intelligence platform.

## Overview

This WebSocket server provides real-time communication between the Universal Intelligence UI and the backend services. It supports:

- Connection handling with proper handshaking
- JSON message parsing and formatting
- Code execution simulation
- Ping/pong mechanism for connection health checks
- Error handling and recovery

## Implementation

The server is built with Python using the `websockets` library. It handles both browser clients (for the UI) and Python client connections.

## Usage

### Starting the server

```bash
# Build and run with Docker
docker build -t websocket-server .
docker run -d -p 8765:8765 --name websocket-server websocket-server

# Or run directly with Python if you have the dependencies installed
python server.py
```

### Testing the connection

A test client is provided to verify the WebSocket server's functionality:

```bash
python test_client.py
```

If successful, you should see a confirmation message that the WebSocket connection works.

## Protocol

The server handles the following message formats:

1. Text messages: Echoed back with JSON formatting
2. JSON messages with `type: "ping"`: Replied with a pong message maintaining the timestamp
3. JSON messages with `type: "execute"`: Simulates code execution and returns a result

## Troubleshooting

If you encounter connection issues:

1. Verify the server is running: `docker ps | grep websocket-server`
2. Check server logs: `docker logs websocket-server`
3. Ensure port 8765 is accessible: `curl -v http://localhost:8765`
4. Try the test client: `python test_client.py`

Browser connections are more complex and may require additional debugging with browser developer tools.

## Notes on WebSocket Versions

The current server is optimized for WebSockets version 15.0.1 (in Docker) and tested with WebSockets version 14.1 (Python client). This version difference can sometimes cause subtle compatibility issues that were addressed in the implementation.
