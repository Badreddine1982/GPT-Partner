"""MCP server entry point for the first GPT Partner connectivity test.

Run locally with:
    python -m gpt_partner.server

For a container deployment, set GPT_PARTNER_HOST=0.0.0.0 and GPT_PARTNER_PORT
to the platform-provided port. Remote exposure must also be protected by the
deployment's HTTPS and authentication layer before connecting ChatGPT.
"""

from __future__ import annotations

import os

from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings

from gpt_partner.core import echo_message, get_status

host = os.environ.get("GPT_PARTNER_HOST", "127.0.0.1")
port = int(os.environ.get("GPT_PARTNER_PORT", "8000"))

mcp = FastMCP(
    "GPT Partner",
    host=host,
    port=port,
    json_response=True,
    stateless_http=True,
    transport_security=TransportSecuritySettings(
        allowed_hosts=["localhost", "127.0.0.1", "testserver", "*.vercel.app", "*.now.sh"],
    ),
)


@mcp.tool()
def partner_status() -> dict:
    """Report the current prototype status without implying remote connectivity."""
    return get_status()


@mcp.tool()
def echo(message: str) -> dict:
    """Echo a message to verify that a request reaches GPT Partner and returns."""
    return echo_message(message)


app = mcp.streamable_http_app()


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
