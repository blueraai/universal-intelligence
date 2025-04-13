FROM python:3.10-slim

WORKDIR /app

# Install dependencies
RUN pip install websockets universal-intelligence

# Copy WebSocket server
COPY server.py .

# Expose WebSocket port
EXPOSE 8765

# Run WebSocket server
CMD ["python", "server.py"]
