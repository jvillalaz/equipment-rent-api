from datetime import datetime
from uuid import UUID

from tools.application import DTO


class LocationCreateRequestSchema(DTO):
  name: str

class LocationResponseSchema(DTO):
  id: UUID
  name: str
  created_at: datetime