from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import Tank, SmartFarmOS
from security.authorization import required_role
from exceptions import (
    SmartFarmNotFoundError,
    TankNotFoundError,
    TankAlreadyExistsError
)
from schemas.tank import CreateTank, UpdateTank, TankReplace
from typing import List, Optional

def get_tanks(db: Session, farm_id: int) -> List[Tank]:
    """Retrieves all active tanks for a given farm ID."""
    return db.query(Tank).filter(
        Tank.smart_farm_os_id == farm_id,
        Tank.is_active == True
    ).all()

def get_tank(db: Session, tank_id: str, farm_id: int) -> Tank:
    """Retrieves a single active tank by its ID and farm ID. Raises TankNotFoundError if not found."""
    db_tank = db.query(Tank).filter(
        Tank.tank_id == tank_id,
        Tank.smart_farm_os_id == farm_id,
        Tank.is_active == True
    ).first()

    if db_tank is None:
        raise TankNotFoundError(
            f"Tank with ID {tank_id} not found for farm ID {farm_id}!"
        )
    return db_tank

def create_tank(
        db: Session,
        tank_data: CreateTank,
        farm_id: int
) -> Tank:
    """Creates a new tank for a specified farm. Raises exceptions if the farm is not found or tank ID already exists."""
    if farm_id is None:
        raise SmartFarmNotFoundError(
            f"Current user does not belong to a farm!"
        )

    db_tank = db.query(Tank).filter(
        Tank.tank_id == tank_data.tank_id,
        Tank.smart_farm_os_id == farm_id,
        Tank.is_active == True
    ).first()

    if db_tank:
        raise TankAlreadyExistsError(
            f"Tank with ID {tank_data.tank_id} already exists"
        )

    db_tank = Tank(
        tank_id=tank_data.tank_id,
        capacity_liters=tank_data.capacity_liters,
        ammonia_ppm=tank_data.ammonia_ppm,
        ph=tank_data.ph,
        temp_c=tank_data.temp_c,
        smart_farm_os_id=farm_id
    )

    db.add(db_tank)
    db.commit()
    db.refresh(db_tank)
    return db_tank

def update_tank(db: Session, tank_id: str, tank_data: UpdateTank, farm_id: int) -> Tank:
  """Partially updates an existing tank's details. Raises TankNotFoundError if not found."""
  db_tank = db.query(Tank).filter(
      Tank.tank_id == tank_id,
      Tank.smart_farm_os_id == farm_id,
      Tank.is_active == True
  ).first()

  if db_tank is None:
    raise TankNotFoundError(
        f"Tank with ID {tank_id} not found for farm ID {farm_id}!"
    )

  for field, value in tank_data.model_dump(exclude_unset=True).items():
    setattr(db_tank, field, value)

  db.commit()
  db.refresh(db_tank)
  return db_tank

def full_tank_update(db: Session, tank_id: str, tank_data: TankReplace, farm_id: int) -> Tank:
  """Fully replaces an existing tank's details with new data. Raises TankNotFoundError if not found."""
  db_tank = db.query(Tank).filter(
      Tank.tank_id == tank_id,
      Tank.smart_farm_os_id == farm_id,
      Tank.is_active == True
  ).first()

  if db_tank is None:
    raise TankNotFoundError(
        f"Tank with ID {tank_id} not found for farm ID {farm_id}!"
    )

  db_tank.capacity_liters = tank_data.capacity_liters
  db_tank.ammonia_ppm = tank_data.ammonia_ppm
  db_tank.ph = tank_data.ph
  db_tank.temp_c = tank_data.temp_c

  db.commit()
  db.refresh(db_tank)
  return db_tank

def delete_tank(db: Session, tank_id: str, farm_id: int) -> Tank:
  """Deactivates a tank by setting its `is_active` status to False. Raises TankNotFoundError if not found."""
  db_tank = db.query(Tank).filter(
      Tank.tank_id == tank_id,
      Tank.smart_farm_os_id == farm_id,
      Tank.is_active == True
  ).first()

  if db_tank is None:
    raise TankNotFoundError(
        f"Tank with ID {tank_id} not found for farm ID {farm_id}!"
    )

  db_tank.is_active = False
  db.commit()
  db.refresh(db_tank)
  return db_tank
