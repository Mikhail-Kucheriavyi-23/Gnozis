from src.chat_api import create_chat, dumps_response, handle_chat


def test_handle_chat_uses_core_chat():
    chat = create_chat(subject="test-user")

    result = handle_chat({"message": "hello"}, chat)

    assert result["state"]["turn"] == 1
    assert result["state"]["last_message"] == "hello"
    assert result["state"]["agency_subject"] == "test-user"
    assert result["response"]


def test_chat_response_is_json_serializable():
    chat = create_chat(subject="test-user")

    result = handle_chat({"message": "hello"}, chat)
    encoded = dumps_response(result)

    assert '"response"' in encoded
    assert '"state"' in encoded


def test_empty_message_is_rejected_by_core_boundary():
    chat = create_chat(subject="test-user")

    try:
        handle_chat({"message": "   "}, chat)
    except ValueError as exc:
        assert str(exc) == "message must not be empty"
    else:
        raise AssertionError("Empty messages must be rejected")
