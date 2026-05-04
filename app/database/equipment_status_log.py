from datetime import datetime

from tortoise import fields, models
import uuid

from tools.application import naive_utcnow


class EquipmentStatusLog(models.Model):
    """
    Stores the status change logs of the equipment.

    Attributes:
        id (UUID): Unique identifier of the equipment status log.
        status (EquipmentStatus): Registered equipment status.
        equipment (Equipment): Corresponding equipment.
        details (str): Additional information about the status change.
        reported_at (datetime): Date and time of the event.
        created_at (datetime): Record creation timestamp.
    """
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    status = fields.ForeignKeyField(
        "models.EquipmentStatus",
        related_name="status_logs",
        null=False
    )
    equipment = fields.ForeignKeyField(
        "models.Equipment",
        related_name="status_logs",
        null=False
    )
    details = fields.CharField(max_length=300, null=True)
    reported_at = fields.DatetimeField(null=False, default=naive_utcnow)
    created_at = fields.DatetimeField(null=False, default=naive_utcnow)

    class Meta:
        table = "EquipmentStatusLogs"
        ordering = ["-created_at"]
