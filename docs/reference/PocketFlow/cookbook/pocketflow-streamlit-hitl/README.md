# PocketFlow Streamlit Human-in-the-Loop (HITL) Application

Minimal Human-in-the-Loop (HITL) web application using PocketFlow and Streamlit. Submit text, review processed output, and approve/reject.

## Features

-   **Streamlit UI:** Simple, interactive interface for submitting tasks and providing feedback, built entirely in Python.
-   **PocketFlow Workflow:** Manages distinct processing stages (initial processing, finalization) using synchronous PocketFlow `Flow`s.
-   **Session State Management:** Utilizes Streamlit's `st.session_state` to manage the current stage of the workflow and to act as the `shared` data store for PocketFlow.
-   **Iterative Feedback Loop:** Allows users to reject processed output and resubmit, facilitating refinement.

## How to Run

1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the Streamlit Application:**
    ```bash
    streamlit run app.py
    ```

3.  **Access the Web UI:**
    Open the URL provided by Streamlit (usually `http://localhost:8501`).

## Files

-   [`app.py`](./app.py): Main Streamlit application logic and UI.
-   [`nodes.py`](./nodes.py): PocketFlow `Node` definitions.
-   [`flows.py`](./flows.py): PocketFlow `Flow` construction.
-   [`utils/process_task.py`](./utils/process_task.py): Simulated task processing utility.
-   [`requirements.txt`](./requirements.txt): Project dependencies.
-   [`README.md`](./README.md): This file.
