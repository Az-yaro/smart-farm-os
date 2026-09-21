from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

class OnBoardingResponse(BaseModel):
    """Represents the response model after a successful farm onboarding process."""
    farm_name: str = Field(..., description="The name of the newly created farm.")
    public_id: str = Field(..., description="The public ID of the newly created farm.")
    username: str = Field(..., description="The username of the initial owner created for the farm.")
    role: str = Field(..., description="The role of the initial owner (always 'Owner').")
    farm_id: int = Field(..., description="The internal database ID of the newly created farm.")
    is_verified: bool = Field(..., description="Indicates if the owner's account has been verified (initially False).")

    model_config = ConfigDict(
        from_attributes=True
    )

class OnBoardingRequest(BaseModel):
    """Represents the request model for onboarding a new farm and its initial owner."""
    farm_name: str = Field(..., description="The desired name for the new smart farm.")
    name: str = Field(..., description="The full name of the farm owner.")
    email: str = Field(..., description="The email address of the farm owner.")
    username: str = Field(..., description="A unique username for the farm owner.")
    password: str = Field(..., description="The password for the farm owner's account.")
