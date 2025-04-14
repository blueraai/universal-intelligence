#!/bin/bash

# WebSocket Connectivity Fix Installation Script
# Created by Claude to fix WebSocket connectivity issues

# Color codes for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Directories
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SERVER_DIR="$ROOT_DIR/server"
SRC_DIR="$ROOT_DIR/src"

# Check if we're in the right directory
if [ ! -d "$SERVER_DIR" ] || [ ! -d "$SRC_DIR" ]; then
    echo -e "${RED}Error: Script must be run from the ui-docs directory${NC}"
    exit 1
fi

echo -e "${BLUE}===== Universal Intelligence WebSocket Connectivity Fix =====${NC}"
echo -e "${YELLOW}This script will install the improved WebSocket implementation.${NC}"
echo -e "${YELLOW}Original files will be backed up before any changes.${NC}"
echo

# Verify the improved files exist
if [ ! -f "$SERVER_DIR/server_improved.py" ]; then
    echo -e "${RED}Error: Improved server file not found at $SERVER_DIR/server_improved.py${NC}"
    exit 1
fi

if [ ! -f "$SRC_DIR/hooks/useWebSocket.ts.improved" ]; then
    echo -e "${RED}Error: Improved WebSocket hook not found at $SRC_DIR/hooks/useWebSocket.ts.improved${NC}"
    exit 1
fi

# Backup and install improved server
echo -e "${BLUE}1. Installing improved WebSocket server...${NC}"
if [ -f "$SERVER_DIR/server.py" ]; then
    if [ ! -f "$SERVER_DIR/server.py.bak" ]; then
        echo -e "   ${YELLOW}Backing up original server...${NC}"
        cp "$SERVER_DIR/server.py" "$SERVER_DIR/server.py.bak"
    fi
    echo -e "   ${GREEN}Installing improved server...${NC}"
    cp "$SERVER_DIR/server_improved.py" "$SERVER_DIR/server.py"
    echo -e "   ${GREEN}Server update complete.${NC}"
else
    echo -e "   ${RED}Error: Original server not found at $SERVER_DIR/server.py${NC}"
    exit 1
fi

# Backup and install improved WebSocket hook
echo -e "${BLUE}2. Installing improved WebSocket hook...${NC}"
if [ -f "$SRC_DIR/hooks/useWebSocket.ts" ]; then
    if [ ! -f "$SRC_DIR/hooks/useWebSocket.ts.bak" ]; then
        echo -e "   ${YELLOW}Backing up original hook...${NC}"
        cp "$SRC_DIR/hooks/useWebSocket.ts" "$SRC_DIR/hooks/useWebSocket.ts.bak"
    fi
    echo -e "   ${GREEN}Installing improved hook...${NC}"
    cp "$SRC_DIR/hooks/useWebSocket.ts.improved" "$SRC_DIR/hooks/useWebSocket.ts"
    echo -e "   ${GREEN}Hook update complete.${NC}"
else
    echo -e "   ${RED}Error: Original hook not found at $SRC_DIR/hooks/useWebSocket.ts${NC}"
    exit 1
fi

# Install test utilities
echo -e "${BLUE}3. Installing WebSocket test utilities...${NC}"
if [ ! -d "$ROOT_DIR/tests" ]; then
    echo -e "   ${YELLOW}Creating tests directory...${NC}"
    mkdir -p "$ROOT_DIR/tests"
fi

echo -e "   ${GREEN}Installation complete!${NC}"
echo
echo -e "${BLUE}===== Next Steps =====${NC}"
echo -e "1. Start the WebSocket server:${NC}"
echo -e "   ${GREEN}cd $ROOT_DIR${NC}"
echo -e "   ${GREEN}python server/server.py${NC}"
echo
echo -e "2. Start the frontend development server:${NC}"
echo -e "   ${GREEN}cd $ROOT_DIR${NC}"
echo -e "   ${GREEN}npm run dev${NC}"
echo
echo -e "3. Test the WebSocket connectivity:${NC}"
echo -e "   ${GREEN}Open http://localhost:5173/tests/browser-test.html in your browser${NC}"
echo
echo -e "4. For more testing options:${NC}"
echo -e "   ${GREEN}./test-websocket-fix.sh${NC}"
echo
echo -e "${YELLOW}If you need to revert to the original implementation:${NC}"
echo -e "   ${GREEN}cp $SERVER_DIR/server.py.bak $SERVER_DIR/server.py${NC}"
echo -e "   ${GREEN}cp $SRC_DIR/hooks/useWebSocket.ts.bak $SRC_DIR/hooks/useWebSocket.ts${NC}"
echo

echo -e "${BLUE}Would you like to run the test script now? (y/n)${NC}"
read -r run_test
if [[ $run_test == "y" || $run_test == "Y" ]]; then
    chmod +x "$ROOT_DIR/test-websocket-fix.sh"
    "$ROOT_DIR/test-websocket-fix.sh"
fi
