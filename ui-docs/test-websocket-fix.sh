#!/bin/bash

# Test WebSocket Connectivity Fix
# This script tests the improved WebSocket implementation
# Created by Claude to fix WebSocket connectivity issues

# Color codes for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Constants
SERVER_PORT=9765
SERVER_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/server"
TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/tests"
IMPROVED_SERVER="server_improved.py"
ORIGINAL_SERVER="server.py"

# Function to check if a port is in use
is_port_in_use() {
    if command -v lsof >/dev/null 2>&1; then
        lsof -i:"$1" >/dev/null 2>&1
        return $?
    else
        # Fallback to netstat if lsof is not available
        netstat -tuln | grep ":$1 " >/dev/null 2>&1
        return $?
    fi
}

# Function to kill processes using a specific port
kill_port_process() {
    if command -v lsof >/dev/null 2>&1; then
        local pid=$(lsof -t -i:"$1" 2>/dev/null)
        if [ -n "$pid" ]; then
            echo -e "${YELLOW}Killing process $pid using port $1${NC}"
            kill -9 "$pid" 2>/dev/null
        fi
    else
        echo -e "${YELLOW}lsof not found, please manually kill any process using port $1${NC}"
    fi
}

# Check Python environment
check_python() {
    if ! command -v python3 >/dev/null 2>&1; then
        echo -e "${RED}Error: Python 3 is required but not found.${NC}"
        exit 1
    fi
    
    # Check for websockets package
    if ! python3 -c "import websockets" >/dev/null 2>&1; then
        echo -e "${YELLOW}Installing websockets package...${NC}"
        python3 -m pip install websockets
        if [ $? -ne 0 ]; then
            echo -e "${RED}Error: Failed to install websockets package.${NC}"
            exit 1
        fi
    fi
}

# Run the original server for comparison
run_original_server() {
    echo -e "${BLUE}===== Testing Original WebSocket Server =====${NC}"
    
    # Kill any existing processes on the port
    if is_port_in_use "$SERVER_PORT"; then
        kill_port_process "$SERVER_PORT"
        sleep 2
    fi
    
    # Start the original server
    echo -e "${GREEN}Starting original WebSocket server...${NC}"
    python3 "$SERVER_DIR/$ORIGINAL_SERVER" &
    SERVER_PID=$!
    
    # Wait for server to start
    sleep 3
    
    if ! is_port_in_use "$SERVER_PORT"; then
        echo -e "${RED}Error: Original server failed to start.${NC}"
        kill -9 $SERVER_PID 2>/dev/null
        return 1
    fi
    
    # Run test against the original server
    echo -e "${GREEN}Running diagnostic test against original server...${NC}"
    python3 "$TEST_DIR/websocket-test.py" --duration 20
    
    # Kill the server
    echo -e "${GREEN}Stopping original server...${NC}"
    kill -9 $SERVER_PID 2>/dev/null
    sleep 2
}

# Run the improved server
run_improved_server() {
    echo -e "\n${BLUE}===== Testing Improved WebSocket Server =====${NC}"
    
    # Kill any existing processes on the port
    if is_port_in_use "$SERVER_PORT"; then
        kill_port_process "$SERVER_PORT"
        sleep 2
    fi
    
    # Start the improved server
    echo -e "${GREEN}Starting improved WebSocket server...${NC}"
    python3 "$SERVER_DIR/$IMPROVED_SERVER" &
    SERVER_PID=$!
    
    # Wait for server to start
    sleep 3
    
    if ! is_port_in_use "$SERVER_PORT"; then
        echo -e "${RED}Error: Improved server failed to start.${NC}"
        kill -9 $SERVER_PID 2>/dev/null
        return 1
    fi
    
    # Run test against the improved server
    echo -e "${GREEN}Running diagnostic test against improved server...${NC}"
    python3 "$TEST_DIR/websocket-test.py" --duration 30 --verbose
    
    # Ask to keep server running
    echo -e "\n${YELLOW}Do you want to keep the improved server running? (y/n)${NC}"
    read -r keep_running
    
    if [[ $keep_running != "y" && $keep_running != "Y" ]]; then
        echo -e "${GREEN}Stopping improved server...${NC}"
        kill -9 $SERVER_PID 2>/dev/null
        sleep 2
    else
        echo -e "${GREEN}Server still running on port $SERVER_PORT. Press Ctrl+C later to stop it.${NC}"
        wait $SERVER_PID
    fi
}

