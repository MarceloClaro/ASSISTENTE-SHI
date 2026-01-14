"""JWT Authentication utilities for Vision API endpoints.

Provides functions to initialize a JWT secret, create and verify tokens.
"""
from __future__ import annotations
import os
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

import jwt

logger = logging.getLogger(__name__)

_DEFAULT_ALG = "HS256"
_SECRET_ENV = "AUTH_SECRET_KEY"

class JWTManager:
    def __init__(self, secret_key: str, algorithm: str = _DEFAULT_ALG, default_exp_seconds: int = 3600) -> None:
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.default_exp_seconds = default_exp_seconds

    def create_token(self, claims: Dict[str, Any], exp_seconds: Optional[int] = None) -> str:
        exp_seconds = exp_seconds or self.default_exp_seconds
        payload = {
            **claims,
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(seconds=exp_seconds),
        }
        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        return token

    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        try:
            if token.startswith("Bearer "):
                token = token[7:]
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            logger.warning("JWT token expired")
            return None
        except jwt.InvalidTokenError as e:
            logger.warning(f"Invalid JWT token: {e}")
            return None

_jwt_manager: Optional[JWTManager] = None


def init_jwt_from_env(default_secret: str = "change-me") -> JWTManager:
    """Initialize JWTManager from environment or fallback default.

    Reads AUTH_SECRET_KEY from environment; if missing, uses provided default.
    """
    global _jwt_manager
    secret = os.getenv(_SECRET_ENV, default_secret)
    _jwt_manager = JWTManager(secret)
    logger.info("JWT manager initialized")
    return _jwt_manager


def get_jwt_manager() -> JWTManager:
    global _jwt_manager
    if _jwt_manager is None:
        init_jwt_from_env()
    assert _jwt_manager is not None
    return _jwt_manager


def require_auth_header(auth_header: Optional[str]) -> Dict[str, Any]:
    if not auth_header:
        raise PermissionError("Authorization header missing")
    mgr = get_jwt_manager()
    payload = mgr.verify_token(auth_header)
    if not payload:
        raise PermissionError("Invalid or expired token")
    return payload
