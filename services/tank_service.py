from fastapi import Depends, HTTPException, status
from database import Tank, SmartFarmOS
from exceptions import TankNotFoundError, SmartFarmNotFoundError

def get_tanks(db):
    return db.query(Tank).filter(
        Tank.is_active == True
    ).all()

def get_tank(db, tank_id):
    db_tank = db.query(Tank).filter(
        Tank.tank_id == tank_id,
        Tank.is_active == True
    ).first()

    if db_tank is None:
        raise TankNotFoundError(
            f"Tank with ID {tank_id} not found!"
        )
    return db_tank

def create_tank(db, tank_data):
    db_tank = Tank(
        tank_id=tank_data.tank_id,
        capacity_liters=tank_data.capacity_liters,
        ammonia_ppm=tank_data.ammonia_ppm,
        ph=tank_data.ph,
        temp_c=tank_data.temp_c,
        smart_farm_os_id=tank_data.smart_farm_os_id
    )

    farm = db.get(SmartFarmOS, tank_data.smart_farm_os_id)
    if farm is None:
        raise SmartFarmNotFoundError(
            detail=f"Farm with ID {tank_data.smart_farm_os_id} does'nt exist!"
        )

    db.add(db_tank)
    db.commit()
    db.refresh(db_tank)
    return db_tank

def update_tank(db, tank_id, tank_data):
  db_tank = db.query(Tank).filter(
      Tank.tank_id == tank_id,
      Tank.is_active == True
  ).first()

  if db_tank is None:
    raise TankNotFoundError(
        f"Tank with ID {tank_id} not found!"
    )

  for field, value in tank_data.model_dump(exclude_unset=True).items():
    setattr(db_tank, field, value)

  db.commit()
  db.refresh(db_tank)
  return db_tank

def full_tank_update(db, tank_id, tank_data):
  db_tank = db.query(Tank).filter(
      Tank.tank_id == tank_id,
      Tank.is_active == True
  ).first()

  if db_tank is None:
    raise TankNotFoundError(
        f"Tank with ID {tank_id} not found!"
    )

  db_tank.capacity_liters = tank_data.capacity_liters
  db_tank.ammonia_ppm = tank_data.ammonia_ppm
  db_tank.ph = tank_data.ph
  db_tank.temp_c = tank_data.temp_c

  db.commit()
  db.refresh(db_tank)
  return db_tank

def delete_tank(db, tank_id):
  db_tank = db.query(Tank).filter(
      Tank.tank_id == tank_id,
      Tank.is_active == True
  ).first()

  if db_tank is None:
    raise TankNotFoundError(
        f"Tank with ID {tank_id} not found!"
    )

  db_tank.is_active = False
  db.commit()
  db.refresh(db_tank)
  return db_tank
