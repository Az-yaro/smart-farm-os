import os
from datetime import datetime
from typing import List, Dict, Any, Optional, TYPE_CHECKING
from sqlalchemy  import create_engine, Column, Integer, String, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column,relationship, sessionmaker

class Base(DeclarativeBase):
  """Base class for declarative models."""
  pass

class SmartFarmOS(Base):
  """Represents the main Smart Farm OS entity, managing multiple tanks, batches, and event logs."""
  __tablename__ = "smart_farm_os"
  id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, doc="Unique identifier for the smart farm.")
  farm_name: Mapped[str] = mapped_column(String(30), unique=True, nullable=False, doc="Name of the smart farm.")
  created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, doc="Timestamp when the farm record was created.")
  updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now, doc="Timestamp when the farm record was last updated.")

  tanks: Mapped[List['Tank']] = relationship(back_populates='smart_farm_os', doc="List of tanks associated with this farm.")
  event_logs: Mapped[List['EventLog']] = relationship(back_populates='smart_farm_os', doc="List of event logs associated with this farm.")
  catfish_batches: Mapped[List['CatFishBatch']] = relationship(back_populates='smart_farm_os', doc="List of catfish batches associated with this farm.")
  users: Mapped[List['User']] = relationship(
      back_populates='smart_farm_os',
      doc="List of users associated with this farm."
  )

  def __repr__(self) -> str:
    """Returns a string representation of the SmartFarmOS object."""
    return f"SmartFarmOS(farm_name={self.farm_name})"

class CatFishBatch(Base):
  """Represents a batch of catfish, linked to a specific farm."""
  __tablename__ = "catfish_batches"
  id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, doc="Unique identifier for the catfish batch.")
  batch_id: Mapped[str] = mapped_column(String(30), unique=True, nullable=False, doc="User-defined unique ID for the batch.")
  count: Mapped[int] = mapped_column(Integer, nullable=False, doc="Number of fish in the batch.")
  avg_weight_g: Mapped[float] = mapped_column(Float, nullable=False, doc="Average weight of a single fish in grams.")
  created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, doc="Timestamp when the batch record was created.")
  updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now, doc="Timestamp when the batch record was last updated.")

  smart_farm_os_id: Mapped[int] = mapped_column(Integer, ForeignKey("smart_farm_os.id"), doc="Foreign key to the SmartFarmOS this batch belongs to.")
  smart_farm_os: Mapped['SmartFarmOS'] = relationship(back_populates='catfish_batches', doc="The SmartFarmOS object this batch belongs to.")
  tanks: Mapped[List['Tank']] = relationship(back_populates='catfish_batches', doc="List of tanks where this batch is housed.")

  def __repr__(self) -> str:
    """Returns a string representation of the CatFishBatch object."""
    return f"CatFishBatch(batch_id={self.batch_id}, count={self.count}, avg_weight_g={self.avg_weight_g})"

class Tank(Base):
  """Represents a fish tank, monitoring water parameters and optionally housing a catfish batch."""
  __tablename__ = "tanks"
  id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, doc="Unique identifier for the tank.")
  tank_id: Mapped[str] = mapped_column(String(30), unique=True, nullable=False, doc="User-defined unique ID for the tank.")
  capacity_liters: Mapped[float] = mapped_column(Float, nullable=False, doc="Maximum water capacity of the tank in liters.")
  ammonia_ppm: Mapped[float] = mapped_column(Float, nullable=False, doc="Ammonia level in parts per million (ppm).")
  ph: Mapped[float] = mapped_column(Float, nullable=False, doc="pH level of the water.")
  temp_c: Mapped[float] = mapped_column(Float, nullable=False, doc="Water temperature in Celsius.")
  created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, doc="Timestamp when the tank record was created.")
  updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now, doc="Timestamp when the tank record was last updated.")
  is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, doc="Indicates whether the tank is active or not.")

  catfish_batch_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("catfish_batches.id"), nullable=True, doc="Foreign key to the CatFishBatch housed in this tank.")
  catfish_batches: Mapped[Optional['CatFishBatch']] = relationship(back_populates='tanks', doc="The CatFishBatch object housed in this tank.")

  smart_farm_os_id: Mapped[int] = mapped_column(Integer, ForeignKey("smart_farm_os.id"), doc="Foreign key to the SmartFarmOS this tank belongs to.")
  smart_farm_os: Mapped['SmartFarmOS'] = relationship(back_populates='tanks', doc="The SmartFarmOS object this tank belongs to.")

  def __repr__(self) -> str:
    """Returns a string representation of the Tank object."""
    return f"Tank(tank_id={self.tank_id}, capacity_liters={self.capacity_liters}, ammonia_ppm={self.ammonia_ppm}, ph={self.ph}, temp_c={self.temp_c})"

