from abc import ABC, abstractmethod
from uuid import UUID

from app.schemas.location_schema import LocationCreateRequestSchema, LocationResponseSchema


class ILocationService(ABC):

  @classmethod
  @abstractmethod
  async def get_locations(cls) -> list[LocationResponseSchema]:
    raise NotImplementedError
  
  @classmethod
  @abstractmethod
  async def get_location_by_id(cls, location_id: UUID) -> LocationResponseSchema | None:
    raise NotImplementedError
  
  @classmethod
  @abstractmethod
  async def get_location_by_name(cls, name: str) -> LocationResponseSchema | None:
    raise NotImplementedError
  
  @classmethod
  @abstractmethod
  async def post_location(cls, location: LocationCreateRequestSchema) -> None:
    raise NotImplementedError