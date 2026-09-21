from pydantic import BaseModel, ConfigDict, Field
from typing import Literal, Optional

class UserResponse(BaseModel):
  """Represents the response model for a user, excluding sensitive information like password hash."""
  name: str = Field(..., description="The user's full name.")
  email: str = Field(..., description="The user's email address.")
  username: str = Field(..., description="The user's unique username.")
  role: str = Field(..., description="The user's role within the farm (e.g., 'Admin', 'manager', 'worker').")
  farm_id: int = Field(..., description="The ID of the farm the user belongs to.")
  is_verified: bool = Field(..., description="Indicates if the user's account has been verified.")

  model_config = ConfigDict(
      from_attributes=True
  )

class UserCreate(BaseModel):
    """Represents the request model for creating a new user."""
    email: str = Field(..., description="The email address for the new user.")
    name: str = Field(..., description="The full name of the new user.")
    username: str = Field(..., description="A unique username for the new user.")
    password: str = Field(..., description="The password for the new user's account.")
    farm_id: int = Field(..., description="The ID of the farm the new user will be associated with.")

class UserUpdate(BaseModel):
    """Represents the request model for updating an existing user's details."""
    name: Optional[str] = Field(None, description="Optional: New full name for the user.")
    email: Optional[str] = Field(None, description="Optional: New email address for the user.")
    username: Optional[str] = Field(None, description="Optional: New unique username for the user.")
    password: Optional[str] = Field(None, description="Optional: New password for the user.")

class UserRoleUpdate(BaseModel):
    """Represents the request model for updating a user's role."""
    role: Literal["Admin", "manager", "worker"] = Field(..., description="The new role to assign to the user.")
