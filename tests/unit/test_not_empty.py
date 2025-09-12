import pytest
from app.api.v1.schemas.user_schema import not_empty

def test_not_empty_with_valid_string():
    field_name = "Username"
    value = "alice"
    result = not_empty(field_name, value)
    assert result == "alice"

def test_not_empty_preserves_whitespace():
    field_name = "Username"
    value = "  alice  "
    result = not_empty(field_name, value)
    assert result == "  alice  "

def test_not_empty_raises_on_empty_string():
    field_name = "Username"
    empty_value = "    "
    with pytest.raises(ValueError) as exc_info:
        not_empty(field_name, empty_value)
    assert "Username field empty." in str(exc_info.value)