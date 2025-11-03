import pytest
from pydantic import ValidationError
from app.api.v1.schemas.user_schema import not_empty, UserCreate, UserLogin

# -----------------------------
# Tests for not_empty helper
# -----------------------------


def test_not_empty_with_valid_string():
    """
    Purpose: Verify that not_empty returns the string as-is if it contains non-whitespace characters.
    Scenario: Input string "Anna" is passed.
    Expected: Returns "Anna" without errors.
    """
    value = "Anna"
    result = not_empty("Username", value)
    assert result == "Anna"


def test_not_empty_preserves_whitespace():
    """
    Purpose: Ensure not_empty does not trim surrounding whitespace.
    Scenario: Input string "  Anna  " is passed.
    Expected: Returns the string unchanged, including whitespace.
    """
    value = "  Anna  "
    result = not_empty("Username", value)
    assert result == "  Anna  "


def test_not_empty_raises_on_empty_string():
    """
    Purpose: Ensure not_empty raises ValueError for empty/whitespace-only strings.
    Scenario: Input string "    " is passed.
    Expected: Raises ValueError with field name included in message.
    """
    empty_value = "    "
    with pytest.raises(ValueError) as exc_info:
        not_empty("Username", empty_value)
    assert "Username field empty." in str(exc_info.value)


# -----------------------------
# Tests for UserCreate schema
# -----------------------------


def test_usercreate_valid():
    """
    Purpose: Validate that a correct UserCreate object is instantiated.
    Scenario: username="Bobby", password="secret", role="customer"
    Expected: Object created successfully with correct fields.
    """
    user = UserCreate(username="Bobby", password="secret", role="customer")
    assert user.username == "Bobby"
    assert user.role == "customer"


def test_usercreate_empty_username():
    """
    Purpose: Ensure validation fails for empty username.
    Scenario: username="" passed to UserCreate.
    Expected: ValidationError raised, error message contains "Username field empty."
    """
    with pytest.raises(ValidationError) as exc_info:
        UserCreate(username="", password="secret", role="customer")
    assert any("Username field empty." in e["msg"] for e in exc_info.value.errors())


def test_usercreate_empty_password():
    """
    Purpose: Ensure validation fails for empty password.
    Scenario: password="" passed to UserCreate.
    Expected: ValidationError raised, error message contains "Password field empty."
    """
    with pytest.raises(ValidationError) as exc_info:
        UserCreate(username="Bobby", password="", role="customer")
    assert any("Password field empty." in e["msg"] for e in exc_info.value.errors())


def test_usercreate_invalid_role():
    """
    Purpose: Ensure validation fails for invalid role values.
    Scenario: role="invalid" passed to UserCreate.
    Expected: ValidationError raised, error location includes 'role'.
    """
    with pytest.raises(ValidationError) as exc_info:
        UserCreate(username="Bobby", password="secret", role="invalid")
    errors = exc_info.value.errors()
    assert any(e["loc"] == ("role",) for e in errors)


# -----------------------------
# Tests for UserLogin schema
# -----------------------------


def test_userlogin_valid():
    """
    Purpose: Validate that a correct UserLogin object is instantiated.
    Scenario: username="Anna", password="1234"
    Expected: Object created successfully with correct fields.
    """
    login = UserLogin(username="Anna", password="1234")
    assert login.username == "Anna"
    assert login.password == "1234"


def test_userlogin_empty_username():
    """
    Purpose: Ensure validation fails for empty username in login.
    Scenario: username="   " (whitespace only)
    Expected: ValidationError raised with message "Username field empty."
    """
    with pytest.raises(ValidationError) as exc_info:
        UserLogin(username="   ", password="1234")
    assert any("Username field empty." in e["msg"] for e in exc_info.value.errors())


def test_userlogin_empty_password():
    """
    Purpose: Ensure validation fails for empty password in login.
    Scenario: password="   " (whitespace only)
    Expected: ValidationError raised with message "Password field empty."
    """
    with pytest.raises(ValidationError) as exc_info:
        UserLogin(username="Anna", password="   ")
    assert any("Password field empty." in e["msg"] for e in exc_info.value.errors())
