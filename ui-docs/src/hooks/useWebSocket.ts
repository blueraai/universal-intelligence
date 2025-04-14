import { useState, useEffect, useCallback, useRef } from 'react';

interface WebSocketMessage {
  type: string;
  [key: string]: unknown;
}

// Define a more specific type for WebSocket message data
type WebSocketData = {
  type: string;
  status?: string;
  message?: string;
  stdout?: string;
  stderr?: string;
  error?: {
    type?: string;
    message?: string;
    traceback?: string;
  } | null;
  timestamp?: number;
  [key: string]: unknown;
};

interface UseWebSocketProps {
  url: string;
  onOpen?: () => void;
  onClose?: () => void;
  onMessage?: (data: WebSocketData) => void;
  onError?: (error: Event) => void;
  reconnectAttempts?: number;
  initialReconnectInterval?: number;
  maxReconnectInterval?: number;
  autoConnect?: boolean;
}

interface UseWebSocketReturn {
  sendMessage: (message: WebSocketMessage) => void;
  lastMessage: WebSocketData | null;
  readyState: number;
  connect: () => void;
  disconnect: () => void;
  isConnected: boolean;
  isConnecting: boolean;
  error: Event | null;
  reconnectCount: number;
  hasGivenUp: boolean;
  resetConnection: () => void;
}

/**
 * Custom hook for WebSocket communication with exponential backoff
 */
