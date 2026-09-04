from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from database import SessionLocal, Tank, SmartFarmOS
from sqlalchemy import select
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
from services import tank_service

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

class TankResponse(BaseModel):
  tank_id: str
  capacity_liters: float
  ammonia_ppm: float
  ph: float
  temp_c: float

  model_config = ConfigDict(
      from_attributes=True
  )

class CreateTank(BaseModel):
  tank_id: str = Field(..., max_length=30)
  capacity_liters: float = Field(..., gt=0)
  ammonia_ppm: float = Field(..., ge=0)
  ph: float = Field(default=7.0, ge=0, le=14)
  temp_c: float = Field(default=28.0, ge=0, le=32)
  smart_farm_os_id: int = Field(default=1, gt=0)

  @field_validator("tank_id")
  @classmethod
  def validate_tank_id(cls, value):
      if not value.startswith("tank-"):
          raise ValueError(
              "Tank ID must start with 'tank-"
          )
      return value

  @model_validator(mode="after")
  def ammonia_temp_validation(self):
      if self.ammonia_ppm > 0.05 and self.temp_c > 32:
          raise ValueError(
            "The tank can't contain high ammonia and temp level at the same time"
        )
      return self

class UpdateTank(BaseModel):
  capacity_liters: float | None = None
  ammonia_ppm: float | None = None
  ph: float | None = None
  temp_c: float | None = None

class TankReplace(BaseModel):
  capacity_liters: float = Field(..., gt=0)
  ammonia_ppm: float  = Field(..., ge=0)
  ph: float = Field(default=7.0, ge=0, le=14)
  temp_c: float = Field(default=28.0, ge=0, le=32)

router = APIRouter(
    prefix="/tanks",
    tags=["Tanks"]
)

@router.get("/", response_model=list[TankResponse])
def get_tanks_(
    db: Session = Depends(get_db)
):
    return tank_service.get_tanks(db)

@router.get("/{tank_id}", response_model=TankResponse)
def get_tank(
    tank_id: str,
    db: Session = Depends(get_db)
):
    return tank_service.get_tank(db, tank_id)

@router.post("/", response_model=TankResponse)
def create_tank(
    tank_data: CreateTank,
    db: Session = Depends(get_db)
):
    return tank_service.create_tank(db, tank_data)

@router.patch("/{tank_id}", response_model=TankResponse)
def update_tank(
    tank_id: str,
    tank_data: UpdateTank,
    db: Session = Depends(get_db)
):
    return tank_service.update_tank(db, tank_id, tank_data)

@router.put("/{tank_id}", response_model=TankResponse)
def full_tank_update(
    tank_id: str,
    tank_data: TankReplace,
    db: Session = Depends(get_db)
):
    return tank_service.full_tank_update(db, tank_id, tank_data)

@router.delete("/{tank_id}", response_model=TankResponse)
def delete_tank(
    tank_id: str,
    db: Session = Depends(get_db)
):
    return tank_service.delete_tank(db, tank_id)
