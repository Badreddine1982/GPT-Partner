import pytest
from starlette.testclient import TestClient

from gpt_partner.server import app


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as test_client:
        yield test_client


def mcp_post(client: TestClient, payload: dict):
    return client.post(
        "/mcp",
        headers={
            "accept": "application/json, text/event-stream",
            "content-type": "application/json",
            "host": "localhost",
            "mcp-protocol-version": "2025-06-18",
        },
        json=payload,
    )


def test_initialize_and_list_tools(client: TestClient):
    initialize = mcp_post(
        client,
        {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2025-06-18",
                "capabilities": {},
                "clientInfo": {"name": "pytest", "version": "1.0"},
            },
        }
    )
    assert initialize.status_code == 200
    assert initialize.json()["result"]["serverInfo"]["name"] == "GPT Partner"

    tools = mcp_post(client, {"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
    assert tools.status_code == 200
    names = {tool["name"] for tool in tools.json()["result"]["tools"]}
    assert names == {"partner_status", "echo"}


def test_tools_call_partner_status_and_echo(client: TestClient):
    status = mcp_post(
        client,
        {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {"name": "partner_status", "arguments": {}},
        }
    )
    assert status.status_code == 200
    assert 'remote_deployment_verified' in status.text
    assert 'false' in status.text

    echo = mcp_post(
        client,
        {
            "jsonrpc": "2.0",
            "id": 4,
            "method": "tools/call",
            "params": {"name": "echo", "arguments": {"message": "round trip"}},
        }
    )
    assert echo.status_code == 200
    assert 'round_trip' in echo.text
    assert 'completed' in echo.text
