#!/bin/bash

# Run the WebSocket server using the Python virtual environment
# This script is used by the npm server command

# Get the directory of this script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
VENV_DIR="$DIR/.venv"

# Activate virtual environment
source "$VENV_DIR/bin/activate"

# Run the server
python3 "$DIR/server/server.py"
