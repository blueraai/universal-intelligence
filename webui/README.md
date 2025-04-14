# Universal Intelligence Web UI

A web-based development UI for the Universal Intelligence framework, inspired by Google's ADK Web UI.

## Setup and Usage

1. Install dependencies:
   ```bash
   pip install fastapi uvicorn
   ```

2. Run the web server:
   ```bash
   cd /path/to/universal-intelligence
   python -m webui.server.web_server
   ```

3. Open your browser at http://127.0.0.1:8000

## Directory Structure

```
webui/
├── __init__.py
├── agents/                # Agent definitions
│   └── test_agent/        # Sample agent
│       ├── __init__.py
│       └── agent.py
├── browser/               # Web UI frontend
│   ├── favicon.svg
│   └── index.html
└── server/                # FastAPI server
    ├── api.py
    └── web_server.py
```

## Features

- Agent selection
- Chat interface
- Debug panel with session info and event details
- Streaming responses via SSE

## Customizing

To create a new agent:

1. Create a new directory in `webui/agents/`
2. Create `__init__.py` and `agent.py` files
3. Define your agent in `agent.py` using the Universal Intelligence framework
4. Export it as `root_agent`

## License

Apache License 2.0
