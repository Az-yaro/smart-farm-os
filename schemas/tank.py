from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
from typing import Optional
from exceptions import (
    TankIDError,
    InvalidValuesError
)

class TankResponse(BaseModel):
  """Represents the response model for tank data."""
  tank_id: str = Field(..., description="The unique identifier for the tank.")
  capacity_liters: float = Field(..., description="The maximum water capacity of the tank in liters.")
  ammonia_ppm: float = Field(..., description="The ammonia level in parts per million (ppm).")
  ph: float = Field(..., description="The pH level of the water.")
  temp_c: float = Field(..., description="The water temperature in Celsius.")

  model_config = ConfigDict(
      from_attributes=True
  )

class CreateTank(BaseModel):
  """Represents the request model for creating a new tank."""
  tank_id: str = Field(..., max_length=30, description="A unique identifier for the new tank, must start with 'tank-'.")
  capacity_liters: float = Field(..., gt=0, description="The maximum water capacity of the tank in liters.")
  ammonia_ppm: float = Field(..., ge=0, description="The initial ammonia level in parts per million (ppm).")
  ph: float = Field(default=7.0, ge=0, le=14, description="The initial pH level of the water.")
  temp_c: float = Field(default=28.0, ge=0, le=32, description="The initial water temperature in Celsius.")

  @field_validator("tank_id")
  @classmethod
  def validate_tank_id(cls, value):
      if not value.startswith("tank-"):
          raise TankIDError(
              "Tank ID must start with 'tank-'"
          )
      return value

  @model_validator(mode="after")
  def ammonia_temp_validation(self):
      if self.ammonia_ppm > 0.05 and self.temp_c > 32:
          raise InvalidValuesError(
            "The tank can't contain high ammonia and temp level at the same time"
        )
      return self

class UpdateTank(BaseModel):
  """Represents the request model for partially updating an existing tank's details."""
  capacity_liters: Optional[float] = Field(None, description="Optional: New maximum water capacity in liters.")
  ammonia_ppm: Optional[float] = Field(None, description="Optional: New ammonia level in ppm.")
  ph: Optional[float] = Field(None, description="Optional: New pH level of the water.")
  temp_c: Optional[float] = Field(None, description="Optional: New water temperature in Celsius.")

class TankReplace(BaseModel):
  """Represents the request model for fully replacing an existing tank's details."""
  capacity_liters: float = Field(..., gt=0, description="The new maximum water capacity in liters.")
  ammonia_ppm: float  = Field(..., ge=0, description="The new ammonia level in ppm.")
  ph: float = Field(default=7.0, ge=0, le=14, description="The new pH level of the water.")
  temp_c: float = Field(default=28.0, ge=0, le=32, description="The new water temperature in Celsius.")