# Install improved WebSocket hook
install_improved_hook() {
    echo -e "\n${BLUE}===== Installing Improved WebSocket Hook =====${NC}"
    
    # Backup current hook
    if [ -f "src/hooks/useWebSocket.ts" ]; then
        if [ ! -f "src/hooks/useWebSocket.ts.bak" ]; then
            echo -e "${GREEN}Backing up original WebSocket hook...${NC}"
            cp "src/hooks/useWebSocket.ts" "src/hooks/useWebSocket.ts.bak"
        fi
        
        # Install improved hook
        echo -e "${GREEN}Installing improved WebSocket hook...${NC}"
        cp "src/hooks/useWebSocket.ts.improved" "src/hooks/useWebSocket.ts"
        echo -e "${GREEN}WebSocket hook updated successfully.${NC}"
    else
        echo -e "${RED}Error: Cannot find the original WebSocket hook at src/hooks/useWebSocket.ts${NC}"
        return 1
    fi
}

# Replace server
install_improved_server() {
    echo -e "\n${BLUE}===== Installing Improved WebSocket Server =====${NC}"
    
    # Backup current server
    if [ -f "$SERVER_DIR/$ORIGINAL_SERVER" ]; then
        if [ ! -f "$SERVER_DIR/${ORIGINAL_SERVER}.bak" ]; then
            echo -e "${GREEN}Backing up original WebSocket server...${NC}"
            cp "$SERVER_DIR/$ORIGINAL_SERVER" "$SERVER_DIR/${ORIGINAL_SERVER}.bak"
        fi
        
        # Install improved server
        echo -e "${GREEN}Installing improved WebSocket server...${NC}"
        cp "$SERVER_DIR/$IMPROVED_SERVER" "$SERVER_DIR/$ORIGINAL_SERVER"
        echo -e "${GREEN}WebSocket server updated successfully.${NC}"
    else
        echo -e "${RED}Error: Cannot find the original WebSocket server at $SERVER_DIR/$ORIGINAL_SERVER${NC}"
        return 1
    fi
}

# Restore backups if needed
restore_backups() {
    echo -e "\n${BLUE}===== Restoring Original Files =====${NC}"
    
    # Restore WebSocket hook
    if [ -f "src/hooks/useWebSocket.ts.bak" ]; then
        echo -e "${GREEN}Restoring original WebSocket hook...${NC}"
        cp "src/hooks/useWebSocket.ts.bak" "src/hooks/useWebSocket.ts"
    fi
    
    # Restore WebSocket server
    if [ -f "$SERVER_DIR/${ORIGINAL_SERVER}.bak" ]; then
        echo -e "${GREEN}Restoring original WebSocket server...${NC}"
        cp "$SERVER_DIR/${ORIGINAL_SERVER}.bak" "$SERVER_DIR/$ORIGINAL_SERVER"
    fi
    
    echo -e "${GREEN}Original files restored.${NC}"
}

# Show menu
show_menu() {
    echo -e "\n${BLUE}===== WebSocket Connectivity Fix Test Menu =====${NC}"
    echo -e "1) ${GREEN}Test original server${NC}"
    echo -e "2) ${GREEN}Test improved server${NC}"
    echo -e "3) ${GREEN}Install improved WebSocket hook${NC}"
    echo -e "4) ${GREEN}Install improved WebSocket server${NC}"
    echo -e "5) ${GREEN}Restore original backups${NC}"
    echo -e "6) ${GREEN}Run frontend development server${NC}"
    echo -e "7) ${GREEN}Open browser test page${NC}"
    echo -e "8) ${GREEN}Run full integration test${NC}"
    echo -e "0) ${RED}Exit${NC}"
    echo -e "\nEnter your choice: "
    read -r choice
    
    case $choice in
        1) run_original_server ;;
        2) run_improved_server ;;
        3) install_improved_hook ;;
        4) install_improved_server ;;
        5) restore_backups ;;
        6) start_frontend ;;
        7) open_browser_test ;;
        8) run_full_test ;;
        0) echo -e "${GREEN}Exiting...${NC}"; exit 0 ;;
        *) echo -e "${RED}Invalid choice. Please try again.${NC}" ;;
    esac
    
    # Return to menu
    show_menu
}

