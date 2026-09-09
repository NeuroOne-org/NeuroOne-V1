"""Tests for password and JWT security primitives."""

from uuid import uuid4

from app.core.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)


def test_password_is_hashed_and_verifiable() -> None:
    password = "safe-clinical-password"
    password_hash = hash_password(password)

    assert password_hash != password
    assert verify_password(password, password_hash)
    assert not verify_password("wrong-password", password_hash)


def test_access_token_round_trip() -> None:
    user_id = uuid4()
    token = create_access_token(
        {"sub": str(user_id), "username": "clinician", "role": "clinician"}
    )

    payload = decode_access_token(token)

    assert payload["sub"] == str(user_id)
    assert payload["role"] == "clinician"
    assert "exp" in payload
