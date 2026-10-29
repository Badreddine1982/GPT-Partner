"""MCP server entry point for the first GPT Partner connectivity test.

Run locally with:
    python -m gpt_partner.server

The initial service exposes only harmless status and echo tools. It does not
execute shell commands, access arbitrary files, or provide a general code runner.
"""

from mcp.server.fastmcp import FastMCP

from gpt_partner.core import echo_message, get_status

mcp = FastMCP("GPT Partner", host="127.0.0.1", port=8000)


@mcp.tool()
def partner_status() -> dict:
    """Report the current prototype status without implying remote connectivity."""
    return get_status()


@mcp.tool()
def echo(message: str) -> dict:
    """Echo a message to verify that a request reaches GPT Partner and returns."""
    return echo_message(message)


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
