from database import User, SmartFarmOS
from security.password import hash_password
from utils.public_id import generate_public_farm_id
from exceptions import (
    UsernameAlreadyExistsError,
    EmailAlreadyExistsError,
    SmartFarmAlreadyExistsError
)
from sqlalchemy.orm import Session
from schemas.onboarding import OnBoardingRequest

def farm_onboarding(db: Session, onboarding_data: OnBoardingRequest) -> tuple[SmartFarmOS, User]:
    """Handles the complete farm onboarding process, including creating a new farm and its initial owner.

    This function performs validation checks to ensure uniqueness of farm name, user email, and username.
    It creates a new SmartFarmOS entry, generates a public ID, hashes the owner's password,
    and creates a new user with 'Owner' role, linking both to the database.

    Args:
        db (Session): The database session.
        onboarding_data (OnBoardingRequest): Pydantic model containing all data for farm and owner creation.

    Returns:
        tuple[SmartFarmOS, User]: A tuple containing the newly created SmartFarmOS object
                                 and the initial owner's User object.

    Raises:
        SmartFarmAlreadyExistsError: If a farm with the given name already exists.
        EmailAlreadyExistsError: If a user with the given email already exists.
        UsernameAlreadyExistsError: If a user with the given username already exists.
        Exception: Catches any other database-related exceptions during the process and rolls back.
    """
    existing_farm = db.query(SmartFarmOS).filter(
        SmartFarmOS.farm_name == onboarding_data.farm_name,
    ).first()

    if existing_farm:
        raise SmartFarmAlreadyExistsError(
            f"Farm with name {onboarding_data.farm_name} already exists!"
        )

    existing_email = db.query(User).filter(
        User.email == onboarding_data.email,
        User.is_active == True
    ).first()

    if existing_email:
        raise EmailAlreadyExistsError(
            f"User with email {onboarding_data.email} already exists!"
        )

    existing_username = db.query(User).filter(
        User.username == onboarding_data.username,
        User.is_active == True
    ).first()

    if existing_username:
        raise UsernameAlreadyExistsError(
            f"User with username {onboarding_data.username} already exists!"
        )

    try:
        public_farm_id = generate_public_farm_id()

        new_farm = SmartFarmOS(
            farm_name=onboarding_data.farm_name,
            public_id=public_farm_id
        )

        db.add(new_farm)
        db.flush()

        hashed_password = hash_password(onboarding_data.password)

        new_user = User(
            email=onboarding_data.email,
            name=onboarding_data.name,
            username=onboarding_data.username,
            password_hash=hashed_password,
            farm_id=new_farm.id,
            role="Owner",
            is_verified = False
        )

        db.add(new_user)
        db.commit()

        db.refresh(new_farm)
        db.refresh(new_user)

        return new_farm, new_user
    except Exception:
        db.rollback()
        raise
