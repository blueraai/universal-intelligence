# Universal Intelligence Playground Connectivity

## Overview

This document focuses exclusively on the connectivity issues between the Universal Intelligence code playground frontend and the WebSocket server backend. Solving these connectivity challenges is critical to allow users to execute code examples directly in the browser.

## Current Status

The code playground component has been implemented in the frontend, but the WebSocket connectivity to the backend server has been experiencing issues:

1. Connection stability problems between browser clients and the WebSocket server
2. Compatibility issues with WebSockets version differences
3. Excessive connection logging overwhelming the server logs
4. Challenges with connection timing and handshake procedures

Recent fixes have addressed some of these issues, but further work is needed to achieve reliable code execution.

## Core Components

### Frontend WebSocket Client

The primary frontend component for WebSocket connectivity is:
- **File**: `ui-docs/src/hooks/useWebSocket.ts`
- **Purpose**: React hook that manages WebSocket connections, handles reconnection logic, and provides an interface for sending/receiving messages.

### Backend WebSocket Server

Two server implementations exist:
- **Primary File**: `ui-docs/server/server.py` - Original WebSocket server with basic functionality
- **Enhanced File**: `ui-docs/server/server_browser.py` - Optimized version specifically for browser clients

## Recent Improvements

1. Fixed WebSocket protocol handling to work with WebSockets v14+ in `ui-docs/server/server_browser.py`
2. Added request header compatibility for different WebSocket library versions
3. Implemented proper handling of connection protocols for browser clients
4. Added delay before WebSocket creation to avoid race conditions
5. Added proper async handling in the React hook for connection management
6. Reduced excessive logging by setting WebSockets server logger to WARNING level

## Remaining Issues

1. **Connection Stability**: Some connections still drop unexpectedly, especially under load
2. **Code Execution Integration**: Need to properly integrate the code editor with the WebSocket client
3. **Error Handling**: Improve error visualization when WebSocket errors occur
4. **Reconnection Strategy**: Enhance the reconnection logic for more reliable recovery

## Technical Implementation Details

### WebSocket Connection Protocol

The WebSocket connection uses a JSON-based message protocol:

```typescript
// Message Types
interface WebSocketMessage {
  type: string;
  [key: string]: unknown;
}

// Example: Code Execution Flow
// Client to Server
{
  "type": "execute",
  "code": "print('Hello, Universal Intelligence!')"
}

// Server to Client (Status)
{
  "type": "status",
  "status": "running",
  "message": "Executing code..."
}

// Server to Client (Result)
{
  "type": "result",
  "status": "completed", // or "error"
  "stdout": "Hello, Universal Intelligence!\n",
  "stderr": "",
  "error": null // or error object
}

// Keep-alive mechanism
{
  "type": "ping",
  "timestamp": 1681234567890
}
```

### Connection Initialization

The critical part of the connection process is:

```typescript
// In useWebSocket.ts
const connect = useCallback(async () => {
  // ...

  // Create WebSocket with protocols to improve compatibility
  // Force a small delay (50ms) before creating the WebSocket to avoid race conditions
  await new Promise(resolve => setTimeout(resolve, 50));

  // Create with explicit protocol for browser compatibility
  socket.current = new WebSocket(url, ['json']);

  // Set binaryType to improve compatibility
  socket.current.binaryType = 'arraybuffer';

  // ...
}, [url, onOpen, onClose, onMessage, onError, reconnectAttempts,
    initialReconnectInterval, maxReconnectInterval, hasGivenUp]);
```

### Server Request Processing

On the server side, request handling must support different WebSocket library versions:

```python
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
```

## Next Steps - Connectivity Focus

To complete the connectivity work, focus on these specific steps:

1. **Verify Connection Stability**
   - Test connections under various load conditions
   - Monitor connection drops and identify patterns
   - Ensure proper reconnection behavior when disconnections occur

2. **Complete Code Editor Integration**
   - Properly wire the code editor component to the WebSocket hook
   - Implement proper status indicators during code execution
   - Handle both successful and failed execution results

3. **Implement Error Recovery**
   - Add specific handling for common WebSocket errors
   - Provide clear feedback to users when connection issues occur
   - Implement automatic recovery strategies when possible

4. **Add Comprehensive Logging**
   - Implement structured logging on both client and server
   - Add connection event tracking for debugging purposes
   - Create a diagnostics panel for connection status (developer mode)

5. **Stress Testing**
   - Test with multiple simultaneous connections
   - Test with various code execution payloads (large outputs, long-running code)
   - Verify performance under different network conditions

## Troubleshooting Guide

When working on WebSocket connectivity issues, use these troubleshooting steps:

1. **Check Browser Console**
   - Look for WebSocket connection errors or warnings
   - Inspect network tab for failed WebSocket connections
   - Verify WebSocket frames for proper message format

2. **Verify Server Logs**
   - Look for connection attempts in the server logs
   - Check for error messages related to specific client connections
   - Verify proper handshake completion for new connections

3. **Test with Different Browsers**
   - Chrome and Firefox handle WebSockets slightly differently
   - Verify behavior is consistent across browsers
   - Use browser developer tools to inspect connection details

4. **Connection Diagnostic Commands**
   - Use network utilities to verify server availability:
     ```bash
     curl -v http://localhost:9765
     ```
   - Test WebSocket connectivity with a simple client:
     ```bash
     python ui-docs/tests/test_websocket.py
     ```

## Success Criteria

The playground connectivity issue will be considered resolved when:

1. Users can connect to the WebSocket server reliably from any browser
2. Code examples execute successfully with proper output display
3. Connection errors are handled gracefully with clear user feedback
4. Reconnection happens automatically when connections are disrupted
5. The system can handle multiple concurrent users executing code examples
