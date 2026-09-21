"""Module for handling JWT token creation and decoding.

This module provides functions to generate and verify JSON Web Tokens (JWTs)
for authentication purposes within the application.
"""
import os
from datetime import datetime, timedelta, timezone
import jwt
from typing import Dict, Any, Optional

SECRET_KEY: str = os.getenv("JWT_SECRET_KEY")

if not SECRET_KEY:
    raise ValueError(
        "JWT_SECRET_KEY environment variable not configured. Please set it in your environment."
    )

ALGORITHM: str = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

def create_access_token(user_id: int) -> str:
    """Creates a new JWT access token for a given user ID.

    The token includes the user ID as a subject ('sub') and an expiration timestamp.

    Args:
        user_id (int): The unique identifier of the user for whom the token is being created.

    Returns:
        str: The encoded JWT access token.
    """
    expire: datetime = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode: Dict[str, Any] = {
        "sub": str(user_id),
        "exp": expire
    }
    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
    """Decodes a JWT access token and returns its payload.

    Args:
        token (str): The JWT access token to decode.

    Returns:
        Optional[Dict[str, Any]]: The decoded token payload as a dictionary if valid,
                                  otherwise None if decoding fails or the token is invalid.
    """
    try:
        payload: Dict[str, Any] = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        return payload
    except jwt.PyJWTError:
        return None
