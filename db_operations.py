from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.orm import joinedload # Import joinedload
from database import SmartFarmOS, CatFishBatch, Tank, EventLog, SessionLocal


def create_farm(farm_name: str) -> Optional[SmartFarmOS]:
    """
    Creates a new SmartFarmOS entry in the database.

    Args:
        farm_name (str): The unique name of the farm.

    Returns:
        Optional[SmartFarmOS]: The created SmartFarmOS object if successful, else None.
    """
    session = SessionLocal() # Get a new session for this operation
    try:
        farm = SmartFarmOS(farm_name=farm_name)
        session.add(farm)
        session.commit()
        session.refresh(farm)
        log_event(farm.id, "FARM MANAGEMENT", f"SmartFarmOS {farm_name} created.", "INFO")
        return farm
    except Exception as e:
        session.rollback()
        print(f"Error creating farm: {e}")
        return None
    finally:
        session.close()

def get_farm_by_name(farm_name: str) -> Optional[SmartFarmOS]:
  """
  Retrieves a SmartFarmOS object from the database by its name.

  Args:
      farm_name (str): The name of the farm to retrieve.

  Returns:
      Optional[SmartFarmOS]: The SmartFarmOS object if found, else None.
  """
  session = SessionLocal() # Get a new session for this operation
  try:
    stmt = select(SmartFarmOS).filter_by(farm_name=farm_name)
    farm = session.scalar(stmt)
    return farm
  except Exception as e:
    print(f"Error getting farm by name: {e}")
    return None
  finally:
    session.close()

def log_event(farm_id: int, category: str, message: str, status: str= "INFO") -> None:
  """
  Logs an event related to a specific farm.

  Args:
      farm_id (int): The ID of the farm the event pertains to.
      category (str): The category of the event (e.g., "WATER_CHECK", "TANK ADDED").
      message (str): A descriptive message for the event.
      status (str): The status of the event (e.g., "INFO", "SUCCESS", "Critical"). Defaults to "INFO".
  """
  session = SessionLocal() # Get a new session for this operation
  try:
    event = EventLog(farm_id=farm_id, category=category, message=message, status=status)
    session.add(event)
    session.commit()
  except Exception as e:
    session.rollback()
    print(f"Error logging event: {e}")
  finally:
    session.close()

def get_all_log(farm_id: int) -> List[EventLog]:
  """
  Retrieves all event logs for a specific farm, ordered by timestamp.

  Args:
      farm_id (int): The ID of the farm.

  Returns:
      List[EventLog]: A list of EventLog objects.
  """
  session = SessionLocal() # Get a new session for this operation
  try:
    stmt = select(EventLog).filter_by(farm_id=farm_id).order_by(EventLog.timestamp.desc())
    return session.scalars(stmt).all()
  except Exception as e:
    print(f"Error getting all logs: {e}")
    return []
  finally:
    session.close()

def add_batch(farm_id: int, batch_id: str, count: int, avg_weight_g: float) -> Optional[CatFishBatch]:
  """
  Adds a new catfish batch to a specific farm in the database.

  Args:
      farm_id (int): The ID of the farm.
      batch_id (str): The unique identifier for the batch.
      count (int): The number of fish in the batch.
      avg_weight_g (float): The average weight of a fish in grams.

  Returns:
      Optional[CatFishBatch]: The created CatFishBatch object if successful, else None.
  """
  session = SessionLocal() # Get a new session for this operation
  try:
    batch = CatFishBatch(smart_farm_os_id=farm_id, batch_id=batch_id, count=count, avg_weight_g=avg_weight_g)
    session.add(batch)
    session.commit()
    session.refresh(batch)
    log_event(farm_id, "BATCH MANAGEMENT", f"Created batch {batch_id} with  {count} fish.", "INFO")
    return batch
  except Exception as e:
    session.rollback()
    print(f"Error adding batch: {e}")
    return None
  finally:
    session.close()

