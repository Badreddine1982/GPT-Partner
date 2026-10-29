"""Small deterministic operations used by the first MCP vertical slice."""

from __future__ import annotations

from typing import Any

PROTOCOL_VERSION = "0.1"
SERVICE_NAME = "GPT Partner"


def get_status() -> dict[str, Any]:
    """Return service identity and honest prototype status.

    This reports process-level application status only. It does not claim that
    ChatGPT is connected, that a remote endpoint is deployed, or that a runtime
    is isolated.
    """
    return {
        "service": SERVICE_NAME,
        "service_version": "0.1.0",
        "protocol_version": PROTOCOL_VERSION,
        "state": "running",
        "stage": "local_mcp_prototype",
        "chatgpt_connected": False,
        "remote_deployment_verified": False,
        "isolated_execution_available": False,
    }


def echo_message(message: str) -> dict[str, str]:
    """Return the exact supplied message for a round-trip connectivity test."""
    if not isinstance(message, str):
        raise TypeError("message must be a string")
    if len(message) > 4000:
        raise ValueError("message exceeds the 4000-character test limit")
    return {"message": message, "round_trip": "completed"}
