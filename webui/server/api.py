
# Copyright 2025 Bluera
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import asyncio
import datetime
import importlib
import json
import logging
import os
from pathlib import Path
import sys
import traceback
import uuid
from typing import Any, Dict, List, Optional, Literal

import click
from fastapi import FastAPI, HTTPException, Query, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, RedirectResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

# Import from universal_intelligence with proper pattern
from universal_intelligence import Agent, Model, Tool

logger = logging.getLogger(__name__)

# Define request/response models
class AgentRunRequest(BaseModel):
    app_name: str
    user_id: str
    session_id: str
    new_message: Dict[str, Any]  # Adapt to your message format
    streaming: bool = False


class Session(BaseModel):
    id: str
    user_id: str
    app_name: str
    state: Dict[str, Any] = {}
    events: List[Dict[str, Any]] = []
    
    def get_contents(self):
        # Adapt this to your event structure
        return [event.get("content", {}) for event in self.events if "content" in event]


# In-memory storage for sessions and agents
sessions_store: Dict[str, Session] = {}
agent_cache: Dict[str, Agent] = {}


def get_timestamp():
    """Get current timestamp in ISO format."""
    return datetime.datetime.now().isoformat()


class Event(BaseModel):
    id: str = Field(default_factory=lambda: f"event_{uuid.uuid4()}")
    author: str
    content: Dict[str, Any] = None
    timestamp: str = Field(default_factory=get_timestamp)
    
    class Config:
        arbitrary_types_allowed = True


class MessageQueue:
    """Simple message queue for async communication."""
    
    def __init__(self):
        self.queue = asyncio.Queue()
        
    async def put(self, message):
        await self.queue.put(message)
        
    async def get(self):
        return await self.queue.get()


