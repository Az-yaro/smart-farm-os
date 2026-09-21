from database import User, SmartFarmOS
from security.password import hash_password
from exceptions import (
    UsernameAlreadyExistsError,
    SmartFarmNotFoundError,
    EmailAlreadyExistsError,
    UserNotFoundError
)
from sqlalchemy.orm import Session
from schemas.user import UserCreate
from typing import Optional

def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """Retrieves a user from the database by their username, ensuring they are active.

    Args:
        db (Session): The database session.
        username (str): The username of the user to retrieve.

    Returns:
        Optional[User]: The User object if found and active, else None.
    """
    return db.query(User).filter(
        User.username == username,
        User.is_active == True
    ).first()

def create_user(db: Session, user_data: UserCreate) -> User:
    """Creates a new user in the database after performing validation checks.

    Args:
        db (Session): The database session.
        user_data (UserCreate): The Pydantic model containing new user's data.

    Returns:
        User: The newly created User object.

    Raises:
        UsernameAlreadyExistsError: If a user with the provided username already exists.
        EmailAlreadyExistsError: If a user with the provided email already exists.
        SmartFarmNotFoundError: If the specified farm_id does not exist.
    """
    existing_user = get_user_by_username(db, user_data.username)
    if existing_user:
        raise UsernameAlreadyExistsError(
            f"User with username {user_data.username} already exists!"
        )

    db_email = db.query(User).filter(
        User.email == user_data.email,
        User.is_active == True
    ).first()

    if db_email:
        raise EmailAlreadyExistsError(
            f"User with email {user_data.email} already exists!"
        )

    farm = db.get(SmartFarmOS, user_data.farm_id)
    if farm is None:
        raise SmartFarmNotFoundError(
            f"Farm with ID {user_data.farm_id} does'nt exist!"
        )

    hashed_password = hash_password(user_data.password)

    db_user = User(
        email=user_data.email,
        name=user_data.name,
        username=user_data.username,
        password_hash=hashed_password,
        role="worker",
        farm_id=user_data.farm_id
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user_role(db: Session, username: str, role: str) -> User:
    """Updates the role of an existing user.

    Args:
        db (Session): The database session.
        username (str): The username of the user whose role is to be updated.
        role (str): The new role for the user.

    Returns:
        User: The updated User object.

    Raises:
        UserNotFoundError: If the user with the specified username is not found.
    """
    user = get_user_by_username(db, username)

    if user is None:
        raise UserNotFoundError(
            f"User with username {username} not found!"
        )

    user.role = role
    db.commit()
    db.refresh(user)
    return user