class EventLog(Base):
  """Represents an event log entry for the farm, recording actions and critical alerts."""
  __tablename__ = "event_logs"
  id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, doc="Unique identifier for the event log entry.")
  category: Mapped[str] = mapped_column(String(30), nullable=False, doc="Category of the event (e.g., 'WATER_CHECK', 'CRITICAL').")
  message: Mapped[str] = mapped_column(String(300), nullable=False, doc="Detailed message describing the event.")
  status: Mapped[str] = mapped_column(String(30), nullable=False, doc="Status of the event (e.g., 'INFO', 'SUCCESS', 'Critical').")
  timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, doc="Timestamp when the event occurred.")

  farm_id: Mapped[int] = mapped_column(Integer, ForeignKey("smart_farm_os.id"), doc="Foreign key to the SmartFarmOS this event belongs to.")
  smart_farm_os: Mapped['SmartFarmOS'] = relationship(back_populates='event_logs', doc="The SmartFarmOS object this event belongs to.")
  def __repr__(self) -> str:
    """Returns a string representation of the EventLog object."""
    return f"EventLog(category={self.category}, message={self.message}, status={self.status}, timestamp={self.timestamp})"

class User(Base):
  __tablename__ = "User"
  id: Mapped[int] = mapped_column(
      Integer,
      primary_key=True,
      autoincrement=True,
      doc="Unique identifier for the user."
  )
  email: Mapped[str] = mapped_column(
      String(50),
      unique=True,
      nullable=False,
      doc="User's email address."
  )
  name: Mapped[str] = mapped_column(
      String(100),
      nullable=False,
      doc="User's full name."
  )

  username: Mapped[str] = mapped_column(
      String(30),
      unique=True,
      nullable=False,
      doc="User's unique username."
  )

  password_hash: Mapped[str] = mapped_column(
      String(255),
      nullable=False,
      doc="User's hashed password."
  )

  role: Mapped[str] = mapped_column(
      String(30),
      nullable=False,
      doc="User's role (e.g., 'admin', 'user')."
  )

  is_active: Mapped[bool] = mapped_column(
      Boolean,
      default=True,
      nullable=False,
      doc="Indicates whether the user account is active or not."
  )

  created_at: Mapped[datetime] = mapped_column(
      DateTime,
      default=datetime.now,
      doc="Timestamp when the user record was created."
  )

  updated_at: Mapped[datetime] = mapped_column(
      DateTime,
      default=datetime.now,
      onupdate=datetime.now,
      doc="Timestamp when the user record was last updated."
  )

  farm_id: Mapped[int] = mapped_column(
      Integer,
      ForeignKey("smart_farm_os.id"),
      doc="Foreign key to the SmartFarmOS this user belongs to."
  )
  smart_farm_os: Mapped['SmartFarmOS'] = relationship(
      back_populates='users',
      doc="The SmartFarmOS object this user belongs to."
  )
  def __repr__(self) -> str:
    """Returns a string representation of the UserModel object."""
    return f"UserModel(email={self.email}, name={self.name}, username={self.username}, role={self.role})"

database_url = os.getenv("DATABASE_URL")
if not database_url:
    raise ValueError("DATABASE_URL not found in environment variables.")

engine = create_engine(database_url, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db() -> None:
  """
  Initializes the database by creating all defined tables.
  This function should be called once at the start of the application.
  """
  Base.metadata.create_all(bind=engine)
