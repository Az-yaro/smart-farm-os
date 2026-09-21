from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from database import SessionLocal, get_db
from schemas.onboarding import OnBoardingRequest, OnBoardingResponse
from services.onboarding_service import farm_onboarding


router = APIRouter(
    prefix="/onboarding",
    tags=["Onboarding"]
)

@router.post("/", response_model=OnBoardingResponse)
def onboard_farm(
    onboarding_data: OnBoardingRequest,
    db: Session = Depends(get_db)
) -> OnBoardingResponse:
    """Onboards a new smart farm and its initial owner.

    This endpoint handles the creation of a new farm entry and an associated
    'Owner' user based on the provided onboarding data.

    Args:
        onboarding_data (OnBoardingRequest): The request body containing farm and owner details.
        db (Session): The database session dependency.

    Returns:
        OnBoardingResponse: The response model containing details of the newly created farm and owner.
    """
    new_farm, new_user = farm_onboarding(db, onboarding_data)

    return OnBoardingResponse(
        farm_name=new_farm.farm_name,
        public_id=new_farm.public_id,
        username=new_user.username,
        role=new_user.role,
        farm_id=new_user.farm_id,
        is_verified=new_user.is_verified
    )
