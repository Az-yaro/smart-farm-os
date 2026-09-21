from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import SessionLocal, get_db
from schemas.auth import LoginRequest
from services.auth_service import authenticate_user
from security.token import create_access_token
from typing import Dict, Any

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
) -> Dict[str, str]:
    """Authenticates a user and returns an access token upon successful login.

    Args:
        form_data (OAuth2PasswordRequestForm): OAuth2 form data containing username and password.
        db (Session): The database session.

    Returns:
        Dict[str, str]: A dictionary containing the access token and token type.
    """
    db_user = authenticate_user(
        db,
        form_data.username,
        form_data.password
    )
    access_token = create_access_token(db_user.id)
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
