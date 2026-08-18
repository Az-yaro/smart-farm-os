import main
import excel
import pdf_report
import database
import db_operations
from typing import List, Dict, Any

def run_farm_operation() -> None:
  print("Starting Smart Farm OS v3.0 Enterprise Engine...\n")
  """
  Runs the main farm operation simulation, including:
  - Initializing the SmartFarmOS.
  - Adding tanks and assigning catfish batches.
  - Performing water quality checks under normal and critical conditions.
  - Printing the audit log.
  - Exporting reports to Excel and PDF.
  """
  # Initialize the database
  database.init_db()

  # Create or get the farm from the database
  farm_name = "Yaro Smart Farm Enterprise"
  farm = db_operations.create_farm(farm_name)
  if not farm:
      farm = db_operations.get_farm_by_name(farm_name)
  if not farm:
      print("Failed to create or retrieve farm Exiting.")
      return

  farm_id = farm.id

  # Create and add batches to the database
  batch_alpha = db_operations.add_batch(farm_id, "CB-2026-01", 30000, 400.0)
  batch_beta = db_operations.add_batch(farm_id, "CB-2026-02", 40000, 350.0)
  batch_gamma = db_operations.add_batch(farm_id, "CB-2026-03", 50000, 300.0)
  batch_delta = db_operations.add_batch(farm_id, "CB-2026-04", 60000, 250.0)
  batch_epsilon = db_operations.add_batch(farm_id, "CB-2026-05", 70000, 200.0)
  batch_zeta = db_operations.add_batch(farm_id, "CB-2026-06", 80000, 150.0)

  # Add tanks to the database, assigning batches by batch_id
  db_operations.add_tank(farm_id, "tank-alpha", 10000, 0.0, 7.0, 28.0, batch_alpha.batch_id if batch_alpha else None)
  db_operations.add_tank(farm_id, "tank-beta", 20000, 0.0, 7.0, 28.0, batch_beta.batch_id if batch_beta else None)
  db_operations.add_tank(farm_id, "tank-gamma", 30000, 0.0, 7.0, 28.0, batch_gamma.batch_id if batch_gamma else None)
  db_operations.add_tank(farm_id, "tank-delta", 40000, 0.0, 7.0, 28.0, batch_delta.batch_id if batch_delta else None)
  db_operations.add_tank(farm_id, "tank-epsilon", 50000, 0.0, 7.0, 28.0, batch_epsilon.batch_id if batch_epsilon else None)
  db_operations.add_tank(farm_id, "tank-zeta", 60000, 0.0, 7.0, 28.0, batch_zeta.batch_id if batch_zeta else None)

  # For biomass and daily feed calculation, retrieve a batch from DB
  if batch_alpha:
    print(f"Biomass: {(batch_alpha.count * batch_alpha.avg_weight_g)/1000.0} kg")
    print(f"Recommend Daily Feed: {round(((batch_alpha.count * batch_alpha.avg_weight_g)/1000.0) * 0.03, 2)} kg\n")

  # Perform water quality checks (updates database records and logs events)
  print("Performing water quality checks...")
  db_operations.update_water_metrics(farm_id, "tank-alpha", 0.01, 7.3, 27.9)
  db_operations.update_water_metrics(farm_id, "tank-beta", 0.02, 7.5, 28.1)
  db_operations.update_water_metrics(farm_id, "tank-gamma", 0.03, 7.7, 28.3)
  db_operations.update_water_metrics(farm_id, "tank-delta", 0.04, 7.9, 28.5)
  db_operations.update_water_metrics(farm_id, "tank-epsilon", 0.05, 8.1, 28.7)
  db_operations.update_water_metrics(farm_id, "tank-zeta", 0.06, 8.3, 28.9)

  # Test critical water quality conditions
  db_operations.update_water_metrics(farm_id, "tank-alpha", 0.1, 9.3, 27.9)
  db_operations.update_water_metrics(farm_id, "tank-beta", 0.2, 9.5, 28.1)
  db_operations.update_water_metrics(farm_id, "tank-gamma", 0.3, 9.7, 28.3)
  db_operations.update_water_metrics(farm_id, "tank-delta", 0.4, 9.9, 28.5)
  db_operations.update_water_metrics(farm_id, "tank-epsilon", 1.5, 10.1, 28.7)
  db_operations.update_water_metrics(farm_id, "tank-zeta", 0.6, 10.3, 28.9)

  # Fetch live records from Database
  tanks_db_objects = db_operations.get_all_tanks(farm_id)
  event_log_db_objects = db_operations.get_all_log(farm_id)

  tank_records = []
  for tank in tanks_db_objects:
      batch = None # Initialize batch to None
      if tank.catfish_batches:
          batch = tank.catfish_batches # This is the sqlalchemy object

      tank_records.append(
          {
              "tank_id": tank.tank_id,
              "capacity_liters": tank.capacity_liters,
              "ammonia_ppm": tank.ammonia_ppm,
              "ph": tank.ph,
              "temp_c": tank.temp_c,
              "batch_id": batch.batch_id if batch else 'None',
              "total_biomass_kg": (batch.count * batch.avg_weight_g)/1000.0 if batch else 0.0,
              "daily_feed_kg": round(((batch.count * batch.avg_weight_g)/1000.0) * 0.03, 2) if batch else 0.0
          }
      )

  log_records = [
      {
          "timestamp": log.timestamp.strftime("%Y/%m/%d %H:%M:%S"), # Format datetime for consistency
          "category": log.category,
          "message": log.message,
          "status": log.status
      }
      for log in event_log_db_objects
  ]

  # Export to Excel & PDF Engines
  print("\nGenerating Export pipelines...")
  try:
    excel.export_excel_report("farm_report", log_records, tank_records)
    print("Multi-Sheet Excel workbook created successfully.")
    pdf_report.generate_pdf_report("farm_report", log_records, tank_records)
    print("Exclusive PDF Digest created successfully.")
  except Exception as e:
    print(f"Error generating reports: {e}")

  print(f"\nSmart Farm OS v3.0  Execution Complete! All systems operational.")

if __name__ == "__main__":
  run_farm_operation()
