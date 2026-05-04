from datetime import datetime
from typing import Optional

from tortoise import fields, models
import uuid

from tools.application import naive_utcnow


class Reservation(models.Model):
    """
    Stores information about reservations made by users.

    Attributes:
        id (UUID): Unique identifier of the reservation.
        user (User): User who made the reservation.
        equipment (Equipment): Reserved equipment.
        start_time (datetime): Reservation start time.
        end_time (datetime): Reservation end time.
        status (ReservationStatus): Reservation status.
        created_at (datetime): Reserved equipment.
    """
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    user = fields.ForeignKeyField(
        "models.User",
        related_name="reservations",
        null=False
    )
    equipment = fields.ForeignKeyField(
        "models.Equipment",
        related_name="reservations",
        null=False
    )
    start_time = fields.DatetimeField(null=False, default=naive_utcnow)
    end_time = fields.DatetimeField(null=False, default=naive_utcnow)
    status = fields.ForeignKeyField(
        "models.ReservationStatus",
        related_name="reservations",
        null=False
    )
    created_at = fields.DatetimeField(null=False, default=naive_utcnow)

    # This field is not part of the actual model definition.
    # It's only added to help the IDE recognize the FK ID attribute.
    user_id: Optional[uuid.UUID]
    equipment_id: Optional[uuid.UUID]
    status_id: Optional[uuid.UUID]

    class Meta:
        table = "Reservations"
        ordering = ["-created_at"]
