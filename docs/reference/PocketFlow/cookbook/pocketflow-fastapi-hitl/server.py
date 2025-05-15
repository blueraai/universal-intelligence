import asyncio
import uuid
import json
import os
from fastapi import FastAPI, Request, HTTPException, status, BackgroundTasks # Import BackgroundTasks
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field # Import Pydantic for request/response models
from typing import Dict, Any, Literal # For type hinting

from flow import create_feedback_flow # PocketFlow imports

# --- Configuration ---
app = FastAPI(title="Minimal Feedback Loop API")

static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'static'))
if os.path.isdir(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")
else:
    print(f"Warning: Static directory '{static_dir}' not found.")

template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))
if os.path.isdir(template_dir):
    templates = Jinja2Templates(directory=template_dir)
else:
    print(f"Warning: Template directory '{template_dir}' not found.")
    templates = None

# --- State Management (In-Memory - NOT FOR PRODUCTION) ---
# Global dictionary to store task state. In production, use Redis, DB, etc.
tasks: Dict[str, Dict[str, Any]] = {}
# Structure: task_id -> {"shared": dict, "status": str, "task_obj": asyncio.Task | None}


# --- Background Flow Runner ---
# This function remains mostly the same, as it defines the work to be done.
# It will be scheduled by FastAPI's BackgroundTasks now.
async def run_flow_background(task_id: str, flow, shared: Dict[str, Any]):
    """Runs the flow in background, uses queue in shared for SSE."""
    # Check if task exists (might have been cancelled/deleted)
    if task_id not in tasks:
        print(f"Background task {task_id}: Task not found, aborting.")
        return
    queue = shared.get("sse_queue")
    if not queue:
        print(f"ERROR: Task {task_id} missing sse_queue in shared store!")
        tasks[task_id]["status"] = "failed"
        # Cannot report failure via SSE if queue is missing
        return

    tasks[task_id]["status"] = "running"
    await queue.put({"status": "running"})
    print(f"Task {task_id}: Background flow starting.")

    final_status = "unknown"
    error_message = None
    try:
        # Execute the potentially long-running PocketFlow
        await flow.run_async(shared)

        # Determine final status based on shared state after flow completion
        if shared.get("final_result") is not None:
            final_status = "completed"
        else:
            # If flow ends without setting final_result
            final_status = "finished_incomplete"
        print(f"Task {task_id}: Flow finished with status: {final_status}")

    except Exception as e:
        final_status = "failed"
        error_message = str(e)
        print(f"Task {task_id}: Flow execution failed: {e}")
        # Consider logging traceback here in production
    finally:
        # Ensure task still exists before updating state
        if task_id in tasks:
            tasks[task_id]["status"] = final_status
            final_update = {"status": final_status}
            if final_status == "completed":
                final_update["final_result"] = shared.get("final_result")
            elif error_message:
                final_update["error"] = error_message
            # Put final status update onto the queue
            await queue.put(final_update)

        # Signal the end of the SSE stream by putting None
        # Must happen regardless of whether task was deleted mid-run
        if queue:
           await queue.put(None)
        print(f"Task {task_id}: Background task ended. Final update sentinel put on queue.")
        # Remove the reference to the completed/failed asyncio Task object
        if task_id in tasks:
            tasks[task_id]["task_obj"] = None

# --- Pydantic Models for Request/Response Validation ---
class SubmitRequest(BaseModel):
    data: str = Field(..., min_length=1, description="Input data for the task")

class SubmitResponse(BaseModel):
    message: str = "Task submitted"
    task_id: str

class FeedbackRequest(BaseModel):
    feedback: Literal["approved", "rejected"] # Use Literal for specific choices

class FeedbackResponse(BaseModel):
    message: str

# --- FastAPI Routes ---
@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def get_index(request: Request):
    """Serves the main HTML frontend."""
    if templates is None:
        raise HTTPException(status_code=500, detail="Templates directory not configured.")
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/submit", response_model=SubmitResponse, status_code=status.HTTP_202_ACCEPTED)
async def submit_task(
    submit_request: SubmitRequest, # Use Pydantic model for validation
    background_tasks: BackgroundTasks # Inject BackgroundTasks instance
):
    """
    Submits a new task. The actual processing runs in the background.
    Returns immediately with the task ID.
    """
    task_id = str(uuid.uuid4())
    feedback_event = asyncio.Event()
    status_queue = asyncio.Queue()

    shared = {
        "task_input": submit_request.data,
        "processed_output": None,
        "feedback": None,
        "review_event": feedback_event,
        "sse_queue": status_queue,
        "final_result": None,
        "task_id": task_id
    }

    flow = create_feedback_flow()

    # Store task state BEFORE scheduling background task
    tasks[task_id] = {
        "shared": shared,
        "status": "pending",
        "task_obj": None # Placeholder for the asyncio Task created by BackgroundTasks
    }

    await status_queue.put({"status": "pending", "task_id": task_id})

    # Schedule the flow execution using FastAPI's BackgroundTasks
    # This runs AFTER the response has been sent
    background_tasks.add_task(run_flow_background, task_id, flow, shared)
    # Note: We don't get a direct reference to the asyncio Task object this way,
    # which is fine for this minimal example. If cancellation were needed,
    # managing asyncio.create_task manually would be necessary.

    print(f"Task {task_id}: Submitted, scheduled for background execution.")
    return SubmitResponse(task_id=task_id)


