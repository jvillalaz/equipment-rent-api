from datetime import datetime
from enum import Enum
from uuid import UUID
from pydantic import Field

from tools.application import DTO


class EquipmentStatusEnum(str, Enum):
    """
    Enum representing the possible statuses of equipment.
    \f
    :param AVAILABLE: Equipment is available for use.
    :param OCCUPIED: Equipment is currently in use.
    :param OFFLINE: Equipment is not connected or unavailable.
    :param MAINTENANCE: Equipment is under maintenance.
    """
    AVAILABLE = "Available"
    OCCUPIED = "Occupied"
    OFFLINE = "Offline"
    MAINTENANCE = "Maintenance"


class EquipmentStatusResponseSchema(DTO):
    """
    Schema for returning equipment status data from the database.
    """
    id: UUID = Field(..., description="Unique identifier of the equipment status")
    name: str = Field(..., description="Name of the equipment status")
    created_at: datetime = Field(..., description="Timestamp when the status was created")


class EquipmentRequestSchema(DTO):
    """
    Request schema for creating a new equipment.
    """
    name: str = Field(..., description="Name of the equipment")
    current_status_id: UUID = Field(..., description="ID of the current equipment status")
    location: UUID | None = Field(None, description="Location identifier of the equipment")
    last_heartbeat: datetime | None = Field(None, description="Timestamp of the last received heartbeat")

class EquipmentResponseSchema(DTO):
    """
    Response schema for newly created equipment.
    """
    id: UUID = Field(..., description="Unique identifier for the equipment")
    name: str = Field(..., description="Name of the equipment")
    current_status_name: EquipmentStatusEnum = Field(..., description="Name of the current equipment status")
    location: UUID | None = Field(None, description="Location identifier of the equipment")
    last_heartbeat: datetime | None = Field(None, description="Last known heartbeat from the equipment")
    created_at: datetime = Field(..., description="Timestamp of equipment creation")


class EquipmentUpdateSchema(DTO):
    """
    Request schema for creating a new equipment.
    """
    name: str | None = Field(..., description="Name of the equipment")
    current_status_id: UUID | None = Field(..., description="ID of the current equipment status")
    location: UUID | None = Field(None, description="Location identifier of the equipment")
    last_heartbeat: datetime | None = Field(None, description="Timestamp of the last received heartbeat")
