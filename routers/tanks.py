from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from database import SessionLocal, Tank, SmartFarmOS, User, get_db
from sqlalchemy import select
from services import tank_service
from security.dependencies import get_current_user
from security.authorization import required_role
from schemas.tank import(
    TankResponse,
    CreateTank,
    UpdateTank,
    TankReplace
)
from typing import List

router = APIRouter(
    prefix="/tanks",
    tags=["Tanks"]
)

@router.get("/", response_model=List[TankResponse])
def get_tanks_(
    db: Session = Depends(get_db),
    current_user=Depends(required_role(
        "worker",
        "manager",
        "Admin",
        "Owner"
    ))
) -> List[TankResponse]:
    """Retrieves a list of all tanks for the current user's farm.

    Args:
        db (Session): The database session.
        current_user (User): The authenticated user.

    Returns:
        List[TankResponse]: A list of tank details.
    """
    return tank_service.get_tanks(
        db,
        current_user.farm_id
    )

@router.get("/{tank_id}", response_model=TankResponse)
def get_tank(
    tank_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(required_role(
        "worker",
        "manager",
        "Admin",
        "Owner"
    ))
) -> TankResponse:
    """Retrieves a single tank by its ID for the current user's farm.

    Args:
        tank_id (str): The ID of the tank to retrieve.
        db (Session): The database session.
        current_user (User): The authenticated user.

    Returns:
        TankResponse: The details of the requested tank.
    """
    return tank_service.get_tank(
        db,
        tank_id,
        current_user.farm_id
    )

@router.post("/", response_model=TankResponse)
def create_tank(
    tank_data: CreateTank,
    db: Session = Depends(get_db),
    current_user = Depends(required_role(
        "manager",
        "Admin",
        "Owner"
    ))
) -> TankResponse:
    """Creates a new tank for the current user's farm.

    Args:
        tank_data (CreateTank): The data for the new tank.
        db (Session): The database session.
        current_user (User): The authenticated user.

    Returns:
        TankResponse: The details of the newly created tank.
    """
    return tank_service.create_tank(
        db,
        tank_data,
        current_user.farm_id
    )

@router.patch("/{tank_id}", response_model=TankResponse)
def update_tank(
    tank_id: str,
    tank_data: UpdateTank,
    db: Session = Depends(get_db),
    current_user=Depends(required_role(
        "Owner",
        "manager",
        "Admin",
        "worker"
    ))
) -> TankResponse:
    """Partially updates an existing tank's details for the current user's farm.

    Args:
        tank_id (str): The ID of the tank to update.
        tank_data (UpdateTank): The partial update data for the tank.
        db (Session): The database session.
        current_user (User): The authenticated user.

    Returns:
        TankResponse: The updated tank details.
    """
    return tank_service.update_tank(
        db,
        tank_id,
        tank_data,
        current_user.farm_id
    )

@router.put("/{tank_id}", response_model=TankResponse)
def full_tank_update(
    tank_id: str,
    tank_data: TankReplace,
    db: Session = Depends(get_db),
    current_user=Depends(required_role(
        "Owner",
        "manager",
        "Admin",
        "worker"
    ))
) -> TankResponse:
    """Fully replaces an existing tank's details for the current user's farm.

    Args:
        tank_id (str): The ID of the tank to replace.
        tank_data (TankReplace): The complete new data for the tank.
        db (Session): The database session.
        current_user (User): The authenticated user.

    Returns:
        TankResponse: The fully updated tank details.
    """
    return tank_service.full_tank_update(
        db,
        tank_id,
        tank_data,
        current_user.farm_id
    )

@router.delete("/{tank_id}", response_model=TankResponse)
def delete_tank(
    tank_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(required_role(
        "Owner",
        "manager",
        "Admin"
    ))
) -> TankResponse:
    """Deletes a tank by setting its `is_active` status to False for the current user's farm.

    Args:
        tank_id (str): The ID of the tank to delete.
        db (Session): The database session.
        current_user (User): The authenticated user.

    Returns:
        TankResponse: The details of the deleted tank (now inactive).
    """
    return tank_service.delete_tank(
        db,
        tank_id,
        current_user.farm_id
    )
