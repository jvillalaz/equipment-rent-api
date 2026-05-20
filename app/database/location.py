import uuid

from tools.application import naive_utcnow
from tortoise import fields, models

class Location(models.Model):
  id = fields.UUIDField(pk=True, default=uuid.uuid4)
  name = fields.CharField(max_length=255, unique=True, null=False)
  created_at = fields.DatetimeField(null=False, default=naive_utcnow)