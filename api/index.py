"""Vercel ASGI entrypoint for the GPT Partner MCP service."""

from gpt_partner.server import app

__all__ = ["app"]
