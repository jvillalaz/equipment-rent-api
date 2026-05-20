from uuid import UUID

from app.database import location
from app.database.location import Location
from app.interfaces.location_interface import ILocationService
from app.schemas.location_schema import LocationCreateRequestSchema, LocationResponseSchema


class LocationPersistence(ILocationService):

  @classmethod
  async def post_location(cls, location: LocationCreateRequestSchema) -> None:

    location_model: Location = Location(name=location.name)
    await location_model.save()

  @classmethod
  async def get_locations(cls) -> list[LocationResponseSchema]:

    location: list[Location] = await Location.all()

    return [LocationResponseSchema(
        id=loc.id,
        name=loc.name,
        created_at=loc.created_at
    ) for loc in location]
  
  @classmethod
  async def get_location_by_id(cls, location_id: UUID) -> LocationResponseSchema | None:

    location: Location | None = await Location.get_or_none(id=location_id)

    if not location:
      return None

    return LocationResponseSchema(
        id=location.id,
        name=location.name,
        created_at=location.created_at
    )
  
  @classmethod
  async def get_location_by_name(cls, name: str) -> LocationResponseSchema | None:

    location: Location | None = await Location.get_or_none(name=name)

    if not location:
      return None

    return LocationResponseSchema(
        id=location.id,
        name=location.name,
        created_at=location.created_at
    )