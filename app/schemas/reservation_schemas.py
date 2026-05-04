from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import Field

from tools.application import DTO


class ReservationStatusEnum(str, Enum):
    """
    Enum representing the possible statuses of a reservation.
    \f
    :param ACTIVE: The reservation is currently active.
    :param COMPLETED: The reservation has been completed successfully.
    :param CANCELED: The reservation was canceled.
    """
    ACTIVE = "Active"
    COMPLETED = "Completed"
    CANCELED = "Canceled"


class ReservationStatusResponseSchema(DTO):
    """
    Response schema for a reservation status.
    """
    id: UUID = Field(..., description="Unique identifier of the reservation status")
    name: str = Field(..., description="Name of the reservation status")
    created_at: datetime = Field(..., description="Creation timestamp")


class ReservationRequestSchema(DTO):
    """
    Request schema for creating a new reservation.
    """
    user_id: UUID = Field(..., description="ID of the user making the reservation")
    equipment_id: UUID = Field(..., description="ID of the equipment being reserved")
    start_time: datetime = Field(..., description="Start time of the reservation")
    end_time: datetime = Field(..., description="End time of the reservation")


class ReservationResponseSchema(DTO):
    """
    Response schema representing a reservation record.
    """
    id: UUID = Field(..., description="Unique ID of the reservation")
    user_name: str = Field(None, description="Name of the user who made the reservation")
    equipment_name: str = Field(None, description="Name of the reserved equipment")
    status_name: str = Field(..., description="Reservation status name")
    start_time: datetime = Field(..., description="Start time of the reservation")
    end_time: datetime = Field(..., description="End time of the reservation")
    created_at: datetime = Field(..., description="Timestamp when reservation was created")


class ReservationUpdateSchema(DTO):
    """
    Response schema for updating a reservation status.
    """
    status_id: UUID = Field(..., description="Reservation status")
