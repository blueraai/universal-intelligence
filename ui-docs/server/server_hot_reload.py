#!/usr/bin/env python

import sys
import time
import subprocess
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Configuration
SERVER_SCRIPT = "server.py"  # The main server script to run
WATCH_PATTERNS = [".py"]     # File extensions to watch for changes

class ChangeHandler(FileSystemEventHandler):
    def __init__(self, restart_func):
        self.restart_func = restart_func
        self.last_modified = time.time()

    def on_modified(self, event):
        if not event.is_directory:
            file_path = event.src_path
            # Only react to .py files
            if any(file_path.endswith(ext) for ext in WATCH_PATTERNS):
                # Avoid reacting to the same file multiple times in quick succession
                current_time = time.time()
                if current_time - self.last_modified > 1:  # 1 second debounce
                    print(f"\n[hot-reload] Detected change in {file_path}")
                    self.last_modified = current_time
                    self.restart_func()

class ServerRunner:
    def __init__(self):
        self.process = None
        self.is_running = False

    def start(self):
        """Start the server process"""
        try:
            # Kill any existing process first
            self.stop()

            # Start a new process
            print(f"[hot-reload] Starting server: {SERVER_SCRIPT}")
            self.process = subprocess.Popen([sys.executable, SERVER_SCRIPT],
                                            stdout=subprocess.PIPE,
                                            stderr=subprocess.STDOUT,
                                            universal_newlines=True,
                                            bufsize=1)
            self.is_running = True

            # Start a thread to read and print output
            import threading
            def read_output():
                for line in self.process.stdout:
                    print(line, end='')
            threading.Thread(target=read_output, daemon=True).start()

        except Exception as e:
            print(f"[hot-reload] Error starting server: {e}")
            self.is_running = False

    def stop(self):
        """Stop the server process if it's running"""
        if self.process and self.is_running:
            print("[hot-reload] Stopping server...")
            try:
                # Try to terminate gracefully first
                self.process.terminate()
                self.process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                # Force kill if it doesn't terminate
                print("[hot-reload] Server didn't terminate gracefully, forcing...")
                self.process.kill()

            self.is_running = False
            self.process = None
            print("[hot-reload] Server stopped")

    def restart(self):
        """Restart the server by stopping and starting it again"""
        self.stop()
        time.sleep(1)  # Small delay to ensure sockets are properly released
        self.start()

def main():
    # Initial setup
    runner = ServerRunner()
    handler = ChangeHandler(runner.restart)

    # Set up file watching
    observer = Observer()
    observer.schedule(handler, path='.', recursive=True)
    observer.start()

    try:
        # Start the server initially
        runner.start()

        # Keep running until interrupted
        print("[hot-reload] Watching for file changes (press Ctrl+C to exit)...")
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n[hot-reload] Stopping...")
        runner.stop()
        observer.stop()

    observer.join()
    print("[hot-reload] Exited cleanly")

if __name__ == "__main__":
    print(f"[hot-reload] Server hot-reload starting")
    main()
