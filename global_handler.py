from fastapi import Request
from fastapi.responses import JSONResponse
from exceptions import (
    WaterQualityError,
    AmmoniaHazardError,
    pHLevelError,
    TankNotFoundError,
    SmartFarmNotFoundError
)


def register_exception_handlers(app):
  @app.exception_handler(TankNotFoundError)
  async def tank_not_found_exception_handler(
      request: Request,
      exc: TankNotFoundError
  ):
    return JSONResponse(
        status_code=404,
        content={"message": f"Tank not found: {exc}"}
    )
  @app.exception_handler(SmartFarmNotFoundError)
  async def farm_not_found_exception_handler(
      request: Request,
      exc: SmartFarmNotFoundError
  ):
      return JSONResponse(
        status_code=404,
        content={"message": f"Farm not found: {exc}"}
      )
