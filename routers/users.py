from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from database import SessionLocal, User, get_db
from schemas.user import UserCreate, UserUpdate, UserResponse, UserRoleUpdate
from services import user_service
from security.authorization import required_role

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/{username}", response_model=UserResponse)
def get_user(
        username: str,
        db: Session = Depends(get_db)
) -> UserResponse:
    """Retrieves user details by username.

    Args:
        username (str): The username of the user to retrieve.
        db (Session): The database session.

    Returns:
        UserResponse: The details of the requested user.
    """
    return user_service.get_user_by_username(db, username)

@router.post("/", response_model=UserResponse)
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
) -> UserResponse:
    """Creates a new user.

    Args:
        user_data (UserCreate): The data for the new user.
        db (Session): The database session.

    Returns:
        UserResponse: The details of the newly created user.
    """
    return user_service.create_user(db, user_data)

@router.patch("/{username}", response_model=UserResponse)
def update_user_role(
    username: str,
    role_data: UserRoleUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(required_role("Owner", "Admin"))
) -> UserResponse:
    """Updates the role of an existing user.

    Args:
        username (str): The username of the user to update.
        role_data (UserRoleUpdate): The new role data for the user.
        db (Session): The database session.
        current_user (User): The authenticated user with appropriate permissions.

    Returns:
        UserResponse: The details of the updated user.
    """
    return user_service.update_user_role(
        db,
        username,
        role_data.role
    )
