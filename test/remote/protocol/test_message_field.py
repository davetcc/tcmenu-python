import pytest

from tcmenu.remote.protocol.message_field import MessageField


# noinspection PyProtectedMember
@pytest.fixture(autouse=True)
def message_field_fixture():
    """
    This code temporarily changes internal dictionary of a MessageField.
    We have to ensure that original entries are set back to avoid
    test failures.
    """
    # Setup
    entries: dict[str, "MessageField"] = MessageField._ALL_FIELDS_DICT.copy()
    MessageField._ALL_FIELDS_DICT.clear()

    yield

    # Teardown
    MessageField._ALL_FIELDS_DICT = entries


def test_message_field():
    message = MessageField("R", "V")

    assert message.first_byte is "R"
    assert message.second_byte is "V"
    assert message.high is "R"
    assert message.low is "V"
    assert message.id == "RV"
    assert str(message) == "Field[RV]"


def test_message_field_duplicate_entry():
    MessageField("A", "A")

    with pytest.raises(ValueError):
        MessageField("A", "A")


def test_message_from_id():
    MessageField("A", "A")

    message = MessageField.from_id("AA")

    assert isinstance(message, MessageField)
    assert message.id == "AA"

    # Invalid message
    with pytest.raises(ValueError):
        MessageField.from_id("AB")
