from datetime import datetime, timedelta, timezone

import jwt
from sqlalchemy import select

from config import settings
from models.user import User
from services.user import verify_password


def test_register_user_success(client):
    response = client.post(
        "/users/",
        json={
            "email": "success@example.com",
            "password": "password123",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["email"] == "success@example.com"
    assert "id" in data
    assert isinstance(data["id"], int)

    # Sensitive fields must not be returned.
    assert "password" not in data
    assert "password_hash" not in data


def test_register_user_with_email_alias(client):
    response = client.post(
        "/users/",
        json={
            "email": "test+alias@example.com",
            "password": "password123",
        },
    )

    assert response.status_code == 201
    assert response.json()["email"] == "test+alias@example.com"


def test_register_user_with_subdomain_email(client):
    response = client.post(
        "/users/",
        json={
            "email": "user@mail.example.com",
            "password": "password123",
        },
    )

    assert response.status_code == 201
    assert response.json()["email"] == "user@mail.example.com"


def test_register_user_with_special_characters_in_password(client):
    response = client.post(
        "/users/",
        json={
            "email": "special@example.com",
            "password": "P@ssw0rd!#$%^&*",
        },
    )

    assert response.status_code == 201


def test_register_user_password_is_hashed(client, db_session):
    email = "hashed@example.com"
    password = "password123"

    response = client.post(
        "/users/",
        json={
            "email": email,
            "password": password,
        },
    )

    assert response.status_code == 201

    user = db_session.scalar(select(User).where(User.email == email))

    assert user is not None
    assert user.password_hash != password
    assert user.password_hash.startswith("$argon2")


def test_register_user_password_can_be_verified(client, db_session):
    email = "verify-password@example.com"
    password = "password123"

    response = client.post(
        "/users/",
        json={
            "email": email,
            "password": password,
        },
    )

    assert response.status_code == 201

    user = db_session.scalar(select(User).where(User.email == email))

    assert user is not None
    assert verify_password(password, user.password_hash) is True
    assert verify_password("wrong-password", user.password_hash) is False


def test_register_user_invalid_email(client):
    response = client.post(
        "/users/",
        json={
            "email": "not-an-email",
            "password": "password123",
        },
    )

    assert response.status_code == 422

    error = response.json()["detail"][0]

    assert error["loc"] == ["body", "email"]


def test_register_user_missing_email(client):
    response = client.post(
        "/users/",
        json={
            "password": "password123",
        },
    )

    assert response.status_code == 422

    error = response.json()["detail"][0]

    assert error["loc"] == ["body", "email"]
    assert error["type"] == "missing"


def test_register_user_missing_password(client):
    response = client.post(
        "/users/",
        json={
            "email": "missing-password@example.com",
        },
    )

    assert response.status_code == 422

    error = response.json()["detail"][0]

    assert error["loc"] == ["body", "password"]
    assert error["type"] == "missing"


def test_register_user_empty_body(client):
    response = client.post(
        "/users/",
        json={},
    )

    assert response.status_code == 422

    errors = response.json()["detail"]

    assert len(errors) == 2

    locations = [error["loc"] for error in errors]

    assert ["body", "email"] in locations
    assert ["body", "password"] in locations


def test_register_user_empty_email(client):
    response = client.post(
        "/users/",
        json={
            "email": "",
            "password": "password123",
        },
    )

    assert response.status_code == 422

    error = response.json()["detail"][0]

    assert error["loc"] == ["body", "email"]


def test_register_user_empty_password(client):
    response = client.post(
        "/users/",
        json={
            "email": "empty-password@example.com",
            "password": "",
        },
    )

    assert response.status_code == 422

    error = response.json()["detail"][0]

    assert error["loc"] == ["body", "password"]

def test_register_user_password_too_short(client):
    response = client.post(
        "/users/",
        json={
            "email": "short-password@example.com",
            "password": "1234567",
        },
    )

    assert response.status_code == 422

    error = response.json()["detail"][0]

    assert error["loc"] == ["body", "password"]


def test_register_user_password_too_long(client):
    response = client.post(
        "/users/",
        json={
            "email": "long-password@example.com",
            "password": "a" * 129,
        },
    )

    assert response.status_code == 422

    error = response.json()["detail"][0]

    assert error["loc"] == ["body", "password"]


def test_register_user_duplicate_email(client):
    payload = {
        "email": "duplicate@example.com",
        "password": "password123",
    }

    first_response = client.post("/users/", json=payload)
    second_response = client.post("/users/", json=payload)

    assert first_response.status_code == 201
    assert second_response.status_code == 409
    assert second_response.json()["detail"] == "Email already registered"


def test_register_user_duplicate_email_with_different_password(client):
    first_response = client.post(
        "/users/",
        json={
            "email": "duplicate-password@example.com",
            "password": "password123",
        },
    )

    second_response = client.post(
        "/users/",
        json={
            "email": "duplicate-password@example.com",
            "password": "completely-different-password",
        },
    )

    assert first_response.status_code == 201
    assert second_response.status_code == 409
    assert second_response.json()["detail"] == "Email already registered"


def test_register_user_invalid_email_type(client):
    response = client.post(
        "/users/",
        json={
            "email": 12345,
            "password": "password123",
        },
    )

    assert response.status_code == 422

    error = response.json()["detail"][0]

    assert error["loc"] == ["body", "email"]


def test_register_user_missing_content_type(client):
    response = client.post(
        "/users/",
        content='{"email": "test@example.com", "password": "password123"}',
    )

    assert response.status_code == 422


def test_login_user_success(client):
    client.post(
        "/users/",
        json={
            "email": "login@example.com",
            "password": "password123",
        },
    )

    response = client.post(
        "/auth/login",
        data={
            "username": "login@example.com",
            "password": "password123",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["access_token"]
    assert data["token_type"] == "bearer"


def test_login_user_with_nonexistent_email(client):
    response = client.post(
        "/auth/login",
        data={
            "username": "doesnotexist@example.com",
            "password": "password123",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"


def test_login_user_with_wrong_password(client):
    client.post(
        "/users/",
        json={
            "email": "wrong-password@example.com",
            "password": "password123",
        },
    )

    response = client.post(
        "/auth/login",
        data={
            "username": "wrong-password@example.com",
            "password": "wrongpassword",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"


def test_login_user_with_empty_password(client):
    client.post(
        "/users/",
        json={
            "email": "empty-login-password@example.com",
            "password": "password123",
        },
    )

    response = client.post(
        "/auth/login",
        data={
            "username": "empty-login-password@example.com",
            "password": "",
        },
    )

    assert response.status_code == 422

    error = response.json()["detail"][0]

    assert error["loc"] == ["body", "password"]


def test_login_user_missing_username(client):
    response = client.post(
        "/auth/login",
        data={
            "password": "password123",
        },
    )

    assert response.status_code == 422

    error = response.json()["detail"][0]

    assert error["loc"] == ["body", "username"]
    assert error["type"] == "missing"


def test_login_user_missing_password(client):
    response = client.post(
        "/auth/login",
        data={
            "username": "test@example.com",
        },
    )

    assert response.status_code == 422

    error = response.json()["detail"][0]

    assert error["loc"] == ["body", "password"]
    assert error["type"] == "missing"


def test_login_user_empty_body(client):
    response = client.post(
        "/auth/login",
        data={},
    )

    assert response.status_code == 422

    errors = response.json()["detail"]

    locations = [error["loc"] for error in errors]

    assert ["body", "username"] in locations
    assert ["body", "password"] in locations


def test_login_user_invalid_email_format(client):
    response = client.post(
        "/auth/login",
        data={
            "username": "not-an-email",
            "password": "password123",
        },
    )

    # Login currently accepts username as a plain string.
    # Email validation happens during registration, not login.
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"


def test_login_user_case_sensitive_password(client):
    client.post(
        "/users/",
        json={
            "email": "case-sensitive@example.com",
            "password": "Password123",
        },
    )

    response = client.post(
        "/auth/login",
        data={
            "username": "case-sensitive@example.com",
            "password": "password123",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"


def test_login_user_case_sensitive_email(client):
    client.post(
        "/users/",
        json={
            "email": "CaseSensitive@example.com",
            "password": "password123",
        },
    )

    response = client.post(
        "/auth/login",
        data={
            "username": "casesensitive@example.com",
            "password": "password123",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"


def test_login_user_with_special_characters_in_password(client):
    password = "P@ssw0rd!#$%^&*"

    client.post(
        "/users/",
        json={
            "email": "special-login@example.com",
            "password": password,
        },
    )

    response = client.post(
        "/auth/login",
        data={
            "username": "special-login@example.com",
            "password": password,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["access_token"]
    assert data["token_type"] == "bearer"


def test_login_user_returns_valid_jwt(client):
    client.post(
        "/users/",
        json={
            "email": "jwt-valid@example.com",
            "password": "password123",
        },
    )

    response = client.post(
        "/auth/login",
        data={
            "username": "jwt-valid@example.com",
            "password": "password123",
        },
    )

    assert response.status_code == 200

    token = response.json()["access_token"]

    payload = jwt.decode(
        token,
        settings.jwt_secret_key,
        algorithms=[settings.jwt_algorithm],
    )

    assert payload is not None


def test_login_user_token_contains_user_id(client):
    register_response = client.post(
        "/users/",
        json={
            "email": "jwt-user-id@example.com",
            "password": "password123",
        },
    )

    assert register_response.status_code == 201

    user_id = register_response.json()["id"]

    response = client.post(
        "/auth/login",
        data={
            "username": "jwt-user-id@example.com",
            "password": "password123",
        },
    )

    assert response.status_code == 200

    token = response.json()["access_token"]

    payload = jwt.decode(
        token,
        settings.jwt_secret_key,
        algorithms=[settings.jwt_algorithm],
    )

    assert payload["sub"] == str(user_id)


def test_login_user_token_contains_expiration(client):
    client.post(
        "/users/",
        json={
            "email": "jwt-exp@example.com",
            "password": "password123",
        },
    )

    response = client.post(
        "/auth/login",
        data={
            "username": "jwt-exp@example.com",
            "password": "password123",
        },
    )

    assert response.status_code == 200

    token = response.json()["access_token"]

    payload = jwt.decode(
        token,
        settings.jwt_secret_key,
        algorithms=[settings.jwt_algorithm],
    )

    assert "exp" in payload
    assert isinstance(payload["exp"], int)


def test_login_user_token_uses_expected_algorithm(client):
    client.post(
        "/users/",
        json={
            "email": "jwt-algorithm@example.com",
            "password": "password123",
        },
    )

    response = client.post(
        "/auth/login",
        data={
            "username": "jwt-algorithm@example.com",
            "password": "password123",
        },
    )

    assert response.status_code == 200

    token = response.json()["access_token"]

    header = jwt.get_unverified_header(token)

    assert header["alg"] == settings.jwt_algorithm


def test_login_user_token_rejects_wrong_secret(client):
    client.post(
        "/users/",
        json={
            "email": "jwt-secret@example.com",
            "password": "password123",
        },
    )

    response = client.post(
        "/auth/login",
        data={
            "username": "jwt-secret@example.com",
            "password": "password123",
        },
    )

    assert response.status_code == 200

    token = response.json()["access_token"]

    wrong_secret = "this-is-a-different-secret-key-2026"

    try:
        jwt.decode(
            token,
            wrong_secret,
            algorithms=[settings.jwt_algorithm],
        )
        assert False, "Token should not be valid with the wrong secret"
    except jwt.InvalidTokenError:
        pass


def test_login_user_token_rejects_modified_token(client):
    client.post(
        "/users/",
        json={
            "email": "jwt-modified@example.com",
            "password": "password123",
        },
    )

    response = client.post(
        "/auth/login",
        data={
            "username": "jwt-modified@example.com",
            "password": "password123",
        },
    )

    assert response.status_code == 200

    token = response.json()["access_token"]

    modified_token = token[:-1] + ("a" if token[-1] != "a" else "b")

    try:
        jwt.decode(
            modified_token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )
        assert False, "Modified token should not be valid"
    except jwt.InvalidTokenError:
        pass

def test_invalid_user_id_in_jwt_returns_401(client):
    token = jwt.encode(
        {
            "sub": "not-an-integer",
            "exp": datetime.now(timezone.utc) + timedelta(minutes=5),
        },
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )

    response = client.get(
        "/notes",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"