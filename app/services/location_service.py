from datetime import datetime
from uuid import UUID, uuid4
from zoneinfo import ZoneInfo

from app.core.exceptions import ConflictException
from app.database import location
from app.interfaces.location_interface import ILocationService
from app.schemas.location_schema import LocationCreateRequestSchema, LocationResponseSchema


class LocationService:

  location_repository: type[ILocationService]

  def __new__(cls, location_repository: type[ILocationService]):
    cls.location_repository = location_repository
    return cls
  
  @classmethod
  async def post_location(cls, location: LocationCreateRequestSchema) -> LocationResponseSchema:

    location_exists: LocationResponseSchema | None = ( await 
      cls.location_repository.get_location_by_name(location.name)
    )

    if location_exists:
      raise ConflictException(detail=f"Location '{location.name}' already exists")  


    await cls.location_repository.post_location(location)

    return LocationResponseSchema(
      id=uuid4(),
      name=location.name,
      created_at=datetime.now(tz=ZoneInfo("America/Manaus"))
    )

  @classmethod
  async def get_locations(cls) -> list[LocationResponseSchema]:
    return await cls.location_repository.get_locations()
  
  @classmethod
  async def get_location_by_id(cls, location_id: UUID) -> LocationResponseSchema | None:
    location_exists: LocationResponseSchema | None = await cls.location_repository.get_location_by_id(location_id)

    if not location_exists:
      return None

    return location_exists
