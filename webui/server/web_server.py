#!/usr/bin/env python3

import os
import sys
import argparse
import uvicorn
from pathlib import Path

# Add webui directory to path
current_dir = Path(__file__).parent
webui_dir = current_dir.parent
# Add parent of webui directory to path (for universal_intelligence imports)
sys.path.append(str(webui_dir.parent))
# Add webui directory to path (for our agent modules)
sys.path.append(str(webui_dir))

from webui.server.api import get_fast_api_app


def main():
    """Run the development web UI server."""
    parser = argparse.ArgumentParser(description="Universal Intelligence Dev Web UI")
    parser.add_argument(
        "--host", type=str, default="127.0.0.1", help="Host to run the server on"
    )
    parser.add_argument(
        "--port", type=int, default=8000, help="Port to run the server on"
    )
    parser.add_argument(
        "--agent-dir", 
        type=str, 
        default=str(webui_dir / "agents"),
        help="Directory containing agent definitions"
    )
    
    args = parser.parse_args()
    
    # Create the agent directory if it doesn't exist
    os.makedirs(args.agent_dir, exist_ok=True)
    
    # Create and configure the FastAPI app
    app = get_fast_api_app(
        agent_dir=args.agent_dir,
        allow_origins=["*"],  # For development - restrict in production
        web=True,
    )
    
    # Start the server
    print(f"Starting web UI server at http://{args.host}:{args.port}")
    print(f"Agent directory: {args.agent_dir}")
    uvicorn.run(app, host=args.host, port=args.port)


if __name__ == "__main__":
    main()
