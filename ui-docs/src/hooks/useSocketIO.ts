import { useState, useEffect, useCallback, useRef } from 'react';
import { io, Socket } from 'socket.io-client';

interface SocketIOMessage {
  type: string;
  [key: string]: unknown;
}

// Define a more specific type for Socket.IO message data
type SocketIOData = {
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

interface UseSocketIOProps {
  url: string;
  onOpen?: () => void;
  onClose?: () => void;
  onMessage?: (data: SocketIOData) => void;
  onError?: (error: Error) => void;
  reconnectAttempts?: number;
  initialReconnectInterval?: number;
  maxReconnectInterval?: number;
  autoConnect?: boolean;
}

interface UseSocketIOReturn {
  sendMessage: (message: SocketIOMessage) => void;
  lastMessage: SocketIOData | null;
  isConnected: boolean;
  isConnecting: boolean;
  error: Error | null;
  reconnectCount: number;
  hasGivenUp: boolean;
  resetConnection: () => void;
}

/**
 * Custom hook for Socket.IO communication with improved reliability
 */
export function useSocketIO({
  url,
  onOpen,
  onClose,
  onMessage,
  onError,
  reconnectAttempts = 3,
  autoConnect = true,
}: UseSocketIOProps): UseSocketIOReturn {
  const [lastMessage, setLastMessage] = useState<SocketIOData | null>(null);
  const [isConnected, setIsConnected] = useState<boolean>(false);
  const [isConnecting, setIsConnecting] = useState<boolean>(false);
  const [error, setError] = useState<Error | null>(null);
  const [hasGivenUp, setHasGivenUp] = useState<boolean>(false);

  const socket = useRef<Socket | null>(null);
  const reconnectCount = useRef<number>(0);
  const reconnectTimeout = useRef<ReturnType<typeof setTimeout> | null>(null);

  // Reset connection state for retrying after giving up
  const resetConnection = useCallback(() => {
    reconnectCount.current = 0;
    setHasGivenUp(false);
    connect();
  }, []);

  // Create a Socket.IO connection
  const connect = useCallback(() => {
    // Don't try to connect if we've given up
    if (hasGivenUp) {
      return;
    }

    // Close any existing connection
    if (socket.current) {
      socket.current.disconnect();
      socket.current = null;
    }

    try {
      console.log(`Connecting to Socket.IO server at ${url}...`);
      setIsConnecting(true);

      // Create Socket.IO client
      socket.current = io(url, {
        reconnection: false,  // We'll handle reconnection ourselves
        transports: ['websocket'],  // Use WebSocket only, more reliable
        timeout: 10000,  // 10 second timeout
      });

      // Connection opened
      socket.current.on('connect', () => {
        console.log('Socket.IO connection established');
        setIsConnected(true);
        setIsConnecting(false);
        reconnectCount.current = 0;
        setHasGivenUp(false);

        // Send a ping immediately to test the connection
        try {
          socket.current?.emit('ping', {
            type: 'ping',
            timestamp: Date.now()
          });
          console.log('Initial ping sent');
        } catch (e) {
          console.error('Error sending initial ping:', e);
        }

        if (onOpen) onOpen();
      });

      // Handle messages
      const handleMessage = (eventName: string, data: unknown) => {
        console.log(`Received ${eventName} message:`, data);
        // Ensure data conforms to expected structure
        const messageData: SocketIOData = typeof data === 'object' && data !== null
          ? data as SocketIOData
          : { type: eventName, message: String(data) };
        setLastMessage(messageData);
        if (onMessage) onMessage(messageData);
      };

      // Listen for various message types
      socket.current.on('connection', (data) => handleMessage('connection', data));
      socket.current.on('status', (data) => handleMessage('status', data));
      socket.current.on('result', (data) => handleMessage('result', data));
      socket.current.on('pong', (data) => handleMessage('pong', data));
      socket.current.on('error', (data) => handleMessage('error', data));
      socket.current.on('echo', (data) => handleMessage('echo', data));

      // Connection closed
      socket.current.on('disconnect', (reason) => {
        console.log(`Socket.IO connection closed: ${reason}`);
        setIsConnected(false);
        setIsConnecting(false);

        // Attempt to reconnect if not intentionally closed
        if (reason !== 'io client disconnect' && reconnectCount.current < reconnectAttempts) {
          reconnectCount.current += 1;

          const delay = 1000 * reconnectCount.current;  // Linear backoff

          console.log(`Socket.IO reconnecting in ${delay}ms (attempt ${reconnectCount.current}/${reconnectAttempts})`);

          // Set a timeout for reconnection
          reconnectTimeout.current = setTimeout(() => {
            connect();
          }, delay);
        } else if (reason !== 'io client disconnect' && reconnectCount.current >= reconnectAttempts) {
          // We've reached the maximum number of reconnection attempts
          console.log(`Maximum Socket.IO reconnection attempts (${reconnectAttempts}) reached.`);
          setHasGivenUp(true);
        }

        if (onClose) onClose();
      });

      // Connection error
      socket.current.on('connect_error', (err) => {
        console.error('Socket.IO connection error:', err);
        setError(err);
        setIsConnecting(false);
        if (onError) onError(err);
      });

    } catch (error) {
      console.error('Socket.IO connection setup error:', error);
      setIsConnecting(false);
      if (error instanceof Error) {
        setError(error);
        if (onError) onError(error);
      }
    }
  }, [url, onOpen, onClose, onMessage, onError, reconnectAttempts, hasGivenUp]);

  // Send a message through Socket.IO
  const sendMessage = useCallback((message: SocketIOMessage) => {
    if (socket.current && socket.current.connected) {
      console.log(`Sending message: ${JSON.stringify(message)}`);

      if (message.type === 'execute') {
        socket.current.emit('execute', message);
      } else if (message.type === 'ping') {
        socket.current.emit('ping', message);
      } else {
        // Default fallback for other message types
        socket.current.emit('message', message);
      }
      return true;
    } else {
      console.error('Socket.IO is not connected');

      // Try to reconnect if not connected and not already in the process of connecting
      if (!isConnecting && !isConnected) {
        console.log('Attempting to reconnect before sending message...');
        connect();
      }
      return false;
    }
  }, [connect, isConnecting, isConnected]);

  // Ping server periodically to keep connection alive
  useEffect(() => {
    if (!isConnected) return;

    const pingInterval = setInterval(() => {
      if (socket.current && socket.current.connected) {
        try {
          socket.current.emit('ping', {
            type: 'ping',
            timestamp: Date.now()
          });
          console.log('Ping sent');
        } catch (e) {
          console.error('Error sending ping:', e);
        }
      }
    }, 15000); // Send ping every 15 seconds

    return () => clearInterval(pingInterval);
  }, [isConnected]);

  // Connect on mount if autoConnect is true
  useEffect(() => {
    if (autoConnect) {
      connect();
    }

    // Clean up on unmount
    return () => {
      if (socket.current) {
        socket.current.disconnect();
        socket.current = null;
      }

      // Clear any pending reconnect timeout
      if (reconnectTimeout.current) {
        clearTimeout(reconnectTimeout.current);
        reconnectTimeout.current = null;
      }
    };
  }, [connect, autoConnect]);

  return {
    sendMessage,
    lastMessage,
    isConnected,
    isConnecting,
    error,
    reconnectCount: reconnectCount.current,
    hasGivenUp,
    resetConnection,
  };
}
