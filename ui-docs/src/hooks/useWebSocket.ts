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
  debug?: boolean;
}

interface UseWebSocketReturn {
  sendMessage: (message: WebSocketMessage) => boolean;
  lastMessage: WebSocketData | null;
  readyState: number;
  connect: () => Promise<void>;
  disconnect: () => void;
  isConnected: boolean;
  isConnecting: boolean;
  error: Error | null;
  reconnectCount: number;
  hasGivenUp: boolean;
  resetConnection: () => Promise<void>;
}

// Custom error class for WebSocket errors
class WebSocketError extends Error {
  event?: Event;
  
  constructor(message: string, event?: Event) {
    super(message);
    this.name = 'WebSocketError';
    this.event = event;
  }
}

/**
 * Enhanced WebSocket hook with improved connection stability
 */
export function useWebSocket({
  url,
  onOpen,
  onClose,
  onMessage,
  onError,
  reconnectAttempts = 5,
  initialReconnectInterval = 1000,
  maxReconnectInterval = 30000,
  autoConnect = true,
  debug = false,
}: UseWebSocketProps): UseWebSocketReturn {
  const [lastMessage, setLastMessage] = useState<WebSocketData | null>(null);
  const [readyState, setReadyState] = useState<number>(WebSocket.CLOSED);
  const [error, setError] = useState<Error | null>(null);
  const [hasGivenUp, setHasGivenUp] = useState<boolean>(false);

  const socket = useRef<WebSocket | null>(null);
  const reconnectCount = useRef<number>(0);
  const reconnectDelay = useRef<number>(initialReconnectInterval);
  const reconnectTimeoutId = useRef<ReturnType<typeof setTimeout> | null>(null);
  const pingIntervalId = useRef<ReturnType<typeof setInterval> | null>(null);
  const connectionTimeoutId = useRef<ReturnType<typeof setTimeout> | null>(null);
  const connectionAttemptTimeoutId = useRef<ReturnType<typeof setTimeout> | null>(null);
  
  // For detecting problematic connections
  const lastPingTime = useRef<number>(0);
  const lastPongTime = useRef<number>(0);
  const connectionStartTime = useRef<number>(0);
  
  // Debug logger
  const log = useCallback((message: string, ...args: any[]) => {
    if (debug) {
      console.log(`[WebSocket] ${message}`, ...args);
    }
  }, [debug]);

  // Check connection state
  const isConnected = readyState === WebSocket.OPEN;
  const isConnecting = readyState === WebSocket.CONNECTING;

  // Reset connection state for retrying after giving up
  const resetConnection = useCallback(async () => {
    log('Resetting connection state');
    reconnectCount.current = 0;
    reconnectDelay.current = initialReconnectInterval;
    setHasGivenUp(false);
    setError(null);
    
    // Clear all timeouts and intervals
    if (reconnectTimeoutId.current) {
      clearTimeout(reconnectTimeoutId.current);
      reconnectTimeoutId.current = null;
    }
    
    if (connectionTimeoutId.current) {
      clearTimeout(connectionTimeoutId.current);
      connectionTimeoutId.current = null;
    }
    
    if (connectionAttemptTimeoutId.current) {
      clearTimeout(connectionAttemptTimeoutId.current);
      connectionAttemptTimeoutId.current = null;
    }
    
    await connect();
  }, [initialReconnectInterval]);

  // Cleanup function to reset all timeouts and intervals
  const cleanup = useCallback(() => {
    log('Cleaning up WebSocket resources');
    
    if (pingIntervalId.current) {
      clearInterval(pingIntervalId.current);
      pingIntervalId.current = null;
    }
    
    if (reconnectTimeoutId.current) {
      clearTimeout(reconnectTimeoutId.current);
      reconnectTimeoutId.current = null;
    }
    
    if (connectionTimeoutId.current) {
      clearTimeout(connectionTimeoutId.current);
      connectionTimeoutId.current = null;
    }
    
    if (connectionAttemptTimeoutId.current) {
      clearTimeout(connectionAttemptTimeoutId.current);
      connectionAttemptTimeoutId.current = null;
    }
    
    // Close socket if it exists
    if (socket.current) {
      try {
        // Remove all event handlers first
        socket.current.onopen = null;
        socket.current.onclose = null;
        socket.current.onmessage = null;
        socket.current.onerror = null;
        
        // Then close the socket
        socket.current.close(1000, 'Intentional disconnect');
      } catch (e) {
        log('Error during socket cleanup', e);
      }
      socket.current = null;
    }
    
    setReadyState(WebSocket.CLOSED);
  }, []);

  // Create a WebSocket connection with improved stability
  const connect = useCallback(async () => {
    // Don't try to connect if we've given up
    if (hasGivenUp) {
      log('Not connecting because we have given up');
      return;
    }

    // Clean up any existing connection first
    cleanup();
    
    try {
      log(`Connecting to WebSocket at ${url}...`);
      
      // Set as connecting before we actually create the socket
      setReadyState(WebSocket.CONNECTING);
      connectionStartTime.current = Date.now();
      
      // Set a timeout for the overall connection attempt
      connectionAttemptTimeoutId.current = setTimeout(() => {
        if (socket.current && socket.current.readyState !== WebSocket.OPEN) {
          log('Connection attempt timed out');
          
          // Force close the socket
          try {
            socket.current.close(1006, 'Connection attempt timed out');
          } catch (e) {
            log('Error closing timed out socket', e);
          }
          
          // This will trigger the onclose handler which handles reconnection
        }
      }, 10000); // 10 second timeout for connection attempt
      
      // Force a delay before creating the WebSocket to avoid race conditions
      await new Promise(resolve => setTimeout(resolve, 100));
      
      // Create with explicit protocol for browser compatibility
      socket.current = new WebSocket(url, ['json']);
      
      // Set binary type for better compatibility
      socket.current.binaryType = 'arraybuffer';
      
      // Connection open handler
      socket.current.onopen = () => {
        log('WebSocket connection established');
        
        // Clear connection attempt timeout
        if (connectionAttemptTimeoutId.current) {
          clearTimeout(connectionAttemptTimeoutId.current);
          connectionAttemptTimeoutId.current = null;
        }
        
        setReadyState(WebSocket.OPEN);
        reconnectCount.current = 0;
        reconnectDelay.current = initialReconnectInterval;
        setHasGivenUp(false);
        setError(null);
        
        // Set a timeout to verify we're getting messages back
        connectionTimeoutId.current = setTimeout(() => {
          if (socket.current?.readyState === WebSocket.OPEN) {
            // Check if we've received any pong since opening
            if (lastPongTime.current < connectionStartTime.current) {
              log('Connection established but no responses received');
              
              // Force reconnection
              try {
                socket.current.close(1000, 'No responses received after connection');
              } catch (e) {
                log('Error closing unresponsive socket', e);
              }
            }
          }
        }, 5000); // 5 second timeout to verify we're getting responses
        
        // Setup ping interval to keep the connection alive
        lastPingTime.current = Date.now();
        pingIntervalId.current = setInterval(() => {
          if (socket.current?.readyState === WebSocket.OPEN) {
            try {
              socket.current.send(JSON.stringify({
                type: 'ping',
                timestamp: Date.now()
              }));
              lastPingTime.current = Date.now();
              log('Ping sent');
              
              // Check if we've received a pong within a reasonable timeframe
              if (lastPongTime.current > 0 && 
                  Date.now() - lastPongTime.current > 45000) { // No pong for 45 seconds
                log('No pong received for too long, forcing reconnect');
                
                // Force close and reconnect
                socket.current.close(1000, 'Connection is stale');
              }
            } catch (e) {
              log('Error sending ping', e);
            }
          }
        }, 15000); // Send ping every 15 seconds
        
        // Send a ping immediately to test the connection
        try {
          socket.current.send(JSON.stringify({
            type: 'ping',
            timestamp: Date.now()
          }));
          lastPingTime.current = Date.now();
          log('Initial ping sent');
        } catch (e) {
          log('Error sending initial ping', e);
        }
        
        if (onOpen) onOpen();
      };
      
      // Message handler
      socket.current.onmessage = (event) => {
        try {
          log('Received message');
          
          const data = JSON.parse(event.data) as WebSocketData;
          setLastMessage(data);
          
          // Update last pong time if this is a pong message
          if (data.type === 'pong') {
            lastPongTime.current = Date.now();
            log('Pong received');
          }
          
          if (onMessage) onMessage(data);
        } catch (e) {
          log('Error parsing WebSocket message', e);
          setError(new Error(`Failed to parse message: ${e}`));
        }
      };
      
      // Close handler
      socket.current.onclose = (event) => {
        log(`WebSocket connection closed: ${event.code} ${event.reason}`);
        
        // Clean up resources
        cleanup();
        
        // Update state
        setReadyState(WebSocket.CLOSED);
        
        // Attempt to reconnect if not intentionally closed
        if (!event.wasClean && reconnectCount.current < reconnectAttempts) {
          reconnectCount.current += 1;
          
          // Exponential backoff with jitter for more reliable reconnection
          const jitter = Math.random() * 0.3 + 0.85; // Random between 0.85 and 1.15
          reconnectDelay.current = Math.min(
            reconnectDelay.current * 1.5 * jitter,
            maxReconnectInterval
          );
          
          log(`Reconnecting in ${reconnectDelay.current}ms (attempt ${reconnectCount.current}/${reconnectAttempts})`);
          
          // Set a timeout for reconnection
          reconnectTimeoutId.current = setTimeout(() => {
            connect();
          }, reconnectDelay.current);
        } else if (!event.wasClean && reconnectCount.current >= reconnectAttempts) {
          // We've reached the maximum number of reconnection attempts
          log(`Maximum WebSocket reconnection attempts (${reconnectAttempts}) reached`);
          setHasGivenUp(true);
          setError(new WebSocketError('Maximum reconnection attempts reached'));
        }
        
        if (onClose) onClose();
      };
      
      // Error handler
      socket.current.onerror = (event) => {
        log('WebSocket error', event);
        setError(new WebSocketError('WebSocket connection error', event));
        
        if (onError) onError(event);
        
        // Note: we don't need to close the socket here as the onclose handler will be called automatically
      };
    } catch (err) {
      log('Error during WebSocket setup', err);
      setError(err instanceof Error ? err : new Error('Failed to create WebSocket connection'));
      setReadyState(WebSocket.CLOSED);
      
      // Try to reconnect
      if (reconnectCount.current < reconnectAttempts) {
        reconnectCount.current += 1;
        reconnectTimeoutId.current = setTimeout(() => {
          connect();
        }, reconnectDelay.current);
      } else {
        setHasGivenUp(true);
      }
    }
  }, [url, onOpen, onClose, onMessage, onError, reconnectAttempts, initialReconnectInterval, maxReconnectInterval, hasGivenUp, cleanup]);

  // Close the WebSocket connection
  const disconnect = useCallback(() => {
    log('Disconnecting WebSocket');
    cleanup();
  }, [cleanup]);

  // Send a message through the WebSocket with improved reliability
  const sendMessage = useCallback((message: WebSocketMessage): boolean => {
    if (socket.current && socket.current.readyState === WebSocket.OPEN) {
      try {
        const messageStr = JSON.stringify(message);
        log(`Sending message: ${messageStr}`);
        socket.current.send(messageStr);
        return true;
      } catch (e) {
        log('Error sending message', e);
        setError(e instanceof Error ? e : new Error('Failed to send message'));
        return false;
      }
    } else {
      log('WebSocket is not connected');
      
      // Try to reconnect if not open and not already in the process of connecting
      if (!isConnecting && socket.current?.readyState !== WebSocket.CONNECTING && !hasGivenUp) {
        log('Attempting to reconnect before sending message...');
        // Use void to ignore the Promise since this is a sync function
        void connect();
      }
      
      return false;
    }
  }, [connect, isConnecting, hasGivenUp]);

  // Force reconnection when server is restarted or if connection is lost
  useEffect(() => {
    if (hasGivenUp) {
      log('Connection has given up, scheduling retry in 5 seconds');
      
      const timer = setTimeout(() => {
        log('Attempting to reconnect automatically after giving up...');
        resetConnection();
      }, 5000); // Try to reconnect every 5 seconds after giving up
      
      return () => clearTimeout(timer);
    }
  }, [hasGivenUp, resetConnection]);

  // Connect on mount if autoConnect is true
  useEffect(() => {
    if (autoConnect) {
      // Small delay before initial connection to ensure component is fully mounted
      const timer = setTimeout(() => {
        connect();
      }, 50);
      
      return () => {
        clearTimeout(timer);
        cleanup();
      };
    }
    
    // Clean up on unmount
    return () => {
      cleanup();
    };
  }, [connect, cleanup, autoConnect]);

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
