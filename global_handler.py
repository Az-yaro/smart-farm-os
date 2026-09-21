from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from exceptions import (
    WaterQualityError,
    AmmoniaHazardError,
    pHLevelError,
    TankNotFoundError,
    SmartFarmNotFoundError,
    UserNotFoundError,
    UsernameAlreadyExistsError,
    InvalidCredentialsError,
    EmailAlreadyExistsError,
    AuthorizationError,
    TankIDError,
    InvalidValuesError,
    SmartFarmAlreadyExistsError,
    TankAlreadyExistsError
)


def register_exception_handlers(app: FastAPI) -> None:
  """
  Registers custom exception handlers with the FastAPI application.

  Args:
      app (FastAPI): The FastAPI application instance.
  """
  @app.exception_handler(TankNotFoundError)
  async def tank_not_found_exception_handler(
      request: Request,
      exc: TankNotFoundError
  ) -> JSONResponse:
    """
    Handles TankNotFoundError exceptions, returning a 404 JSON response.
    """
    return JSONResponse(
        status_code=404,
        content={"message": f"Tank not found: {exc}"}
    )
  @app.exception_handler(SmartFarmNotFoundError)
  async def farm_not_found_exception_handler(
      request: Request,
      exc: SmartFarmNotFoundError
  ) -> JSONResponse:
      """
      Handles SmartFarmNotFoundError exceptions, returning a 404 JSON response.
      """
      return JSONResponse(
        status_code=404,
        content={"message": f"Farm not found: {exc}"}
      )
  @app.exception_handler(UserNotFoundError)
  async def user_not_found_exception_handler(
      request: Request,
      exc: UserNotFoundError
  ) -> JSONResponse:
    """
    Handles UserNotFoundError exceptions, returning a 404 JSON response.
    """
    return JSONResponse(
        status_code=404,
        content={"message": f"User not found: {exc}"}
    )
  @app.exception_handler(UsernameAlreadyExistsError)
  async def username_already_exists_exception_handler(
      request: Request,
      exc: UsernameAlreadyExistsError
  ) -> JSONResponse:
    """
    Handles UsernameAlreadyExistsError exceptions, returning a 400 JSON response.
    """
    return JSONResponse(
        status_code=400,
        content={"message": f"Username already exists: {exc}"}
    )
  @app.exception_handler(InvalidCredentialsError)
  async def invalid_credentials_exception_handler(
      request: Request,
      exc: InvalidCredentialsError
  ) -> JSONResponse:
    """
    Handles InvalidCredentialsError exceptions, returning a 401 JSON response.
    """
    return JSONResponse(
        status_code=401,
        content={"message": f"Invalid credentials: {exc}"}
    )
  @app.exception_handler(EmailAlreadyExistsError)
  async def email_already_exists_exception_handler(
      request: Request,
      exc: EmailAlreadyExistsError
  ) -> JSONResponse:
    """
    Handles EmailAlreadyExistsError exceptions, returning a 400 JSON response.
    """
    return JSONResponse(
        status_code=400,
        content={"message": f"Email already exists: {exc}"}
    )
  @app.exception_handler(AuthorizationError)
  async def authorization_error_exception_handler(
      request: Request,
      exc: AuthorizationError
  ) -> JSONResponse:
    """
    Handles AuthorizationError exceptions, returning a 403 JSON response.
    """
    return JSONResponse(
        status_code=403,
        content={"message": f"Authorization error: {exc}"}
    )

  @app.exception_handler(TankIDError)
  async def tank_id_error_exception_handler(
      request: Request,
      exc: TankIDError
  ) -> JSONResponse:
    """
    Handles TankIDError exceptions, returning a 400 JSON response.
    """
    return JSONResponse(
        status_code=400,
        content={"message": f"Invalid tank ID: {exc}"}
    )

  @app.exception_handler(InvalidValuesError)
  async def invalid_values_error_exception_handler(
      request: Request,
      exc: InvalidValuesError
  ) -> JSONResponse:
    """
    Handles InvalidValuesError exceptions, returning a 400 JSON response.
    """
    return JSONResponse(
        status_code=400,
        content={"message": f"Invalid values error: {exc}"}
    )

  @app.exception_handler(SmartFarmAlreadyExistsError)
  async def smart_farm_already_exists_exception_handler(
      request: Request,
      exc: SmartFarmAlreadyExistsError
  ) -> JSONResponse:
    """
    Handles SmartFarmAlreadyExistsError exceptions, returning a 400 JSON response.
    """
    return JSONResponse(
        status_code=400,
        content={"message": f"Farm already exists: {exc}"}
    )

  @app.exception_handler(TankAlreadyExistsError)
  async def tank_already_exists_exception_handler(
      request: Request,
      exc: TankAlreadyExistsError
  ) -> JSONResponse:
    """
    Handles TankAlreadyExistsError exceptions, returning a 400 JSON response.
    """
    return JSONResponse(
        status_code=400,
        content={"message": f"Tank already exists: {exc}"}
    )
