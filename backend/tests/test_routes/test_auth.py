import pytest

from src.models.user import User
from src.utils.auth import get_password_hash


@pytest.mark.asyncio
async def test_register_creates_user(client):
    """POST /api/auth/register returns 201 with access_token."""
    resp = await client.post(
        "/api/auth/register",
        json={"email": "new@user.com", "password": "securepass"},
    )
    assert resp.status_code == 201
    data = resp.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_register_duplicate_email(client, db_session):
    """POST /api/auth/register returns 409 when email already exists."""
    user = User(email="dup@user.com", hashed_password=get_password_hash("pw"))
    db_session.add(user)
    await db_session.commit()

    resp = await client.post(
        "/api/auth/register",
        json={"email": "dup@user.com", "password": "anotherpass"},
    )
    assert resp.status_code == 409


@pytest.mark.asyncio
async def test_login_valid_credentials(client, db_session):
    """POST /api/auth/login returns 200 with access_token for valid credentials."""
    user = User(email="login@user.com", hashed_password=get_password_hash("correctpw"))
    db_session.add(user)
    await db_session.commit()

    resp = await client.post(
        "/api/auth/login",
        json={"email": "login@user.com", "password": "correctpw"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_invalid_credentials(client, db_session):
    """POST /api/auth/login returns 401 for invalid credentials."""
    user = User(email="bad@user.com", hashed_password=get_password_hash("realpass"))
    db_session.add(user)
    await db_session.commit()

    resp = await client.post(
        "/api/auth/login",
        json={"email": "bad@user.com", "password": "wrongpass"},
    )
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_login_nonexistent_user(client):
    """POST /api/auth/login returns 401 for non-existent email."""
    resp = await client.post(
        "/api/auth/login",
        json={"email": "nobody@user.com", "password": "whatever"},
    )
    assert resp.status_code == 401
