"""Module for managing security dependencies, including OAuth2 scheme and current user retrieval.

This module defines the OAuth2PasswordBearer scheme and a dependency function
`get_current_user` to extract and validate the current authenticated user from a JWT.
"""
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import SessionLocal, User, get_db
from security.token import decode_access_token
from exceptions import InvalidCredentialsError


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="auth/login"
)

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """Retrieves and validates the current authenticated user from a JWT.

    This function acts as a FastAPI dependency, extracting the JWT from the request,
    decoding it, and fetching the corresponding user from the database.

    Args:
        token (str): The JWT token extracted from the request header.
        db (Session): The database session.

    Returns:
        User: The authenticated and active User object.

    Raises:
        InvalidCredentialsError: If the token is invalid, expired, malformed,
                                 or if the user associated with the token is not found or inactive.
    """
    payload = decode_access_token(token)

    if payload is None:
        raise InvalidCredentialsError(
            "Invalid or expired token"
        )

    user_id = payload.get("sub")

    if user_id is None:
        raise InvalidCredentialsError(
            "Invalid token: user_id not found in token payload"
        )

    user = db.get(User, int(user_id))

    if user is None or not user.is_active:
        raise InvalidCredentialsError(
            "Invalid credentials"
        )
    return user
