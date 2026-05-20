

from uuid import UUID

from app.database import location
from app.schemas.location_schema import LocationCreateRequestSchema, LocationResponseSchema
from app.services.location_service import LocationService
from fastapi import APIRouter, status


location_router = APIRouter(
  prefix="/locations",
  tags=["Locations"]
)

@location_router.post(
  "/",
  response_model=LocationResponseSchema,
  status_code=status.HTTP_201_CREATED,

)
async def post_location(location: LocationCreateRequestSchema) -> LocationResponseSchema:
  return await LocationService.post_location(location)

@location_router.get("/", response_model=list[LocationResponseSchema], status_code=status.HTTP_200_OK)
async def get_locations() -> list[LocationResponseSchema]:
  return await LocationService.get_locations()

@location_router.get(
  "/{location_id}",
  response_model=LocationResponseSchema or None,
  status_code=status.HTTP_200_OK
)
async def get_specific_location(location_id: UUID) -> LocationResponseSchema | None:
  return await LocationService.get_location_by_id(location_id)

@location_router.delete(
  "/{location_id}",
  response_model=None,
  status_code=status.HTTP_204_NO_CONTENT
)
async def delete_specific_location(location_id: UUID) -> LocationResponseSchema | None:
  return await LocationService.delete_location_by_id(location_id)