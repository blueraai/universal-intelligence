#!/usr/bin/env python

import asyncio
import websockets
import json
import logging
import sys
import argparse
import time
from typing import Dict, Any, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger('websocket-diagnostics')

# Connection statistics
stats = {
    "connection_attempts": 0,
    "successful_connections": 0,
    "failed_connections": 0,
    "disconnections": 0,
    "messages_sent": 0,
    "messages_received": 0,
    "errors": 0,
    "last_ping_time": 0,
    "last_pong_time": 0,
    "avg_round_trip_ms": 0,
    "round_trip_samples": []
}

# Parse command line arguments
parser = argparse.ArgumentParser(description="WebSocket Connection Diagnostic Tool")
parser.add_argument("--url", default="ws://localhost:9765", help="WebSocket server URL")
parser.add_argument("--protocol", default="json", help="WebSocket subprotocol")
parser.add_argument("--duration", type=int, default=30, help="Test duration in seconds")
parser.add_argument("--ping-interval", type=int, default=5, help="Ping interval in seconds")
parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose logging")
args = parser.parse_args()

# Set log level based on verbosity
if args.verbose:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)

# Maximum number of round-trip time samples to keep
MAX_RTT_SAMPLES = 50

# Start time for calculating test duration
start_time = time.time()

async def send_ping(websocket) -> None:
    """Send a ping message and record the time"""
    try:
        timestamp = int(time.time() * 1000)
        ping_message = json.dumps({
            "type": "ping",
            "timestamp": timestamp
        })
        await websocket.send(ping_message)
        stats["last_ping_time"] = timestamp
        stats["messages_sent"] += 1
        logger.debug(f"Sent ping at {timestamp}")
    except Exception as e:
        logger.error(f"Error sending ping: {e}")
        stats["errors"] += 1

async def execute_test_code(websocket) -> None:
    """Send a simple code execution request"""
    try:
        code = "print('Hello from diagnostic client')"
        execute_message = json.dumps({
            "type": "execute",
            "code": code
        })
        await websocket.send(execute_message)
        stats["messages_sent"] += 1
        logger.info("Sent code execution request")
    except Exception as e:
        logger.error(f"Error sending code execution: {e}")
        stats["errors"] += 1

async def receive_handler(websocket) -> None:
    """Handle incoming messages"""
    try:
        while True:
            try:
                # Set a timeout to avoid blocking forever
                message = await asyncio.wait_for(websocket.recv(), timeout=1.0)
                stats["messages_received"] += 1
                
                try:
                    data = json.loads(message)
                    logger.debug(f"Received message type: {data.get('type', 'unknown')}")
                    
                    # Handle pong messages
                    if data.get("type") == "pong":
                        now = int(time.time() * 1000)
                        ping_time = data.get("timestamp", 0)
                        stats["last_pong_time"] = now
                        
                        if ping_time > 0:
                            # Calculate round-trip time
                            rtt = now - ping_time
                            stats["round_trip_samples"].append(rtt)
                            
                            # Keep only the most recent samples
                            if len(stats["round_trip_samples"]) > MAX_RTT_SAMPLES:
                                stats["round_trip_samples"] = stats["round_trip_samples"][-MAX_RTT_SAMPLES:]
                            
                            # Update average RTT
                            stats["avg_round_trip_ms"] = sum(stats["round_trip_samples"]) / len(stats["round_trip_samples"])
                            
                            logger.debug(f"Round-trip time: {rtt}ms, Avg: {stats['avg_round_trip_ms']:.2f}ms")
                            
                    # Log execution results
                    elif data.get("type") == "result":
                        status = data.get("status", "unknown")
                        logger.info(f"Received execution result: {status}")
                        
                        if status == "error" and data.get("error"):
                            logger.error(f"Execution error: {data.get('error').get('message', 'Unknown error')}")
                            
                except json.JSONDecodeError:
                    logger.warning(f"Received non-JSON message: {message}")
                    
            except asyncio.TimeoutError:
                # Just a timeout in receiving, continue the loop
                pass
                
            except websockets.exceptions.ConnectionClosed as e:
                logger.warning(f"Connection closed during receive: {e}")
                stats["disconnections"] += 1
                break
                
            except Exception as e:
                logger.error(f"Error in receive handler: {e}")
                stats["errors"] += 1
                break
                
    except Exception as e:
        logger.error(f"Fatal error in receive handler: {e}")
        stats["errors"] += 1

