
class WaterQualityError(Exception):
  """Base exception for errors related to water quality."""
  pass

class AmmoniaHazardError(WaterQualityError):
  """Raised when the Ammonia level exceeds the safe limit (0.05 ppm)."""
  pass

class pHLevelError(WaterQualityError):
  """Raised when the pH level falls outside the safe range (6.5 - 8.5)."""
  pass

class TankNotFoundError(Exception):
  """Raised when a tank is not found in the database."""
  pass

class SmartFarmNotFoundError(Exception):
  """Raised when a farm is not found in the database."""
  pass
