import httpx
from httpx_sse import connect_sse
from typing import Any, AsyncIterable
from common.types import (
    AgentCard,
    GetTaskRequest,
    SendTaskRequest,
    SendTaskResponse,
    JSONRPCRequest,
    JSONRPCResponse,
    JSONRPCError,
    GetTaskResponse,
    CancelTaskResponse,
    CancelTaskRequest,
    SetTaskPushNotificationRequest,
    SetTaskPushNotificationResponse,
    GetTaskPushNotificationRequest,
    GetTaskPushNotificationResponse,
    A2AClientHTTPError,
    A2AClientJSONError,
    SendTaskStreamingRequest,
    SendTaskStreamingResponse,
    Task,
    TaskPushNotificationConfig,
    TaskStatusUpdateEvent,
    TaskArtifactUpdateEvent,
)
import json
import logging

# Configure a logger specific to the client
logger = logging.getLogger("A2AClient")

class A2AClientError(Exception):
    """Base class for A2A client errors"""
    def __init__(self, message):
        super().__init__(message)

class RpcError(Exception):
    code: int
    data: Any = None
    def __init__(self, code: int, message: str, data: Any = None):
        super().__init__(message)
        self.name = "RpcError"
        self.code = code
        self.data = data

class A2AClient:
    def __init__(self, agent_card: AgentCard = None, url: str = None):
        if agent_card:
            self.url = agent_card.url.rstrip("/")
        elif url:
            self.url = url.rstrip("/")
        else:
            raise ValueError("Must provide either agent_card or url")
        self.fetchImpl = httpx.AsyncClient(timeout=None)

    def _generateRequestId(self):
        import time
        return int(time.time() * 1000)

    async def _send_request(self, request: JSONRPCRequest) -> dict[str, Any]:
        req_id = request.id
        req_method = request.method
        req_dump = request.model_dump(exclude_none=True)

        logger.info(f"-> Sending Request (ID: {req_id}, Method: {req_method}):\n{json.dumps(req_dump, indent=2)}")

        try:
            response = await self.fetchImpl.post(
                self.url, json=req_dump, timeout=60.0
            )
            logger.info(f"<- Received HTTP Status {response.status_code} for Request (ID: {req_id})")
            response_text = await response.aread()
            logger.debug(f"Raw Response Body (ID: {req_id}):\n{response_text.decode('utf-8', errors='replace')}")

            response.raise_for_status()

            try:
                json_response = json.loads(response_text)
            except json.JSONDecodeError as e:
                logger.error(f"Failed to decode JSON response (ID: {req_id}): {e}")
                raise A2AClientJSONError(f"Failed to decode JSON: {e}") from e

            if "error" in json_response and json_response["error"] is not None:
                rpc_error = json_response["error"]
                logger.warning(f"<- Received JSON-RPC Error (ID: {req_id}): Code={rpc_error.get('code')}, Msg='{rpc_error.get('message')}'")
                raise RpcError(rpc_error.get("code", -32000), rpc_error.get("message", "Unknown RPC Error"), rpc_error.get("data"))

            logger.info(f"<- Received Success Response (ID: {req_id}):\n{json.dumps(json_response, indent=2)}")
            return json_response

        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP Error for Request (ID: {req_id}): {e.response.status_code} - {e.request.url}")
            error_body = await e.response.aread()
            raise A2AClientHTTPError(e.response.status_code, f"{e}. Body: {error_body.decode('utf-8', errors='replace')}") from e
        except httpx.RequestError as e:
            logger.error(f"Request Error for (ID: {req_id}): {e}")
            raise A2AClientError(f"Network or request error: {e}") from e
        except RpcError:
             raise
        except Exception as e:
             logger.error(f"Unexpected error during request (ID: {req_id}): {e}", exc_info=True)
             raise A2AClientError(f"Unexpected error: {e}") from e

    async def send_task(self, payload: dict[str, Any]) -> SendTaskResponse:
        request = SendTaskRequest(params=payload)
        response_dict = await self._send_request(request)
        return SendTaskResponse(**response_dict)

    async def send_task_streaming(
        self, payload: dict[str, Any]
    ) -> AsyncIterable[SendTaskStreamingResponse]:
        request = SendTaskStreamingRequest(params=payload)
        req_id = request.id
        req_dump = request.model_dump(exclude_none=True)

        logger.info(f"-> Sending Streaming Request (ID: {req_id}, Method: {request.method}):\n{json.dumps(req_dump, indent=2)}")

        try:
            async with self.fetchImpl.stream("POST", self.url, json=req_dump, timeout=None) as response:
                 logger.info(f"<- Received HTTP Status {response.status_code} for Streaming Request (ID: {req_id})")
                 response.raise_for_status()

                 buffer = ""
                 async for line in response.aiter_lines():
                     if not line:
                         if buffer.startswith("data:"):
                             data_str = buffer[len("data:"):].strip()
                             logger.debug(f"Received SSE Data Line (ID: {req_id}): {data_str}")
                             try:
                                 sse_data_dict = json.loads(data_str)
                                 yield SendTaskStreamingResponse(**sse_data_dict)
                             except json.JSONDecodeError as e:
                                 logger.error(f"Failed to decode SSE JSON (ID: {req_id}): {e}. Data: '{data_str}'")
                             except Exception as e:
                                 logger.error(f"Error processing SSE data (ID: {req_id}): {e}. Data: '{data_str}'", exc_info=True)
                         elif buffer:
                             logger.debug(f"Received non-data SSE line (ID: {req_id}): {buffer}")
                         buffer = ""
                     else:
                         buffer += line + "\n"

                 if buffer:
                     logger.warning(f"SSE stream ended with partial data in buffer (ID: {req_id}): {buffer}")

                 logger.info(f"SSE Stream ended for request ID: {req_id}")

        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP Error during streaming connection (ID: {req_id}): {e.response.status_code} - {e.request.url}")
            error_body = await e.response.aread()
            raise A2AClientHTTPError(e.response.status_code, f"{e}. Body: {error_body.decode('utf-8', errors='replace')}") from e
        except httpx.RequestError as e:
             logger.error(f"Request Error during streaming (ID: {req_id}): {e}")
             raise A2AClientError(f"Network or request error during streaming: {e}") from e
        except Exception as e:
            logger.error(f"Unexpected error during streaming (ID: {req_id}): {e}", exc_info=True)
            raise A2AClientError(f"Unexpected streaming error: {e}") from e

    async def get_task(self, payload: dict[str, Any]) -> GetTaskResponse:
        request = GetTaskRequest(params=payload)
        response_dict = await self._send_request(request)
        return GetTaskResponse(**response_dict)

    async def cancel_task(self, payload: dict[str, Any]) -> CancelTaskResponse:
        request = CancelTaskRequest(params=payload)
        response_dict = await self._send_request(request)
        return CancelTaskResponse(**response_dict)

    async def set_task_callback(
        self, payload: dict[str, Any]
    ) -> SetTaskPushNotificationResponse:
        request = SetTaskPushNotificationRequest(params=payload)
        response_dict = await self._send_request(request)
        return SetTaskPushNotificationResponse(**response_dict)

    async def get_task_callback(
        self, payload: dict[str, Any]
    ) -> GetTaskPushNotificationResponse:
        request = GetTaskPushNotificationRequest(params=payload)
        response_dict = await self._send_request(request)
        return GetTaskPushNotificationResponse(**response_dict)