export function useWebSocket({
  url,
  onOpen,
  onClose,
  onMessage,
  onError,
  reconnectAttempts = 3,
  initialReconnectInterval = 1000,
  maxReconnectInterval = 30000,
  autoConnect = true,
}: UseWebSocketProps): UseWebSocketReturn {
  const [lastMessage, setLastMessage] = useState<WebSocketData | null>(null);
  const [readyState, setReadyState] = useState<number>(WebSocket.CLOSED);
  const [error, setError] = useState<Event | null>(null);
  const [hasGivenUp, setHasGivenUp] = useState<boolean>(false);

  const socket = useRef<WebSocket | null>(null);
  const reconnectCount = useRef<number>(0);
  const reconnectDelay = useRef<number>(initialReconnectInterval);
  const reconnectTimeoutId = useRef<ReturnType<typeof setTimeout> | null>(null);

  // Check connection state
  const isConnected = readyState === WebSocket.OPEN;
  const isConnecting = readyState === WebSocket.CONNECTING;

  // Reset connection state for retrying after giving up
  const resetConnection = useCallback(async () => {
    reconnectCount.current = 0;
    reconnectDelay.current = initialReconnectInterval;
    setHasGivenUp(false);
    await connect();
  }, [initialReconnectInterval]);

  // Create a WebSocket connection
  const connect = useCallback(async () => {
    // Don't try to connect if we've given up
    if (hasGivenUp) {
      return;
    }

    // Close any existing connection
    if (socket.current) {
      try {
        // Clean close of existing connection
        socket.current.onclose = null; // Remove existing handler
        socket.current.onerror = null; // Remove existing handler
        socket.current.close(1000, "Closing for new connection");
      } catch (e) {
        console.error("Error closing existing connection:", e);
      }
      socket.current = null;
    }

      // Create a new WebSocket instance
      try {
        console.log(`Connecting to WebSocket at ${url}...`);

        // For debugging, log navigator information if in browser environment
        if (typeof navigator !== 'undefined') {
          console.log(`Browser: ${navigator.userAgent}`);
        }

        // Create WebSocket with protocols to improve compatibility
        // Force a small delay (50ms) before creating the WebSocket to avoid race conditions
        await new Promise(resolve => setTimeout(resolve, 50));

        // Create with explicit protocol for browser compatibility
        socket.current = new WebSocket(url, ['json']);

        // Set binaryType to improve compatibility
        socket.current.binaryType = 'arraybuffer';
        setReadyState(WebSocket.CONNECTING);

      // Connection opened
      socket.current.onopen = () => {
        console.log('WebSocket connection established');
        setReadyState(WebSocket.OPEN);
        reconnectCount.current = 0;
        reconnectDelay.current = initialReconnectInterval;
        setHasGivenUp(false);

        // Send a ping immediately to test the connection
        try {
          socket.current?.send(JSON.stringify({
            type: 'ping',
            timestamp: Date.now()
          }));
          console.log('Initial ping sent');
        } catch (e) {
          console.error('Error sending initial ping:', e);
        }

        if (onOpen) onOpen();
      };

      // Listen for messages
      socket.current.onmessage = (event) => {
        try {
          console.log(`Received message: ${event.data}`);
          const data = JSON.parse(event.data) as WebSocketData;
          setLastMessage(data);
          if (onMessage) onMessage(data);
        } catch (e) {
          console.error('Error parsing WebSocket message:', e);
        }
      };

      // Connection closed
      socket.current.onclose = (event) => {
        console.log(`WebSocket connection closed: ${event.code} ${event.reason}`);
        setReadyState(WebSocket.CLOSED);

        // Attempt to reconnect if not intentionally closed
        if (!event.wasClean && reconnectCount.current < reconnectAttempts) {
          reconnectCount.current += 1;

          // Exponential backoff with max limit
          reconnectDelay.current = Math.min(
            reconnectDelay.current * 1.5,
            maxReconnectInterval
          );

          console.log(`WebSocket reconnecting in ${reconnectDelay.current}ms (attempt ${reconnectCount.current}/${reconnectAttempts})`);

          // Set a timeout for reconnection
          reconnectTimeoutId.current = setTimeout(() => {
            connect();
          }, reconnectDelay.current);
        } else if (!event.wasClean && reconnectCount.current >= reconnectAttempts) {
          // We've reached the maximum number of reconnection attempts
          console.log(`Maximum WebSocket reconnection attempts (${reconnectAttempts}) reached.`);
          setHasGivenUp(true);
        }

        if (onClose) onClose();
      };

      // Connection error
      socket.current.onerror = (event) => {
        console.error('WebSocket error:', event);
        setError(event);
        if (onError) onError(event);
      };
    } catch (error) {
      console.error('WebSocket connection error:', error);
    }
  }, [url, onOpen, onClose, onMessage, onError, reconnectAttempts, initialReconnectInterval, maxReconnectInterval, hasGivenUp]);

  // Close the WebSocket connection
  const disconnect = useCallback(() => {
    if (socket.current) {
      socket.current.close();
      socket.current = null;
    }

    // Clear any pending reconnect timeout
    if (reconnectTimeoutId.current) {
      clearTimeout(reconnectTimeoutId.current);
      reconnectTimeoutId.current = null;
    }

    setReadyState(WebSocket.CLOSED);
  }, []);

  // Send a message through the WebSocket
  const sendMessage = useCallback((message: WebSocketMessage) => {
    if (socket.current && socket.current.readyState === WebSocket.OPEN) {
      const messageStr = JSON.stringify(message);
      console.log(`Sending message: ${messageStr}`);
      socket.current.send(messageStr);
      return true;
    } else {
      console.error('WebSocket is not connected');
      // Try to reconnect if not open and not already in the process of connecting
      if (!isConnecting && socket.current?.readyState !== WebSocket.CONNECTING) {
        console.log('Attempting to reconnect before sending message...');
        // Use void to ignore the Promise since this is a sync function
        void connect();
      }
      return false;
    }
  }, [connect, isConnecting]);

  // Ping server periodically to keep connection alive
  useEffect(() => {
    if (!isConnected) return;

    const pingInterval = setInterval(() => {
      if (socket.current?.readyState === WebSocket.OPEN) {
        try {
          socket.current.send(JSON.stringify({
            type: 'ping',
            timestamp: Date.now()
          }));
          console.log('Ping sent');
        } catch (e) {
          console.error('Error sending ping:', e);
        }
      }
    }, 15000); // Send ping every 15 seconds

    return () => clearInterval(pingInterval);
  }, [isConnected]);

  // Force reconnection when server is restarted or if connection is lost
  useEffect(() => {
    if (hasGivenUp) {
      const timer = setTimeout(() => {
        console.log('Attempting to reconnect automatically after giving up...');
        resetConnection();
      }, 5000); // Try to reconnect every 5 seconds after giving up

      return () => clearTimeout(timer);
    }
  }, [hasGivenUp, resetConnection]);

  // Connect on mount if autoConnect is true
  useEffect(() => {
    if (autoConnect) {
      connect();
    }

    // Clean up on unmount
    return () => {
      disconnect();
    };
  }, [connect, disconnect, autoConnect]);

  return {
    sendMessage,
    lastMessage,
    readyState,
    connect,
    disconnect,
    isConnected,
    isConnecting,
    error,
    reconnectCount: reconnectCount.current,
    hasGivenUp,
    resetConnection,
  };
}