def add_tank(farm_id: int, tank_id: str, capacity_liters: float, ammonia_ppm: float, ph: float, temp_c: float, batch_id: Optional[str] = None) -> Optional[Tank]:
  """
  Adds a new tank to a specific farm in the database, optionally assigning a catfish batch.

  Args:
      farm_id (int): The ID of the farm.
      tank_id (str): The unique identifier for the tank.
      capacity_liters (float): The maximum water capacity of the tank in liters.
      ammonia_ppm (float): Initial ammonia level in ppm.
      ph (float): Initial pH level.
      temp_c (float): Initial temperature in Celsius.
      batch_id (Optional[str]): The ID of the catfish batch to assign, if any.

  Returns:
      Optional[Tank]: The created Tank object if successful, else None.
  """
  session = SessionLocal() # Get a new session for this operation
  try:
    catfish_batch_obj = None
    if batch_id:
        batch_stmt = select(CatFishBatch).filter_by(batch_id=batch_id, smart_farm_os_id=farm_id)
        catfish_batch_obj = session.scalar(batch_stmt)
        if not catfish_batch_obj:
            print(f"Warning: Batch with ID {batch_id} not found for farm_id {farm_id}. Tank will be added without a batch.")

    tank = Tank(
        smart_farm_os_id=farm_id,
        tank_id=tank_id,
        capacity_liters=capacity_liters,
        ammonia_ppm=ammonia_ppm,
        ph=ph,
        temp_c=temp_c,
        catfish_batch_id=catfish_batch_obj.id if catfish_batch_obj else None
    )
    session.add(tank)
    session.commit()
    session.refresh(tank)
    log_event(farm_id, "TANK MANAGEMENT", f"Registered tank {tank_id} with capacity {capacity_liters} liters.", "INFO")
    return tank
  except Exception as e:
    session.rollback()
    print(f"Error adding tank: {e}")
    return None
  finally:
    session.close()

def update_water_metrics(farm_id: int, tank_id: str, ammonia_ppm: float, ph: float, temp_c: float) -> bool:
  """
  Updates the water quality metrics for a specific tank in the database.
  Logs critical events if ammonia or pH levels are unsafe.

  Args:
      farm_id (int): The ID of the farm.
      tank_id (str): The ID of the tank to update.
      ammonia_ppm (float): The new ammonia level in ppm.
      ph (float): The new pH level.
      temp_c (float): The new temperature in Celsius.

  Returns:
      bool: True if the update was successful, False otherwise.
  """
  session = SessionLocal() # Get a new session for this operation
  try:
    stmt = select(Tank).where(Tank.tank_id == tank_id, Tank.smart_farm_os_id == farm_id)
    tank = session.scalar(stmt)
    if not tank:
      print(f"Tank with ID {tank_id} not found for farm_id {farm_id}!")
      return False
    tank.ammonia_ppm = ammonia_ppm
    tank.ph = ph
    tank.temp_c = temp_c
    session.commit()
    session.refresh(tank)

    if ammonia_ppm > 0.05:
      log_event(farm_id, "WATER SAFETY", f"High ammonia in {tank_id} {ammonia_ppm}ppm!", "Critical") # Added 'ppm!' for clarity
    if ph < 6.5 or ph > 8.5:
      log_event(farm_id, "WATER SAFETY", f"Unsafe pH in {tank_id} {ph}!", "Critical")
    return True

  except Exception as e:
    session.rollback()
    print(f"Error updating water metrics for {tank_id}: {e}")
    return False
  finally:
    session.close()

def get_all_tanks(farm_id: int) -> List[Tank]:
  """
  Retrieves all tanks for a specific farm, eagerly loading associated catfish batches.

  Args:
      farm_id (int): The ID of the farm.

  Returns:
      List[Tank]: A list of Tank objects with their associated CatFishBatch objects.
  """
  session = SessionLocal() # Get a new session for this operation
  try:
    # Eagerly load the catfish_batches relationship to avoid DetachedInstanceError
    stmt = select(Tank).options(joinedload(Tank.catfish_batches)).filter_by(smart_farm_os_id=farm_id)
    return session.scalars(stmt).all()
  except Exception as e:
    print(f"Error getting all tanks: {e}")
    return []
  finally:
    session.close()
