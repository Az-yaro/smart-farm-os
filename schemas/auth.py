from pydantic import (
    BaseModel,
    Field
)
class LoginRequest(BaseModel):
    """Represents the request model for user login."""
    username: str = Field(..., description="The user's username.")
    password: str = Field(..., description="The user's password.")
