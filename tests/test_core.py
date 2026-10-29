from gpt_partner.core import echo_message, get_status


def test_status_does_not_claim_chatgpt_connection_or_runtime():
    status = get_status()
    assert status["state"] == "running"
    assert status["chatgpt_connected"] is False
    assert status["remote_deployment_verified"] is False
    assert status["isolated_execution_available"] is False


def test_echo_returns_exact_message():
    message = "GPT Partner round-trip test / اختبار الاتصال"
    assert echo_message(message) == {
        "message": message,
        "round_trip": "completed",
    }


def test_echo_rejects_oversized_message():
    try:
        echo_message("x" * 4001)
    except ValueError as exc:
        assert "4000-character" in str(exc)
    else:
        raise AssertionError("Oversized message should be rejected")