# Start frontend server for testing
start_frontend() {
    echo -e "\n${BLUE}===== Starting Frontend Server =====${NC}"
    
    # Kill any existing processes on the port 5173 (default Vite port)
    if command -v lsof >/dev/null 2>&1; then
        local pid=$(lsof -t -i:5173 2>/dev/null)
        if [ -n "$pid" ]; then
            echo -e "${YELLOW}Killing process $pid using port 5173${NC}"
            kill -9 "$pid" 2>/dev/null
        fi
    fi
    
    # Start the frontend in development mode
    echo -e "${GREEN}Starting frontend development server...${NC}"
    
    # Check if npm is installed
    if ! command -v npm >/dev/null 2>&1; then
        echo -e "${RED}Error: npm is required but not found.${NC}"
        return 1
    fi
    
    # Run npm dev in the background
    npm run dev &
    FRONTEND_PID=$!
    
    # Wait for server to start
    echo -e "${GREEN}Waiting for frontend server to start...${NC}"
    sleep 5
    
    # Check if the process is still running
    if ! kill -0 $FRONTEND_PID 2>/dev/null; then
        echo -e "${RED}Error: Frontend server failed to start.${NC}"
        return 1
    fi
    
    echo -e "${GREEN}Frontend server started successfully at http://localhost:5173${NC}"
    echo -e "${GREEN}Open browser test at: http://localhost:5173/tests/browser-test.html${NC}"
    
    # Ask to keep server running
    echo -e "\n${YELLOW}Press Enter to stop the frontend server when done testing or Ctrl+C to exit...${NC}"
    read -r
    
    # Kill the frontend server
    if kill -0 $FRONTEND_PID 2>/dev/null; then
        echo -e "${GREEN}Stopping frontend server...${NC}"
        kill -9 $FRONTEND_PID 2>/dev/null
    fi
}

# Open browser test page
open_browser_test() {
    echo -e "\n${BLUE}===== Opening Browser Test =====${NC}"
    
    # Check if we can open a browser
    if command -v open >/dev/null 2>&1; then
        echo -e "${GREEN}Opening browser test page...${NC}"
        open "http://localhost:5173/tests/browser-test.html"
    elif command -v xdg-open >/dev/null 2>&1; then
        echo -e "${GREEN}Opening browser test page...${NC}"
        xdg-open "http://localhost:5173/tests/browser-test.html"
    else
        echo -e "${YELLOW}Please open this URL in your browser: http://localhost:5173/tests/browser-test.html${NC}"
    fi
}

# Run full integration test
run_full_test() {
    echo -e "\n${BLUE}===== Running Full Integration Test =====${NC}"
    
    # Make sure we have the improved server and hook installed
    install_improved_server
    install_improved_hook
    
    # Start the WebSocket server
    echo -e "${GREEN}Starting WebSocket server...${NC}"
    python3 "$SERVER_DIR/$ORIGINAL_SERVER" &
    SERVER_PID=$!
    
    # Wait for server to start
    sleep 2
    
    if ! is_port_in_use "$SERVER_PORT"; then
        echo -e "${RED}Error: WebSocket server failed to start.${NC}"
        return 1
    fi
    
    # Start the frontend
    start_frontend
    
    # Kill the WebSocket server
    if kill -0 $SERVER_PID 2>/dev/null; then
        echo -e "${GREEN}Stopping WebSocket server...${NC}"
        kill -9 $SERVER_PID 2>/dev/null
    fi
}

# Main function
main() {
    echo -e "${BLUE}WebSocket Connectivity Fix Test Script${NC}"
    echo -e "${YELLOW}This script will help test the improved WebSocket implementation${NC}"
    
    # Navigate to the project root directory
    cd "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)" || exit 1
    
    # Check Python environment
    check_python
    
    # Show menu
    show_menu
}

# Run main function
main