def get_fast_api_app(
    *,
    agent_dir: str,
    allow_origins: Optional[List[str]] = None,
    web: bool = True,
) -> FastAPI:
    """Create and configure the FastAPI application.
    
    Args:
        agent_dir: Directory containing agent definitions
        allow_origins: CORS origins to allow
        web: Whether to serve the web UI
        
    Returns:
        Configured FastAPI application
    """
    app = FastAPI()

    if allow_origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=allow_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    if agent_dir not in sys.path:
        sys.path.append(agent_dir)

    @app.get("/list-apps")
    def list_apps() -> List[str]:
        """List available agent applications."""
        base_path = Path(agent_dir)
        if not base_path.exists():
            raise HTTPException(status_code=404, detail="Path not found")
        if not base_path.is_dir():
            raise HTTPException(status_code=400, detail="Not a directory")
        
        agent_names = [
            x
            for x in os.listdir(base_path)
            if os.path.isdir(os.path.join(base_path, x))
            and not x.startswith(".")
            and x != "__pycache__"
        ]
        agent_names.sort()
        return agent_names

    @app.get(
        "/apps/{app_name}/users/{user_id}/sessions/{session_id}",
        response_model_exclude_none=True,
    )
    def get_session(app_name: str, user_id: str, session_id: str) -> Session:
        """Get a specific session."""
        session_key = f"{app_name}_{user_id}_{session_id}"
        if session_key not in sessions_store:
            raise HTTPException(status_code=404, detail="Session not found")
        return sessions_store[session_key]

    @app.get(
        "/apps/{app_name}/users/{user_id}/sessions",
        response_model_exclude_none=True,
    )
    def list_sessions(app_name: str, user_id: str) -> List[Session]:
        """List all sessions for a user."""
        return [
            session
            for key, session in sessions_store.items()
            if key.startswith(f"{app_name}_{user_id}_")
        ]

    @app.post(
        "/apps/{app_name}/users/{user_id}/sessions/{session_id}",
        response_model_exclude_none=True,
    )
    def create_session_with_id(
        app_name: str,
        user_id: str,
        session_id: str,
        state: Optional[Dict[str, Any]] = None,
    ) -> Session:
        """Create a new session with a specific ID."""
        session_key = f"{app_name}_{user_id}_{session_id}"
        if session_key in sessions_store:
            logger.warning("Session already exists: %s", session_id)
            raise HTTPException(
                status_code=400, detail=f"Session already exists: {session_id}"
            )

        new_session = Session(
            id=session_id,
            user_id=user_id,
            app_name=app_name,
            state=state or {},
        )
        sessions_store[session_key] = new_session
        logger.info("New session created: %s", session_id)
        return new_session

    @app.post(
        "/apps/{app_name}/users/{user_id}/sessions",
        response_model_exclude_none=True,
    )
    def create_session(
        app_name: str,
        user_id: str,
        state: Optional[Dict[str, Any]] = None,
    ) -> Session:
        """Create a new session with a generated ID."""
        session_id = str(uuid.uuid4())
        new_session = Session(
            id=session_id,
            user_id=user_id,
            app_name=app_name,
            state=state or {},
        )
        
        session_key = f"{app_name}_{user_id}_{session_id}"
        sessions_store[session_key] = new_session
        logger.info("New session created: %s", session_id)
        return new_session

    @app.delete("/apps/{app_name}/users/{user_id}/sessions/{session_id}")
    def delete_session(app_name: str, user_id: str, session_id: str):
        """Delete a session."""
        session_key = f"{app_name}_{user_id}_{session_id}"
        if session_key in sessions_store:
            del sessions_store[session_key]
            return {"status": "success"}
        else:
            raise HTTPException(status_code=404, detail="Session not found")

    @app.post("/run", response_model_exclude_none=True)
    async def agent_run(req: AgentRunRequest) -> List[Dict[str, Any]]:
        """Run an agent with a new message and return all events."""
        session_key = f"{req.app_name}_{req.user_id}_{req.session_id}"
        if session_key not in sessions_store:
            raise HTTPException(status_code=404, detail="Session not found")
            
        # Get or load agent
        agent = _get_agent(req.app_name)
        
        # Process the message through the agent
        input_text = req.new_message.get("parts", [{}])[0].get("text", "")
        if not input_text and "content" in req.new_message:
            input_text = req.new_message.get("content", "")
        
        # Add user message to session
        user_event = Event(
            author="user",
            content={
                "role": "user",
                "parts": [{"text": input_text}]
            }
        )
        sessions_store[session_key].events.append(user_event.dict())
        
        try:
            # Process the message through the agent
            response, _ = agent.process(input=input_text)
            
            # Create agent response event
            agent_event = Event(
                author="agent",
                content={
                    "role": "assistant",
                    "parts": [{"text": response}]
                }
            )
            
            # Add to session
            sessions_store[session_key].events.append(agent_event.dict())
            
            return [user_event.dict(), agent_event.dict()]
        except Exception as e:
            logger.exception(f"Error processing message: {e}")
            # Create error event
            error_event = Event(
                author="agent",
                content={
                    "role": "assistant",
                    "parts": [{"text": f"Error: {str(e)}"}]
                }
            )
            sessions_store[session_key].events.append(error_event.dict())
            return [user_event.dict(), error_event.dict()]

    @app.post("/run_sse")
    async def agent_run_sse(req: AgentRunRequest) -> StreamingResponse:
        """Run an agent with streaming response via SSE."""
        session_key = f"{req.app_name}_{req.user_id}_{req.session_id}"
        if session_key not in sessions_store:
            raise HTTPException(status_code=404, detail="Session not found")
            
        # SSE endpoint
        async def event_generator():
            try:
                # Get agent
                agent = _get_agent(req.app_name)
                
                # Extract message text
                input_text = req.new_message.get("parts", [{}])[0].get("text", "")
                if not input_text and "content" in req.new_message:
                    input_text = req.new_message.get("content", "")
                
                # Create user message event
                user_event = Event(
                    author="user",
                    content={
                        "role": "user",
                        "parts": [{"text": input_text}]
                    }
                )
                
                # Add to session
                sessions_store[session_key].events.append(user_event.dict())
                
                # Yield user event
                yield f"data: {user_event.json()}\n\n"
                
                # Process message
                response, logs = agent.process(input=input_text)
                
                # Create agent response event
                agent_event = Event(
                    author="agent",
                    content={
                        "role": "assistant",
                        "parts": [{"text": response}]
                    }
                )
                
                # Add to session
                sessions_store[session_key].events.append(agent_event.dict())
                
                # Yield agent event
                yield f"data: {agent_event.json()}\n\n"
                
            except Exception as e:
                logger.exception("Error in event_generator: %s", e)
                
                # Create error event
                error_event = Event(
                    author="agent",
                    content={
                        "role": "assistant",
                        "parts": [{"text": f"Error: {str(e)}"}]
                    }
                )
                
                # Add to session
                sessions_store[session_key].events.append(error_event.dict())
                
                # Yield error event
                yield f"data: {error_event.json()}\n\n"

        return StreamingResponse(
            event_generator(),
            media_type="text/event-stream",
        )

    @app.websocket("/run_live")
    async def agent_live_run(
        websocket: WebSocket,
        app_name: str,
        user_id: str,
        session_id: str,
        modalities: List[Literal["TEXT", "AUDIO"]] = Query(
            default=["TEXT", "AUDIO"]
        ),
    ) -> None:
        """Run an agent with bidirectional WebSocket communication."""
        await websocket.accept()

        session_key = f"{app_name}_{user_id}_{session_id}"
        if session_key not in sessions_store:
            await websocket.close(code=1002, reason="Session not found")
            return

        # Create message queue
        message_queue = MessageQueue()

        async def forward_events():
            try:
                # Get agent
                agent = _get_agent(app_name)
                
                # Initial welcome message
                welcome_event = Event(
                    author="agent",
                    content={
                        "role": "assistant",
                        "parts": [{"text": "Hello! I'm ready to chat."}]
                    }
                )
                
                # Add to session
                sessions_store[session_key].events.append(welcome_event.dict())
                
                # Send welcome message
                await websocket.send_text(welcome_event.json())
                
                # Process messages from the queue
                while True:
                    # Get message from queue
                    message = await message_queue.get()
                    
                    # Extract text
                    input_text = message.get("parts", [{}])[0].get("text", "")
                    if not input_text and "content" in message:
                        input_text = message.get("content", "")
                    
                    # Create user message event
                    user_event = Event(
                        author="user",
                        content={
                            "role": "user",
                            "parts": [{"text": input_text}]
                        }
                    )
                    
                    # Add to session
                    sessions_store[session_key].events.append(user_event.dict())
                    
                    try:
                        # Process message
                        response, logs = agent.process(input=input_text)
                        
                        # Create agent response event
                        agent_event = Event(
                            author="agent",
                            content={
                                "role": "assistant",
                                "parts": [{"text": response}]
                            }
                        )
                        
                        # Add to session
                        sessions_store[session_key].events.append(agent_event.dict())
                        
                        # Send agent response
                        await websocket.send_text(agent_event.json())
                        
                    except Exception as e:
                        logger.exception(f"Error processing message: {e}")
                        
                        # Create error event
                        error_event = Event(
                            author="agent",
                            content={
                                "role": "assistant",
                                "parts": [{"text": f"Error: {str(e)}"}]
                            }
                        )
                        
                        # Add to session
                        sessions_store[session_key].events.append(error_event.dict())
                        
                        # Send error event
                        await websocket.send_text(error_event.json())
            
            except Exception as e:
                logger.exception(f"Error in forward_events: {e}")

        async def process_messages():
            try:
                while True:
                    # Receive message
                    data = await websocket.receive_text()
                    
                    # Parse message
                    message = json.loads(data)
                    
                    # Add to queue
                    await message_queue.put(message)
                    
            except WebSocketDisconnect:
                logger.info("WebSocket disconnected")
            except Exception as e:
                logger.exception(f"Error in process_messages: {e}")

        # Run both tasks concurrently
        tasks = [
            asyncio.create_task(forward_events()),
            asyncio.create_task(process_messages()),
        ]
        
        try:
            # Wait for either task to complete
            done, pending = await asyncio.wait(
                tasks, return_when=asyncio.FIRST_COMPLETED
            )
            
            # Check for exceptions
            for task in done:
                try:
                    task.result()
                except WebSocketDisconnect:
                    logger.info("Client disconnected")
                except Exception as e:
                    logger.exception("Error in WebSocket task: %s", e)
                    
            # Cancel pending tasks
            for task in pending:
                task.cancel()
                
        except Exception as e:
            logger.exception("Error in WebSocket handler: %s", e)
            
            # Cancel all tasks
            for task in tasks:
                if not task.done():
                    task.cancel()

    def _get_agent(app_name: str) -> Agent:
        """Get or create an agent for the given app."""
        if app_name in agent_cache:
            return agent_cache[app_name]
            
        try:
            # Import the agent module
            logger.info(f"Loading agent: {app_name}")
            agent_module = importlib.import_module(app_name)
            
            # Get the root_agent from the module
            agent = getattr(agent_module.agent, "root_agent", None)
            
            if not agent:
                raise ValueError(f"Agent module {app_name} does not have a root_agent attribute")
                
            agent_cache[app_name] = agent
            return agent
        except Exception as e:
            logger.exception(f"Error loading agent: {e}")
            raise HTTPException(
                status_code=500, detail=f"Failed to load agent: {str(e)}"
            )

    # Mount the web UI if enabled
    if web:
        BASE_DIR = Path(__file__).parent.resolve()
        BROWSER_PATH = BASE_DIR.parent / "browser"

        @app.get("/")
        async def redirect_to_dev_ui():
            return RedirectResponse("/dev-ui")

        @app.get("/dev-ui")
        async def dev_ui():
            return FileResponse(BROWSER_PATH / "index.html")

        app.mount(
            "/", StaticFiles(directory=BROWSER_PATH, html=True), name="static"
        )

    return app
