# GPT-Partner

A governed capability and execution layer for GPT, designed to connect tools, isolated computing environments, authorization workflows, and evidence-driven learning through a unified interface.

## Current milestone: connectivity prototype

The first vertical slice exposes two harmless MCP tools:

- `partner_status` — reports what the application knows about its current prototype state.
- `echo` — returns a supplied message for a round-trip interaction test.

This is intentionally small. The service does **not** execute shell commands, run arbitrary code, or claim that ChatGPT is already connected.

## Run locally

Requires Python 3.11 or later.

```bash
python -m venv .venv
```

Activate the virtual environment, then install the package and development dependencies:

```bash
python -m pip install -e ".[dev]"
```

Run the unit tests:

```bash
pytest
```

Start the MCP service:

```bash
python -m gpt_partner.server
```

The initial server is configured for local testing at `127.0.0.1:8000` using the MCP Streamable HTTP transport. Confirm the installed MCP SDK's startup output and endpoint behavior in the actual environment before treating the endpoint as operational.

## What this proves — and what it does not

When the tests are actually run, they can validate the deterministic core functions. Starting the server can validate local process startup. An MCP client round-trip is a separate test. Connecting ChatGPT to a remotely reachable endpoint is another separate milestone.

Current repository state alone does not prove any of those runtime outcomes. Remote ChatGPT connectivity requires a reachable deployment, HTTPS as required by the target client, appropriate authentication, and explicit configuration of the supported ChatGPT connector path. Those have not yet been configured or verified.

## Safety boundary

The prototype exposes only status and echo. Do not add general-purpose shell execution, arbitrary filesystem access, or unrestricted code execution to this initial endpoint. Any future state-changing capability must have an explicit authorization contract and tests before it is exposed.

## Project state

- Specification: `GPTP-SPEC-BOOTSTRAP-001 v0.1`
- Current status: `PROPOSED / EXPERIMENTAL / NOT VERIFIED / NOT ADOPTED`
- Current focus: establish a real request/response path before expanding capabilities.
