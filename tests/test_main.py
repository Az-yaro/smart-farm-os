import pytest
from main import CatFishBatch, Tank
from exceptions import AmmoniaHazardError, pHLevelError

def test_catfish_batch():
  batch = CatFishBatch(
      batch_id="CB-2026-01",
      count=30000,
      avg_weight_g=400.0
  )

  assert batch.total_biomass_kg == 12000.0

def test_daily_feed_calculation():
  feed_ratio = 0.03
  batch = CatFishBatch(
      batch_id="CB-2026-01",
      count=30000,
      avg_weight_g=400.0
  )

  assert batch.calculate_daily_feed() == 360

def test_tank_safety():
  tank = Tank(
      tank_id="tank-alpha",
      capacity_liters=10000,
      ammonia_ppm=0.0,
      ph=7.0,
      temp_c=28.0
  )
  tank.check_water_safety()

def test_high_ammonia():
  tank = Tank(
      tank_id="tank-beta",
      capacity_liters=10000,
      ammonia_ppm=0.05,
      ph=7.0,
      temp_c=28.0
  )
  with pytest.raises(AmmoniaHazardError):
    tank.check_water_safety()

def test_unsafe_ph():
  tank = Tank(
      tank_id="tank-gamma",
      capacity_liters=10000,
      ammonia_ppm=0.0,
      ph=9.0,
      temp_c=28.0
  )
  with pytest.raises(pHLevelError):
    tank.check_water_safety()