def print_status(final=False) -> None:
    """Print current diagnostic statistics"""
    runtime = int(time.time() - start_time)
    
    if final:
        print("\n" + "="*50)
        print("WEBSOCKET CONNECTION DIAGNOSTIC RESULTS")
        print("="*50)
    else:
        print("\n" + "-"*30)
        print(f"STATUS UPDATE (runtime: {runtime}s)")
        print("-"*30)
        
    print(f"Connection attempts:   {stats['connection_attempts']}")
    print(f"Successful connections: {stats['successful_connections']}")
    print(f"Failed connections:    {stats['failed_connections']}")
    print(f"Disconnections:        {stats['disconnections']}")
    print(f"Messages sent:         {stats['messages_sent']}")
    print(f"Messages received:     {stats['messages_received']}")
    print(f"Errors encountered:    {stats['errors']}")
    
    if stats["round_trip_samples"]:
        print(f"Average round-trip:    {stats['avg_round_trip_ms']:.2f}ms")
        
        if len(stats["round_trip_samples"]) >= 3:
            samples = sorted(stats["round_trip_samples"])
            min_rtt = samples[0]
            max_rtt = samples[-1]
            median_rtt = samples[len(samples)//2]
            print(f"Min/Median/Max RTT:    {min_rtt}/{median_rtt}/{max_rtt}ms")
    
    if final:
        success_rate = 0
        if stats["connection_attempts"] > 0:
            success_rate = (stats["successful_connections"] / stats["connection_attempts"]) * 100
            
        print(f"Connection success rate: {success_rate:.1f}%")
        
        if stats["successful_connections"] > 0:
            stability_score = 100 * (1 - (stats["disconnections"] / stats["successful_connections"]))
            print(f"Connection stability:   {stability_score:.1f}%")
            
        # Overall assessment
        if success_rate >= 90 and stats["errors"] < 3:
            print("\nOVERALL: EXCELLENT - Connection is stable and reliable")
        elif success_rate >= 75 and stats["errors"] < 10:
            print("\nOVERALL: GOOD - Connection is working with minor issues")
        elif success_rate >= 50:
            print("\nOVERALL: FAIR - Connection works but has stability issues")
        else:
            print("\nOVERALL: POOR - Connection has serious problems")
            
        print("\nDIAGNOSTIC RECOMMENDATIONS:")
        if stats["failed_connections"] > stats["successful_connections"]:
            print("- Check if the WebSocket server is running and accessible")
            print("- Verify network connectivity and firewall settings")
            
        if stats["disconnections"] > 3:
            print("- Server may be closing connections prematurely")
            print("- Check server logs for connection errors")
            
        if stats.get("avg_round_trip_ms", 0) > 500:
            print("- Network latency is high, which may impact real-time feedback")
            
        if stats["errors"] > 10:
            print("- Investigate frequent errors in the server or client implementation")

async def diagnostic_client() -> None:
    """Main diagnostic client function"""
    connection_alive = False
    
    logger.info(f"Starting WebSocket diagnostic test against {args.url}")
    logger.info(f"Using subprotocol: {args.protocol}")
    logger.info(f"Test will run for {args.duration} seconds")
    
    while time.time() - start_time < args.duration:
        if not connection_alive:
            try:
                logger.info(f"Connecting to {args.url}...")
                stats["connection_attempts"] += 1
                
                async with websockets.connect(
                    args.url,
                    subprotocols=[args.protocol],
                    max_size=10_000_000,
                    ping_interval=None,  # We'll handle our own pings
                    close_timeout=2      # Quick close timeout
                ) as websocket:
                    stats["successful_connections"] += 1
                    connection_alive = True
                    logger.info("Connection established successfully")
                    
                    # Start receive handler
                    receiver_task = asyncio.create_task(receive_handler(websocket))
                    
                    # Main client loop
                    ping_time = 0
                    code_time = 10  # First code execution after 10 seconds
                    last_status_time = 0
                    
                    loop_start_time = time.time()
                    while time.time() - start_time < args.duration and connection_alive:
                        current_time = time.time()
                        
                        # Send ping on interval
                        if current_time - ping_time >= args.ping_interval:
                            await send_ping(websocket)
                            ping_time = current_time
                            
                        # Execute test code periodically
                        if current_time - code_time >= 15:  # Every 15 seconds
                            await execute_test_code(websocket)
                            code_time = current_time
                            
                        # Print status every 10 seconds
                        if current_time - last_status_time >= 10:
                            print_status()
                            last_status_time = current_time
                            
                        # Check if receive task is still alive
                        if receiver_task.done():
                            exception = receiver_task.exception()
                            if exception:
                                logger.error(f"Receiver task failed: {exception}")
                                stats["errors"] += 1
                            connection_alive = False
                            break
                            
                        # Small sleep to avoid CPU spinning
                        await asyncio.sleep(0.1)
                        
                    # Test completed or connection lost
                    if receiver_task.done():
                        try:
                            await receiver_task
                        except Exception as e:
                            logger.error(f"Receiver task error: {e}")
                    else:
                        receiver_task.cancel()
                        try:
                            await receiver_task
                        except asyncio.CancelledError:
                            pass
                            
                    connection_alive = False
                    
            except websockets.exceptions.WebSocketException as e:
                logger.error(f"WebSocket error: {e}")
                stats["failed_connections"] += 1
                stats["errors"] += 1
                connection_alive = False
                
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                stats["failed_connections"] += 1
                stats["errors"] += 1
                connection_alive = False
                
            # If connection failed, wait before retrying
            if not connection_alive:
                retry_delay = min(5 * stats["failed_connections"], 30)
                logger.info(f"Will retry connection in {retry_delay} seconds...")
                await asyncio.sleep(retry_delay)
    
    # Test complete
    logger.info("Diagnostic test completed")
    print_status(final=True)

if __name__ == "__main__":
    try:
        asyncio.run(diagnostic_client())
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
        print_status(final=True)
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        print_status(final=True)
