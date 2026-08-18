from exception import WaterQualityError, AmmoniaHazardError, pHLevelError
from datetime import datetime
from typing import Dict, List, Any, Optional
import db_operations # Import db_operations

class CatFishBatch:
  """Represents a batch of catfish in a farm, tracking their biomass and feed requirements."""

  def __init__(self, batch_id: str, count: int, avg_weight_g: float):
    """
    Initializes a new CatFishBatch.

    Args:
      batch_id (str): Unique identifier for the batch.
      count (int): Number of fish in the batch.
      avg_weight_g (float): Average weight of a single fish in grams.
    """
    self.batch_id: str = batch_id
    self.count: int = count
    self.avg_weight_g: float = avg_weight_g

  @property
  def total_biomass_kg(self) -> float:
    """Calculates total biomass of the batch in kilograms.

    Returns:
      float: The total biomass of the batch in kilograms.
    """
    return (self.count * self.avg_weight_g)/1000.0

  def calculate_daily_feed(self, ratio_feed: float = 0.03) -> float:
    """
    Calculates the recommended daily feed in kilograms based on total biomass.

    Args:
      ratio_feed (float): The feeding ratio (e.g., 0.03 for 3% of biomass).

    Returns:
      float: The calculated daily feed in kilograms, rounded to two decimal places.
    """
    return round(self.total_biomass_kg * ratio_feed, 2)

class Tank:
  """Represents a single fish tank within the smart farm, monitoring water quality and assigned batches."""

  def __init__(self, tank_id: str, capacity_liters: float, ammonia_ppm: float = 0.0, ph: float = 7.0, temp_c: float = 28.0):
    """
    Initializes a new Tank.

    Args:
      tank_id (str): Unique identifier for the tank.
      capacity_liters (float): The maximum water capacity of the tank in liters.
      ammonia_ppm (float): Ammonia level in ppm.
      ph (float): pH level.
      temp_c (float): Temperature in Celsius.
    """
    self.tank_id: str = tank_id
    self.capacity_liters: float = capacity_liters
    self.batch: Optional[CatFishBatch] = None # Still an in-memory representation if assigned
    self.ammonia_ppm: float = ammonia_ppm
    self.ph: float = ph
    self.temp_c: float = temp_c

  def assign_batch(self, batch: CatFishBatch) -> None:
    """
    Assigns a CatFishBatch to this tank. (In-memory assignment for simulation)

    Args:
      batch (CatFishBatch): The catfish batch to assign to the tank.
    """
    self.batch = batch

  def check_water_safety(self) -> None:
    """
    Validates real-world water chemical thresholds for ammonia and pH.

    Raises:
      AmmoniaHazardError: If the ammonia level exceeds the safe limit.
      pHLevelError: If the pH level falls outside the safe range.
    """
    if self.ammonia_ppm >= 0.05:
      raise AmmoniaHazardError(
            f"DANGER! Tank id: {self.tank_id} is in critical condition, ammonia level is {self.ammonia_ppm} ppm! (Limit: 0.05 ppm)"
        )

    if self.ph < 6.5 or self.ph > 8.5:
      raise pHLevelError(
            f"WARNING! Tank id: {self.tank_id} in an unsafe condition, pH level is at {self.ph}! (Safe Range: 6.5 - 8.5)"
        )

class SmartFarmOS:
  """Manages the overall operations of a smart fish farm, delegating persistence to db_operations."""

  def __init__(self, farm_id: int, farm_name: str):
    """
    Initializes the SmartFarmOS instance with a database farm_id.

    Args:
      farm_id (int): The ID of the farm in the database.
      farm_name (str): The name of the smart farm.
    """
    self.farm_id: int = farm_id
    self.farm_name: str = farm_name
    # Tanks and event_log are now managed by the database
    # self.tanks: Dict[str, Tank] = {}
    # self.event_log: List[Dict[str, Any]] = []

  def add_tank(self, tank_id: str, capacity_liters: float, ammonia_ppm: float, ph: float, temp_c: float, batch_id: Optional[str] = None) -> None:
    """
    Adds a new tank to the farm's management system via the database.

    Args:
      tank_id (str): The Tank ID.
      capacity_liters (float): The maximum water capacity.
      ammonia_ppm (float): Initial ammonia level.
      ph (float): Initial pH level.
      temp_c (float): Initial temperature.
      batch_id (Optional[str]): Optional batch ID to assign.
    """
    db_operations.add_tank(self.farm_id, tank_id, capacity_liters, ammonia_ppm, ph, temp_c, batch_id)

  def _log_event(self, category: str, message: str, status: str = "INFO") -> None:
    """
    Logs an event with a timestamp, category, message, and status to the database.

    Args:
      category (str): The category of the event (e.g., "WATER_CHECK", "TANK ADDED").
      message (str): A descriptive message for the event.
      status (str): The status of the event (e.g., "INFO", "SUCCESS", "Critical"). Defaults to "INFO".
    """
    db_operations.log_event(self.farm_id, category, message, status)

  def perform_water_check(self, tank_id: str, ammonia: float, ph: float, temp: float) -> None:
    """
    Performs a water quality check for a specific tank and logs the result to the database.

    Args:
      tank_id (str): The ID of the tank to check.
      ammonia (float): The ammonia level in ppm.
      ph (float): The pH level.
      temp (float): The water temperature in Celsius.
    """
    # We first update the water metrics in the database
    success: bool = db_operations.update_water_metrics(self.farm_id, tank_id, ammonia, ph, temp)

    if success:
        # Retrieve the updated tank from the database to check safety
        # This requires a new db_operations function to get a single tank by ID and farm_id
        # For now, we'll simulate the check based on passed values for immediate feedback
        # In a full ORM implementation, we might fetch the Tank object and call its check_water_safety method
        # For simplicity and to reuse main.Tank's logic here, we'll use a temporary Tank instance.
        temp_tank: Tank = Tank(tank_id, 0, ammonia, ph, temp) # Capacity is irrelevant for water check

        try:
            temp_tank.check_water_safety()
            self._log_event("WATER_CHECK", f"{tank_id} parameter optimal. pH={ph}, Ammonia={ammonia}ppm", "SUCCESS")
            print(f"{tank_id} water parameter normal")
        except WaterQualityError as e:
            self._log_event("WATER ALERT", str(e), "Critical")
            print(f"[{tank_id}] ALERT DISPATCHED: {e}")
    else:
        print(f"Failed to update water metrics for tank {tank_id} in the database.")

  def print_audit_log(self) -> None:
    """
    Prints all recorded events in the farm's audit log from the database to the console.
    """
    logs: List[Any] = db_operations.get_all_log(self.farm_id)
    print(f"\n========== {self.farm_name.upper()}, SYSTEM LOGS ==========")
    for log in logs:
      print(f"[{log.timestamp.strftime('%Y/%m/%d %H:%M:%S')}] [{log.status}] [{log.message}] [{log.category}]")
