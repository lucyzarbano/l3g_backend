from __future__ import annotations

import base64
import hashlib
import hmac
import json
import time
from dataclasses import dataclass
from typing import Any

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from lib.config import settings

security = HTTPBearer(auto_error=False)


@dataclass(frozen=True)
class AuthenticatedUser:
    username: str


def authenticate_admin(username: str, password: str) -> bool:
    username_matches = hmac.compare_digest(username, settings.admin_username)
    password_matches = hmac.compare_digest(password, settings.admin_password)
    return username_matches and password_matches


def create_access_token(username: str) -> str:
    issued_at = int(time.time())
    payload = {
        "sub": username,
        "iat": issued_at,
        "exp": issued_at + settings.jwt_expires_minutes * 60,
    }
    header = {"alg": "HS256", "typ": "JWT"}
    signing_input = f"{_b64_json(header)}.{_b64_json(payload)}"
    signature = _sign(signing_input)
    return f"{signing_input}.{signature}"


def get_current_admin_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
) -> AuthenticatedUser:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise _unauthorized()

    payload = _decode_token(credentials.credentials)
    username = payload.get("sub")
    expires_at = payload.get("exp")

    if not isinstance(username, str) or not isinstance(expires_at, int):
        raise _unauthorized()

    if expires_at < int(time.time()):
        raise _unauthorized("Token expired")

    return AuthenticatedUser(username=username)


def _decode_token(token: str) -> dict[str, Any]:
    parts = token.split(".")
    if len(parts) != 3:
        raise _unauthorized()

    signing_input = f"{parts[0]}.{parts[1]}"
    expected_signature = _sign(signing_input)
    if not hmac.compare_digest(parts[2], expected_signature):
        raise _unauthorized()

    try:
        payload = json.loads(_b64_decode(parts[1]))
    except (ValueError, json.JSONDecodeError) as exc:
        raise _unauthorized() from exc

    if not isinstance(payload, dict):
        raise _unauthorized()

    return payload


def _sign(value: str) -> str:
    digest = hmac.new(settings.jwt_secret_key.encode("utf-8"), value.encode("utf-8"), hashlib.sha256).digest()
    return _b64_encode(digest)


def _b64_json(value: dict[str, Any]) -> str:
    return _b64_encode(json.dumps(value, separators=(",", ":")).encode("utf-8"))


def _b64_encode(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).rstrip(b"=").decode("ascii")


def _b64_decode(value: str) -> str:
    padding = "=" * (-len(value) % 4)
    return base64.urlsafe_b64decode(f"{value}{padding}").decode("utf-8")


def _unauthorized(detail: str = "Invalid authentication credentials") -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )

