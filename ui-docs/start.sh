#!/bin/bash

# Start script for Universal Intelligence UI and WebSocket Server
# This script is a simple wrapper around the npm start command

# Color constants
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Starting Universal Intelligence Development Environment${NC}"
echo -e "${YELLOW}This script will start both the UI and WebSocket server${NC}"
echo -e "${YELLOW}Press Ctrl+C to stop both servers${NC}"
echo

# Check if node and npm are installed
if ! command -v npm &> /dev/null; then
    echo -e "${RED}Error: npm is not installed or not found in PATH${NC}"
    exit 1
fi

# Check if Python is installed
if ! command -v python &> /dev/null && ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python is not installed or not found in PATH${NC}"
    exit 1
fi

# Check for required Python packages
PYTHON="python3"
if ! command -v python3 &> /dev/null; then
    # Fall back to python only if it's version 3.x
    if command -v python &> /dev/null; then
        PYTHON_VERSION=$(python --version 2>&1 | awk '{print $2}' | cut -d'.' -f1)
        if [ "$PYTHON_VERSION" = "3" ]; then
            PYTHON="python"
        else
            echo -e "${RED}Error: Python 3 is required but not found${NC}"
            exit 1
        fi
    else
        echo -e "${RED}Error: Python 3 is required but not found${NC}"
        exit 1
    fi
fi

# Check for websockets package and install if not found
if ! $PYTHON -c "import websockets" &> /dev/null; then
    echo -e "${YELLOW}Python websockets package not found. Installing...${NC}"
    $PYTHON -m pip install websockets
    if [ $? -ne 0 ]; then
        echo -e "${RED}Failed to install websockets package. Trying with pip3...${NC}"
        pip3 install websockets
        if [ $? -ne 0 ]; then
            echo -e "${RED}Failed to install websockets package. Please install it manually:${NC}"
            echo -e "${YELLOW}pip install websockets${NC}"
            exit 1
        fi
    fi
    echo -e "${GREEN}Successfully installed websockets package${NC}"
fi

# Start both servers
echo -e "${GREEN}Starting UI and WebSocket servers...${NC}"
cd "$(dirname "$0")"
npm run start

# This point is reached when servers are stopped
echo
echo -e "${GREEN}Servers stopped${NC}"
