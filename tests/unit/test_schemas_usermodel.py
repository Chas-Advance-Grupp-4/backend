import pytest
from pydantic import ValidationError
from app.api.v1.schemas.user_schema import not_empty, UserCreate, UserLogin

# --- not_empty tests ---
def test_not_empty_with_valid_string():
    value = "Anna"
    result = not_empty("Username", value)
    assert result == "Anna"

def test_not_empty_preserves_whitespace():
    value = "  Anna  "
    result = not_empty("Username", value)
    assert result == "  Anna  "

def test_not_empty_raises_on_empty_string():
    empty_value = "    "
    with pytest.raises(ValueError) as exc_info:
        not_empty("Username", empty_value)
    assert "Username field empty." in str(exc_info.value)

# --- UserCreate schema tests ---
def test_usercreate_valid():
    user = UserCreate(username="Bobby", password="secret", role="customer")
    assert user.username == "Bobby"
    assert user.role == "customer"

def test_usercreate_empty_username():
    with pytest.raises(ValidationError) as exc_info:
        UserCreate(username="", password="secret", role="customer")
    assert any("Username field empty." in e['msg'] for e in exc_info.value.errors())

def test_usercreate_empty_password():
    with pytest.raises(ValidationError) as exc_info:
        UserCreate(username="Bobby", password="", role="customer")
    assert any("Password field empty." in e['msg'] for e in exc_info.value.errors())

def test_usercreate_invalid_role():
    with pytest.raises(ValidationError) as exc_info:
        UserCreate(username="Bobby", password="secret", role="invalid")
    errors = exc_info.value.errors()
    assert any(e['loc'] == ('role',) for e in errors)

# --- UserLogin schema tests ---
def test_userlogin_valid():
    login = UserLogin(username="Anna", password="1234")
    assert login.username == "Anna"
    assert login.password == "1234"

def test_userlogin_empty_username():
    with pytest.raises(ValidationError) as exc_info:
        UserLogin(username="   ", password="1234")
    assert any("Username field empty." in e['msg'] for e in exc_info.value.errors())

def test_userlogin_empty_password():
    with pytest.raises(ValidationError) as exc_info:
        UserLogin(username="Anna", password="   ")
    assert any("Password field empty." in e['msg'] for e in exc_info.value.errors())
