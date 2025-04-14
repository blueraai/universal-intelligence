# Universal Intelligence Development Environment

This document explains how to start both the UI frontend and WebSocket server together.

## Combined Start Command

We've added a single command to start both the UI frontend and WebSocket backend together using `concurrently`. This provides:

- Both servers running in parallel
- Combined log output in a single terminal
- Prefixed logs with "ui" and "be" to distinguish the source
- Automatic shutdown of both servers when one terminates

## Prerequisites

The system uses a Python virtual environment (`.venv`) to manage Python dependencies. The start script will:

1. Create this virtual environment if it doesn't exist
2. Install all required Python packages into the virtual environment
3. Run the server within that environment

## Usage

```bash
cd ui-docs
npm run start
```

This single command will:
1. Set up the Python virtual environment and install dependencies
2. Start the frontend development server on port 5173
3. Start the WebSocket server on port 9765
4. Display all logs in a single terminal with "ui" and "be" prefixes

## What Happens

When you run the start command:

1. The frontend development server starts on port 5173
2. The WebSocket server starts on port 9765
3. All logs are displayed in the same terminal window with clear prefixes
4. Press Ctrl+C to stop both servers

## Testing the WebSocket Connection

Once both servers are running, you can test the WebSocket connectivity using:

1. Browser Test: http://localhost:5173/websocket-test.html
2. Python Test: `python tests/websocket_diagnostic.py`

## Troubleshooting

If you encounter any issues:

1. Check that port 5173 is available for the frontend server
2. Check that port 9765 is available for the WebSocket server
3. Make sure the Python virtual environment is set up correctly:
   ```bash
   rm -rf .venv  # Remove problematic virtual environment
   npm run install-py-deps  # Create a fresh one
   ```

## Individual Components

If you prefer to start the servers separately:

```bash
# Install Python dependencies
npm run install-py-deps

# Start the frontend (Terminal 1)
npm run dev

# Start the WebSocket server (Terminal 2)
npm run server
```