@app.post("/feedback/{task_id}", response_model=FeedbackResponse)
async def provide_feedback(task_id: str, feedback_request: FeedbackRequest):
    """Provides feedback (approved/rejected) to potentially unblock a waiting task."""
    if task_id not in tasks:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    task_info = tasks[task_id]
    shared = task_info["shared"]
    queue = shared.get("sse_queue")
    review_event = shared.get("review_event")

    async def report_error(message, status_code=status.HTTP_400_BAD_REQUEST):
        # Helper to log, put status on queue, and raise HTTP exception
        print(f"Task {task_id}: Feedback error - {message}")
        if queue: await queue.put({"status": "feedback_error", "error": message})
        raise HTTPException(status_code=status_code, detail=message)

    if not review_event:
        # This indicates an internal setup error if the task exists but has no event
        await report_error("Task not configured for feedback", status.HTTP_500_INTERNAL_SERVER_ERROR)
    if review_event.is_set():
        # Prevent processing feedback multiple times or if the task isn't waiting
        await report_error("Task not awaiting feedback or feedback already sent", status.HTTP_409_CONFLICT)

    feedback = feedback_request.feedback # Already validated by Pydantic
    print(f"Task {task_id}: Received feedback via POST: {feedback}")

    # Update status *before* setting the event, so client sees 'processing' first
    if queue: await queue.put({"status": "processing_feedback", "feedback_value": feedback})
    tasks[task_id]["status"] = "processing_feedback" # Update central status tracker

    # Store feedback and signal the waiting ReviewNode
    shared["feedback"] = feedback
    review_event.set()

    return FeedbackResponse(message=f"Feedback '{feedback}' received")


# --- SSE Endpoint ---
@app.get("/stream/{task_id}")
async def stream_status(task_id: str):
    """Streams status updates for a given task using Server-Sent Events."""
    if task_id not in tasks or "sse_queue" not in tasks[task_id]["shared"]:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task or queue not found")

    queue = tasks[task_id]["shared"]["sse_queue"]

    async def event_generator():
        """Yields SSE messages from the task's queue."""
        print(f"SSE Stream: Client connected for {task_id}")
        try:
            while True:
                # Wait for the next status update from the queue
                update = await queue.get()
                if update is None: # Sentinel value indicates end of stream
                    print(f"SSE Stream: Sentinel received for {task_id}, closing stream.")
                    yield f"data: {json.dumps({'status': 'stream_closed'})}\n\n"
                    break

                sse_data = json.dumps(update)
                print(f"SSE Stream: Sending for {task_id}: {sse_data}")
                yield f"data: {sse_data}\n\n" # SSE format: "data: <json>\n\n"
                queue.task_done() # Acknowledge processing the queue item

        except asyncio.CancelledError:
            # This happens if the client disconnects
            print(f"SSE Stream: Client disconnected for {task_id}.")
        except Exception as e:
            # Log unexpected errors during streaming
            print(f"SSE Stream: Error in generator for {task_id}: {e}")
            # Optionally send an error message to the client if possible
            try:
                yield f"data: {json.dumps({'status': 'stream_error', 'error': str(e)})}\n\n"
            except Exception: # Catch errors if yield fails (e.g., connection already closed)
                pass
        finally:
            print(f"SSE Stream: Generator finished for {task_id}.")
            # Consider cleanup here (e.g., removing task if no longer needed)
            # if task_id in tasks: del tasks[task_id]

    # Use FastAPI/Starlette's StreamingResponse for SSE
    headers = {'Cache-Control': 'no-cache', 'X-Accel-Buffering': 'no'}
    return StreamingResponse(event_generator(), media_type="text/event-stream", headers=headers)

# --- Main Execution Guard (for running with uvicorn) ---
if __name__ == "__main__":
    print("Starting FastAPI server using Uvicorn is recommended:")
    print("uvicorn server:app --reload --host 0.0.0.0 --port 8000")
    # Example using uvicorn programmatically (less common than CLI)
    # import uvicorn
    # uvicorn.run(app, host="0.0.0.0", port=8000)