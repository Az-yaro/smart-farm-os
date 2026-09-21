
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

class UserNotFoundError(Exception):
  """Raised when a user is not found in the database."""
  pass

class UsernameAlreadyExistsError(Exception):
  """Raised when a user already exists in the database."""
  pass

class InvalidCredentialsError(Exception):
  """Raised when invalid credentials are provided during authentication."""
  pass

class EmailAlreadyExistsError(Exception):
  """Raised when the provided email already exists in the database."""
  pass

class AuthorizationError(Exception):
    """Raised when authorization fails."""
    pass

class TankIDError(Exception):
  """Raised when invalid tank ID is provided."""
  pass

class TankNameError(Exception):
  """Raised when invalid tank name is provided."""
  pass

class InvalidValuesError(Exception):
  """Raised when invalid values are provided."""
  pass

class SmartFarmAlreadyExistsError(Exception):
  """Raised when a farm already exists in the database."""
  pass

class TankAlreadyExistsError(Exception):
  """Raised when a tank already exists in the database."""
  pass
