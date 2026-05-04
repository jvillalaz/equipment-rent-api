from datetime import datetime
from uuid import UUID

from pydantic import Field

from tools.application import DTO


class EquipmentStatusLogResponseSchema(DTO):
    """
    Response schema for equipment status log entries.
    """
    id: UUID = Field(..., description="Unique identifier of the status log")
    equipment_status: str = Field(..., description="Name of the equipment status")
    equipment_name: str = Field(..., description="Name of the equipment status")
    details: str | None = Field(None, description="Additional details about the status event")
    reported_at: datetime = Field(..., description="Date and time when the event occurred")
    created_at: datetime = Field(..., description="Timestamp of log creation")
