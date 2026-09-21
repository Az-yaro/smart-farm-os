from database import User
from sqlalchemy import select
from sqlalchemy.orm import Session
from security.password import verify_password
from exceptions import (
    InvalidCredentialsError
)

def authenticate_user(db: Session, username: str, password: str) -> User:
    """Authenticates a user based on username and password.

    Args:
        db (Session): The database session.
        username (str): The username of the user to authenticate.
        password (str): The plain-text password provided by the user.

    Returns:
        User: The authenticated User object.

    Raises:
        InvalidCredentialsError: If the username is not found, the user is inactive,
                                 or the password does not match.
    """
    db_user = db.query(User).filter(
        User.username == username,
        User.is_active == True
    ).first()

    if db_user is None:
        raise InvalidCredentialsError(
            "Invalid username or password"
        )

    if not verify_password(password, db_user.password_hash):
        raise InvalidCredentialsError(
            "Invalid username or password"
        )

    return db_user
